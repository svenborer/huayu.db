from marshmallow import fields
from app import (
    ma,
    db
)
from app.models import (
    Vocabulary,
    GrammaticalTerm,
    Chapter
)

class VocabularySchema(ma.ModelSchema):
    class Meta:
        model = Vocabulary
        sqla_session = db.session
        fields = ['hanzi', 'pinyin', 'chapter_id', 'pinyin_numerical', 'translation', 'favorite']
    chapters = fields.Nested('ChapterSchema', many=True)
    translation = fields.Nested('TranslationSchema', default=[], many=True)
    favorite = fields.Nested('FavoriteSchema', default=[], many=True)

class TranslationSchema(ma.ModelSchema):
    class Meta:
        fields = ['translation_en', 'gram_term_id', 'gram_term', 'example']
    id = fields.Int()
    vocabulary_id = fields.Int()
    translation_en = fields.Str()
    gram_term_id = fields.Str()
    gram_term = fields.Nested('GrammaticalTermSchema')
    example = fields.Nested('ExampleSchema', default=[], many=True)

class FavoriteSchema(ma.ModelSchema):
    class Meta:
        fields = ['favorite']

class ChapterSchema(ma.ModelSchema):
    class Meta:
        fields = ['id', 'color']

class ExampleSchema(ma.ModelSchema):
    example = fields.Str()

class GrammaticalTermSchema(ma.ModelSchema):
    class Meta:
        fields = ['id', 'color']