# Generated by Django 4.2.4 on 2023-09-05 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0004_downloadlink"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0006_alter_profile_address_alter_profile_first_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PurchasedItem",
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
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cart.dataset"
                    ),
                ),
                (
                    "download_link",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cart.downloadlink",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
