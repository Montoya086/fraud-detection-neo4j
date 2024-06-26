from src.api.schemas.account import AccountCreationPayload, GetAllAccountsPayload
from py2neo import Node, Relationship, Graph
from uuid import uuid4
from datetime import datetime
from faker import Faker
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO_URI")
user = os.getenv("NEO_USER")
password = os.getenv("NEO_PASSWORD")

fake = Faker()
graph = Graph(uri, auth=(user, password))

def upgrade_account_action(request):
    try:
        account_numbers = request.account_numbers
        is_premium = request.is_premium
        
        query = """
        UNWIND $account_numbers AS account_number
        MATCH (cuenta:Cuenta {numeroCuenta: account_number})
        SET cuenta.esPremium = $is_premium
        """
        graph.run(query, account_numbers=account_numbers, is_premium=is_premium)
        return {"message": "Accounts " + ("upgraded to premium!" if is_premium else "downgraded!")  , "status": 200, "data": account_numbers}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}

def delete_account_action(account_number: str):
    try:
        query = """
        MATCH (cuenta:Cuenta {numeroCuenta: $account_number})
        DETACH DELETE cuenta
        """
        graph.run(query, account_number=account_number)
        return {"message": "Account deleted", "status": 200, "data": {}}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}

def get_account_by_number(account_number: str):
    try:
        query = """
        MATCH (banco)-[:GESTIONA]->(cuenta:Cuenta {numeroCuenta: $account_number})
        OPTIONAL MATCH (cliente)-[:TIENE]->(cuenta)
        RETURN cuenta, cliente, banco
        """
        result = graph.run(query, account_number=account_number).data()
        print(result)
        if result:
            parsed_result = dict(result[0])
            if parsed_result["cliente"] is None:
                parsed_result["cliente"] = {}
            else :
                parsed_result["cliente"] = dict(parsed_result["cliente"])
            parsed_result["cuenta"] = dict(parsed_result["cuenta"])
            parsed_result["banco"] = dict(parsed_result["banco"])
            parsed_result["cuenta"]["fechaCreacion"] = parsed_result["cuenta"]["fechaCreacion"].isoformat()
            return {
                "message": "Account and associated client and bank data found",
                "status": 200,
                "data": parsed_result  
            }
        else:
            return {"message": "Account not found", "status": 404, "data": {}}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}

def create_account_action(request):
    try:
        account_id = str(uuid4())
        fechaCreacion=datetime.now()

        account = Node("Cuenta", 
                    tipoCuenta=request.tipo, 
                    saldo=request.saldo, 
                    id=account_id, 
                    fechaCreacion=fechaCreacion,
                    numeroCuenta=fake.iban()
                    )
        bank = graph.nodes.match("Banco", id=request.bank_id).first()
        owner = graph.nodes.match("Cliente", id=request.cliente_id).first()

        graph.create(account)

        if bank:
            graph.merge(Relationship(bank, "GESTIONA", account, fecha_creacion=fechaCreacion, relacion_id=str(uuid4()), detalle=fake.sentence()))
        else:
            return {"message": "Bank not found", "status": 404, "data": {}}

        if owner:
            graph.merge(Relationship(owner, "TIENE", account, fecha_creacion=fechaCreacion, relacion_id=str(uuid4()), detalle=fake.sentence()))

            graph.merge(Relationship(owner, "PERTENECE_A", bank, fecha_creacion=fechaCreacion, relacion_id=str(uuid4()), detalle=fake.sentence()))
        else:
            return {"message": "Client not found", "status": 404, "data": {}}
        
        saved_account = graph.nodes.match("Cuenta", id=account_id).first()
        if saved_account:
            account_data = dict(saved_account)
            account_data['fechaCreacion'] = account_data['fechaCreacion'].isoformat()

            return {"message": "Account created", "status": 201, "data": account_data}
        else:
            return {"message": "Account not created", "status": 500, "data": {}}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}
    
def get_all_accounts(request: GetAllAccountsPayload):
    try:
        if request.order_by == "date":
            query = """
            MATCH (cuenta:Cuenta)
            OPTIONAL MATCH (cliente)-[:TIENE]->(cuenta)
            OPTIONAL MATCH (banco)-[:GESTIONA]->(cuenta)
            RETURN cuenta, collect(cliente) AS clientes, collect(banco) AS bancos, cuenta.fechaCreacion
            ORDER BY cuenta.fechaCreacion """ + request.order.upper()
        if request.order_by == "balance":
            query = """
            MATCH (cuenta:Cuenta)
            OPTIONAL MATCH (cliente)-[:TIENE]->(cuenta)
            OPTIONAL MATCH (banco)-[:GESTIONA]->(cuenta)
            RETURN cuenta, collect(cliente) AS clientes, collect(banco) AS bancos, cuenta.fechaCreacion
            ORDER BY cuenta.saldo """ + request.order.upper()
        else:
            query = """
            MATCH (cuenta:Cuenta)
            OPTIONAL MATCH (cliente)-[:TIENE]->(cuenta)
            OPTIONAL MATCH (banco)-[:GESTIONA]->(cuenta)
            RETURN cuenta, collect(cliente) AS clientes, collect(banco) AS bancos, cuenta.fechaCreacion
            ORDER BY cuenta.saldo """ + request.order.upper()
            
        result = graph.run(query).data()
        accounts = []
        for record in result:
            account_info = record["cuenta"]
            clientes = [dict(cliente) for cliente in record["clientes"] if cliente]
            bancos = [dict(banco) for banco in record["bancos"] if banco]
            account_info["clientes"] = clientes
            account_info["bancos"] = bancos
            if "fechaCreacion" in account_info:
                account_info["fechaCreacion"] = account_info["fechaCreacion"].isoformat()
            accounts.append(account_info)
        
        if accounts:
            return {"message": "All accounts retrieved successfully.", "status": 200, "data": accounts}
        else:
            return {"message": "No accounts found.", "status": 404, "data": []}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": []}
