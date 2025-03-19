# Generated by Django 4.2.16 on 2025-03-18 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts_app', '0001_initial'),
        ('calls_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('document', models.FileField(upload_to='proposals/')),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('under_review', 'Under Review'), ('feedback', 'Feedback Provided'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='submitted', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='accounts_app.customuser')),
                ('grant_call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='calls_app.grantcall')),
            ],
        ),
    ]
