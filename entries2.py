import pymysql

databaseServerIP            = "127.0.0.1"  # IP address of the MySQL database server
databaseUserName            = "root"       # User name of the database server
databaseUserPassword        = "root"           # Password for the database user
charSet                     = "utf8mb4"     # Character set
cusrorType                  = pymysql.cursors.DictCursor
connectionInstance   = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,charset=charSet,cursorclass=cusrorType)


try:
    cur = connectionInstance.cursor()                       
    cur .execute("USE INS")
    cur.execute("SELECT CaseType FROM caseprocess")
    rows = cur.fetchall()

    for row in rows:
        print(row)


except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionInstance.close()

