import sqlite3
from datetime import datetime
from config import DATABASE

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_schema():
    conn = get_db_connection()
    cur = conn.cursor()

    # Crear tabla usuarios si no existe
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        nombre TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        fecha_hora_ultimo_inicio TEXT,
        rol TEXT NOT NULL CHECK (rol IN ('ADMIN','PRODUCTOS','ALMACENES'))
    )
    """)

    # Revisar columnas de productos
    cur.execute("PRAGMA table_info(productos)")
    cols_p = [r[1] for r in cur.fetchall()]
    if 'fecha_hora_creacion' not in cols_p:
        cur.execute("ALTER TABLE productos ADD COLUMN fecha_hora_creacion TEXT")
    if 'fecha_hora_ultima_modificacion' not in cols_p:
        cur.execute("ALTER TABLE productos ADD COLUMN fecha_hora_ultima_modificacion TEXT")
    if 'ultimo_usuario_en_modificar' not in cols_p:
        cur.execute("ALTER TABLE productos ADD COLUMN ultimo_usuario_en_modificar TEXT")

    # Revisar columnas de almacenes
    cur.execute("PRAGMA table_info(almacenes)")
    cols_a = [r[1] for r in cur.fetchall()]
    if 'fecha_hora_creacion' not in cols_a:
        cur.execute("ALTER TABLE almacenes ADD COLUMN fecha_hora_creacion TEXT")
    if 'fecha_hora_ultima_modificacion' not in cols_a:
        cur.execute("ALTER TABLE almacenes ADD COLUMN fecha_hora_ultima_modificacion TEXT")
    if 'ultimo_usuario_en_modificar' not in cols_a:
        cur.execute("ALTER TABLE almacenes ADD COLUMN ultimo_usuario_en_modificar TEXT")

    conn.commit()
    conn.close()

def seed_usuarios(admin_pw_md5: str, prod_pw_md5: str, almac_pw_md5: str):
    conn = get_db_connection()
    cur = conn.cursor()
    usuarios = [
        ('ADMIN', admin_pw_md5, None, 'ADMIN'),
        ('PRODUCTOS', prod_pw_md5, None, 'PRODUCTOS'),
        ('ALMACENES', almac_pw_md5, None, 'ALMACENES')
    ]
    for u in usuarios:
        cur.execute("""
            INSERT OR IGNORE INTO usuarios (nombre, password, fecha_hora_ultimo_inicio, rol)
            VALUES (?,?,?,?)
        """, u)
    conn.commit()
    conn.close()
