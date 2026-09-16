"""
Configuración inicial del paquete config de ACADEMIX.
Garantiza la compatibilidad con MySQL usando PyMySQL como driver nativo en entornos Windows/Linux.
"""
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
