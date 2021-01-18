from enum import unique
from logging import debug
import sys
import sqlite3
import argparse
from pyrae import dle
import time
# import spacy

# nlp = spacy.load("es_core_news_sm")

from peewee import *
import datetime

import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

db = SqliteDatabase("vocab.db")


class BaseModel(Model):
    class Meta:
        database = db
        debug = True


class BookInfo(BaseModel):
    class Meta:
        table_name = "BOOK_INFO"
    id = TextField(unique=True)
    asin = TextField()
    guid = TextField()
    lang = TextField()
    title = TextField()
    authors = TextField()

class DictInfo(BaseModel):
    class Meta:
        table_name = "DICT_INFO"
    id = TextField(unique=True)
    asin = TextField()
    langin = TextField()
    langout = TextField()

class Word(BaseModel):
    class Meta:
        table_name = "WORDS"
    id = TextField(unique=True)
    word = TextField(column_name="word")
    stem = TextField()
    lang = TextField()
    category = IntegerField(default=0)
    timestamp = IntegerField(default=0)
    profileid = TextField()

class Lookup(BaseModel):
    class Meta:
        table_name = "LOOKUPS"
    id = TextField(unique=True)
    word_key = TextField()
    book_key = TextField()
    dict_key = TextField()

    pos = TextField()
    usage = TextField()
    timestamp = IntegerField(default=0)

db.connect()

lookup = (Lookup
    .select(Lookup.usage, Word.stem, Word.word)
    .join(Word, JOIN.LEFT_OUTER, on=(Word.id == Lookup.word_key))
    .where(Word.lang == "es")
    .where(Lookup.book_key == "Preterito_imperfecto:DE2DB34D")
    .group_by(Word.stem)
)

# https://developer.oxforddictionaries.com/documentation
od_url = "https://od-api.oxforddictionaries.com/api/v2/entries/es/perro?strictMatch='false'"
od_header = {"app_key": "04b62b3384b577e13c8c08721d7a38cf", "app_id": "52f6522b"}

for l in lookup:
    print(l.word.stem)
    res = dle.search_by_word(word=l.word.stem)
    print(res.to_dict())

