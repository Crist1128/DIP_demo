import pymysql

class DatabaseConnector:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True  # 启用自动提交
            )
            self.cursor = self.conn.cursor()
            print("Connected to the database")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Disconnected from the database")

    
    #上下文管理器
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

class DatabaseQueries:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_diagnosis_by_code(self, diagnosis_code):
        query = "SELECT DiagnosisID, DiagnosisName FROM diagnosis WHERE DiagnosisCode = %s"
        self.cursor.execute(query, (diagnosis_code,))
        return self.cursor.fetchone()

    def get_scoring_records_by_diagnosis_id(self, diagnosis_id):
        query = "SELECT ScoringID, ProcedureCodes, ScoringValue FROM scoring WHERE DiagnosisID = %s"
        self.cursor.execute(query, (diagnosis_id,))
        return self.cursor.fetchall()
