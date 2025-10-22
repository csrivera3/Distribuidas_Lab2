import socket
import json
import threading

def enviar_comando(cmd):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 12345))
        s.send(cmd.encode())
        data = s.recv(4096).decode()
        s.close()
        resp = json.loads(data)
        print("Respuesta:", resp)
    except Exception as e:
        print("Error:", e)

def menu():
    print("\nMENÚ PRINCIPAL")
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
        threading.Thread(target=enviar_comando, args=(f"AGREGAR|{id_}|{nombre}|{materia}|{calif}",)).start()
    elif opcion == '2':
        id_ = input("ID: ")
        threading.Thread(target=enviar_comando, args=(f"BUSCAR|{id_}",)).start()
    elif opcion == '3':
        id_ = input("ID: ")
        nueva = input("Nueva calificación: ")
        threading.Thread(target=enviar_comando, args=(f"ACTUALIZAR|{id_}|{nueva}",)).start()
    elif opcion == '4':
        id_ = input("ID: ")
        threading.Thread(target=enviar_comando, args=(f"ELIMINAR|{id_}",)).start()
    elif opcion == '5':
        threading.Thread(target=enviar_comando, args=("LISTAR",)).start()
    elif opcion == '6':
        break
    else:
        print("Opción inválida.")
