import csv
import random
from py2neo import Graph, Node, Relationship
from datetime import datetime
from uuid import uuid4
from faker import Faker

fake = Faker()

# Conexión a Neo4j
graph = Graph("neo4j+s://bead2851.databases.neo4j.io", auth=("neo4j", "ZQJ2jIyYXp3eZjy8AVDzVb9CxjiYzkNJTjkzjHRx440"))

def generar_empleados_clientes(n, clientes):
    empleados_clientes = random.sample(clientes, n)
    for empleado_cliente in empleados_clientes:
        empleado_cliente.update({"empleado_id": str(uuid4()), "fecha_contratacion": str(fake.date_between(start_date='-10y', end_date='today'))})
    return empleados_clientes

def cargar_nodos_desde_csv(nombre_archivo, etiqueta):
    with open(f"data/{nombre_archivo}", 'r', newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            if etiqueta == 'Cliente':
                fila['numeros_alternativos'] = [fake.phone_number() for _ in range(random.randint(1, 3))]
            nodo = Node(etiqueta, **fila)
            graph.create(nodo)

def crear_relaciones():
    # Obtener todos los nodos necesarios
    clientes = list(graph.nodes.match("Cliente"))
    cuentas = list(graph.nodes.match("Cuenta"))
    transacciones = list(graph.nodes.match("Transacción"))
    bancos = list(graph.nodes.match("Banco"))
    productos = list(graph.nodes.match("Producto"))

    # Cliente-Tiene-Cuenta
    for cliente in clientes:
        cuenta_asociada = random.choice(cuentas)
        rel = Relationship(cliente, "TIENE", cuenta_asociada, fecha_creacion=str(datetime.now()), relacion_id=str(uuid4()), detalle=fake.sentence())
        graph.create(rel)

    # Transacción de una cuenta a otra
    for transaccion in transacciones:
        cuenta_origen = random.choice(cuentas)
        cuenta_destino = random.choice([c for c in cuentas if c != cuenta_origen])
        rel_origen = Relationship(cuenta_origen, "REALIZA_TRANSACCION", transaccion, fecha_creacion=str(datetime.now()), relacion_id=str(uuid4()), detalle=fake.sentence())
        rel_destino = Relationship(transaccion, "RECIBE_TRANSACCION", cuenta_destino, fecha_creacion=str(datetime.now()), relacion_id=str(uuid4()), detalle=fake.sentence())
        graph.create(rel_origen)
        graph.create(rel_destino)

    # Cliente-Usa-Producto
    for cliente in clientes:
        producto_usado = random.choice(productos)
        rel = Relationship(cliente, "USA", producto_usado, fecha_creacion=str(datetime.now()), relacion_id=str(uuid4()), detalle=fake.sentence())
        graph.create(rel)

    # Banco-Gestiona-Cuenta
    for banco in bancos:
        cuenta_gestionada = random.choice(cuentas)
        rel = Relationship(banco, "GESTIONA", cuenta_gestionada, fecha_creacion=str(datetime.now()), relacion_id=str(uuid4()), detalle=fake.sentence())
        graph.create(rel)

    # Banco-Ofrece-Producto
    for banco in bancos:
        producto_ofrecido = random.choice(productos)
        rel = Relationship(banco, "OFRECE", producto_ofrecido, fecha_creacion=str(datetime.now()), relacion_id=str(uuid4()), detalle=fake.sentence())
        graph.create(rel)

    # Cliente-Pertenece-A-Banco
    for cliente in clientes:
        banco_perteneciente = random.choice(bancos)
        rel = Relationship(cliente, "PERTENECE_A", banco_perteneciente, fecha_creacion=str(datetime.now()), relacion_id=str(uuid4()), detalle=fake.sentence())
        graph.create(rel)

    # Transacción-Realizada-En-Banco
    for transaccion in transacciones:
        banco_realizador = random.choice(bancos)
        rel = Relationship(transaccion, "REALIZADA_EN", banco_realizador, fecha_creacion=str(datetime.now()), relacion_id=str(uuid4()), detalle=fake.sentence())
        graph.create(rel)

    # Producto-Vinculado-A-Cuenta
    for producto in productos:
        cuenta_vinculada = random.choice(cuentas)
        rel = Relationship(producto, "VINCULADO_A", cuenta_vinculada, fecha_creacion=str(datetime.now()), relacion_id=str(uuid4()), detalle=fake.sentence())
        graph.create(rel)

    # Cliente-Reporta-Transacción (como fraude)
    for cliente in clientes:
        # Asumiendo que no todos los clientes reportan transacciones
        if random.choices([True, False], weights=[20, 80], k=1)[0]:
            transaccion_reportada = random.choice(transacciones)
            rel = Relationship(cliente, "REPORTA", transaccion_reportada, fecha_creacion=str(datetime.now()), relacion_id=str(uuid4()), detalle="Transacción sospechosa reportada por el cliente")
            graph.create(rel)


def cargar_datos_y_crear_relaciones():
    # Cargar nodos
    cargar_nodos_desde_csv('clientes.csv', 'Cliente')
    cargar_nodos_desde_csv('cuentas.csv', 'Cuenta')
    cargar_nodos_desde_csv('transacciones.csv', 'Transacción')
    cargar_nodos_desde_csv('bancos.csv', 'Banco')
    cargar_nodos_desde_csv('productos.csv', 'Producto')

    clientes = list(graph.nodes.match("Cliente"))
    empleados_clientes = generar_empleados_clientes(100, clientes)
    for empleado_cliente in empleados_clientes:
        empleado_cliente_nodo = Node("Cliente", "Empleado", **empleado_cliente)
        graph.create(empleado_cliente_nodo)

    # Crear relaciones
    crear_relaciones()

if __name__ == '__main__':
    cargar_datos_y_crear_relaciones()
