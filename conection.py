import pymysql

class ConectionDB:
    def __init__(self):
        self.host = "localhost"  
        self.user = "root"       
        self.password = ""      
        self.database = "motormedico"  
        self.port = 3306         

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

