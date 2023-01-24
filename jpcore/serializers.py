from rest_framework import serializers
from jpcore.models import Radical

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

class RadicalSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Radical
        fields = ['number', 'radical', 'strokes', 'meaning', 'reading', 'frequency', 'position', 'notes']
