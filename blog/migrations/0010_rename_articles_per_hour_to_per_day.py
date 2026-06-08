from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_aimodelconfig_is_paused'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aimodelconfig',
            old_name='articles_per_hour',
            new_name='articles_per_day',
        ),
    ]
