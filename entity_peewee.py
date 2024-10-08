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

    
class Schedule(BaseModel):
    name = TextField()
    status = TextField()
    days = TextField()
    hours = TextField()
    lastExecution = DateTimeField()
    user = ForeignKeyField(User, backref='schedules')
    
    def toJson(self):
        safxTablesJson = '[]'
        criteriasJson = '[]'
        if len(self.safxTables) > 0:
            safxTablesJson = '['
            for safxTable in self.safxTables:
                safxTableJson = '{ "id":' + str(safxTable.id) + ', "name": "' + safxTable.name + '"},'
                safxTablesJson = safxTablesJson + safxTableJson
            safxTablesJson = safxTablesJson[0:len(safxTablesJson)-1] + ']'

        if len(self.criterias) > 0:
            criteriasJson = '['
            for criteria in self.criterias:      
                criteriasJson = criteriasJson + criteria.toJson() + ','
            criteriasJson = criteriasJson[0:len(criteriasJson)-1] + ']'
                  
        return '{' + '"id" : ' + str(self.id) + ',' + '"name" : "' + self.name + '",' + '"status" : "' + self.status + '",' + '"userName" : "' + self.user.name + '", "safxTables": ' + safxTablesJson + ', "criterias": ' + criteriasJson + ' }'
    
    
class ScheduleLog(BaseModel):
    numLote = TextField()
    executionDate = DateTimeField()
    errorMessage = TextField()
    status = TextField()
    integrationStatus = TextField()
    schedule = ForeignKeyField(Schedule, backref='scheduleLogs')
    #private List<ScheduleLogIntergrationError> taxOneErrors;
    
    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"executionDate" : "' + str(self.executionDate) + '",' + '"status" : "' + self.status + '",' + '"scheduleName" : "' + self.schedule.name + '" }'
    
    def toJsonFull(self):
        taxOneErrorsJson = '[]'
        if len(self.taxOneErrors) > 0:
            taxOneErrorsJson = '['
            for taxOneError in self.taxOneErrors:      
                taxOneErrorsJson = taxOneErrorsJson + taxOneError.toJson() + ','
            taxOneErrorsJson = taxOneErrorsJson[0:len(taxOneErrorsJson)-1] + ']'

        return '{' + '"id" : ' + str(self.id) + ',' + '"executionDate" : "' + str(self.executionDate) + '",' + '"status" : "' + self.status + '",' + '"scheduleName" : "' + self.schedule.name + '", "taxOneErrors" : ' + taxOneErrorsJson + '}'
    
    
class ScheduleLogIntergrationError(BaseModel):
    numeroReg = IntegerField()
    codigoErro = TextField()
    descricaoErro = TextField()
    nomeCampo = TextField()
    chaveRegistro = TextField()
    scheduleLog = ForeignKeyField(ScheduleLog, backref='taxOneErrors')
    
    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"numeroReg" : "' + str(self.numeroReg) + '",' + '"codigoErro" : "' + self.codigoErro + '",' + '"descricaoErro" : "' + self.descricaoErro + '",' + '"nomeCampo" : "' + self.nomeCampo + '",' + '"chaveRegistro" : "' + self.chaveRegistro + '" }'
    


NoteThroughDeferred = DeferredThroughModel()

class SAFXTable(BaseModel):
    name = TextField()
    description = TextField()
    dsTable = ForeignKeyField(DSTable, backref='safxTables', null=True)
    schedules = ManyToManyField(Schedule, backref='safxTables', through_model=NoteThroughDeferred)    

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
    dsColumn = ForeignKeyField(DSColumn, backref='SAFXColumns', null=True)

    def toJson(self):
        dsColumnId = ''
        dsColumnName = ''
        if self.dsColumn:
            dsColumnId = self.dsColumn.id
            dsColumnName = self.dsColumn.name
        return '{' + '"id" : ' + str(self.id) + ',' + '"name" : "' + self.name + '",' + '"columnType" : "' + self.columnType + '",' + '"required" : ' + str(self.required).lower() + ',' + '"position" : ' + str(self.position) + ',' + '"size" : ' + str(self.size) + ','  + '"dsColumnId" : "' + str(dsColumnId) + '",' + '"dsColumnName" : "' + dsColumnName + '"}'


class Criteria(BaseModel):
    operator = TextField()
    value = TextField()
    #private String additionalValue = TextField()
    safxColumn = ForeignKeyField(SAFXColumn)
    schedule = ForeignKeyField(Schedule, backref='criterias')

    def toJson(self):
        safxColumnJson = '{"id" :' + str(self.safxColumn.id) + ', "name": "' + self.safxColumn.name + '", '
        safxColumnJson = safxColumnJson + '"safxTable" : {"id": ' + str(self.safxColumn.safxTable.id) + '} }'
        return '{' + '"id" : ' + str(self.id) + ',' + '"operator" : "' + self.operator + '",' + '"value" : "' + self.value + '",' + '"safxColumn" : ' + safxColumnJson + ' }'


class SAFXTableSchedule(BaseModel):
    safxTable = ForeignKeyField(SAFXTable)
    schedule = ForeignKeyField(Schedule)

    class Meta:
        primary_key = False
        table_name = 'safxtable_schedule'

NoteThroughDeferred.set_model(SAFXTableSchedule)

db.create_tables([Email, User, Upload, DataSourceConfiguration, DSTable, DSColumn, SAFXTable, SAFXColumn, Schedule, ScheduleLog, ScheduleLogIntergrationError, Criteria, SAFXTable.schedules.get_through_model()])



