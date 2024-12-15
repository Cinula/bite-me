from django.db import migrations

def add_tables(apps, schema_editor):
    Table = apps.get_model('booking', 'Table')

    # Indoor Tables
    indoor_tables = [
        # Two-seater tables (Romantic/Couple tables)
        {'number': 'T1', 'capacity': 2},
        {'number': 'T2', 'capacity': 2},
        {'number': 'T3', 'capacity': 2},
        {'number': 'T4', 'capacity': 2},

        # Four-seater tables (Family/Small Group tables)
        {'number': 'T5', 'capacity': 4},
        {'number': 'T6', 'capacity': 4},
        {'number': 'T7', 'capacity': 4},
        {'number': 'T8', 'capacity': 4},

        # Six-seater tables (Medium Group tables)
        {'number': 'T9', 'capacity': 6},
        {'number': 'T10', 'capacity': 6},
        {'number': 'T11', 'capacity': 6},

        # Eight-seater tables (Large Group tables)
        {'number': 'T12', 'capacity': 8},
        {'number': 'T13', 'capacity': 8},
    ]

    # Bar Area Tables
    bar_tables = [
        {'number': 'B1', 'capacity': 4},  # Bar high table
        {'number': 'B2', 'capacity': 4},  # Bar high table
        {'number': 'B3', 'capacity': 2},  # Bar counter seats
        {'number': 'B4', 'capacity': 2},  # Bar counter seats
    ]

    # Outdoor Tables
    outdoor_tables = [
        {'number': 'O1', 'capacity': 6},  # Outdoor garden table
        {'number': 'O2', 'capacity': 6},  # Outdoor garden table
        {'number': 'O3', 'capacity': 4},  # Outdoor terrace table
        {'number': 'O4', 'capacity': 4},  # Outdoor terrace table
    ]

    # VIP/Private Dining Tables
    vip_tables = [
        {'number': 'VIP1', 'capacity': 10},  # Private dining room
        {'number': 'VIP2', 'capacity': 12},  # Large private dining room
    ]

    # Create all tables
    for table in indoor_tables + bar_tables + outdoor_tables + vip_tables:
        Table.objects.create(**table)

def remove_tables(apps, schema_editor):
    Table = apps.get_model('booking', 'Table')
    Table.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_tables, remove_tables),
    ] 