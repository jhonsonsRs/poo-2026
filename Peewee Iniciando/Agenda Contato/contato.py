import datetime
from peewee import *

db = SqliteDatabase('contatos.db')

class Contato(Model): # type: ignore
    nome = CharField()
    telefone = CharField()
    data_cadastro = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def __str__(self):
        return (f"ID: {self.id} | Nome: {self.nome} | Telefone: {self.telefone} | Data de cadastro {self.data_cadastro}")

db.connect()
db.create_tables([Contato])
