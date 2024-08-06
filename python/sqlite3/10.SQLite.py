import sqlite3
# from pathlib import Path

class DBConnector():
    
    # constructor
    # ruta a la db de sqlite
    def __init__(self, ruta_a_db: str) -> None:
        self.database = ruta_a_db
        print("Usando base de datos:", self.database)
    
    def conectar(self):
        conn = sqlite3.connect(self.database)
        return conn
    
    def desconectar(self, conn) -> None:
        conn.close()

    def ejecutar_query(self, query):
        """Como el cursor no se puede acceder cuando se cierra conexión habría que añadir aquí lógica para hacer fetchall o fetchone... para devolver lista iterable en Python"""
        conn = self.conectar()
        cur = conn.cursor()
        resultado = cur.execute(query)
        datos = resultado.fetchall()
        conn.commit()
        self.desconectar(conn)
        return datos
    
    # create table
    def crear_tabla(self, query) -> None:
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        self.desconectar(conn)

    # podemos pasarle una fuente de datos como un CSV:
    def seed(self, datos):
        insert_query = '''INSERT INTO tblUsuarios (usuario, nombre, sexo, nivel, email, telefono, marca, compañia, saldo, activo)
        VALUES (?,?,?,?,?,?,?,?,?,?);'''
        conn = self.conectar()
        cur = conn.cursor()
        for dato in datos:
            cur.execute(insert_query, dato)
        conn.commit()
        self.desconectar(conn)
    
    # leer datos
      # order by... 
    def select(self, id=None):
        datos = []
        if id:
            select_all_query='''SELECT * from tblUsuarios WHERE idx = ?;'''
            conn = self.conectar()
            cur = conn.cursor()
            datos = cur.execute(select_all_query, (id, )).fetchone()
            conn.commit()
            self.desconectar(conn)
        else:
            select_all_query='''SELECT * from tblUsuarios;'''
            #conn = self.conectar()
            #cur = conn.cursor()
            #datos = cur.execute(select_all_query).fetchall()
            datos = self.ejecutar_query(select_all_query)
            #conn.commit()
            #self.desconectar(conn)
        return datos if datos else []
    
    # actualizar
    def update(self, columna, valor, id):
        update_query=f'''UPDATE tblUsuarios SET {columna} = ? WHERE idx = ?'''
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute(update_query, (valor, id, ))
        conn.commit()
        self.desconectar(conn)
    
    # borrar por id
    def delete(self, id):
        delete_query='''DELETE FROM tblUsuarios WHERE idx = ?;'''
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute(delete_query, (id, ))
        conn.commit()
        self.desconectar(conn)
    

if __name__ == '__main__':
    db_conn = DBConnector("db.sqlite3")

    # Create table
    nombre_tabla = "tblUsuarios"
    create_table_query = f'''CREATE TABLE IF NOT EXISTS {nombre_tabla} (
          idx INTEGER PRIMARY KEY AUTOINCREMENT,
          usuario TEXT NOT NULL,
          nombre TEXT NOT NULL,
          sexo TEXT CHECK(sexo IN ('M', 'H')),
          nivel INTEGER CHECK(nivel BETWEEN 0 AND 255),
          email TEXT,
          telefono TEXT,
          marca TEXT,
          compañia TEXT,
          saldo REAL,
          activo INTEGER CHECK(activo IN (0, 1))
        )'''
    db_conn.crear_tabla(create_table_query)

    # Seed
    datos = [
        ('p3p3', 'Pepe', 'H', 3, 'pepe@rana.frog', '123', 'PEPU', 'Le Pepe', -1.0, 1),
        ('jua7', 'Juan', 'M', 2, 'juan@correo.com', '456', 'JUAN', 'La Juan', 0.0, 1)
    ]
    
    db_conn.seed(datos)

    datos = db_conn.select() # SELECT * from tblUsuarios
    print("")
    print("SELECT all:")
    print(datos)

    # datos = db_conn.select(1) # SELECT * from tblUsuarios WHERE idx = 1;
    # print("")
    # print("SELECT de id 1:")
    # print(datos)

    # datos = db_conn.select(99) # SELECT * from tblUsuarios WHERE idx = 1;
    # print("")
    # print("SELECT de id 99 sale vacío:")
    # print(datos)

    # datos = db_conn.update('saldo', 100, 1) 
    # print("")
    # print("UPDATE de saldo:")
    # datos = db_conn.select(1) # volvemos a hacer el SELECT para ver que funcionó
    # print(datos)

    # datos = db_conn.delete(2) 
    # print("")
    # print("DELETE de id 2:")
    # datos = db_conn.select() # hago SELECT de todo para ver que se ha borrado
    # print([dato[0] for dato in datos])