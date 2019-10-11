from app import app, db, ma
from app.models import Translation, Vocabulary, Chapter, Book, GrammaticalTerm, Statistic, Grammar, TranslationExample, GrammarExample, asoc_translation_example

@app.shell_context_processor
def make_shell_context():
    return {'db': db, \
        'Vocabulary': Vocabulary, \
        'Chapter': Chapter, \
        'Book': Book, \
        'GrammaticalTerm': GrammaticalTerm, \
        'Translation' : Translation, \
        'TranslationExample' : TranslationExample, \
        'Statistic' : Statistic, \
        'Grammar' : Grammar, \
        'asoc_translation_example' : asoc_translation_example}
