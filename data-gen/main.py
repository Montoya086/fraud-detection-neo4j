import csv
import random
from faker import Faker
from datetime import datetime

fake = Faker()

folder = "data/"

def generar_clientes(n):
    return [{"id": i, "nombre": fake.name(), "direccion": fake.address(), "telefono": fake.phone_number(), "esPremium": fake.boolean()} for i in range(n)]

def generar_cuentas(n, clientes_ids):
    cuentas = []
    for i in range(n):
        cliente_id = random.choice(clientes_ids)
        cuenta = {"id": i, "cliente_id": cliente_id, "numeroCuenta": fake.iban(), "saldo": round(random.uniform(1000, 100000), 2), "tipoCuenta": random.choice(["Ahorro", "Corriente"]), "fechaCreacion": fake.date_between(start_date='-10y', end_date='today')}
        cuentas.append(cuenta)
    return cuentas

def generar_transacciones(n, cuentas_ids):
    transacciones = []
    for i in range(n):
        cuenta_id = random.choice(cuentas_ids)
        transaccion = {"id": i, "cuenta_id": cuenta_id, "monto": round(random.uniform(5, 10000), 2), "fecha": fake.date_time_between(start_date='-1y', end_date='now'), "esFraudulenta": fake.boolean(), "metodoPago": random.choice(["Tarjeta", "Transferencia", "Efectivo"])}
        transacciones.append(transaccion)
    return transacciones

def generar_bancos(n):
    return [{"id": i, "nombre": fake.company(), "direccion": fake.address(), "pais": fake.country(), "telefono": fake.phone_number(), "calificacion": random.randint(1, 5)} for i in range(n)]

def generar_productos(n, bancos_ids):
    productos = []
    for i in range(n):
        banco_id = random.choice(bancos_ids)
        producto = {"id": i, "banco_id": banco_id, "tipo": random.choice(["Tarjeta de Crédito", "Préstamo Personal", "Hipoteca"]), "condiciones": fake.sentence(), "fechaOferta": fake.date_between(start_date='-5y', end_date='today'), "limiteCredito": random.randint(1000, 50000)}
        productos.append(producto)
    return productos

def guardar_csv(datos, nombre_archivo):
    with open(folder + nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=datos[0].keys())
        writer.writeheader()
        writer.writerows(datos)

def generar_y_guardar_datos():
    clientes = generar_clientes(1000)
    bancos = generar_bancos(100)

    clientes_ids = [cliente['id'] for cliente in clientes]
    bancos_ids = [banco['id'] for banco in bancos]

    cuentas = generar_cuentas(1500, clientes_ids)
    transacciones = generar_transacciones(2000, [cuenta['id'] for cuenta in cuentas])
    productos = generar_productos(400, bancos_ids)

    guardar_csv(clientes, 'clientes.csv')
    guardar_csv(cuentas, 'cuentas.csv')
    guardar_csv(transacciones, 'transacciones.csv')
    guardar_csv(bancos, 'bancos.csv')
    guardar_csv(productos, 'productos.csv')

if __name__ == '__main__':
    generar_y_guardar_datos()
