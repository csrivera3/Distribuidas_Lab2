
import socket
import csv
import json
import os

ARCHIVO_NRC = 'nrcs.csv'

def inicializar_nrcs():
    """Crea el archivo de NRCs con datos de ejemplo si no existe"""
    if not os.path.exists(ARCHIVO_NRC):
        with open(ARCHIVO_NRC, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['NRC', 'Materia'])
            
            # Agregar NRCs de ejemplo
            nrcs_ejemplo = [
                ['MAT101', 'Matemáticas Básicas'],
                ['MAT102', 'Cálculo Diferencial'],
                ['FIS101', 'Física General'],
                ['FIS102', 'Física Avanzada'],
                ['PROG101', 'Programación I'],
                ['PROG102', 'Programación II'],
                ['BDD101', 'Bases de Datos'],
                ['RED101', 'Redes de Computadoras'],
                ['SO101', 'Sistemas Operativos'],
                ['ING101', 'Inglés Técnico'],
                ['ETC101', 'Ética Profesional'],
                ['ADM101', 'Administración de Proyectos']
            ]
            writer.writerows(nrcs_ejemplo)
        print("Archivo de NRCs creado con datos de ejemplo")

def listar_nrcs():
    """Lista todos los NRCs disponibles"""
    try:
        with open(ARCHIVO_NRC, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return {"status": "ok", "data": data}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def buscar_nrc(nrc_buscar):
    """Busca un NRC específico"""
    try:
        with open(ARCHIVO_NRC, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['NRC'] == nrc_buscar:
                    return {"status": "ok", "data": row}
        
        return {"status": "not_found", "mensaje": f"NRC {nrc_buscar} no encontrado"}
    
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def agregar_nrc(nrc_nuevo, materia_nueva):
    """Agrega un nuevo NRC (opcional, para extensión futura)"""
    try:
        # Verificar si el NRC ya existe
        with open(ARCHIVO_NRC, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['NRC'] == nrc_nuevo:
                    return {"status": "error", "mensaje": f"NRC {nrc_nuevo} ya existe"}
        
        # Agregar el nuevo NRC
        with open(ARCHIVO_NRC, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([nrc_nuevo, materia_nueva])
        
        return {"status": "ok", "mensaje": f"NRC {nrc_nuevo} agregado exitosamente"}
    
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def procesar_comando(comando):
    """Procesa los comandos recibidos de los clientes"""
    partes = comando.strip().split('|')
    op = partes[0]
    
    if op == 'LISTAR_NRC':
        return listar_nrcs()
    
    elif op == 'BUSCAR_NRC' and len(partes) == 2:
        return buscar_nrc(partes[1])
    
    elif op == 'AGREGAR_NRC' and len(partes) == 3:
        return agregar_nrc(partes[1], partes[2])
    
    else:
        return {"status": "error", "mensaje": "Comando inválido"}

# Configuración principal del servidor de NRCs
if _name_ == "_main_":
    # Inicializar el archivo de NRCs
    inicializar_nrcs()
    
    # Crear socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12346))  # Puerto diferente al principal
    server_socket.listen(3)  # Permitir múltiples consultas
    print("=" * 50)
    print("   SERVICIO DE VALIDACIÓN DE NRCs")
    print("=" * 50)
    print("Servidor escuchando en puerto 12346...")
    print("NRCs disponibles: MAT101, MAT102, FIS101, FIS102, PROG101, etc.")
    print("Presiona Ctrl+C para detener el servidor")
    
    try:
        while True:
            # Esperar conexión de cliente
            client_socket, addr = server_socket.accept()
            print(f"\n✅ Cliente NRC conectado desde {addr}")
            
            # Recibir datos del cliente
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(f"📨 Comando recibido: {data}")
                respuesta = procesar_comando(data)
                print(f"📤 Respuesta enviada: {respuesta['status']}")
                client_socket.send(json.dumps(respuesta).encode('utf-8'))
            
            client_socket.close()
            print(f"❌ Cliente NRC {addr} desconectado")
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor de NRCs detenido.")
    finally:
        server_socket.close()