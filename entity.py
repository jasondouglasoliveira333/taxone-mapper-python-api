import datetime

from typing import List
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

engine = create_engine("postgresql+psycopg2://conam:conam123@localhost:5432/taxone_python") #, echo=True)

class BaseModel(DeclarativeBase):
    pass

class Email(BaseModel):
    __tablename__ = "email"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(30))
    
    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"email" : "' + self.email + '",' + '"type" : "' + self.type + '" }'


class User(BaseModel):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    creationDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    lastAccess: Mapped[datetime.datetime] = mapped_column(DateTime)
    
    uploads: Mapped[List["Upload"]] = relationship(
        back_populates="user"
    )


class Upload(BaseModel):
    __tablename__ = "upload"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    fileName: Mapped[str] = mapped_column(String(50))
    layoutVersion: Mapped[str] = mapped_column(String(50))
    creationDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    user: Mapped["User"] = relationship(back_populates="uploads")

    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"fileName" : "' + self.fileName + '",' + '"layoutVersion" : "' + self.layoutVersion + '",' + '"creationDate" : "2004-08-21T01:30:00.000-05:00",' + '"status" : "' + self.status + '", "userName": "' + self.user.name + '"  }'


class DataSourceConfiguration(BaseModel):
    __tablename__ = "datasourceconfiguration"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    resourceNames: Mapped[str] = mapped_column(String(50))
    dataSourceType: Mapped[str] = mapped_column(String(50))
    
    dsTables: Mapped[List["DSTable"]] = relationship(
        back_populates="dataSourceConfiguration"
    )
    
    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"url" : "' + self.url + '",' + '"username" : "' + self.username + '",' + '"password" : "' + self.password + '",' + '"resourceNames" : "' + self.resourceNames + '",' + '"dataSourceType" : "' + self.dataSourceType + '"}'
 
 
class DSTable(BaseModel):
    __tablename__ = "dstable"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    dataSourceConfiguration_id: Mapped[int] = mapped_column(ForeignKey("datasourceconfiguration.id")) #table name
    dataSourceConfiguration: Mapped["DataSourceConfiguration"] = relationship(back_populates="dsTables")
    
    dsColumns: Mapped[List["DSColumn"]] = relationship(
        back_populates="dsTable"
    )
    
    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"name" : "' + self.name + '"}'


class DSColumn(BaseModel):
    __tablename__ = "dscolumn"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    columnType: Mapped[str] = mapped_column(String(255))
    size: Mapped[int] = mapped_column(Integer)
    
    dsTable_id: Mapped[int] = mapped_column(ForeignKey("dstable.id")) #table name
    dsTable: Mapped["DSTable"] = relationship(back_populates="dsColumns")


    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"name" : "' + self.name + '",' + '"columnType" : "' + self.columnType + '",' + '"size" : ' + str(self.size) + ',' + '"dsTable" : {"name": "' + self.dsTable.name + '" } }'


class SAFXTable(BaseModel):
    __tablename__ = "safxtable"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))

    dsTable_id: Mapped[int] = mapped_column(ForeignKey("dstable.id")) #table name
    dsTable: Mapped["DSTable"] = relationship()
    
    safxColumns: Mapped[List["SAFXColumn"]] = relationship(
        back_populates="safxTable"
    )
    
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedule.id")) #table name
    schedule: Mapped["Schedule"] = relationship()
    
    #schedules = ManyToManyField(Schedule, backref='safxTables', through_model=NoteThroughDeferred)    

    def toJson(self):
        dsTableId = ''
        dsTableName = ''
        if self.dsTable:
            dsTableId = self.dsTable.id
            dsTableName = self.dsTable.name
        return '{' + '"id" : ' + str(self.id) + ',' + '"name" : "' + self.name + '",' + '"description" : "' + self.description + '",' + '"dsTableId" : "' + str(dsTableId) + '",' + '"dsTableName" : "' + dsTableName + '"}'

    
