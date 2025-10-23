# Laboratorio 2 – Sistema Distribuido de Registro de Calificaciones

**Materia**: Aplicaciones Distribuidas  
**Integrantes**: Ronny Ibarra, Javier Ramos, Carlos Rivera  
**Profesor**: Geovanny Cudco  
**Institución**: Universidad de las Fuerzas Armadas ESPE  
=======

Laboratorio 2 – Sistema Distribuido de Registro de Calificaciones
Materia: Aplicaciones Distribuidas
Integrantes: Ronny Ibarra, Javier Ramos, Carlos Rivera
Profesor: Geovanny Cudco
Institución: Universidad de las Fuerzas Armadas ESPE


---

## Introducción

Este laboratorio implementa un **sistema distribuido cliente-servidor** para el registro de calificaciones de estudiantes utilizando **sockets TCP** en Python. El proyecto se divide en dos etapas:

1. **Servidor Secuencial (sin hilos)**: Procesa un cliente a la vez, gestionando operaciones CRUD sobre un archivo CSV.
2. **Servidor Concurrente (con hilos)**: Maneja múltiples clientes simultáneamente y valida materias mediante un servidor de NRC, simulando un escenario de microservicios.

El sistema aplica conceptos de **persistencia distribuida**, **comunicación entre procesos**, **concurrencia** y el **teorema CAP**, priorizando **consistencia** y **disponibilidad**.

---

## Objetivos

### Objetivo General
Desarrollar un sistema distribuido con persistencia en CSV, validación de materias (NRC) y concurrencia mediante hilos.

### Objetivos Específicos
- Ejecutar operaciones **CRUD** sobre un archivo CSV usando sockets TCP.
- Implementar control de **duplicados** para IDs de estudiantes.
- Incorporar **concurrencia** con hilos (`threading`).
- Desarrollar un servidor externo para **validar NRCs**.
- Asegurar **comunicación** entre servidores y manejo de errores.

---

## Arquitectura del Sistema

El sistema consta de tres módulos principales:

| **Módulo**         | **Descripción**                                                                 |
|--------------------|---------------------------------------------------------------------------------|
| `sin_hilos/`       | Servidor secuencial que atiende un cliente por conexión.                        |
| `con_hilos/`       | Servidor concurrente que maneja múltiples clientes y valida NRCs.               |
| `nrcs_server.py`   | Microservicio independiente que valida los NRCs registrados.                    |

### Estructura de Directorios
```
laboratorio_2/
├── README.md
├── calificaciones.csv
├── sin_hilos/
│   ├── server.py
│   └── client.py
├── con_hilos/
│   ├── server.py
│   └── client.py
└── nrcs_server.py
```

---

## Parte 1 – Servidor Sin Hilos

El servidor secuencial gestiona operaciones **CRUD** sobre un archivo `calificaciones.csv` utilizando sockets TCP y mensajes en formato JSON.

### Funcionalidades
- **Agregar calificación**: Registra una nueva calificación.
- **Buscar por ID**: Busca un registro por ID de estudiante.
- **Actualizar calificación**: Modifica un registro existente.
- **Eliminar registro**: Elimina un registro por ID.
- **Listar calificaciones**: Muestra todas las calificaciones.

### Validaciones
- **Prohibición de IDs duplicados**: No se permite registrar IDs existentes.
- **Manejo de errores**: Si un ID no existe en operaciones de buscar, actualizar o eliminar, se retorna `"ID no encontrado"`.
- **Creación automática**: Si `calificaciones.csv` no existe, se crea con encabezados.

### Ejemplo de Ejecución
**Entrada (Cliente)**:
```
1. Agregar Calificación
ID: 1
Nombre: Carlos
Materia: Distribuidas
Calificación: 20
```

**Salida (Servidor)**:
```json
{"status": "ok", "mensaje": "Calificación agregada para Carlos"}
```

**Archivo Generado (`calificaciones.csv`)**:
```csv
ID,Nombre,Materia,Calificacion
1,Carlos,Distribuidas,20
1,Carlos,Vida,20
7,Alexis,Mate,16
```

---

## Parte 2 – Servidor Con Hilos y Validación de NRC

El servidor concurrente utiliza **hilos** (`threading`) para atender múltiples clientes simultáneamente. Además, integra un servidor de NRCs para validar materias antes de registrar o actualizar calificaciones.

### Comunicación Inter-Servidores
El servidor de calificaciones consulta al servidor de NRCs mediante un socket en el puerto `12346`.

**Ejemplo de Solicitud**:
```
```
**<img width="1418" height="758" alt="Image" src="https://github.com/user-attachments/assets/5be1f6c2-07dd-4f7f-96ae-f7f09bc86eab" />**:
BUSCAR NRC|MAT201

**Respuesta del Servidor NRC**:
```json
{"status": "ok", "materia": "Mate"}
```

**Error por NRC Inválido**:
```json
{"status": "error", "mensaje": "Materia/NRC no válida"}
```

### Ejemplo de Archivo NRCs (`nrcs.csv`)
```csv
NRC,Materia
MAT101,Matemáticas
FIS201,Física
MAT201,Mate
PROG301,Programación
```

### Ejemplo de Archivo Calificaciones (`calificaciones.csv`)
```csv
ID,Nombre,Materia,Calificacion
1,Carlos,Vida,20
2,Chavi,Digital,12
3,Carlos,Vida,20
4,Angelo,Linux,20
```

---

## Instrucciones de Ejecución

### A. Servidor Sin Hilos
```bash
cd sin_hilos
python server.py
python client.py
```

### B. Servidor Con Hilos
```bash
cd con_hilos
python server.py
python client.py
```

### C. Ejecución con Validación de NRC
1. **Terminal 1**: Iniciar servidor NRC
   ```bash
   python nrcs_server.py
   ```
2. **Terminal 2**: Iniciar servidor de calificaciones
   ```bash
   cd con_hilos && python server.py
   ```
3. **Terminal 3+**: Iniciar clientes
   ```bash
   cd con_hilos && python client.py
   ```

---

## Limitaciones
- **Acceso concurrente**: No hay control total de acceso al archivo CSV, lo que puede causar **race conditions**.
- **Dependencia del servidor NRC**: Si está inactivo, los registros son rechazados.
- **Escalabilidad limitada**: Los hilos son locales, sin distribución entre nodos.

---

## Conclusiones
- Se implementó un sistema distribuido modular y funcional con comunicación cliente-servidor.
- El servidor de NRCs demostró el principio de **microservicios** en sistemas distribuidos.
- La concurrencia con hilos incrementó la **disponibilidad** sin afectar la **consistencia**.
- Se aplicaron conceptos del **teorema CAP**, priorizando consistencia y disponibilidad.
- El laboratorio fortaleció conocimientos en **sockets TCP**, manejo de archivos CSV y coordinación entre procesos.

---

## Referencias
- Documentación oficial de Python (`socket`, `csv`, `json`, `threading`).
- Tanenbaum, A. (2021). *Distributed Systems: Principles and Paradigms*.
- Brewer, E. (2000). *Towards Robust Distributed Systems (The CAP Theorem)*.
- Universidad de las Fuerzas Armadas ESPE – Laboratorio 2: Aplicaciones Distribuidas.
