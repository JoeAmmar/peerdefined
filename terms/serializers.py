from rest_framework import serializers
from definitions.models import Definition, Authors, Synonym, Discipline
from definitions.models import Authors
from terms.models import Term



class AuthorsSerializer(serializers.ModelSerializer):
    fullAPACitation = serializers.CharField(source='citation')
    inTextCitation = serializers.CharField(source='in_text')
    class Meta:
        model = Authors
        fields = ['inTextCitation', 'fullAPACitation', 'doi']

class DefinitionSerializer(serializers.ModelSerializer):
    author = AuthorsSerializer(many=True,read_only=True)
    synonym = serializers.StringRelatedField(many=True, read_only=True)
    discipline = serializers.StringRelatedField(many=True, read_only=True)
    definition = serializers.CharField(source='defs')
    citationNumber = serializers.CharField(source='citeNumber')
    class Meta:
        model = Definition
        fields = ['author', 'year','definition','citationNumber','discipline', 'synonym']

class TermSerializer(serializers.ModelSerializer):
    definitions = DefinitionSerializer(many=True,read_only=True)
    term = serializers.CharField(source='name')
    class Meta:
        model = Term
        fields = ['term','definitions']
