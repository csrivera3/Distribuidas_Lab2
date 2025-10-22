import socket
import threading
import csv
import os
import json

ARCHIVO_CSV = "calificaciones.csv"
lock = threading.Lock()

# -----------------------------
# Funciones de gestión del CSV
# -----------------------------
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
    return {"status": "ok", "mensaje": "Calificación agregada correctamente."}

def buscar_por_id(id_est):
    with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["ID"] == id_est:
                return {"status": "ok", "data": row}
    return {"status": "error", "mensaje": "Estudiante no encontrado."}

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
    return {"status": "ok", "mensaje": "Calificación actualizada."} if encontrado else {"status": "error", "mensaje": "ID no encontrado."}

def eliminar_por_id(id_est):
    filas, eliminado = [], False
    with lock:
        with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["ID"] != id_est:
                    filas.append(row)
                else:
                    eliminado = True
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["ID", "Nombre", "Materia", "Calificacion"])
            writer.writeheader()
            writer.writerows(filas)
    if eliminado:
        return {"status": "ok", "mensaje": "Registro eliminado."}
    else:
        return {"status": "error", "mensaje": "ID no encontrado."}

def listar_todos():
    with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        return {"status": "ok", "data": reader}

# -----------------------------
# Procesamiento de comandos
# -----------------------------
def procesar_comando(cmd):
    partes = cmd.split('|')
    op = partes[0].upper()

    if op == "AGREGAR":
        return agregar_calificacion(*partes[1:])
    elif op == "BUSCAR":
        return buscar_por_id(partes[1])
    elif op == "ACTUALIZAR":
        return actualizar_calificacion(partes[1], partes[2])
    elif op == "ELIMINAR":
        return eliminar_por_id(partes[1])
    elif op == "LISTAR":
        return listar_todos()
    else:
        return {"status": "error", "mensaje": "Comando inválido."}

# -----------------------------
# Manejo de hilos y conexiones
# -----------------------------
def manejar_cliente(conn, addr):
    print(f"🔗 Conexión desde {addr}")
    try:
        data = conn.recv(4096).decode()
        if not data:
            return
        print(f"📩 Comando recibido: {data}")
        resp = procesar_comando(data)
        conn.send(json.dumps(resp, indent=2, ensure_ascii=False).encode())
    except Exception as e:
        print("❌ Error manejando cliente:", e)
    finally:
        conn.close()
        print(f"🔒 Conexión cerrada con {addr}")

# -----------------------------
# Servidor principal
# -----------------------------
def main():
    inicializar_csv()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 12345))
    s.listen(5)
    print("💻 Servidor concurrente listo en puerto 12345...")

    try:
        while True:
            conn, addr = s.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo.start()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido manualmente.")
    finally:
        s.close()

# -----------------------------
if __name__ == "__main__":
    main()
