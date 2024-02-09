import time
from raebot import search_words
import genanki
from peewee import *

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
    # .where(Lookup.book_key == "Preterito_imperfecto:DE2DB34D")
    .group_by(Word.stem)
)

css ="""
.word {
    font-weight: bold;
    text-align: center;
    font-family: sans-serif;
    font-size: 15pt
}
.usage {
    font-family: sans-serif;
    font-size: 13pt;
}
.word-type {
    font-family: system-ui;
    font-size: 12pt;
}
.definition {
    font-family: system-ui;
    font-size: 14pt;
}
.examples {
    font-family: sans-serif;
    font-size: 13pt;
}
.synonyms {
    font-family: sans-serif;
    font-size: 13pt;
}
"""

my_model = genanki.Model(
  1607392322,
  'Simple Model',
  fields=[
    {'name': 'Word'},
    {'name': 'Example'},
    {'name': 'Definition'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '<div class="word">{{Word}}</div><p class="usage">{{Example}}</p>',
      'afmt': '{{FrontSide}}<hr id="answer">{{Definition}}',
    },
  ],
  css=css
  )

my_deck = genanki.Deck(
  2059400222,
  'Vocabularios Kindle')

unknown = []
exceptions = []

for l in lookup:
    print(l.word.stem)
    # if l.word.stem.startswith("P"):
    #     break
    try:
        res = search_words(l.word.stem)
    except:
        exceptions.append(l.word.stem)
        continue
    if not res:
        unknown.append(l.word.stem)
        continue
    defis = res[0].definitions[:3]
    dd =  ""
    for defi in defis:
        dd += '<div>(<span class="word-type">'
        dd += " ".join(defi.types)
        dd += '</span>) <span class="definition">'
        dd += defi.definition
        dd += "</span>"
        if defi.examples:
            dd += '<span class="examples"> 📜 '
            dd += " "
            dd += " ".join(defi.examples)
            dd += "</span>"
        if hasattr(defi, "synonyms") and defi.synonyms:
            dd += '<br><span class="synonyms"> SIN.: '
            dd += " ".join(defi.synonyms)
            dd += "</span>"
        if hasattr(defi, "antonyms") and defi.antonyms:
            dd += '<br><span class="synonyms">ANT.: '
            dd += " ".join(defi.antonyms)
            dd += "</span>"
        dd += "</div><br>"
    my_note = genanki.Note(
        model=my_model,
        fields=[res[0].text, l.usage, dd]
    )
    my_deck.add_note(my_note)
    time.sleep(1)

genanki.Package(my_deck).write_to_file('output.apkg')
open("unknown.txt", "w").write("\n".join(unknown))
open("exceptions.txt", "w").write("\n".join(exceptions))
