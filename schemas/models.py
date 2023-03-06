from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


# Create your models here.

class Schema(models.Model):
    class SeparatorChoice(models.TextChoices):
        Comma = ','
        Semicolon = ';'

    class StringCharacterChoice(models.TextChoices):
        Quote = "'"
        DoubleQuote = '"'

    name = models.CharField(max_length=200)
    user = models.ForeignKey(UserModel, related_name='schemas', on_delete=models.CASCADE)
    column_separator = models.CharField(max_length=2, choices=SeparatorChoice.choices, default=SeparatorChoice.Comma)
    string_character = models.CharField(max_length=2, choices=StringCharacterChoice.choices,
                                        default=StringCharacterChoice.DoubleQuote)
    created_at = models.DateTimeField(auto_now_add=True)


class Column(models.Model):
    class TypeChoices(models.TextChoices):
        Full_name = 'Full Name'
        Job = 'Job'
        Email = 'Email'
        Company = 'Company'
        Integer = 'Integer'
        Address = 'Address'

    name = models.CharField(max_length=255)
    column_type = models.CharField(max_length=50, choices=TypeChoices.choices, default=TypeChoices.Integer)
    order = models.PositiveIntegerField()
    range_from = models.PositiveIntegerField(null=True, blank=True)
    range_to = models.PositiveIntegerField(null=True, blank=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    class Meta:
        ordering = ('order',)

    class DataSetModel(models.Model):
        # rows quantity, sep and string quotes? Mb here or in schema model
        pass
