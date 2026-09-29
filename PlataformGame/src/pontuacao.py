from peewee import *

db = SqliteDatabase('pontuacao.db')

class Pontuacao(Model):
    nome_player = CharField()
    pontuacao = FloatField()
    tempo = FloatField()

    class Meta:
        database = db


db.connect()
db.create_tables([Pontuacao])