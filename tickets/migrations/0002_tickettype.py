# Generated by Django 3.1.2 on 2020-10-27 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('qty', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='TicketTypes', related_query_name='TicketTypes', to='tickets.event')),
            ],
        ),
    ]