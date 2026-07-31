import sqlite3

#Creamos la db con connect('nombre_de_la_db').
connection = sqlite3.connect('publicaciones.db')

#Para manipularla, necesitamos de un cursor. Lo creamos con cursor()
cursor = connection.cursor()

#Creamos la tabla (si es que no existe) de las publicaciones con el excecute + cadena de sql.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS publicaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fuente TEXT NOT NULL,
        id_externo TEXT NOT NULL,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        version TEXT,
        anio INTEGER NOT NULL,
        km INTEGER NOT NULL,
        ciudad TEXT,
        provincia TEXT,
        url_original TEXT NOT NULL,
        activo INTEGER DEFAULT 1,
        fecha_primera_deteccion TEXT NOT NULL,
        fecha_ultima_actualizacion TEXT NOT NULL,
        UNIQUE(fuente, id_externo)
    )
''')

#Creamos la tabla (si es que no existe) del historial de precios también con el excecute + cadena de sql.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS precios_historicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        auto_id INTEGER NOT NULL,
        precio INTEGER NOT NULL,
        moneda TEXT NOT NULL,
        fecha_registro TEXT NOT NULL,
        FOREIGN KEY (auto_id) REFERENCES autos(id)
    )
""")

connection.commit()
connection.close()
print("Tablas creadas (o ya existían).")