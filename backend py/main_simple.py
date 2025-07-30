#!/usr/bin/env python3
"""
Sistema Médico BI - API Principal
Integración con Blockchain y Snowflake
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import snowflake.connector
from web3 import Web3
import json


# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Sistema Médico BI API", version="1.0.0")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos
app.mount("/PrediSalud", StaticFiles(directory="PrediSalud"), name="predisalud")

# Servir archivos CSS, JS e imágenes directamente desde templates
app.mount("/css", StaticFiles(directory="PrediSalud/templates/css"), name="css")
app.mount("/js", StaticFiles(directory="PrediSalud/templates/js"), name="js")
app.mount("/images", StaticFiles(directory="PrediSalud/templates/images"), name="images")
app.mount("/plugins", StaticFiles(directory="PrediSalud/templates/plugins"), name="plugins")

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_aqui")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración Snowflake
SNOWFLAKE_CONFIG = {
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': os.getenv('SNOWFLAKE_DATABASE'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA')
}

# Configuración Web3 - Usando la misma configuración que Hardhat
ETHEREUM_RPC_URL = os.getenv('ETHEREUM_RPC_URL', 'http://127.0.0.1:8545')
SEPOLIA_URL = os.getenv('SEPOLIA_URL', ETHEREUM_RPC_URL)  # Usar variable de entorno como Hardhat
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

print(f"🔗 Configurando Web3 con URL: {SEPOLIA_URL}")

# Inicializar Web3
w3 = Web3(Web3.HTTPProvider(SEPOLIA_URL))

# Cargar direcciones de contratos
try:
    with open('blockchain/contract-addresses-sepolia.json', 'r') as f:
        contract_addresses = json.load(f)
        print(f"✅ Contratos cargados: {list(contract_addresses.keys())}")
except FileNotFoundError:
    print("⚠️ Archivo de contratos no encontrado, usando direcciones por defecto")
    contract_addresses = {
        "MedicalRecords": "0x0000000000000000000000000000000000000000",
        "PatientConsent": "0x0000000000000000000000000000000000000000", 
        "MedicalAudit": "0x0000000000000000000000000000000000000000"
    }

# Modelos Pydantic
class UserRegister(BaseModel):
    username: str
    password: str
    email: str
    rol: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class PacienteRegistro(BaseModel):
    nombre: str
    apellidos: str
    fecha_nacimiento: str
    genero: str
    dni: str
    telefono: str
    email: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    codigo_postal: Optional[str] = None
    grupo_sanguineo: Optional[str] = None
    alergias: Optional[str] = None
    medicamentos: Optional[str] = None
    antecedentes: Optional[str] = None
    contacto_emergencia_nombre: Optional[str] = None
    contacto_emergencia_relacion: Optional[str] = None
    contacto_emergencia_telefono: Optional[str] = None
    consentimiento_datos: bool = False
    consentimiento_emergencia: bool = False
    consentimiento_investigacion: bool = False

class MedicalRecordCreate(BaseModel):
    patient_id: str
    diagnosis: str
    treatment: str

class PatientConsentUpdate(BaseModel):
    data_sharing: bool
    research_participation: bool
    emergency_access: bool

class AuditLogCreate(BaseModel):
    action: str
    details: str
    record_hash: Optional[str] = None

class PacienteRegistroOriginal(BaseModel):
    id_paciente: str
    nombre_completo: str
    edad: Optional[int] = None
    genero: str
    fecha_nacimiento: Optional[str] = None
    domicilio_completo: Optional[str] = None
    municipio: Optional[str] = None
    codigo_postal: Optional[str] = None
    institucion: Optional[str] = None
    clave_paciente: Optional[str] = None
    consentimiento_informado: bool
    historial_hospitalizaciones: Optional[str] = None
    historial_cirugias: Optional[str] = None
    alergias: Optional[str] = None
    antecedentes_familiares: Optional[str] = None
    antecedentes_personales: Optional[str] = None
    fecha_consulta: str
    hora_consulta: str
    signos_vitales_temperatura: Optional[float] = None
    signos_vitales_frecuencia_cardiaca: Optional[int] = None
    signos_vitales_glucosa: Optional[int] = None
    sintomas: str
    tiempo_evolucion_sintomas: Optional[str] = None
    diagnostico_cie10: Optional[str] = None
    diagnostico_base: Optional[str] = None
    tratamiento: Optional[str] = None
    resultado_laboratorio: Optional[str] = None
    pronostico: Optional[str] = None
    clasificacion_riesgo: str
    notas_evolucion: Optional[str] = None

# Función para conectar a Snowflake
def get_snowflake_connection():
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        return conn
    except Exception as e:
        print(f"Error conectando a Snowflake: {str(e)}")
        return None

# Función para verificar token JWT
def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token requerido")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Función para crear token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar usuario en base de datos
def verify_user(username: str, password: str):
    # Simulación de verificación de usuario
    # En producción, verificarías contra la base de datos
    users = {
        "doctor1": {"password": "password123", "rol": "doctor", "user_id": 1},
        "nurse1": {"password": "password123", "rol": "nurse", "user_id": 2},
        "admin1": {"password": "password123", "rol": "admin", "user_id": 3},
        "staff1": {"password": "password123", "rol": "staff", "user_id": 4},
        "user1": {"password": "password123", "rol": "user", "user_id": 5}
    }
    
    if username in users and users[username]["password"] == password:
        return users[username]
    return None

# Endpoints
@app.get("/")
def root():
    """Página de inicio del sistema"""
    return FileResponse("PrediSalud/templates/index.html")

@app.get("/api/status")
def api_status():
    """Status de la API (el JSON que antes estaba en /)"""
    return {
        "message": "Sistema Médico BI API",
        "version": "1.0.0",
        "status": "running",
        "blockchain": "connected" if w3.is_connected() else "disconnected"
    }

@app.get("/login")
def serve_login():
    return FileResponse("PrediSalud/templates/login_integrated.html")

@app.get("/login-new")
def serve_login_new():
    return FileResponse("PrediSalud/templates/login_integrated.html")

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse("PrediSalud/templates/dashboard_mejorado.html")

@app.get("/dashboard.html")
def serve_dashboard_html():
    return FileResponse("PrediSalud/templates/dashboard_mejorado.html")

@app.get("/dashboard2.html")
def serve_dashboard2():
    """Servir dashboard principal del sistema médico"""
    return FileResponse("PrediSalud/templates/dashboard2.html")

@app.get("/registro")
def serve_registro():
    return FileResponse("PrediSalud/templates/registro.html")

@app.post("/api/auth/logout")
def logout_user():
    """Endpoint de logout - solo confirma el logout del lado del servidor"""
    return {
        "status": "success",
        "message": "Sesión cerrada exitosamente"
    }

# Endpoints adicionales para las páginas del dashboard
@app.get("/index.html")
def serve_index():
    return FileResponse("PrediSalud/templates/index.html")

@app.get("/dashboard-analytics.html")
def serve_dashboard_analytics():
    return FileResponse("PrediSalud/templates/dashboard-analytics.html")

@app.get("/table-databases.html")
def serve_table_databases():
    return FileResponse("PrediSalud/templates/table-databases.html")

@app.get("/registro.html")
def serve_registro_html():
    return FileResponse("PrediSalud/templates/registro.html")

@app.get("/about.html")
def serve_about():
    return FileResponse("PrediSalud/templates/about.html")

@app.get("/contact.html")
def serve_contact():
    return FileResponse("PrediSalud/templates/contact.html")

@app.get("/service.html")
def serve_service():
    return FileResponse("PrediSalud/templates/service.html")

@app.get("/appoinment.html")
def serve_appointment():
    return FileResponse("PrediSalud/templates/appoinment.html")

@app.get("/department.html")
def serve_department():
    return FileResponse("PrediSalud/templates/department.html")

@app.get("/doctor.html")
def serve_doctor():
    return FileResponse("PrediSalud/templates/doctor.html")

@app.get("/calendar.html")
def serve_calendar():
    # Si no existe calendar.html, redirigir a agenda médica disponible
    return FileResponse("PrediSalud/templates/appoinment.html")

@app.get("/registro_pacientes.html")
def serve_registro_pacientes():
    return FileResponse("PrediSalud/templates/registro_pacientes.html")

@app.get("/dashboard_mejorado.html")
def serve_dashboard_mejorado():
    return FileResponse("PrediSalud/templates/dashboard_mejorado.html")

# Páginas de análisis y grupos de riesgo
@app.get("/grupos_riesgo_professional.html")
def serve_grupos_riesgo_professional():
    return FileResponse("PrediSalud/templates/grupos_riesgo_professional.html")

@app.get("/grupos_riesgo_glassmorphism.html")
def serve_grupos_riesgo_glassmorphism():
    return FileResponse("PrediSalud/templates/grupos_riesgo_glassmorphism.html")

@app.get("/analisis_tratamientos.html")
def serve_analisis_tratamientos():
    return FileResponse("PrediSalud/templates/analisis_tratamientos.html")

@app.get("/blockchain_records.html")
def serve_blockchain_records():
    return FileResponse("PrediSalud/templates/blockchain_records.html")

@app.get("/dashboard_principal.html")
def serve_dashboard_principal():
    return FileResponse("PrediSalud/templates/dashboard_principal.html")

@app.get("/dashboard_sigma.html")
def serve_dashboard_sigma():
    return FileResponse("PrediSalud/templates/dashboard_sigma.html")

# Redirecciones para páginas que no existen a páginas relevantes
@app.get("/form_elements.html")
def serve_form_elements():
    # Redirigir a registro de pacientes
    return FileResponse("PrediSalud/templates/registro_pacientes.html")

@app.get("/table_basic.html")
def serve_table_basic():
    # Redirigir a tabla de bases de datos
    return FileResponse("PrediSalud/templates/table-databases.html")

@app.get("/chart-inline.html")
def serve_chart_inline():
    # Redirigir a dashboard de análisis
    return FileResponse("PrediSalud/templates/dashboard-analytics.html")

@app.get("/datamaps.html")
def serve_datamaps():
    # Redirigir a análisis de grupos de riesgo
    return FileResponse("PrediSalud/templates/grupos_riesgo_professional.html")

# Endpoints genéricos para páginas en desarrollo
@app.get("/form_advanced.html")
def serve_form_advanced():
    return FileResponse("PrediSalud/templates/dashboard-analytics.html")

@app.get("/form_validation.html")
def serve_form_validation():
    return FileResponse("PrediSalud/templates/grupos_riesgo_professional.html")

@app.get("/form_wizard.html")
def serve_form_wizard():
    return FileResponse("PrediSalud/templates/dashboard-analytics.html")

@app.get("/table_advanced.html")
def serve_table_advanced():
    return FileResponse("PrediSalud/templates/table-databases.html")

@app.get("/table_datatables.html")
def serve_table_datatables():
    return FileResponse("PrediSalud/templates/table-databases.html")

@app.get("/chart-chartjs.html")
def serve_chart_chartjs():
    return FileResponse("PrediSalud/templates/dashboard-analytics.html")

@app.get("/chart-apexcharts.html")
def serve_chart_apexcharts():
    return FileResponse("PrediSalud/templates/dashboard-analytics.html")

# Endpoint genérico para páginas HTML no definidas (al final)
from fastapi import Request
from fastapi.responses import HTMLResponse
import os

@app.get("/{page_name}.html")
def serve_generic_html_page(page_name: str):
    """Endpoint genérico para páginas HTML no definidas"""
    file_path = f"PrediSalud/templates/{page_name}.html"
    
    # Verificar si el archivo existe
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        # Si no existe, redirigir al index
        return FileResponse("PrediSalud/templates/index.html")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "blockchain": "connected" if w3.is_connected() else "disconnected",
        "snowflake": "connected" if get_snowflake_connection() else "disconnected"
    }

@app.post("/api/auth/register")
def register_user(user: UserRegister):
    try:
        # Verificar si el usuario ya existe
        conn = get_snowflake_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Verificar si el usuario existe
        cursor.execute(
            "SELECT COUNT(*) FROM USUARIOS WHERE USERNAME = %s",
            (user.username,)
        )
        result = cursor.fetchone()
        
        if result[0] > 0:
            raise HTTPException(status_code=400, detail="El usuario ya existe")
        
        # Insertar nuevo usuario
        cursor.execute("""
            INSERT INTO USUARIOS (USERNAME, PASSWORD, EMAIL, ROL, FECHA_REGISTRO)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP())
        """, (user.username, user.password, user.email, user.rol))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "message": "Usuario registrado exitosamente",
            "username": user.username,
            "rol": user.rol
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando usuario: {str(e)}")

@app.post("/api/auth/login")
def login_user(user: UserLogin):
    try:
        # Verificar usuario
        user_data = verify_user(user.username, user.password)
        if not user_data:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        # Crear token
        access_token = create_access_token(
            data={"sub": user.username, "rol": user_data["rol"], "user_id": user_data["user_id"]}
        )
        
        return {
            "status": "success",
            "access_token": access_token,
            "token_type": "bearer",
            "username": user.username,
            "rol": user_data["rol"],
            "user_id": user_data["user_id"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en login: {str(e)}")

@app.post("/api/auth/verify")
def verify_token_endpoint(authorization: str = Header(None)):
    """Verificar token JWT"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token requerido")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"username": username, "valid": True}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/api/auth/verify")
