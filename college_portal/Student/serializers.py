from rest_framework import serializers
from.models import Student_table
class Studentserializers(serializers.model(serializers)):
    class meta:
        model=Student_table
        fields=['reg_no','name','email']
        