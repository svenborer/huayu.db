from marshmallow import fields
from app import (
    ma,
    db
)
from app.models import (
    Vocabulary,
    Translation
)

class VocabularySchema(ma.ModelSchema):
    class Meta:
        model = Vocabulary
        sqla_session = db.session
    pinyin = fields.Str()
    pinyin_numerical = fields.Str()
    color = fields.Str()
    translation = fields.Nested('VocabularyTranslationSchema', default=[], many=True)

class VocabularyTranslationSchema(ma.ModelSchema):
    id = fields.Int()
    vocabulary_id = fields.Int()
    translation_en = fields.Str()
    example = fields.Str()
    gram_term_id = fields.Str()

class TranslationSchema(ma.ModelSchema):
    class Meta:
        model = Translation
        sqla_session = db.session
    vocabulary = fields.Nested('TranslationVocabularySchema', default=None)

class TranslationVocabularySchema(ma.ModelSchema):
    id = fields.Int()
    hanzi = fields.Str()
    chapter_id = fields.Int()
    vocab_id = fields.Int()
