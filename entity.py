from peewee import *

db = PostgresqlDatabase('taxone_python', user='conam', password='conam123',
                           host='localhost', port=5432)
class BaseModel(Model):
    class Meta:
        database = db

class Email(BaseModel):
    email = TextField()
    type  = TextField()
    
    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"email" : "' + self.email + '",' + '"type" : "' + self.type + '" }'

class User(BaseModel):
	name = TextField()
	password = TextField()
	creationDate = DateTimeField()
	lastAccess = DateTimeField()

class Upload(BaseModel):
    fileName = TextField()
    layoutVersion = TextField()
    creationDate = DateTimeField()
    status = TextField()
    user = ForeignKeyField(User, backref='uploads')

    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"fileName" : "' + self.fileName + '",' + '"layoutVersion" : "' + self.layoutVersion + '",' + '"creationDate" : "2004-08-21T01:30:00.000-05:00",' + '"status" : "' + self.status + '", "userName": "' + self.user.name + '"  }'


class DataSourceConfiguration(BaseModel):
    url = TextField()
    username = TextField()
    password = TextField()
    resourceNames = TextField()
    dataSourceType = TextField()

    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"url" : "' + self.url + '",' + '"username" : "' + self.username + '",' + '"password" : "' + self.password + '",' + '"resourceNames" : "' + self.resourceNames + '",' + '"dataSourceType" : "' + self.dataSourceType + '"}'
    
class DSTable(BaseModel):
    name = TextField()
    dataSourceConfiguration = ForeignKeyField(DataSourceConfiguration, backref='dsTables')
    
    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"name" : "' + self.name + '"}'

class DSColumn(BaseModel):
    name = TextField()
    columnType = TextField()
    size = IntegerField()
    dsTable = ForeignKeyField(DSTable, backref='dsColumns')

    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"name" : "' + self.name + '",' + '"columnType" : "' + self.columnType + '",' + '"size" : ' + str(self.size) + ',' + '"dsTable" : {"name": "' + self.dsTable.name + '" } }'
    


class SAFXTable(BaseModel):
    name = TextField()
    description = TextField()
    dsTable = ForeignKeyField(DSTable, backref='SAFXTables', null=True)

    def toJson(self):
        dsTableId = ''
        dsTableName = ''
        if self.dsTable:
            dsTableId = self.dsTable.id
            dsTableName = self.dsTable.name
        return '{' + '"id" : ' + str(self.id) + ',' + '"name" : "' + self.name + '",' + '"description" : "' + self.description + '",' + '"dsTableId" : "' + str(dsTableId) + '",' + '"dsTableName" : "' + dsTableName + '"}'
    
class SAFXColumn(BaseModel):
    name = TextField()
    columnType = TextField()
    required = BooleanField()
    position = IntegerField()
    size = IntegerField()
    safxTable = ForeignKeyField(SAFXTable, backref='SAFXColumns')
    dsColumn = ForeignKeyField(DSColumn, backref='SAFXTables', null=True)

    def toJson(self):
        dsColumnId = ''
        dsColumnName = ''
        if self.dsColumn:
            dsColumnId = self.dsColumn.id
            dsColumnName = self.dsColumn.name
        return '{' + '"id" : ' + str(self.id) + ',' + '"name" : "' + self.name + '",' + '"columnType" : "' + self.columnType + '",' + '"required" : ' + str(self.required).lower() + ',' + '"position" : ' + str(self.position) + ',' + '"size" : ' + str(self.size) + ','  + '"dsColumnId" : "' + str(dsColumnId) + '",' + '"dsColumnName" : "' + dsColumnName + '"}'
    

db.create_tables([Email, User, Upload, DataSourceConfiguration, DSTable, DSColumn, SAFXTable, SAFXColumn])