def verify_token_get(authorization: str = Header(None)):
    """Verificar token JWT (GET method)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token requerido")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"username": username, "valid": True}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/api/dashboard/stats")
def get_dashboard_stats(authorization: str = Header(None)):
    """Obtener estadísticas del dashboard"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token requerido")
    
    try:
        # Simular estadísticas (en producción, consultarías Snowflake)
        stats = {
            "patient_count": 1250,
            "consultations_today": 45,
            "blockchain_records": 892,
            "active_users": 23
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

@app.get("/api/blockchain/status")
def get_blockchain_status():
    """Obtener estado de la conexión blockchain"""
    try:
        is_connected = w3.is_connected()
        
        if is_connected:
            chain_id = w3.eth.chain_id
            network_name = "sepolia" if chain_id == 11155111 else f"chain_{chain_id}"
            
            return {
                "status": "connected",
                "network_id": chain_id,
                "network_name": network_name,
                "latest_block": w3.eth.block_number,
                "contracts": contract_addresses,
                "rpc_url": SEPOLIA_URL,
                "message": f"✅ Conectado a {network_name}"
            }
        else:
            return {
                "status": "disconnected",
                "network_id": None,
                "network_name": "unknown",
                "latest_block": None,
                "contracts": {},
                "rpc_url": SEPOLIA_URL,
                "message": "❌ No conectado a blockchain"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"❌ Error: {str(e)}"
        }

@app.post("/api/pacientes/registrar")
def registrar_paciente(paciente: PacienteRegistro, payload: dict = Depends(verify_token)):
    """Registrar un nuevo paciente"""
    try:
        conn = get_snowflake_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Verificar si el paciente ya existe por DNI
        cursor.execute(
            "SELECT COUNT(*) FROM PACIENTES WHERE DNI = %s",
            (paciente.dni,)
        )
        result = cursor.fetchone()
        
        if result[0] > 0:
            raise HTTPException(status_code=400, detail="Ya existe un paciente con este DNI")
        
        # Generar ID único para el paciente
        import uuid
        paciente_id = f"P{str(uuid.uuid4())[:8].upper()}"
        
        # Insertar paciente
        cursor.execute("""
            INSERT INTO PACIENTES (
                ID_PACIENTE, NOMBRE, APELLIDO, FECHA_NACIMIENTO, GENERO, DNI, TELEFONO,
                EMAIL, DIRECCION, CIUDAD, CODIGO_POSTAL, GRUPO_SANGUINEO,
                ALERGIAS, MEDICAMENTOS, ANTECEDENTES,
                CONTACTO_EMERGENCIA_NOMBRE, CONTACTO_EMERGENCIA_RELACION, CONTACTO_EMERGENCIA_TELEFONO,
                CONSENTIMIENTO_DATOS, CONSENTIMIENTO_EMERGENCIA, CONSENTIMIENTO_INVESTIGACION,
                FECHA_REGISTRO, VERIFICACION_BLOCKCHAIN
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP(), FALSE
            )
        """, (
            paciente_id, paciente.nombre, paciente.apellidos, paciente.fecha_nacimiento,
            paciente.genero, paciente.dni, paciente.telefono, paciente.email,
            paciente.direccion, paciente.ciudad, paciente.codigo_postal,
            paciente.grupo_sanguineo, paciente.alergias, paciente.medicamentos,
            paciente.antecedentes, paciente.contacto_emergencia_nombre,
            paciente.contacto_emergencia_relacion, paciente.contacto_emergencia_telefono,
            paciente.consentimiento_datos, paciente.consentimiento_emergencia,
            paciente.consentimiento_investigacion
        ))
        
        # El ID del paciente ya fue generado arriba
        
        # Crear registro en blockchain (simulado)
        try:
            # Aquí iría la lógica real de blockchain
            blockchain_hash = f"0x{paciente_id:064x}"
            
            # Actualizar verificación blockchain
            cursor.execute(
                "UPDATE PACIENTES SET VERIFICACION_BLOCKCHAIN = TRUE WHERE ID_PACIENTE = %s",
                (paciente_id,)
            )
            
        except Exception as e:
            print(f"Error en blockchain: {str(e)}")
            # Continuar sin blockchain si hay error
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "message": "Paciente registrado exitosamente",
            "paciente_id": paciente_id,
            "blockchain_verified": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando paciente: {str(e)}")

@app.post("/api/pacientes/registrar-original")
def registrar_paciente_original(paciente: PacienteRegistroOriginal, payload: dict = Depends(verify_token)):
    """Registrar un nuevo paciente usando el formulario original"""
    try:
        conn = get_snowflake_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Verificar si el paciente ya existe por ID
        cursor.execute(
            "SELECT COUNT(*) FROM PACIENTES WHERE ID_PACIENTE = %s",
            (paciente.id_paciente,)
        )
        result = cursor.fetchone()
        
        if result[0] > 0:
            raise HTTPException(status_code=400, detail="Ya existe un paciente con este ID")
        
        # Insertar paciente con datos del formulario original
        cursor.execute("""
            INSERT INTO PACIENTES (
                ID_PACIENTE, NOMBRE, APELLIDO, FECHA_NACIMIENTO, GENERO, 
                DOMICILIO_COMPLETO, MUNICIPIO, CODIGO_POSTAL, ALERGIAS, 
                ANTECEDENTES_PERSONALES, CONSENTIMIENTO_DATOS, 
                FECHA_CONSULTA, HORA_CONSULTA, SINTOMAS, CLASIFICACION_RIESGO,
                FECHA_REGISTRO, VERIFICACION_BLOCKCHAIN
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                CURRENT_TIMESTAMP(), FALSE
            )
        """, (
            paciente.id_paciente, 
            paciente.nombre_completo.split()[0] if paciente.nombre_completo else None,  # Primer nombre
            " ".join(paciente.nombre_completo.split()[1:]) if paciente.nombre_completo and len(paciente.nombre_completo.split()) > 1 else None,  # Apellidos
            paciente.fecha_nacimiento,
            paciente.genero,
            paciente.domicilio_completo,
            paciente.municipio,
            paciente.codigo_postal,
            paciente.alergias,
            paciente.antecedentes_personales,
            paciente.consentimiento_informado,
            paciente.fecha_consulta,
            paciente.hora_consulta,
            paciente.sintomas,
            paciente.clasificacion_riesgo
        ))
        
        # Crear registro en blockchain (simulado)
        try:
            blockchain_hash = f"0x{hash(paciente.id_paciente):064x}"
            
            # Actualizar verificación blockchain
            cursor.execute(
                "UPDATE PACIENTES SET VERIFICACION_BLOCKCHAIN = TRUE WHERE ID_PACIENTE = %s",
                (paciente.id_paciente,)
            )
            
        except Exception as e:
            print(f"Error en blockchain: {str(e)}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "Paciente registrado exitosamente",
            "paciente_id": paciente.id_paciente,
            "blockchain_verified": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando paciente: {str(e)}")

@app.get("/api/pacientes")
def obtener_pacientes(payload: dict = Depends(verify_token)):
    """Obtener lista de pacientes"""
    try:
        conn = get_snowflake_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Obtener pacientes con paginación
        cursor.execute("""
            SELECT ID_PACIENTE, NOMBRE, APELLIDO, DNI, TELEFONO, 
                   FECHA_NACIMIENTO, GENERO, VERIFICACION_BLOCKCHAIN
            FROM PACIENTES 
            ORDER BY FECHA_REGISTRO DESC 
            LIMIT 50
        """)
        
        pacientes = []
        for row in cursor.fetchall():
            pacientes.append({
                "id": row[0],
                "nombre": row[1],
                "apellidos": row[2],
                "dni": row[3],
                "telefono": row[4],
                "fecha_nacimiento": str(row[5]),
                "genero": row[6],
                "blockchain_verified": row[7]
            })
        
        cursor.close()
        conn.close()
        
        return {
            "pacientes": pacientes,
            "total": len(pacientes)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo pacientes: {str(e)}")

@app.get("/api/pacientes/{paciente_id}")
def obtener_paciente(paciente_id: int, payload: dict = Depends(verify_token)):
    """Obtener información detallada de un paciente"""
    try:
        conn = get_snowflake_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM PACIENTES WHERE ID_PACIENTE = %s
        """, (paciente_id,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        # Obtener nombres de columnas
        columns = [desc[0] for desc in cursor.description]
        
        # Crear diccionario con datos del paciente
        paciente_data = dict(zip(columns, row))
        
        cursor.close()
        conn.close()
        
        return paciente_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo paciente: {str(e)}")

@app.post("/api/blockchain/medical-record")
def create_medical_record(record: MedicalRecordCreate, payload: dict = Depends(verify_token)):
    """Crear registro médico en blockchain"""
    try:
        # Simular creación en blockchain
        record_hash = f"0x{hash(record.patient_id + record.diagnosis):064x}"
        
        return {
            "message": "Registro médico creado en blockchain",
            "record_hash": record_hash,
            "patient_id": record.patient_id,
            "diagnosis": record.diagnosis,
            "treatment": record.treatment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en blockchain: {str(e)}")

@app.post("/api/blockchain/consent")
def update_patient_consent(consent: PatientConsentUpdate, payload: dict = Depends(verify_token)):
    """Actualizar consentimiento del paciente en blockchain"""
    try:
        # Simular actualización en blockchain
        consent_hash = f"0x{hash(str(consent.data_sharing) + str(consent.research_participation)):064x}"
        
        return {
            "message": "Consentimiento actualizado en blockchain",
            "consent_hash": consent_hash,
            "data_sharing": consent.data_sharing,
            "research_participation": consent.research_participation,
            "emergency_access": consent.emergency_access
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en blockchain: {str(e)}")

@app.post("/api/blockchain/audit-log")
def create_audit_log(audit: AuditLogCreate, payload: dict = Depends(verify_token)):
    """Crear log de auditoría en blockchain"""
    try:
        # Simular creación en blockchain
        log_hash = f"0x{hash(audit.action + audit.details):064x}"
        
        return {
            "message": "Log de auditoría creado en blockchain",
            "log_hash": log_hash,
            "action": audit.action,
            "details": audit.details,
            "user": payload.get("sub")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en blockchain: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 