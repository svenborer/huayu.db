from app import app, db
from app.models import (
    Vocabulary, 
    Translation, 
    TranslationExample, 
    Book, 
    Chapter, 
    GrammaticalTerm, 
    Grammar,
    GrammarExample,
    asoc_translation_example, 
    asoc_grammar_example
)
import csv

Vocabulary.query.delete()
Translation.query.delete()
TranslationExample.query.delete()
Chapter.query.delete()
Book.query.delete()
GrammaticalTerm.query.delete()
Grammar.query.delete()
GrammarExample.query.delete()

v_count = 0
t_count = 0
te_count = 0
g_count = 0
ge_count = 0

with open('csv/main.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        v_id = row['vocabulary.id']
        v_hanzi = row['vocabulary.hanzi']
        v_chapter_id = row['vocabulary.chapter_id']
        v_number_in_chapter = row['vocabulary.number_in_chapter']
        if v_id and v_hanzi and v_chapter_id and v_number_in_chapter:
            v_count += 1
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
            t_count += 1
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
            te_count += 1
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

with open('csv/tbl_grammar.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        g_id = row['grammar.id']
        g_grammar_pattern = row['grammar.grammar_pattern']
        g_search_pattern = row['grammar.search_pattern']
        g_short_description = row['grammar.short_description']
        g_explanation = row['grammar.explanation']
        g_chapter_id = row['grammar.chapter_id']
        if g_id and g_grammar_pattern and g_search_pattern and g_short_description and g_explanation and g_chapter_id:
            g_count += 1
            v = Grammar(
                id = g_id,
                grammar_pattern = g_grammar_pattern,
                search_pattern = g_search_pattern,
                short_description = g_short_description,
                explanation = g_explanation,
                chapter_id = g_chapter_id
            )
            db.session.add(v)
        a_grammar_id = row['asoc_grammar_example.grammar_id']
        a_example_id = row['asoc_grammar_example.example_id']
        ge_example = row['grammarexample.example']
        if a_example_id and ge_example:
            ge_count += 1
            ge = GrammarExample(
                id = a_example_id,
                example = ge_example
            )
            db.session.add(ge)
        if a_grammar_id and a_example_id:
            s = asoc_grammar_example.insert().values(
                grammar_id=a_grammar_id,
                example_id=a_example_id)
            db.session.execute(s)
try:
    db.session.commit()
    print('Imported {} vocabulary.'.format(v_count))
    print('Imported {} translations.'.format(t_count))
    print('Imported {} translation examples.'.format(te_count))
    print('Imported {} grammar.'.format(g_count))
    print('Imported {} grammar examples.'.format(ge_count))
except Exception as e:
    print(e)