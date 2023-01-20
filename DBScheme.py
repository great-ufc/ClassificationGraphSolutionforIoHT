from DatabaseQueryFunctions import create_table
from DatabaseQueryFunctions import drop_table
from DatabaseQueryFunctions import add_Column
from DatabaseQueryFunctions import update_Column
from DatabaseQueryFunctions import drop_Column
from datetime import datetime, timezone, timedelta

class DBScheme:
    def __init__(self, connection_db):
        self.connection_db = connection_db
    
    def createTableByEntity(self, entity):
        table_name = str(entity.__name__)
        colsName = [i for i in entity().__dict__.keys() if i[:1] != '_'][1:]
        colsBaseValue = [i for i in entity().__dict__.values()][1:]
        colsType = [type(i).__name__ for i in entity().__dict__.values()][1:]
        #drop_table(connection_db, table_name)
        print(colsName)
        colunms = []
        for i in range(len(colsName)):
            colsTypeList = self.getColType([colsType[i],colsBaseValue[i]])
            colunms.append([colsName[i],colsTypeList[0],colsTypeList[1]])
        create_table (self.connection_db, table_name, colunms)
        
    def updateTableByEntity(self, table_name, mode, col, type_col):
        if mode == "ADD":
            add_Column(self.connection_db, table_name, col, type_col)
        elif mode == "Update":
            update_Column(self.connection_db, table_name, col, type_col)
        elif mode == "drop":
            drop_Column(self.connection_db, table_name, col)
                    
    def getColType(self, Type):
        colType = []
        if Type[0] == 'str':
            colType.append('string 150')
        elif Type[0] == 'int':
            colType.append('int')
        elif Type[0] == 'datetime':
            colType.append('date')
        elif Type[0] == 'float':
            colType.append('float')
        elif Type[0] == 'bool':
            colType.append('bit')
        elif Type[0] == 'list':
            colType.append('longstring')
        colType.append(True if Type[1] != None or Type[1] != "" else False)
        return colType