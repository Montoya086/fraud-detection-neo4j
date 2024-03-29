from src.api.schemas.account import AccountCreationPayload
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
        MATCH (banco)-[:GESTIONA]->(cuenta:Cuenta {numeroCuenta: $account_number})<-[:TIENE]-(cliente)
        RETURN cuenta, cliente, banco
        """
        result = graph.run(query, account_number=account_number).data()
        
        if result:
            return {
                "message": "Account and associated client and bank data found",
                "status": 200,
                "data": result[0]  
            }
        else:
            return {"message": "Account not found", "status": 404, "data": {}}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}

def create_account_action(request):
    try:
        account_id = str(uuid4())
        fechaCreacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

            return {"message": "Account created", "status": 201, "data": account_data}
        else:
            return {"message": "Account not created", "status": 500, "data": {}}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}
    
