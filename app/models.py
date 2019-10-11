import pinyin
import pinyin.cedict
import hashlib
import re
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from marshmallow import fields
from app import (
    db,
    ma
)

COLOR_CODES = ['rgba-blue-strong',
    'rgba-red-strong',
    'rgba-pink-strong',
    'rgba-purple-strong',
    'rgba-indigo-strong',
    'rgba-cyan-strong',
    'rgba-teal-strong',
    'rgba-green-strong',
    'rgba-orange-strong',
    'rgba-stylish-strong'
    ]

asoc_translation_example = db.Table('tbl_translation_example_asoc', db.Model.metadata,
    db.Column('translation_id', db.Integer, db.ForeignKey('tbl_translation.id')),
    db.Column('example_id', db.Integer, db.ForeignKey('tbl_translation_example.id'))
)

asoc_grammar_example = db.Table('tbl_grammar_example_asoc', db.Model.metadata,
    db.Column('grammar_id', db.Integer, db.ForeignKey('tbl_grammar.id')),
    db.Column('example_id', db.Integer, db.ForeignKey('tbl_grammar_example.id'))
)

class Vocabulary(db.Model):
    __tablename__ = 'tbl_vocabulary'
    id = db.Column(db.Integer, primary_key=True)
    hanzi = db.Column(db.String(32), index=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('tbl_chapter.id'))
    number_in_chapter = db.Column(db.Integer)
    translation = db.relationship(
        'Translation',
        backref='vocabulary',
        lazy='dynamic'
    )

    @property
    def pinyin(self):
        return pinyin.get(self.hanzi)

    @property
    def pinyin_numerical(self):
        return pinyin.get(self.hanzi, format="numerical")

    @property
    def auto_translation_en(self):
        return pinyin.cedict.translate_word(self.hanzi)

    @property
    def additional_examples(self):
        return get_more_examples(self.hanzi)
    
    @property
    def additional_vocabulary(self):
        v = Vocabulary.query \
            .filter(Vocabulary.hanzi == self.hanzi) \
            .filter(Vocabulary.id != self.id).all()
        return v

    def __repr__(self):
        return '<Hanzi {}>'.format(self.hanzi)

class Translation(db.Model):
    __tablename__ = 'tbl_translation'
    id = db.Column(db.Integer, primary_key=True)
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('tbl_vocabulary.id'))
    translation_en = db.Column(db.String(128), index=True)
    gram_term_id = db.Column(db.Integer, db.ForeignKey('tbl_grammatical_term.id'))
    example = db.relationship(
        'TranslationExample',
        secondary=asoc_translation_example
    )

    def __repr__(self):
        return '<Translation {}>'.format(self.translation_en)

class TranslationExample(db.Model):
    __tablename__ = 'tbl_translation_example'
    id = db.Column(db.Integer, primary_key=True)
    example = db.Column(db.String(256))

    def __repr__(self):
        return '<Translation Example {}>'.format(self.example)

class Grammar(db.Model):
    __tablename__ = 'tbl_grammar'
    id = db.Column(db.Integer, primary_key=True)
    grammar_pattern = db.Column(db.String(64))
    search_pattern = db.Column(db.String(64))
    short_description = db.Column(db.String(64))
    explanation = db.Column(db.String(4096))
    chapter_id = db.Column(db.Integer, db.ForeignKey('tbl_chapter.id'))
    example = db.relationship(
        'GrammarExample',
        secondary=asoc_grammar_example
    )

    @property
    def additional_examples(self):
        return get_more_grammar_examples(self.search_pattern)

    def __repr__(self):
        return '<Grammar {}>'.format(self.grammar_pattern)

class GrammarExample(db.Model):
    __tablename__ = 'tbl_grammar_example'
    id = db.Column(db.Integer, primary_key=True)
    example = db.Column(db.String(256))

    def __repr__(self):
        return '<GrammarExample {}>'.format(self.example)

class Book(db.Model):
    __tablename__ = 'tbl_book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    short_name = db.Column(db.String(32))
    chapters = db.relationship(
        'Chapter',
        backref='book',
        lazy='dynamic'
    )

    @property
    def color(self):
        return get_color_code(self.name)

    def __repr__(self):
        return '<Book {}>'.format(self.name)

class Chapter(db.Model):
    __tablename__ = 'tbl_chapter'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(128))
    book_id = db.Column(db.Integer, db.ForeignKey('tbl_book.id'))
    vocabulary = db.relationship(
        'Vocabulary',
        backref='chapter',
        lazy='dynamic'
    )
    grammar = db.relationship(
        'Grammar',
        backref='chapter',
        lazy='dynamic'
    )

    @property
    def color(self):
        return get_color_code(self.name)

    @property
    def full_name(self):
        return '({}) {}'.format(self.id, self.name)

    def __repr__(self):
        return '<Chapter {}>'.format(self.name)

class GrammaticalTerm(db.Model):
    __tablename__ = 'tbl_grammatical_term'
    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(32))
    translation = db.relationship(
        'Translation',
        backref='gram_term',
        lazy='dynamic'
    )

    @property
    def color(self):
        return get_color_code(self.id)

    def __repr__(self):
        return '<Term {}>'.format(self.id)

class Statistic(db.Model):
    __tablename__ = 'tbl_statistic'
    id = db.Column(db.Integer, primary_key=True)
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('tbl_vocabulary.id'))
    result = db.Column(db.String(32))

    def __repr__(self):
        return '<Stat {}>'.format(self.id)

def get_more_grammar_examples(search_pattern):
    all_examples = []
    examples = TranslationExample.query.filter(TranslationExample.example.like(search_pattern)).all()
    for e in examples:
        for f in e.example.split('|'):
            if re.match(search_pattern.replace('%','.*'), f) and f not in all_examples:
                all_examples.append(f)
    return all_examples

def get_more_examples(hanzi):
    splitter = '／'
    all_examples = []
    hanzi = hanzi.split(splitter)
    for h in hanzi:
        filter = '%{}%'.format(h)
        if '…' in h:
            split = h.split('…')
            filter = '%{}%{}%'.format(split[0], split[1])
        examples = db.session \
            .query(TranslationExample.example) \
            .filter(TranslationExample.example.like(filter)) \
            .all()
        for e in examples:
            for f in e.example.split('|'):
                if (h in f or re.match(filter.replace('%','.*'), f) is not None) and f not in all_examples:
                    all_examples.append(f)
    return all_examples

def get_color_code(input):
    color_codes_length = len(COLOR_CODES)
    checksum = hashlib.md5(input.encode('utf-8')).hexdigest()
    random = re.sub(r'[^0-9]', '', checksum)
    index = int(random) % color_codes_length
    return COLOR_CODES[index]
