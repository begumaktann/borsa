# Generated by Django 4.2.4 on 2023-08-31 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0003_cartitem_checked_out"),
    ]

    operations = [
        migrations.CreateModel(
            name="DownloadLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("download_token", models.CharField(max_length=100, unique=True)),
                ("link_expiration", models.DateTimeField()),
            ],
        ),
    ]
