from marshmallow import fields
from app import (
    ma,
    db
)
from app.models import (
    Vocabulary,
    GrammaticalTerm
)

class VocabularySchema(ma.ModelSchema):
    class Meta:
        model = Vocabulary
        sqla_session = db.session
    pinyin = fields.Str()
    pinyin_numerical = fields.Str()
    translation = fields.Nested('TranslationSchema', default=[], many=True)

class TranslationSchema(ma.ModelSchema):
    id = fields.Int()
    vocabulary_id = fields.Int()
    translation_en = fields.Str()
    gram_term_id = fields.Str()
    gram_term = fields.Nested('GrammaticalTermSchema')
    example = fields.Nested('ExampleSchema', default=[], many=True)

class ExampleSchema(ma.ModelSchema):
    example = fields.Str()

class GrammaticalTermSchema(ma.ModelSchema):
    id = fields.Str()
    color = fields.Str()