import socket
import threading
import csv
import os
import json

ARCHIVO_CSV = "calificaciones.csv"
lock = threading.Lock()

def inicializar_csv():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Nombre", "Materia", "Calificacion"])

def agregar_calificacion(id_est, nombre, materia, calificacion):
    with lock:
        with open(ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([id_est, nombre, materia, calificacion])
    return {"status": "ok", "mensaje": "Calificación agregada."}

def buscar_por_id(id_est):
    with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["ID"] == id_est:
                return {"status": "ok", "data": row}
    return {"status": "error", "mensaje": "No encontrado."}

def actualizar_calificacion(id_est, nueva_calif):
    filas, encontrado = [], False
    with lock:
        with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["ID"] == id_est:
                    row["Calificacion"] = nueva_calif
                    encontrado = True
                filas.append(row)
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["ID", "Nombre", "Materia", "Calificacion"])
            writer.writeheader()
            writer.writerows(filas)
    return {"status": "ok", "mensaje": "Actualizado."} if encontrado else {"status": "error", "mensaje": "No existe ID."}

def procesar_comando(cmd):
    partes = cmd.split('|')
    op = partes[0].upper()
    if op == "AGREGAR":
        return agregar_calificacion(*partes[1:])
    elif op == "BUSCAR":
        return buscar_por_id(partes[1])
    elif op == "ACTUALIZAR":
        return actualizar_calificacion(partes[1], partes[2])
    else:
        return {"status": "error", "mensaje": "Comando inválido"}

def manejar_cliente(conn, addr):
    print(f"Conexión desde {addr}")
    try:
        data = conn.recv(4096).decode()
        resp = procesar_comando(data)
        conn.send(json.dumps(resp).encode())
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

def main():
    inicializar_csv()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 12345))
    s.listen(5)
    print("💻 Servidor concurrente listo en puerto 12345...")

    while True:
        conn, addr = s.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()

if __name__ == "__main__":
    main()
