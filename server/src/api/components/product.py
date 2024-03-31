from py2neo import Graph
from faker import Faker
import os
from dotenv import load_dotenv
from uuid import uuid4
from datetime import datetime

load_dotenv()

uri = os.getenv("NEO_URI")
user = os.getenv("NEO_USER")
password = os.getenv("NEO_PASSWORD")

fake = Faker()
graph = Graph(uri, auth=(user, password))

def create_product_action(request):
    try:
        tipo = request.tipo
        limiteCredito = request.limite_credito
        condiciones = request.condiciones
        bank_id = request.bank_id
        product_id = str(uuid4())
        fecha_oferta = datetime.now()

        query = """
        MATCH (banco:Banco {id: $bank_id})
        CREATE (producto:Producto {id: $product_id, tipo: $tipo, limiteCredito: $limiteCredito, condiciones: $condiciones, fechaOferta: $fecha_oferta, banco_id: $bank_id})
        MERGE (banco)-[:OFRECE]->(producto)
        RETURN producto
        """
        result = graph.run(query, product_id=product_id, tipo=tipo, limiteCredito=limiteCredito, condiciones=condiciones, bank_id=bank_id, fecha_oferta=fecha_oferta).data()
        parsed_result = dict(result[0]["producto"])
        parsed_result["fechaOferta"] = parsed_result["fechaOferta"].isoformat()
        return {"message": "Product created", "status": 201, "data": parsed_result}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}


def delete_products_action(request):
    try:
        product_ids = request.product_ids
        query = """
        UNWIND $product_ids AS product_id
        MATCH (producto:Producto {id: product_id})
        DETACH DELETE producto
        """
        graph.run(query, product_ids=product_ids)
        return {"message": "Products deleted", "status": 200, "data": product_ids}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}

def get_products_by_bank(bank_id: str):
    try:
        query = """
        MATCH (banco:Banco {id: $bank_id})-[:OFRECE]->(producto:Producto)
        RETURN producto
        """
        result = graph.run(query, bank_id=bank_id).data()
        print(result)
        if result:
            parsed_result = []
            for product in result:
                parsed_result.append(dict(product['producto']))
            
            for product in parsed_result:
                product["fechaOferta"] = product["fechaOferta"].isoformat()

            return {
                "message": "Products found",
                "status": 200,
                "data": parsed_result
            }
        else:
            return {"message": "Products not found", "status": 404, "data": {}}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}