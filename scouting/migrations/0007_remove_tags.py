from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scouting", "0006_scoutreport_owner"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="scoutreport",
            name="tags",
        ),
        migrations.DeleteModel(
            name="Tag",
        ),
    ]
