# kindle_to_anki_es

Converts Kindle Vocabularies into Anki Cards

## What exactly does it do?

For each pair of word and example from `vocab.db` (from Kindle):

1. Find the meaning from RAE with [raebot](https://github.com/weiwei/raebot).
2. Combine all into well-formatted card
3. Assemble cards into Anki format

## Notes

1. [MS Translator][https://docs.microsoft.com/en-us/azure/cognitive-services/translator/]
2. [OL][https://languages.oup.com/google-dictionary-es/]
3. [DLE][https://dle.rae.es/]
4. ???

The plan was to use spacy for step 2 and 3, but apparently spacy isn't accurate enough. Use Kindle word stem instead.
