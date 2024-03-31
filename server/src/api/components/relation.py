from py2neo import Graph
from faker import Faker
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO_URI")
user = os.getenv("NEO_USER")
password = os.getenv("NEO_PASSWORD")

fake = Faker()
graph = Graph(uri, auth=(user, password))

def delete_relations_action(request):
    try:
        relations = request.relation_ids
        query = """
        UNWIND $relations AS relation_id
        MATCH ()-[r]->() WHERE r.relacion_id = relation_id
        DELETE r
        """
        graph.run(query, relations=relations)
        return {"message": "Relations deleted successfully", "status": 200, "data": relations}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}

def update_relations_action(request):
    try:
        relations = request.relation_ids
        details = request.details
        query = """
        UNWIND $relations AS relation_id
        MATCH ()-[r]->() WHERE r.relacion_id = relation_id
        SET r.detalle = $details
        """
        graph.run(query, relations=relations, details=details)
        return {"message": "Relations updated successfully", "status": 200, "data": relations}
    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}