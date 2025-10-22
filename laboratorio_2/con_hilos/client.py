import socket
import json

def enviar_comando(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 12345))
    s.send(cmd.encode())
    data = s.recv(4096).decode()
    s.close()
    return json.loads(data)

def menu():
    print("\n📋 MENÚ PRINCIPAL")
    print("1. Agregar calificación")
    print("2. Buscar por ID")
    print("3. Actualizar calificación")
    print("4. Eliminar por ID")
    print("5. Listar todos")
    print("6. Salir")
    return input("Seleccione opción: ")

while True:
    opcion = menu()
    if opcion == '1':
        id_ = input("ID: ")
        nombre = input("Nombre: ")
        materia = input("Materia: ")
        calif = input("Calificación: ")
        resp = enviar_comando(f"AGREGAR|{id_}|{nombre}|{materia}|{calif}")
    elif opcion == '2':
        id_ = input("ID: ")
        resp = enviar_comando(f"BUSCAR|{id_}")
    elif opcion == '3':
        id_ = input("ID: ")
        nueva = input("Nueva calificación: ")
        resp = enviar_comando(f"ACTUALIZAR|{id_}|{nueva}")
    elif opcion == '4':
        id_ = input("ID: ")
        resp = enviar_comando(f"ELIMINAR|{id_}")
    elif opcion == '5':
        resp = enviar_comando("LISTAR")
    elif opcion == '6':
        break
    else:
        print("Opción inválida.")
        continue
    print("Respuesta:", resp)
