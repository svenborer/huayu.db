from app import app, db
from app.models import Vocabulary, Translation, TranslationExample, asoc_translation_example, asoc_grammar_example
import csv

Vocabulary.query.delete()
Translation.query.delete()
TranslationExample.query.delete()

with open('csv/main.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        v_id = row['vocabulary.id']
        v_hanzi = row['vocabulary.hanzi']
        v_chapter_id = row['vocabulary.chapter_id']
        v_number_in_chapter = row['vocabulary.number_in_chapter']
        if v_id and v_hanzi and v_chapter_id and v_number_in_chapter:
            v = Vocabulary(
                id = v_id,
                hanzi = v_hanzi,
                chapter_id = v_chapter_id,
                number_in_chapter = v_number_in_chapter
            )
            db.session.add(v)
        t_id = row['translation.id']
        t_vocabulary_id = row['translation.vocabulary_id']
        t_translation_en = row['translation.translation_en']
        t_gram_term_id = row['translation.gram_term_id']
        if t_id and t_vocabulary_id and t_translation_en and t_gram_term_id:
            t = Translation(
                id = t_id,
                vocabulary_id = t_vocabulary_id,
                translation_en = t_translation_en,
                gram_term_id = t_gram_term_id
            )
            db.session.add(t)
        a_translation_id = row['asoc_translation_example.translation_id']
        a_example_id = row['asoc_translation_example.example_id']
        te_example = row['translationexample.example']
        if a_example_id and te_example:
            te = TranslationExample(
                id = a_example_id,
                example = te_example
            )
            db.session.add(te)
        if a_translation_id and a_example_id:
            s = asoc_translation_example.insert().values(
                translation_id=a_translation_id,
                example_id=a_example_id)
            db.session.execute(s)

db.session.commit()