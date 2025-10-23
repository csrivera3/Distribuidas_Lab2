<<<<<<< HEAD
Laboratorio 2 – Sistema Distribuido de Registro de Calificaciones
<img width="1418" height="758" alt="Image" src="https://github.com/user-attachments/assets/b08d1e68-0731-4f49-885e-af050284707c" />
Materia: Aplicaciones Distribuidas
Integrantes: Ronny Ibarra, Javier Ramos, Carlos Rivera
Profesor: Geovanny Cudco
Institución: Universidad de las Fuerzas Armadas ESPE

Introducción

Este laboratorio tiene como propósito implementar un sistema distribuido cliente-servidor para el registro de calificaciones de estudiantes utilizando sockets TCP en Python.

El trabajo se divide en dos etapas:

Servidor secuencial (sin hilos): procesa un cliente a la vez, gestionando operaciones CRUD sobre un archivo CSV.

Servidor concurrente (con hilos): permite manejar múltiples clientes simultáneamente y valida las materias mediante un servidor adicional de NRC, simulando un escenario de microservicios.

El proyecto aplica conceptos de persistencia distribuida, comunicación entre procesos, concurrencia y teorema CAP, priorizando la consistencia y disponibilidad del sistema.

Objetivos
Objetivo general

Desarrollar un sistema distribuido con persistencia en CSV, validación de materias (NRC) y concurrencia mediante hilos.

Objetivos específicos

Ejecutar operaciones CRUD sobre un archivo CSV usando sockets TCP.

Implementar control de duplicados para IDs de estudiantes.

Incorporar concurrencia con hilos (threading).

Desarrollar un servidor externo para validar NRCs.

Asegurar comunicación entre servidores y manejo de errores.

 Arquitectura del sistema

El sistema está conformado por tres módulos principales:

Módulo	Descripción
sin_hilos/	Servidor secuencial que atiende un cliente por conexión.
con_hilos/	Servidor concurrente que maneja múltiples clientes y valida NRCs.
nrcs_server.py	Microservicio independiente que valida los NRCs registrados.
Estructura de directorios
laboratorio_2/
│
├── README.md
├── calificaciones.csv
│
├── sin_hilos/
│   ├── server.py
│   └── client.py
│
├── con_hilos/
│   ├── server.py
│   └── client.py
│
└── nrcs_server.py

Parte 1 – Servidor sin hilos

El servidor secuencial permite manejar operaciones básicas sobre un archivo CSV.
Se establece comunicación cliente-servidor mediante sockets TCP, intercambiando mensajes en formato JSON.

Funcionalidades

Agregar calificación

Buscar por ID

Actualizar calificación

Eliminar registro

Listar todas las calificaciones

 Validaciones

No se permite registrar IDs duplicados.

Si un ID no existe en las operaciones de buscar, actualizar o eliminar, se retorna "ID no encontrado".

El servidor crea automáticamente calificaciones.csv con encabezados si no existe.

Ejemplo de ejecución

Evidencia – Menú del cliente


 Evidencia – Ejecución del servidor sin hilos


Entrada (cliente):

1. Agregar Calificación
ID: 1
Nombre: Carlos
Materia: Distribuidas
Calificación: 20


Salida (servidor):

{"status": "ok", "mensaje": "Calificación agregada para Carlos"}


Archivo generado (calificaciones.csv):

ID,Nombre,Materia,Calificacion
1,Carlos,Distribuidas,20
1,Carlos,Vida,20
7,Alexis,Mate,16


Evidencia – Archivo CSV generado


Parte 2 – Servidor con hilos y validación NRC

En esta segunda fase se desarrolla un servidor concurrente utilizando hilos (threading) para atender múltiples clientes al mismo tiempo.
Además, se agrega un servidor de NRCs que valida las materias antes de registrar o actualizar calificaciones.

Evidencia – Servidor concurrente con múltiples clientes


Comunicación inter-servidores

El servidor de calificaciones consulta al servidor de NRC mediante un socket en el puerto 12346:

Ejemplo de solicitud:

BUSCAR NRC|MAT201


Respuesta del servidor NRC:

{"status": "ok", "materia": "Mate"}


Si el NRC no existe, la operación es rechazada con:

{"status": "error", "mensaje": "Materia/NRC no válida"}

Ejemplo de archivo NRCs (nrcs.csv)
NRC,Materia
MAT101,Matemáticas
FIS201,Física
MAT201,Mate
PROG301,Programación


Evidencia – Servidor NRC activo


Evidencia de ejecución

Evidencia – Cliente agregando calificación válida


Evidencia – Cliente intentando NRC inválido


Evidencia – Operación concurrente


Ejemplo de archivo calificaciones.csv post-ejecución:
ID,Nombre,Materia,Calificacion
1,Carlos,Vida,20
2,Chavi,Digital,12
3,Carlos,Vida,20
4,Angelo,Linux,20

Instrucciones de ejecución
A. Servidor sin hilos
cd sin_hilos
python server.py
python client.py

B. Servidor con hilos
cd con_hilos
python server.py
python client.py

C. Ejecución con validación de NRC
# Terminal 1
python nrcs_server.py

# Terminal 2
cd con_hilos && python server.py

# Terminal 3+
cd con_hilos && python client.py

Limitaciones

No hay control total de acceso concurrente al archivo CSV (posibles race conditions).

Dependencia directa del servidor NRC (si está inactivo, se rechazan los registros).

Escalabilidad limitada a hilos locales (no hay distribución entre nodos).

Conclusiones

Se logró implementar un sistema distribuido modular y funcional con comunicación cliente-servidor.

La adición del servidor de NRCs demostró el principio de microservicios en sistemas distribuidos.

La concurrencia con hilos incrementó la disponibilidad sin afectar la consistencia del sistema.

Se fortalecieron los conceptos del teorema CAP, priorizando consistencia y disponibilidad.

El laboratorio permitió afianzar el uso de sockets TCP, manejo de archivos CSV y coordinación entre procesos.

Referencias

Documentación de Python (socket, csv, json, threading).

Tanenbaum, A. (2021). Distributed Systems: Principles and Paradigms.

Brewer, E. (2000). Towards Robust Distributed Systems (The CAP Theorem).

Universidad de las Fuerzas Armadas ESPE – Laboratorio 2: Aplicaciones Distribuidas.
=======
# Distribuidas_Lab2
#Sistema de Gestión de Calificaciones
>>>>>>> 50f7da8eac7b00989bad98106d254cecd0136002
