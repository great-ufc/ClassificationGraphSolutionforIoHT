from . import DatabaseConnection


class DBConnection:
    def __init__(self):
        self.connection = None
        self.db_name = ""
        self.connection_db = None
        
    def connnectToDB(self):
        DatabaseConnection.connection = DatabaseConnection.initServerConnection()
        DatabaseConnection.db_name = 'KnowlegeGraphDB'
        DatabaseConnection.create_database(DatabaseConnection.connection, DatabaseConnection.db_name)
        DatabaseConnection.connection_db = DatabaseConnection.initDBConnection()
        #attributes
        self.connection = DatabaseConnection.connection
        self.db_name = DatabaseConnection.db_name
        self.connection_db = DatabaseConnection.connection_db    
    
    def dropDB(self):
        DatabaseConnection.drop_database(self.connection, self.db_name)