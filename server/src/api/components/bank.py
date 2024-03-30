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
    

def hire_bank_action(client_ids):
    try:
        clients_data = [{'client_id': client_id, 'id_empleado': str(uuid4())} for client_id in client_ids]

        query = """
        UNWIND $clients_data AS client_data
        MATCH (client:Cliente {id: client_data.client_id})
        SET client:Empleado,
            client.fecha_contratacion = $fecha_contratacion,
            client.empleado_id = client_data.id_empleado
        """
        graph.run(query, 
                clients_data=clients_data, 
                fecha_contratacion=datetime.now().strftime("%Y-%m-%d"))
        return {"message": "Clients hired", "status": 200, "data": clients_data}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}
    
def fire_bank_action(worker_ids):
    try:
        query = """
        UNWIND $worker_ids AS worker_id
        MATCH (client:Empleado {empleado_id: worker_id})
        REMOVE client:Empleado
        SET client.fecha_contratacion = NULL,
            client.id_empleado = NULL
        """
        graph.run(query, worker_ids=worker_ids)
        return {"message": "Clients fired", "status": 200, "data": {}}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}