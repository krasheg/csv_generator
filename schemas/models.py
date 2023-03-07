from django.contrib.auth import get_user_model
from django.db import models
from django.core.files.storage import default_storage
from .services import fake_data

import csv
import os
from csv_generator.settings import MEDIA_ROOT,MEDIA_URL

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


class DataSet(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, blank=True, null=True)
    rows = models.IntegerField()
    download_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    def create_csv_file(self):
        schema = self.schema
        print(schema)
        try:
            os.mkdir(MEDIA_ROOT)
        except OSError:
            pass
        csv.register_dialect(
            "MyDialect",
            delimiter=str(schema.column_separator),
            quotechar=str(schema.string_character),
            quoting=csv.QUOTE_ALL,
        )
        columns = Column.objects.filter(schema=schema).values()
        field_names = [i['name'] for i in columns]
        download_link = f"{MEDIA_URL}schema_{schema.id}_dataset_{self.id}.csv"
        file_path = os.path.join(MEDIA_ROOT, f"schema_{schema.id}_dataset_{self.id}.csv")
        with default_storage.open(file_path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=field_names, dialect='MyDialect')
            writer.writeheader()
            for i in range(self.rows):
                row = {}
                for col in columns:
                    column_name = col["name"]
                    if (
                            col["range_from"]
                            and col["range_to"]
                            and col["column_type"] == 'Integer'
                    ):
                        value = fake_data(
                            col["column_type"],
                            (col["range_from"], col["range_to"]),
                        )
                    else:
                        value = fake_data(col["column_type"])
                    row[column_name] = value
                writer.writerow(row)

        self.download_url = download_link
        self.status = 'Ready'
        self.save()
        return self.download_url

    class Meta:
        ordering = ('created_at',)
