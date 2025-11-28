import hashlib

def md5(s: str) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def require_login(session):
    return ('usuario' in session) and ('rol' in session)

def can_edit_productos(rol: str) -> bool:
    return rol in ('ADMIN', 'PRODUCTOS')

def can_edit_almacenes(rol: str) -> bool:
    return rol in ('ADMIN', 'ALMACENES')
