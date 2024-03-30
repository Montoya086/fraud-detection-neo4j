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