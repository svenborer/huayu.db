import random
import re
from sqlalchemy import (
    func,
    or_
)
from datetime import datetime
from flask import (
    render_template,
    flash,
    redirect,
    request,
    url_for,
    jsonify
)
from app.models import (
    Vocabulary,
    Translation,
    Chapter,
    Book,
    GrammaticalTerm,
    Statistic,
    Grammar,
    TranslationExample,
    Favorite
)
from app.schemas import (
    VocabularySchema
)
from app.helper import *
from app import (
    app,
    db,
    ma
)

@app.route('/huayu-db/')
@app.route('/huayu-db/index')
def index():
    return redirect(url_for('vocabulary'))

@app.route('/huayu-db/vocabulary')
def vocabulary():
    vocabulary = Vocabulary.query \
        .order_by(Vocabulary.chapter_id.desc()) \
        .limit(200)
    return render_template('vocabulary.html',
        title='Vocabulary',
        vocabulary=vocabulary)

@app.route('/huayu-db/vocabulary/favorite')
def vocabulary_by_favorite():
    vocabulary = Vocabulary.query \
        .filter(Vocabulary.id == Favorite.vocabulary_id) \
        .filter(Favorite.favorite == True) \
        .order_by(Vocabulary.id.desc()) \
        .limit(200)
    return render_template('vocabulary.html',
        title='Favorite Vocabulary',
        vocabulary=vocabulary)


@app.route('/huayu-db/vocabulary/grammatical_term/<gram_term_id>')
def vocabulary_by_grammatical_term(gram_term_id):
    vocabulary = Vocabulary.query \
        .join(Translation, (Translation.vocabulary_id == Vocabulary.id)) \
        .filter(Translation.gram_term_id == gram_term_id)
    if vocabulary.first() is None:
        flash('No content found for grammatical term {}'.format(gram_term_id))
        return redirect(url_for('index'))
    title = '{}'.format(gram_term_id)
    return render_template('vocabulary.html',
        title=title,
        vocabulary=vocabulary)

@app.route('/huayu-db/vocabulary/chapter/<chapter_id>')
def vocabulary_by_chapter(chapter_id):
    vocabulary = Vocabulary.query \
        .filter(Vocabulary.chapter_id == chapter_id)
    if vocabulary.first() is None:
        flash('No content found for chapter {}'.format(chapter_id))
        return redirect(url_for('index'))
    title = '{}'.format(vocabulary.first().chapter.name)
    return render_template('vocabulary.html',
        title=title,
        vocabulary=vocabulary)

@app.route('/huayu-db/vocabulary/book/<book_id>')
def vocabulary_by_book(book_id):
    vocabulary = Vocabulary.query \
        .join(Chapter, Book) \
        .filter(Book.id == book_id)
    if vocabulary.first() is None:
        flash('No content found for book {}'.format(book_id))
        return redirect(url_for('index'))
    title = '{}'.format(vocabulary.first().chapter.book.name)
    return render_template('vocabulary.html',
        title=title,
        vocabulary=vocabulary)

@app.route('/huayu-db/grammar')
def grammar():
    grammar = Grammar.query \
        .order_by(Grammar.chapter_id.desc())
    return render_template('grammar.html',
        title='Grammar',
        grammar=grammar)

@app.route('/huayu-db/grammar/chapter/<chapter_id>')
def grammar_by_chapter(chapter_id):
    grammar = Grammar.query \
        .filter(Grammar.chapter_id == chapter_id)
    if grammar.first() is None:
        flash('No content found for chapter {}'.format(chapter_id))
        return redirect(url_for('index'))
    title = '{}'.format(grammar.first().chapter.name)
    return render_template('grammar.html',
        title=title,
        grammar=grammar)

@app.route('/huayu-db/grammar/book/<book_id>')
def grammar_by_book(book_id):
    grammar = Grammar.query \
        .join(Chapter, (Chapter.id == Grammar.chapter_id)) \
        .join(Book, (Book.id == Chapter.book_id)) \
        .filter(Book.id == book_id)
    if grammar.first() is None:
        flash('No content found for chapter {}'.format(chapter_id))
        return redirect(url_for('index'))
    title = '{}'.format(grammar.first().chapter.name)
    return render_template('grammar.html',
        title=title,
        grammar=grammar)

