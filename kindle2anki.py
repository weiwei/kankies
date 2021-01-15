from enum import unique
from logging import debug
import sys
import sqlite3
import argparse
import spacy

nlp = spacy.load("es_core_news_sm")

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
    .group_by(Word.stem)
)
for l in lookup:
    doc = nlp(l.usage)
    for word in doc:
        if word.text.lower() == l.word.word.lower():
            print(word.text, l.word.stem, word.lemma_, word.pos_)

