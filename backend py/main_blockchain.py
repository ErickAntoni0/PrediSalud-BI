#!/usr/bin/env python3
"""
API FastAPI con integración blockchain para Sistema Médico BI
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import snowflake.connector
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel
from web3_medical_integration import MedicalBlockchain

# Cargar variables de entorno
load_dotenv()

# Configuración de seguridad
SECRET_KEY = os.getenv('SECRET_KEY', 'tu_clave_secreta_aqui')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de seguridad HTTP
security = HTTPBearer()

app = FastAPI(
    title="Sistema Médico BI API con Blockchain",
    description="API para Sistema de Business Intelligence Médico con autenticación y blockchain",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Parámetros de conexión a Snowflake desde variables de entorno
conn_params = {
    'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
    'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'MEGAMARKET'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
}

# Inicializar blockchain
blockchain = MedicalBlockchain()

# Modelos Pydantic
class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    rol: str = "USUARIO"

class PacienteCreate(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: str
    genero: str
    telefono: str
    email: str = None
    direccion: str = None

class ConsultaCreate(BaseModel):
    id_paciente: str
    fecha_consulta: str
    motivo_consulta: str
    sintomas: str = None

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
    record_hash: str = None

def get_snowflake_connection():
    """Obtener conexión a Snowflake"""
    return snowflake.connector.connect(**conn_params)

def verify_password(plain_password, hashed_password):
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Generar hash de contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Crear token de acceso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificar token de autenticación"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/")
def root():
    return {
        "message": "Bienvenido al Sistema Médico BI API con Blockchain!", 
        "version": "1.0.0",
        "blockchain_status": blockchain.get_connection_status()
    }

@app.get("/api/health")
def health_check():
    """Verificar estado de la API, Snowflake y Blockchain"""
    try:
        # Verificar Snowflake
        conn = get_snowflake_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        snowflake_status = "connected"
    except Exception as e:
        snowflake_status = f"error: {str(e)}"
    
    # Verificar Blockchain
    blockchain_status = blockchain.get_connection_status()
    
    return {
        "status": "healthy", 
        "database": snowflake_status,
        "blockchain": blockchain_status
    }

@app.post("/api/auth/register")
def register_user(user: UserRegister):
    """Registrar nuevo usuario"""
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        
        # Verificar si el usuario ya existe
        cur.execute("SELECT COUNT(*) FROM USUARIOS WHERE NOMBRE_USUARIO = %s OR EMAIL = %s", 
                   (user.username, user.email))
        if cur.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail="Usuario o email ya existe")
        
        # Crear nuevo usuario
        user_id = f"USER_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        password_hash = get_password_hash(user.password)
        
        cur.execute("""
            INSERT INTO USUARIOS (ID_USUARIO, NOMBRE_USUARIO, EMAIL, PASSWORD_HASH, ROL)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, user.username, user.email, password_hash, user.rol))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "success", "message": "Usuario registrado exitosamente", "user_id": user_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {str(e)}")

@app.post("/api/auth/login")
def login_user(user: UserLogin):
    """Iniciar sesión de usuario"""
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        
        # Buscar usuario
        cur.execute("""
            SELECT ID_USUARIO, NOMBRE_USUARIO, PASSWORD_HASH, ROL 
            FROM USUARIOS 
            WHERE NOMBRE_USUARIO = %s AND ACTIVO = TRUE
        """, (user.username,))
        
        result = cur.fetchone()
        if not result:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        user_id, username, password_hash, rol = result
        
        # Verificar contraseña
        if not verify_password(user.password, password_hash):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
        # Crear token de acceso
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username, "user_id": user_id, "rol": rol}, 
            expires_delta=access_token_expires
        )
        
        cur.close()
        conn.close()
        
        return {
            "status": "success",
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user_id,
            "username": username,
            "rol": rol
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en login: {str(e)}")

@app.get("/api/pacientes")
def get_pacientes(current_user: str = Depends(verify_token)):
    """Obtener lista de pacientes"""
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT ID_PACIENTE, NOMBRE, APELLIDO, FECHA_NACIMIENTO, GENERO, 
                   TELEFONO, EMAIL, FECHA_REGISTRO
            FROM PACIENTES 
            WHERE ACTIVO = TRUE
            ORDER BY FECHA_REGISTRO DESC
        """)
        
        pacientes = []
        for row in cur.fetchall():
            pacientes.append({
                "id_paciente": row[0],
                "nombre": row[1],
                "apellido": row[2],
                "fecha_nacimiento": str(row[3]) if row[3] else None,
                "genero": row[4],
                "telefono": row[5],
                "email": row[6],
                "fecha_registro": str(row[7]) if row[7] else None
            })
        
        cur.close()
        conn.close()
        
        return {"status": "success", "data": pacientes, "total": len(pacientes)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pacientes: {str(e)}")

@app.post("/api/pacientes")
def create_paciente(paciente: PacienteCreate, current_user: str = Depends(verify_token)):
    """Crear nuevo paciente"""
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        
        paciente_id = f"PAC_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        cur.execute("""
            INSERT INTO PACIENTES (ID_PACIENTE, NOMBRE, APELLIDO, FECHA_NACIMIENTO, 
                                 GENERO, TELEFONO, EMAIL, DIRECCION)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (paciente_id, paciente.nombre, paciente.apellido, paciente.fecha_nacimiento,
              paciente.genero, paciente.telefono, paciente.email, paciente.direccion))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "success", "message": "Paciente creado exitosamente", "id_paciente": paciente_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear paciente: {str(e)}")

