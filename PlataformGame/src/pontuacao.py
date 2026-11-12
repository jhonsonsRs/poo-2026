import datetime
from pathlib import Path

from peewee import (Model, SqliteDatabase, CharField, IntegerField,
                    FloatField, DateTimeField)

db = SqliteDatabase(Path(__file__).resolve().with_name('ranking.db'))


class BaseModel(Model):
    class Meta:
        database = db


class Pontuacao(BaseModel):
    nome_jogador = CharField()
    pontos = IntegerField()
    tempo_partida = FloatField()
    modo = CharField(default='quick')
    data_hora = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.nome_jogador} - {self.pontos} pts ({self.tempo_partida:.1f}s)"


db.connect(reuse_if_open=True)
db.create_tables([Pontuacao])

# Bancos criados antes da separação dos modos ainda não possuem esta coluna.
colunas = {coluna.name for coluna in db.get_columns(Pontuacao._meta.table_name)}
if 'modo' not in colunas:
    db.execute_sql(
        "ALTER TABLE pontuacao ADD COLUMN modo TEXT NOT NULL DEFAULT 'quick'"
    )
