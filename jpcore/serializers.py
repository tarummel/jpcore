from rest_framework import serializers
from jpcore.models import Kanji, Radical

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

class KanjiSerializer(DynamicFieldsModelSerializer):
    radicals = serializers.PrimaryKeyRelatedField(queryset = Radical.objects.all(), many = True)
    
    class Meta:
        model = Kanji
        fields = ['kanji', 'strokes', 'radicals']

    def simplified(self, kanji):
        return f'{kanji.kanji}{kanji.strokes}'

class RadicalSerializer(DynamicFieldsModelSerializer):
    kanji_set = KanjiSerializer(read_only = True, many = True)

    class Meta:
        model = Radical
        fields = ['number', 'radical', 'strokes', 'meaning', 'reading', 'frequency', 'position', 'notes', 'kanji_set']

    def simplified(self, radical):
        return f'{radical.radical}{radical.strokes}'