class SAFXColumn(BaseModel):
    __tablename__ = "safxcolumn"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    columnType: Mapped[str] = mapped_column(String(255))
    required: Mapped[bool] = mapped_column(Boolean)
    position: Mapped[int] = mapped_column(Integer)
    size: Mapped[int] = mapped_column(Integer)
    
    safxTable_id: Mapped[int] = mapped_column(ForeignKey("safxtable.id")) #table name
    safxTable: Mapped["SAFXTable"] = relationship(back_populates="safxColumns")
    dsColumn_id: Mapped[int] = mapped_column(ForeignKey("dscolumn.id"), nullable=True) #table name
    dsColumn: Mapped["DSColumn"] = relationship()

    def toJson(self):
        dsColumnId = ''
        dsColumnName = ''
        if self.dsColumn:
            dsColumnId = self.dsColumn.id
            dsColumnName = self.dsColumn.name
        return '{' + '"id" : ' + str(self.id) + ',' + '"name" : "' + self.name + '",' + '"columnType" : "' + self.columnType + '",' + '"required" : ' + str(self.required).lower() + ',' + '"position" : ' + str(self.position) + ',' + '"size" : ' + str(self.size) + ','  + '"dsColumnId" : "' + str(dsColumnId) + '",' + '"dsColumnName" : "' + dsColumnName + '"}'


class Criteria(BaseModel):
    __tablename__ = "criteria"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    operator: Mapped[str] = mapped_column(String(255))
    value: Mapped[str] = mapped_column(String(255))

    safxColumn_id: Mapped[int] = mapped_column(ForeignKey("safxcolumn.id")) #table name
    safxColumn: Mapped["SAFXColumn"] = relationship()
    
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedule.id")) #table name
    schedule: Mapped["Schedule"] = relationship() 
 
    def toJson(self):
        safxColumnJson = '{"id" :' + str(self.safxColumn.id) + ', "name": "' + self.safxColumn.name + '", '
        safxColumnJson = safxColumnJson + '"safxTable" : {"id": ' + str(self.safxColumn.safxTable.id) + '} }'
        return '{' + '"id" : ' + str(self.id) + ',' + '"operator" : "' + self.operator + '",' + '"value" : "' + self.value + '",' + '"safxColumn" : ' + safxColumnJson + ' }'

    
class Schedule(BaseModel):
    __tablename__ = "schedule"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(10))
    days: Mapped[str] = mapped_column(String(255))
    hours: Mapped[str] = mapped_column(String(255))
    lastExecution: Mapped[datetime.datetime] = mapped_column(DateTime)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id")) #table name
    user: Mapped["User"] = relationship()
    
    safxTables: Mapped[List["SAFXTable"]] = relationship(
        back_populates="schedule"
    )

    criterias: Mapped[List["Criteria"]] = relationship(
        back_populates="schedule"
    )
    
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
    __tablename__ = "schedulelog"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    numLote: Mapped[str] = mapped_column(String(255))
    executionDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    errorMessage: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(10))
    integrationStatus: Mapped[str] = mapped_column(String(255))
    
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedule.id")) #table name
    schedule: Mapped["Schedule"] = relationship()

    taxOneErrors: Mapped[List["ScheduleLogIntergrationError"]] = relationship(
        back_populates="scheduleLog"
    )

    #schedule = ForeignKeyField(Schedule, backref='scheduleLogs')
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
    __tablename__ = "schedulelogintergrationerror"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    numeroReg: Mapped[int] = mapped_column(Integer)
    codigoErro: Mapped[str] = mapped_column(String(255))
    descricaoErro: Mapped[str] = mapped_column(String(255))
    nomeCampo: Mapped[str] = mapped_column(String(255))
    chaveRegistro: Mapped[str] = mapped_column(String(255))

    scheduleLog_id: Mapped[int] = mapped_column(ForeignKey("schedulelog.id")) #table name
    scheduleLog: Mapped["ScheduleLog"] = relationship()
    
    #scheduleLog = ForeignKeyField(ScheduleLog, backref='taxOneErrors')
    
    def toJson(self):
        return '{' + '"id" : ' + str(self.id) + ',' + '"numeroReg" : "' + str(self.numeroReg) + '",' + '"codigoErro" : "' + self.codigoErro + '",' + '"descricaoErro" : "' + self.descricaoErro + '",' + '"nomeCampo" : "' + self.nomeCampo + '",' + '"chaveRegistro" : "' + self.chaveRegistro + '" }'
    
