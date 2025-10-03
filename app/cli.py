from __future__ import annotations
from flask import current_app
from flask.cli import with_appcontext
from . import db
from .models import Property
import click


@click.group()
def dbcli():
    """Database custom commands."""
    pass


@dbcli.command("create")
@with_appcontext
def create_db():
    db.create_all()
    click.echo("Database tables created.")


@dbcli.command("drop")
@with_appcontext
def drop_db():
    db.drop_all()
    click.echo("Database tables dropped.")


@dbcli.command("seed")
@with_appcontext
def seed_db():
    if Property.query.count() > 0:
        click.echo("Properties already seeded.")
        return

    demo_props = [
        Property(
            title="Modern Family Home",
            description="Spacious 4 bed, 3 bath with updated kitchen and large backyard.",
            price=650000,
            address="123 Oak St",
            city="Seattle",
            state="WA",
            zip_code="98101",
            beds=4,
            baths=3,
            sqft=2200,
            lot_size=5000,
            property_type="house",
            year_built=2010,
            latitude=47.6062,
            longitude=-122.3321,
            image_url="https://images.unsplash.com/photo-1560185127-6a8c0b4e0f4b?q=80&w=1600&auto=format&fit=crop",
        ),
        Property(
            title="Downtown Condo",
            description="Bright 2 bed condo with city views, walk to amenities.",
            price=480000,
            address="456 Pine Ave Apt 12B",
            city="Seattle",
            state="WA",
            zip_code="98102",
            beds=2,
            baths=1.5,
            sqft=950,
            lot_size=None,
            property_type="condo",
            year_built=2015,
            latitude=47.6097,
            longitude=-122.3331,
            image_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?q=80&w=1600&auto=format&fit=crop",
        ),
        Property(
            title="Cozy Suburban Townhouse",
            description="3 bed, 2 bath townhouse with garage and community park access.",
            price=420000,
            address="789 Cedar Ct",
            city="Bellevue",
            state="WA",
            zip_code="98004",
            beds=3,
            baths=2,
            sqft=1400,
            lot_size=None,
            property_type="townhouse",
            year_built=2005,
            latitude=47.6101,
            longitude=-122.2015,
            image_url="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=1600&auto=format&fit=crop",
        ),
    ]

    db.session.add_all(demo_props)
    db.session.commit()
    click.echo(f"Seeded {len(demo_props)} properties.")


def init_app(app):
    app.cli.add_command(dbcli, name="dbx")
