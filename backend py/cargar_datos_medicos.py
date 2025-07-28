import os
import uuid
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
import snowflake.connector

# Cargar variables de entorno
load_dotenv()

# Parámetros de conexión a Snowflake desde variables de entorno
conn_params = {
    'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
    'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'MEGAMARKET'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
}

def generar_id():
    """Generar ID único"""
    return str(uuid.uuid4()).replace('-', '')[:12]

def cargar_usuarios_ejemplo():
    """Cargar usuarios de ejemplo"""
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    usuarios = [
        ('USER_001', 'admin', 'admin@clinica.com', 'admin123', 'ADMIN'),
        ('USER_002', 'doctor1', 'doctor1@clinica.com', 'doctor123', 'DOCTOR'),
        ('USER_003', 'doctor2', 'doctor2@clinica.com', 'doctor123', 'DOCTOR'),
        ('USER_004', 'enfermera1', 'enfermera1@clinica.com', 'enfermera123', 'ENFERMERA'),
        ('USER_005', 'recepcionista', 'recepcion@clinica.com', 'recepcion123', 'RECEPCION')
    ]
    
    print("👥 Cargando usuarios de ejemplo...")
    
    for user_id, username, email, password, rol in usuarios:
        try:
            # Hash de la contraseña (en producción usarías passlib)
            password_hash = f"hash_{password}"
            
            cur.execute("""
                INSERT INTO USUARIOS (ID_USUARIO, NOMBRE_USUARIO, EMAIL, PASSWORD_HASH, ROL)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, username, email, password_hash, rol))
            
            print(f"✅ Usuario {username} creado")
            
        except Exception as e:
            print(f"❌ Error al crear usuario {username}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()

def cargar_pacientes_ejemplo():
    """Cargar pacientes de ejemplo"""
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    pacientes = [
        ('PAC_001', 'Juan', 'Pérez', '1985-03-15', 'M', '555-0101', 'juan.perez@email.com', 'Calle 123, Ciudad'),
        ('PAC_002', 'María', 'García', '1990-07-22', 'F', '555-0102', 'maria.garcia@email.com', 'Avenida 456, Ciudad'),
        ('PAC_003', 'Carlos', 'López', '1978-11-08', 'M', '555-0103', 'carlos.lopez@email.com', 'Calle 789, Ciudad'),
        ('PAC_004', 'Ana', 'Martínez', '1992-04-30', 'F', '555-0104', 'ana.martinez@email.com', 'Avenida 321, Ciudad'),
        ('PAC_005', 'Luis', 'Rodríguez', '1988-09-12', 'M', '555-0105', 'luis.rodriguez@email.com', 'Calle 654, Ciudad'),
        ('PAC_006', 'Sofia', 'Hernández', '1995-01-25', 'F', '555-0106', 'sofia.hernandez@email.com', 'Avenida 987, Ciudad'),
        ('PAC_007', 'Miguel', 'González', '1982-06-18', 'M', '555-0107', 'miguel.gonzalez@email.com', 'Calle 147, Ciudad'),
        ('PAC_008', 'Elena', 'Fernández', '1987-12-03', 'F', '555-0108', 'elena.fernandez@email.com', 'Avenida 258, Ciudad'),
        ('PAC_009', 'Roberto', 'Torres', '1993-08-14', 'M', '555-0109', 'roberto.torres@email.com', 'Calle 369, Ciudad'),
        ('PAC_010', 'Carmen', 'Jiménez', '1989-05-20', 'F', '555-0110', 'carmen.jimenez@email.com', 'Avenida 741, Ciudad')
    ]
    
    print("👤 Cargando pacientes de ejemplo...")
    
    for paciente_id, nombre, apellido, fecha_nac, genero, telefono, email, direccion in pacientes:
        try:
            cur.execute("""
                INSERT INTO PACIENTES (ID_PACIENTE, NOMBRE, APELLIDO, FECHA_NACIMIENTO, 
                                     GENERO, TELEFONO, EMAIL, DIRECCION)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (paciente_id, nombre, apellido, fecha_nac, genero, telefono, email, direccion))
            
            print(f"✅ Paciente {nombre} {apellido} creado")
            
        except Exception as e:
            print(f"❌ Error al crear paciente {nombre}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()

def cargar_enfermedades_ejemplo():
    """Cargar enfermedades de ejemplo"""
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    enfermedades = [
        ('ENF_001', 'Hipertensión', 'Presión arterial alta', 'Cardiovascular', 'Dolor de cabeza, mareos', 'Medicamentos antihipertensivos'),
        ('ENF_002', 'Diabetes Tipo 2', 'Alteración en el metabolismo de la glucosa', 'Endocrinología', 'Sed excesiva, fatiga', 'Control de dieta y medicamentos'),
        ('ENF_003', 'Asma', 'Inflamación de las vías respiratorias', 'Respiratorio', 'Dificultad para respirar, tos', 'Inhaladores broncodilatadores'),
        ('ENF_004', 'Artritis', 'Inflamación de las articulaciones', 'Reumatología', 'Dolor articular, rigidez', 'Antiinflamatorios y fisioterapia'),
        ('ENF_005', 'Depresión', 'Trastorno del estado de ánimo', 'Psiquiatría', 'Tristeza, pérdida de interés', 'Terapia y antidepresivos')
    ]
    
    print("🏥 Cargando enfermedades de ejemplo...")
    
    for enf_id, nombre, descripcion, categoria, sintomas, tratamiento in enfermedades:
        try:
            cur.execute("""
                INSERT INTO ENFERMEDADES (ID_ENFERMEDAD, NOMBRE_ENFERMEDAD, DESCRIPCION, 
                                        CATEGORIA, SINTOMAS, TRATAMIENTO_RECOMENDADO)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (enf_id, nombre, descripcion, categoria, sintomas, tratamiento))
            
            print(f"✅ Enfermedad {nombre} creada")
            
        except Exception as e:
            print(f"❌ Error al crear enfermedad {nombre}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()

def cargar_consultas_ejemplo():
    """Cargar consultas de ejemplo"""
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    # Generar fechas de consulta
    fecha_base = datetime.now()
    consultas = []
    
    for i in range(1, 11):
        consulta_id = f"CON_{i:03d}"
        paciente_id = f"PAC_{i:03d}"
        usuario_id = "USER_002" if i % 2 == 0 else "USER_003"
        fecha_consulta = fecha_base + timedelta(days=i)
        
        motivos = [
            "Control rutinario",
            "Dolor de cabeza",
            "Fiebre y malestar",
            "Revisión de medicamentos",
            "Síntomas respiratorios"
        ]
        
        motivo = random.choice(motivos)
        
        consultas.append((
            consulta_id, paciente_id, usuario_id, fecha_consulta,
            motivo, "Síntomas reportados por el paciente", "COMPLETADA"
        ))
    
    print("📋 Cargando consultas de ejemplo...")
    
    for consulta_id, paciente_id, usuario_id, fecha_consulta, motivo, sintomas, estado in consultas:
        try:
            cur.execute("""
                INSERT INTO CONSULTAS (ID_CONSULTA, ID_PACIENTE, ID_USUARIO, FECHA_CONSULTA,
                                     MOTIVO_CONSULTA, SINTOMAS, ESTADO_CONSULTA)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (consulta_id, paciente_id, usuario_id, fecha_consulta, motivo, sintomas, estado))
            
            print(f"✅ Consulta {consulta_id} creada")
            
        except Exception as e:
            print(f"❌ Error al crear consulta {consulta_id}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()

def cargar_datos_completos():
    """Cargar todos los datos de ejemplo"""
    print("🚀 Iniciando carga de datos médicos de ejemplo...")
    print("=" * 60)
    
    cargar_usuarios_ejemplo()
    print()
    
    cargar_pacientes_ejemplo()
    print()
    
    cargar_enfermedades_ejemplo()
    print()
    
    cargar_consultas_ejemplo()
    print()
    
    print("🎉 ¡Carga de datos médicos completada!")
    print("📊 Datos cargados:")
    print("  • 5 usuarios (admin, doctores, enfermeras)")
    print("  • 10 pacientes")
    print("  • 5 enfermedades comunes")
    print("  • 10 consultas de ejemplo")

if __name__ == "__main__":
    cargar_datos_completos() 