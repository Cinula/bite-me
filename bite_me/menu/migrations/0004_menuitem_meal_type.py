from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0003_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='meal_type',
            field=models.CharField(
                choices=[
                    ('breakfast', 'Breakfast'),
                    ('lunch', 'Lunch'),
                    ('dinner', 'Dinner')
                ],
                default='lunch',
                max_length=10
            ),
        ),
    ] 