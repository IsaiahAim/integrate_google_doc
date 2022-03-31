from rest_framework import serializers
from .models import Memo, Template


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = '__all__'
        read_only_fields = ['url', 'provider', 'document_id', 'created_by']


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ['url', 'provider', 'document_id', 'created_by']
