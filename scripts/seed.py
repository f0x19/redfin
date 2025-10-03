from app import create_app, db
from app.models import Property

app = create_app()

with app.app_context():
    if Property.query.count() == 0:
        sample = [
            Property(
                title="Lakeview Luxury Estate",
                description="Expansive views with floor-to-ceiling windows and chef's kitchen.",
                price=1850000,
                address="10 Lakeview Dr",
                city="Kirkland",
                state="WA",
                zip_code="98033",
                beds=5,
                baths=4.5,
                sqft=4200,
                lot_size=12000,
                property_type="house",
                year_built=2018,
                latitude=47.6769,
                longitude=-122.2053,
                image_url="https://images.unsplash.com/photo-1505692952047-1a78307da8f2?q=80&w=1600&auto=format&fit=crop",
            ),
        ]
        db.session.add_all(sample)
        db.session.commit()
        print("Seeded 1 property (scripts/seed.py)")
    else:
        print("Database already has properties; skipping seed.")
