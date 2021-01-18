# kindle_to_anki_es

Converts Kindle Vocabularies into Anki Cards

## What exactly does it do?

For each pair of word and example from `vocab.db`:

1. Find the most likely meaning from a translation service.
2. Determine the type of the word from the example (`habla` is verb or noun)
3. Find the root form of the word (`habla` to `hablar` if it's a verb)
4. Find it's entry from a ES-ES _and_ a ES-EN dictionary
5. Combine all into well-formatted card
6. Assemble cards into Anki format

## What dictionaries and translation services

1. [MS Translator][https://docs.microsoft.com/en-us/azure/cognitive-services/translator/]
2. [OL][https://languages.oup.com/google-dictionary-es/]
3. [DLE][https://dle.rae.es/]
4. ???

## Notes

The plan was to use spacy for step 2 and 3, but apparently spacy isn't accurate enough. Use Kindle word stem instead.
