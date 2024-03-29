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

def get_banks_action(name: str):
    try:
        name_lower = name.lower() if name else None 

        if not name_lower: 
            query = """
            MATCH (banco:Banco)
            RETURN banco
            """
            result = graph.run(query).data()
        else:
            query = """
            MATCH (banco:Banco)
            WHERE toLower(banco.nombre) CONTAINS $name_lower
            RETURN banco
            """
            result = graph.run(query, name_lower=name_lower).data()

        print(result)
        return {"message": "Banks found", "status": 200, "data": result}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}
    

def get_bank_action(bank_id: str):
    try:
        query = """
        MATCH (cliente:Cliente)-[:PERTENECE_A]->(banco:Banco {id: $bank_id})
        OPTIONAL MATCH (banco)-[:GESTIONA]->(cuenta:Cuenta)
        RETURN banco, count(DISTINCT cliente) AS clientes_count, count(DISTINCT cuenta) AS cuentas_count
        """
        result = graph.run(query, bank_id=bank_id).data()

        if result:
            bank_data = result[0]
            return {
                "message": "Bank found",
                "status": 200,
                "data": {
                    "banco": bank_data['banco'],
                    "clientes_count": bank_data['clientes_count'],
                    "cuentas_count": bank_data['cuentas_count']
                }
            }
        else:
            return {"message": "Bank not found", "status": 404, "data": {}}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}