@app.route('/huayu-db/chapter/<chapter_id>')
def chapter(chapter_id):
    vocabulary = Vocabulary.query \
        .filter(Vocabulary.chapter_id == chapter_id)
    grammar = Grammar.query \
        .filter(Grammar.chapter_id == chapter_id)
    grammar_by_chapter = {}
    gr = db.session.query(GrammaticalTerm.id).all()
    stats = {}
    stats['START'] = 0
    for g in gr:
        i = db.session \
            .query(func.count(Translation.gram_term_id)) \
            .join(Vocabulary, (Vocabulary.id == Translation.vocabulary_id)) \
            .filter(Translation.gram_term_id == g.id) \
            .filter(Vocabulary.chapter_id == chapter_id).all()
        stats[g.id] = i[0][0]
    stats['END'] = 0
    grammar_by_chapter[chapter_id] = stats
    tones = {}
    for i in range(1,5):
        tones[i] = 0
    for v in [v.pinyin_numerical for v in vocabulary]:
        for i in range(1,5):
            regex = '[{}]'.format(i)
            tones[i] += len(re.findall(regex, v))
    if vocabulary.first() is None and grammar.first() is None:
        flash('No content found for chapter {}'.format(chapter_id))
        return redirect(url_for('index'))
    title = '{}'.format(vocabulary.first().chapter.name)
    return render_template('chapter.html',
        title=title,
        vocabulary=vocabulary,
        grammar=grammar,
        grammar_by_chapter=grammar_by_chapter,
        tones=tones)

@app.route('/huayu-db/print/<chapter_id>')
def print(chapter_id):
    vocabulary = Vocabulary.query \
        .filter(Vocabulary.chapter_id == chapter_id) \
        .order_by(Vocabulary.chapter_id.desc())
    grammar = Grammar.query \
        .filter(Grammar.chapter_id == chapter_id)
    grammar_by_chapter = {}
    gr = db.session.query(GrammaticalTerm.id).all()
    stats = {}
    stats['START'] = 0
    for g in gr:
        i = db.session \
            .query(func.count(Translation.gram_term_id)) \
            .join(Vocabulary, (Vocabulary.id == Translation.vocabulary_id)) \
            .filter(Translation.gram_term_id == g.id) \
            .filter(Vocabulary.chapter_id == chapter_id).all()
        stats[g.id] = i[0][0]
    stats['END'] = 0
    grammar_by_chapter[chapter_id] = stats
    tones = {}
    for i in range(1,5):
        tones[i] = 0
    for v in [v.pinyin_numerical for v in vocabulary]:
        for i in range(1,5):
            regex = '[{}]'.format(i)
            tones[i] += len(re.findall(regex, v))
    if vocabulary.first() is None and grammar.first() is None:
        flash('No content found for chapter {}'.format(chapter_id))
        return redirect(url_for('index'))
    title = '第{}本書，第{}顆：{}'.format(vocabulary.first().chapter.book.id, vocabulary.first().chapter.number, vocabulary.first().chapter.name)
    return render_template('chapter_print.html',
        title=title,
        vocabulary=vocabulary,
        grammar=grammar,
        grammar_by_chapter=grammar_by_chapter,
        tones=tones)

@app.route('/huayu-db/get/vocabulary/<vocabulary_id>')
def get_vocabulary(vocabulary_id):
    vocabulary = Vocabulary.query \
        .filter_by(id=vocabulary_id) \
        .first_or_404()
    if vocabulary is None:
        return redirect(url_for('index'))
    return render_template('get_vocabulary.html',
        title='Vocabulary {}'.format(vocabulary.hanzi),
        vocabulary=vocabulary)

@app.route('/huayu-db/get/grammar/<grammar_id>')
def get_grammar(grammar_id):
    if grammar_id == 'random':
        grammar = Grammar.query \
            .order_by(func.random()) \
            .first()
    else:
        grammar = Grammar.query \
            .filter_by(id=grammar_id) \
            .first_or_404()
    if grammar is None:
        return redirect(url_for('index'))
    return render_template('get_grammar.html',
        title='Get Grammar',
        grammar=grammar)

