from rest_framework import serializers
from .models import Banks,Branches


class BankSerializer(serializers.ModelSerializer):
    """Serializer for the bank objects"""
    class Meta:
        model = Banks
        fields = ['name','id']
        read_only_field = ['id']


class BranchSerialzier(serializers.ModelSerializer):
    """Serializer for the branch objects}"""
    class Meta:
        model = Branches
        fields = ['ifsc','bank_id','branch','address','city','district','state']
        read_only_fields = fields