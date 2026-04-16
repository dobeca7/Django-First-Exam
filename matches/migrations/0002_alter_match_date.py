from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("matches", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="date",
            field=models.DateField(),
        ),
    ]
