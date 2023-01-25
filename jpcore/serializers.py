from rest_framework import serializers
from jpcore import models

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class JMdictKanjiSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.JMdictKanji
        fields = ['content', 'information', 'priorities']

class JMdictReadingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.JMdictReading
        fields = ['content', 'restrictions', 'information', 'priorities']

class JMdictGlossarySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.JMdictGlossary
        fields = ['gloss', 'language', 'type']

class JMdictSourceSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.JMdictSource
        fields = ['content', 'language', 'partial', 'waseieigo']

class JMdictSenseSerializer(DynamicFieldsModelSerializer):
    jglossary = JMdictGlossarySerializer(many = True, read_only = True)
    jsource = JMdictSourceSerializer(many = True, read_only = True)

    class Meta:
        model = models.JMdictSense
        fields = ['xreferences', 'antonyms', 'parts_of_speech', 'fields', 'misc', 'dialects', 'information', 'jglossary', 'jsource']

class JMdictEntrySerializer(DynamicFieldsModelSerializer):
    jkanji = JMdictKanjiSerializer(many = True, read_only = True)
    jreading = JMdictReadingSerializer(many = True, read_only = True)
    jsense = JMdictSenseSerializer(many = True, read_only = True)

    class Meta:
        model = models.JMdictEntry
        fields = ['jkanji', 'jreading', 'jsense']

class KanjiSerializer(DynamicFieldsModelSerializer):
    # TODO: research a better way?
    radicals = serializers.PrimaryKeyRelatedField(queryset = models.Radical.objects.all(), many = True)
    
    class Meta:
        model = models.Kanji
        fields = ['kanji', 'strokes', 'radicals']

    def simplified(self, kanji):
        return f'{kanji.kanji}{kanji.strokes}'

class RadicalSerializer(DynamicFieldsModelSerializer):
    kanji_set = KanjiSerializer(read_only = True, many = True)

    class Meta:
        model = models.Radical
        fields = ['number', 'radical', 'strokes', 'meaning', 'reading', 'frequency', 'position', 'notes', 'kanji_set']

    def simplified(self, radical):
        return f'{radical.radical}{radical.strokes}'