@app.get("/api/consultas")
def get_consultas(current_user: str = Depends(verify_token)):
    """Obtener lista de consultas"""
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT c.ID_CONSULTA, c.ID_PACIENTE, p.NOMBRE, p.APELLIDO,
                   c.FECHA_CONSULTA, c.MOTIVO_CONSULTA, c.ESTADO_CONSULTA,
                   c.FECHA_CREACION
            FROM CONSULTAS c
            JOIN PACIENTES p ON c.ID_PACIENTE = p.ID_PACIENTE
            ORDER BY c.FECHA_CONSULTA DESC
        """)
        
        consultas = []
        for row in cur.fetchall():
            consultas.append({
                "id_consulta": row[0],
                "id_paciente": row[1],
                "nombre_paciente": f"{row[2]} {row[3]}",
                "fecha_consulta": str(row[4]) if row[4] else None,
                "motivo_consulta": row[5],
                "estado_consulta": row[6],
                "fecha_creacion": str(row[7]) if row[7] else None
            })
        
        cur.close()
        conn.close()
        
        return {"status": "success", "data": consultas, "total": len(consultas)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener consultas: {str(e)}")

@app.post("/api/consultas")
def create_consulta(consulta: ConsultaCreate, current_user: str = Depends(verify_token)):
    """Crear nueva consulta"""
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        
        consulta_id = f"CON_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        cur.execute("""
            INSERT INTO CONSULTAS (ID_CONSULTA, ID_PACIENTE, ID_USUARIO, FECHA_CONSULTA,
                                 MOTIVO_CONSULTA, SINTOMAS)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (consulta_id, consulta.id_paciente, current_user, consulta.fecha_consulta,
              consulta.motivo_consulta, consulta.sintomas))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "success", "message": "Consulta creada exitosamente", "id_consulta": consulta_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear consulta: {str(e)}")

# ===== ENDPOINTS BLOCKCHAIN =====

@app.get("/api/blockchain/status")
def get_blockchain_status():
    """Obtener estado de la conexión blockchain"""
    return blockchain.get_connection_status()

@app.post("/api/blockchain/medical-record")
def create_blockchain_medical_record(record: MedicalRecordCreate, current_user: str = Depends(verify_token)):
    """Crear registro médico en blockchain"""
    try:
        result = blockchain.create_medical_record(
            record.patient_id,
            record.diagnosis,
            record.treatment
        )
        
        if result['success']:
            return {
                "status": "success",
                "message": "Registro médico creado en blockchain",
                "data": result
            }
        else:
            raise HTTPException(status_code=500, detail=f"Error en blockchain: {result['error']}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear registro médico: {str(e)}")

@app.get("/api/blockchain/medical-record/{record_hash}")
def get_blockchain_medical_record(record_hash: str, current_user: str = Depends(verify_token)):
    """Obtener registro médico desde blockchain"""
    try:
        result = blockchain.get_medical_record(record_hash)
        
        if result['success']:
            return {
                "status": "success",
                "data": result
            }
        else:
            raise HTTPException(status_code=404, detail=f"Registro no encontrado: {result['error']}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener registro médico: {str(e)}")

@app.post("/api/blockchain/consent")
def update_patient_consent(consent: PatientConsentUpdate, current_user: str = Depends(verify_token)):
    """Actualizar consentimiento del paciente en blockchain"""
    try:
        result = blockchain.update_patient_consent(
            consent.data_sharing,
            consent.research_participation,
            consent.emergency_access
        )
        
        if result['success']:
            return {
                "status": "success",
                "message": "Consentimiento actualizado en blockchain",
                "data": result
            }
        else:
            raise HTTPException(status_code=500, detail=f"Error en blockchain: {result['error']}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar consentimiento: {str(e)}")

@app.get("/api/blockchain/consent/{patient_address}")
def get_patient_consent(patient_address: str, current_user: str = Depends(verify_token)):
    """Obtener consentimiento del paciente desde blockchain"""
    try:
        result = blockchain.get_patient_consent(patient_address)
        
        if result['success']:
            return {
                "status": "success",
                "data": result
            }
        else:
            raise HTTPException(status_code=404, detail=f"Consentimiento no encontrado: {result['error']}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener consentimiento: {str(e)}")

@app.post("/api/blockchain/audit-log")
def create_audit_log(audit: AuditLogCreate, current_user: str = Depends(verify_token)):
    """Crear log de auditoría en blockchain"""
    try:
        result = blockchain.create_audit_log(
            audit.action,
            audit.details,
            audit.record_hash
        )
        
        if result['success']:
            return {
                "status": "success",
                "message": "Log de auditoría creado en blockchain",
                "data": result
            }
        else:
            raise HTTPException(status_code=500, detail=f"Error en blockchain: {result['error']}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear log de auditoría: {str(e)}")

@app.get("/api/dashboard/medical")
def get_medical_dashboard(current_user: str = Depends(verify_token)):
    """Obtener dashboard médico con información de blockchain"""
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        
        # Estadísticas generales
        cur.execute("SELECT COUNT(*) FROM PACIENTES WHERE ACTIVO = TRUE")
        total_pacientes = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM CONSULTAS")
        total_consultas = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM USUARIOS WHERE ACTIVO = TRUE")
        total_usuarios = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM CONSULTAS WHERE ESTADO_CONSULTA = 'PROGRAMADA'")
        consultas_programadas = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        # Estado de blockchain
        blockchain_status = blockchain.get_connection_status()
        
        return {
            "status": "success",
            "dashboard": {
                "total_pacientes": total_pacientes,
                "total_consultas": total_consultas,
                "total_usuarios": total_usuarios,
                "consultas_programadas": consultas_programadas,
                "blockchain_status": blockchain_status
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener dashboard: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 