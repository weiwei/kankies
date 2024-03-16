import time
import genanki
import re

css ="""
.es-word {
    font-weight: bold;
    text-align: center;
    font-family: sans-serif;
    font-size: 15pt
}
.fr-word {
    font-weight: bold;
    text-align: center;
    font-family: sans-serif;
    font-size: 15pt
}
.ipa {
    font-family: system-ui;
    text-align: center;
    font-size: 15pt;
}
"""

my_model = genanki.Model(
  1607392344,
  'EF Model',
  fields=[
    {'name': 'esWord'},
    {'name': 'frWord'},
    {'name': 'ipa'},
  ],
  templates=[
    {
      'name': 'EF Model 1',
      'qfmt': '<div class="es-word">{{esWord}}</div>',
      'afmt': '{{FrontSide}}<hr id="answer"><p class="fr-word">{{frWord}}</p><p class="ipa">{{ipa}}</p>',
    },
  ],
  css=css
  )

id = 2059400222;
name = 'Vocabulario Francés'
deck = None
decks = []

regex = re.compile(r"(.+)\s—\s(.+)\s(\[.+\])")

for line in open("./vocab_fr.txt", encoding='utf-8'):
    line = line.strip()
    if line.startswith("# "):
        sect_name = line.split(" ", 1)[1]
        sect_deck_name = f"{name}::{sect_name}"
    elif line.startswith("## "):
        if deck is not None:
            decks.append(deck)
        id += 1
        chap_name = line.split(" ", 1)[1]
        chap_deck_name = f"{sect_deck_name}::{chap_name}"
        deck = genanki.Deck(id, chap_deck_name)
    elif "—" in line:
        result = regex.match(line)
        es_word, fr_word, ipa = result.groups()
        my_note = genanki.Note(
            model=my_model,
            fields=[es_word, fr_word, ipa]
        )
        deck.add_note(my_note)
    else:
        continue
else:
    decks.append(deck)

genanki.Package(decks).write_to_file('vocafr.apkg')

