import socket
import json

def mostrar_menu():
    menu = """
--- Menú de Calificaciones ---
1. Agregar calificación
2. Buscar por ID
3. Actualizar calificación
4. Listar todas
5. Eliminar por ID
6. Salir
"""
    print(menu, flush=True)  
    return input("Elija opción: ").strip()  

def enviar_comando(comando):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        client_socket.send(comando.encode('utf-8'))
        respuesta = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
        return json.loads(respuesta)
    except Exception as e:
        return {"status": "error", "mensaje": f"No se pudo conectar al servidor: {e}"}

while True:
    opcion = mostrar_menu()

    if opcion == "1":
        id_est = input("ID: ").strip()
        nombre = input("Nombre: ").strip()
        nrc_type = input("¿Ingresar NRC por nombre o número? (nombre/numero): ").lower()
        if nrc_type == 'nombre':
            materia = input("Nombre de la materia: ")
        elif nrc_type == 'numero':
            materia = input("Número de NRC: ")
        else:
            print("Opción inválida. Use 'nombre' o 'numero'.")
            continue
        calif = input("Calificación: ").strip()
        res = enviar_comando(f"AGREGAR|{id_est}|{nombre}|{materia}|{calif}")
        print(res.get("mensaje", "Sin mensaje"))

    elif opcion == "2":
        id_est = input("ID: ").strip()
        res = enviar_comando(f"BUSCAR|{id_est}")
        if res.get("status") == "ok":
            data = res["data"]
            print(f"Nombre: {data['Nombre']}, Materia: {data['Materia']}, Calificación: {data['Calificacion']}")
        else:
            print(res.get("mensaje", "Sin mensaje"))

    elif opcion == "3":
        id_est = input("ID: ").strip()
        nueva_calif = input("Nueva calificación: ").strip()
        res = enviar_comando(f"ACTUALIZAR|{id_est}|{nueva_calif}")
        print(res.get("mensaje", "Sin mensaje"))

    elif opcion == "4":
        res = enviar_comando("LISTAR")
        if res.get("status") == "ok":
            for row in res["data"]:
                print(f"ID: {row['ID_Estudiante']}, Nombre: {row['Nombre']}, Materia: {row['Materia']}, Calificación: {row['Calificacion']}")
        else:
            print(res.get("mensaje", "Sin mensaje"))

    elif opcion == "5":
        id_est = input("ID: ").strip()
        res = enviar_comando(f"ELIMINAR|{id_est}")
        print(res.get("mensaje", "Sin mensaje"))

    elif opcion == "6":
        print("Saliendo del programa...")
        break

    else:
        print("Opción inválida, por favor intente nuevamente.")