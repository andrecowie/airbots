from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

class Question(Model):
    class Meta:
        table_name = 'graphene-question'
        region = 'ap-southeast-2'
    id = UnicodeAttribute(hash_key=True)
    text = UnicodeAttribute(null=True)
