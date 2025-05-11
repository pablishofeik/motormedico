import pymysql

class ConectionDB:
    def __init__(self):
        self.host = "localhost"  # Cambia si usas otro host
        self.user = "root"       # Cambia al usuario de tu base de datos
        self.password = ""       # Cambia a tu contraseña
        self.database = ""  # Cambia al nombre de tu base de datos
        self.port = 3306         # Cambia si tu base de datos usa otro puerto

    def connect(self):
        try:
            conection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            print("Conexión exitosa a la base de datos")
            return conection
        except pymysql.MySQLError as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

