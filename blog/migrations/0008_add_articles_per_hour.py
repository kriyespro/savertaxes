from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_add_humanize_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodelconfig',
            name='articles_per_hour',
            field=models.IntegerField(
                default=5,
                verbose_name='Articles Per Hour (autopublish rate)',
                help_text=(
                    'How many articles autopublish generates per cron run. '
                    'Sets the delay between articles: 3600 ÷ this number (seconds). '
                    'E.g. 5 = one article every 12 min. Max 20 recommended.'
                ),
            ),
        ),
    ]
