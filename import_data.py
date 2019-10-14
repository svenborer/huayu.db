from app import app, db
from app.models import Vocabulary, Translation, TranslationExample, Book, Chapter, GrammaticalTerm, asoc_translation_example, asoc_grammar_example
import csv

Vocabulary.query.delete()
Translation.query.delete()
TranslationExample.query.delete()
Chapter.query.delete()
Book.query.delete()
GrammaticalTerm.query.delete()

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

with open('csv/tbl_chapter.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        c_id = row['id']
        c_number = row['number']
        c_name = row['name']
        c_book_id = row['book_id']
        if c_id and c_number and c_name and c_book_id:
            c = Chapter(
                id = c_id,
                number = c_number,
                name = c_name,
                book_id = c_book_id
            )
            db.session.add(c)

with open('csv/tbl_book.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        b_id = row['id']
        b_name = row['name']
        b_short_name = row['short_name']
        if b_id and b_name and b_short_name:
            b = Book(
                id = b_id,
                name = b_name,
                short_name = b_short_name
            )
            db.session.add(b)

with open('csv/tbl_grammatical_term.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        g_id = row['id']
        g_name = row['name']
        if g_id and g_name:
            g = GrammaticalTerm(
                id = g_id,
                name = g_name,
            )
            db.session.add(g)

db.session.commit()