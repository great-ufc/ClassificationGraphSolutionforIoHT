import mysql.connector
from mysql.connector import Error

#Execute Query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        print("Query successful")
        return result
    except Error as err:
        print(f"Error: '{err}'")



#create table 
def create_table(connection_db, table_name, cols):
    try:
        sql = "CREATE TABLE " + table_name + " ("
        sql += table_name+"_id INT AUTO_INCREMENT PRIMARY KEY,"
        for col in cols:            
                #col name
                sql+= col[0] + " "
                #col type
                typo = col[1].split(" ")
                if(len(typo)>1):
                    if(typo[0] == "string"):
                        typo[0] = "VARCHAR"
                    sql+= typo[0]+"("+typo[1]+")" + " "
                else:                
                    typo2 = col[1].split("_")
                    if (len(typo2) > 1):
                        if(typo2[0] == "int"):
                            typo2[0] = "INT"

                        if(typo2[1] == "unique"):
                            typo2[1] = "UNIQUE"
                        
                        sql+= typo2[0]+ " " + typo2[1] + " "
                    else:
                        if typo2[0] == "int" :
                            typo2[0] = "INT"
                        if typo2[0] == "date":
                            typo2[0] = "DATE"
                        if typo2[0] == "float":
                            typo2[0] = "FLOAT"
                        if typo2[0] == "logstring":
                            typo2[0] = "NVARCHAR(4000)"
                        if typo2[0] == "bit":
                            typo2[0] = "BIT"
                        sql+= typo2[0]+ " "
                
                #col null verification
                if col[2]:
                    sql+= "NOT NULL"
                
                sql+=","
        sql += " updateTime DATE);"
        #print(sql)
        execute_query(connection_db, sql)
    except Error as err:
        print(f"Error: '{err}'")

#drop table    
def drop_table(connection_db, table_name):
    try:
        sql = "Drop table " + table_name
        execute_query(connection_db, sql)
    except Error as err:
        print(f"Error: '{err}'")


#alter table add colunms 
def add_Column(connection_db, table_name, column, dataType):
    try: 
        sql = "Alter table " + table_name + " ADD " + column + " " + dataType
        execute_query(connection_db, sql)
    except Error as err:
        print(f"Error: '{err}'")

#ALTER TABLE table_name
def drop_Column(connection_db, table_name, column):
    try: 
        sql = "Alter table " + table_name + " Drop " + column
        execute_query(connection_db, sql)
    except Error as err:
        print(f"Error: '{err}'")

#alter table alter colunms
def update_Column(connection_db, table_name, column, dataType):
    try:
        drop_Column(connection_db, table_name, column)
        add_Column(connection_db, table_name, column, dataType)
    except Error as err:
        print(f"Error: '{err}'")

#insert record
def insertRecord(connection_db, table_name, values):
    try:
        colsSql = ""
        valuesSql = ""        
        for col, value in values.items():
            colsSql += col + ","
            if type(value) is str:
                valuesSql += "\""+value+ "\"" + ","
            else:
                valuesSql += str(value) + ","
        colsSql += "updateTime"
        valuesSql += "now()"
        
        sql = "INSERT INTO "+ table_name + " ("
        sql += colsSql
        sql += ") Values ("
        sql += valuesSql
        sql += ")"
        print(sql)
        
        execute_query(connection_db, sql)
    except Error as err:
        print(f"Error: '{err}'")   

#delete record
def deleteRecord(connection_db, table_name, id_value):
    try:
        sql = "DELETE FROM " + table_name + " WHERE "+table_name+ "_id="+ str(id_value)
        execute_query(connection_db, sql)
    except Error as err:
        print(f"Error: '{err}'")

#update record
def updateRecord(connection_db, table_name, value, conditions):
    try:
        if type(list(value.values())[0]) is str:
            if type(val) is str:
                sql = "UPDATE " + table_name + " SET "+ list(value.keys())[0] + " = \""+ list(value.values())[0] + "\" WHERE "
            else:
                sql = "UPDATE " + table_name + " SET "+ list(value.keys())[0] + " = "+ list(value.values())[0] + " WHERE "
            conditionsSQL = ""
            for key, val in conditions.items():
                if type(val) is str:
                    conditionsSQL += str(key) + " like \"%"+ val + "%\" AND "
                else:
                    conditionsSQL += str(key) + " = "+ str(val) + " AND "
            conditionsSQL = conditionsSQL[0:len(conditionsSQL)-4]
            sql+= conditionsSQL
        else:
            sql = "UPDATE " + table_name + " SET "+ list(value.keys())[0] + " = "+ list(value.values())[0] + " WHERE "
            conditionsSQL = ""
            for key, val in conditions.items():
                if type(val) is str:
                    conditionsSQL += str(key) + " like \"%"+ val + "%\" AND "
                else:
                    conditionsSQL += str(key) + " = "+ str(val) + " AND "
            conditionsSQL = conditionsSQL[0:len(conditionsSQL)-4]
            sql+= conditionsSQL  
        return execute_query(connection_db, sql)
    except Error as err:
        print(f"Error: '{err}'")


#find all records
def findAll(connection_db, table_name):
    try:
        sql = "SELECT * FROM " + table_name
        return execute_query(connection_db, sql)
    except Error as err:
        print(f"Error: '{err}'")

#find a specific record by id 
def findById(connection_db, table_name, id_value):
    try: 
        sql = "SELECT * FROM " + table_name + " WHERE "+table_name+"_id = "+str(id_value)
        return execute_query(connection_db, sql)[0]
    except Error as err:
        print(f"Error: '{err}'")

#find a specific record by specific cols
def findByValue(connection_db, table_name, conditions):
    try:
        sql = "SELECT * FROM " + table_name + " WHERE "
        conditionsSQL = ""
        for key, val in conditions.items():
            if type(val) is str:
                conditionsSQL += str(key) + " like \"%"+ val + "%\""
                conditionsSQL += ' '+'A'+'N'+'D'+ ' '
            else:
                conditionsSQL += str(key) + " = "+ str(val)
                conditionsSQL += " AND "
        conditionsSQL = conditionsSQL[0:len(conditionsSQL)-4]
        sql+= conditionsSQL
        return execute_query(connection_db, sql)
    except Error as err:
        print(f"Error: '{err}'")