@app.route('/huayu-db/search/', methods=['GET'])
def search():
    query = request.args.get('q')
    pattern = '%{}%'.format(query)
    vocabulary = Vocabulary.query \
        .join(Translation)\
        .filter(or_(Translation.translation_en.like(pattern), Vocabulary.hanzi.like(pattern))).all()
    grammar = Grammar.query \
        .filter(Grammar.grammar_pattern.like(pattern)).all()
    return render_template('search.html',
        title='Search: {}'.format(query),
        vocabulary=vocabulary,
        grammar=grammar)

@app.route('/huayu-db/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        chapters = request.form.getlist('chapters')
        type = request.form.get('type')
        limit = request.form.get('limit')
        if limit == '':
            limit = 1000
        favorites = request.form.get('favorites_only')
        title = 'Test Chapter {}'.format(chapters)
        list = get_vocabulary_id_list(chapters = chapters, limit = limit)
        return render_template('test_chapter.html',
            title=title,
            list=list,
            type=type)
    else:
        chapters = get_chapter_dict()
        return render_template('test.html', title='Test', chapters=chapters)

@app.route('/huayu-db/statistic')
def statistic():
    grammar_by_chapter = {}
    gr = db.session.query(GrammaticalTerm.id).all()
    for c in Chapter.query.all():
        stats = {}
        stats['START'] = 0
        for g in gr:
            i = db.session \
                .query(func.count(Translation.gram_term_id)) \
                .join(Vocabulary, (Vocabulary.id == Translation.vocabulary_id)) \
                .filter(Translation.gram_term_id == g.id) \
                .filter(Vocabulary.chapter_id == c.id).all()
            stats[g.id] = i[0][0]
        stats['END'] = 0
        grammar_by_chapter[c.id] = stats
    vocab_by_chapter = db.session \
        .query(Vocabulary.chapter_id, func.count(Vocabulary.chapter_id)) \
        .group_by(Vocabulary.chapter_id) \
        .all()
    total = []
    for i in range(0, len(vocab_by_chapter)):
        total.append((vocab_by_chapter[i][0], sum([v[1] for v in vocab_by_chapter[:i+1]])))
    
    chapter_list = [c.chapter_id for c in db.session.query(Vocabulary.chapter_id).order_by(Vocabulary.chapter_id).group_by(Vocabulary.chapter_id).all()]
    unique_chars = []
    new_chars = {}
    totalNewChars = {}
    c_unique_chars = {}
    cTotal = 0

    for c in chapter_list:
        new_chars[c] = 0
        c_unique_chars[c] = 0
        c_unique_chars_c = []
        vocab_list = [v.hanzi for v in Vocabulary.query.filter(Vocabulary.chapter_id == c).all()]
        for v in vocab_list:
            for index in range(len(v)):
                if v[index] not in unique_chars:
                    unique_chars.append(v[index])
                    new_chars[c] += 1
                    cTotal += 1
                if v[index] not in c_unique_chars_c:
                    c_unique_chars_c.append(v[index])
                    c_unique_chars[c] += 1
        totalNewChars[c] = cTotal

    return render_template('statistic.html',
        title='Statistics',
        grammar_by_chapter=grammar_by_chapter,
        vocab_by_chapter=vocab_by_chapter,
        new_chars=new_chars,
        totalNewChars=totalNewChars,
        c_unique_chars=c_unique_chars,
        total=total)

@app.route('/huayu-db/api/vocab/<vocab_id>', methods=['GET'])
def get_vocab_by_id(vocab_id):
    vocab = (
        Vocabulary.query.filter(Vocabulary.id == vocab_id)
        .one_or_none()
    )
    if vocab is not None:
        vocab_schema = VocabularySchema()
        data = vocab_schema.dump(vocab)
        return data

@app.route('/huayu-db/vocabulary/favorite/<vocab_id>', methods=['GET'])
def favorite_vocab(vocab_id):
    is_vocab = Vocabulary.query.filter(Vocabulary.id == vocab_id).first_or_404()
    if is_vocab:
        is_fav = Favorite.query.filter(Favorite.vocabulary_id == vocab_id).all()
        if is_fav:
            text = '{} has been removed from favorites.'
            Favorite.query.filter(Favorite.vocabulary_id == vocab_id).delete()
        else:
            text = '{} has been added to favorites.'
            f = Favorite(vocabulary_id = vocab_id, favorite = True)
            db.session.add(f)
        db.session.commit()
        return text.format(vocab_id)
    else:
        return redirect(url_for('index'))

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}
