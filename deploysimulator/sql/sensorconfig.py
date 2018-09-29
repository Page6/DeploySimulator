from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def createConfiguration():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(':memory:')
    if not db.open():
        QMessageBox.critical(None, "Cannot open database",
                "Unable to establish a database connection.\n"
                "This example needs SQLite support. Please read the Qt SQL "
                "driver documentation for information how to build it.\n\n"
                "Click Cancel to exit.",
                QMessageBox.Cancel)
        return False
        
    query = QSqlQuery()
    query.exec_("create table Sensorconfig(id int primary key, "
                "name varchar(20), num integer, range integer, "
                "angle integer, color varchar(20))")
    query.exec_("insert into Sensorconfig values(001, 'sensor1', 30, 1, 60, 'blue')")
    query.exec_("insert into Sensorconfig values(002, 'sensor2', 30, 1, 30, 'green')")
    
    return True
