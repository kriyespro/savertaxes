from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_add_articles_per_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodelconfig',
            name='is_paused',
            field=models.BooleanField(
                default=False,
                verbose_name='Pause Autopublish',
                help_text='When checked, the autopublish command exits immediately without generating any articles.',
            ),
        ),
    ]
