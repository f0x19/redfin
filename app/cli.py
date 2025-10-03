from __future__ import annotations

import random
from typing import List

import click
from faker import Faker

from .extensions import db
from .models import Property, PropertyImage


def register_cli(app) -> None:
    @app.cli.command("seed")
    @click.option("--count", default=100, help="Number of properties to create.")
    def seed_command(count: int) -> None:
        """Seed the database with fake properties and images."""
        fake = Faker()
        property_types: List[str] = ["house", "condo", "townhouse", "apartment"]

        click.echo(f"Seeding {count} properties...")

        created = 0
        for _ in range(count):
            price = random.randrange(150_000, 2_500_000, 1000)
            bedrooms = random.randint(1, 6)
            bathrooms = round(random.uniform(1, 5), 1)
            sqft = random.randrange(600, 6000, 10)
            lot = random.randrange(1000, 20000, 50)

            city = fake.city()
            state = fake.state_abbr()

            prop = Property(
                title=f"{bedrooms}BR {random.choice(['Modern','Cozy','Spacious','Charming'])} {random.choice(property_types).title()}",
                address_line=fake.street_address(),
                city=city,
                state=state,
                zipcode=fake.postcode(),
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                property_type=random.choice(property_types),
                square_feet=sqft,
                lot_size_sqft=lot,
                latitude=float(fake.latitude()),
                longitude=float(fake.longitude()),
                year_built=random.randint(1950, 2023),
                description=fake.paragraph(nb_sentences=4),
                status=random.choice(["for_sale", "pending", "sold"]),
            )

            # Add 3-6 images, first one primary
            num_images = random.randint(3, 6)
            for j in range(num_images):
                # Use picsum.photos for placeholder images
                width = random.choice([640, 720, 800, 960])
                height = random.choice([420, 480, 540, 600])
                url = f"https://picsum.photos/{width}/{height}?random={fake.uuid4()}"
                img = PropertyImage(url=url, is_primary=(j == 0))
                prop.images.append(img)

            db.session.add(prop)
            created += 1

            if created % 50 == 0:
                db.session.commit()
                click.echo(f"Committed {created} properties...")

        db.session.commit()
        click.echo(f"Done. Created {created} properties.")
