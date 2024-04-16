from py2neo import Graph
from faker import Faker
import os
from dotenv import load_dotenv
from src.api.schemas.transaction import Transaction
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

load_dotenv()

uri = os.getenv("NEO_URI")
user = os.getenv("NEO_USER")
password = os.getenv("NEO_PASSWORD")

fake = Faker()
graph = Graph(uri, auth=(user, password))


def obtain_transactional_data():
    query = """
    MATCH (t:Transacción)
    OPTIONAL MATCH (t)-[:RECIBE_TRANSACCION]->(c:Cuenta)<-[:GESTIONA]-(b:Banco)
    OPTIONAL MATCH (c)<-[:TIENE]-(cliente:Cliente)
    RETURN t.id AS id_transaccion, 
           t.monto AS monto, 
           t.esFraudulenta AS etiqueta,
           c.tipoCuenta AS tipo_cuenta,
           b.id AS banco_id,
           cliente.id IS NOT NULL AS cuenta_tiene_dueño
    """
    result = graph.run(query).to_data_frame()
    return result


def prepare_new_transaction_data(transaction: Transaction):
    query = """
    MATCH (c:Cuenta {numeroCuenta: $to_account_number})<-[:GESTIONA]-(b:Banco)
    OPTIONAL MATCH (c)<-[:TIENE]-(cliente:Cliente)
    RETURN c.tipoCuenta AS tipo_cuenta, b.id AS banco_id, cliente.id IS NOT NULL AS cuenta_tiene_dueño
    """
    result = graph.run(query, to_account_number=transaction.to_account_number).to_data_frame().iloc[0]

    new_transaction_data = {
        'monto': transaction.monto,
        'tipo_cuenta': result.tipo_cuenta,
        'banco_id': result.banco_id,
        'cuenta_tiene_dueño': result.cuenta_tiene_dueño,
    }

    df=pd.DataFrame([new_transaction_data])
    df["cuenta_tiene_dueño"] = df["cuenta_tiene_dueño"].map({True: 1, False: 0})
    df["tipo_cuenta"] = df["tipo_cuenta"].map({"Corriente": 0, "Ahorro": 1})
    return df


class SingletonModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonModel, cls).__new__(cls)
            cls._model = RandomForestClassifier() 
            cls._train_model()
        return cls._instance

    @staticmethod
    def _train_model():
        df = obtain_transactional_data()  
        
        df["etiqueta"] = df["etiqueta"].map({True: 1, False: 0})
        df["cuenta_tiene_dueño"] = df["cuenta_tiene_dueño"].map({True: 1, False: 0})
        df["tipo_cuenta"] = df["tipo_cuenta"].map({"Corriente": 0, "Ahorro": 1})

        X = df.drop(['id_transaccion', 'etiqueta'], axis=1)
        y = df['etiqueta']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        SingletonModel._model.fit(X_train, y_train)  

    @staticmethod
    def get_model():
        return SingletonModel._model


def evaluate_transaction_action(request: Transaction):
    try:
        modelInstance = SingletonModel()
        model = modelInstance.get_model()
        
        new_transaction_data = prepare_new_transaction_data(request)
        prediction = model.predict(new_transaction_data)

        return {
            "message": "Transaction evaluated",
            "status": 200,
            "data": {"is_fraudulent": bool(prediction[0])}
        }

    except Exception as e:
        return {"message": str(e), "status": 500, "data": {}}