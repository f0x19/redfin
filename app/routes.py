from __future__ import annotations
from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import or_, and_, desc
from . import db
from .models import Property

bp = Blueprint("main", __name__)


@bp.get("/")
def home():
    return render_template("home.html")


@bp.get("/listings")
def listings_page():
    return render_template("listings.html")


@bp.get("/property/<int:property_id>")
def property_detail_page(property_id: int):
    return render_template("property_detail.html", property_id=property_id)


@bp.get("/api/properties")
def api_properties_list():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 12))

    q = Property.query

    # Filters
    city = request.args.get("city")
    state = request.args.get("state")
    min_price = request.args.get("min_price", type=int)
    max_price = request.args.get("max_price", type=int)
    min_beds = request.args.get("min_beds", type=int)
    min_baths = request.args.get("min_baths", type=float)
    property_type = request.args.get("property_type")
    search = request.args.get("q")

    if city:
        q = q.filter(Property.city.ilike(f"%{city}%"))
    if state:
        q = q.filter(Property.state.ilike(f"%{state}%"))
    if min_price is not None:
        q = q.filter(Property.price >= min_price)
    if max_price is not None:
        q = q.filter(Property.price <= max_price)
    if min_beds is not None:
        q = q.filter(Property.beds >= min_beds)
    if min_baths is not None:
        q = q.filter(Property.baths >= min_baths)
    if property_type:
        q = q.filter(Property.property_type == property_type)
    if search:
        q = q.filter(
            or_(
                Property.title.ilike(f"%{search}%"),
                Property.description.ilike(f"%{search}%"),
                Property.address.ilike(f"%{search}%"),
                Property.city.ilike(f"%{search}%"),
                Property.state.ilike(f"%{search}%"),
                Property.zip_code.ilike(f"%{search}%"),
            )
        )

    # Sorting: newest first default
    sort = request.args.get("sort", "new")
    if sort == "price_asc":
        q = q.order_by(Property.price.asc())
    elif sort == "price_desc":
        q = q.order_by(Property.price.desc())
    else:
        q = q.order_by(Property.created_at.desc())

    pagination = db.paginate(q, page=page, per_page=per_page, error_out=False)

    return jsonify(
        {
            "items": [p.to_dict() for p in pagination.items],
            "page": pagination.page,
            "pages": pagination.pages,
            "total": pagination.total,
            "per_page": pagination.per_page,
        }
    )


@bp.get("/api/properties/<int:property_id>")
def api_property_detail(property_id: int):
    prop = Property.query.get_or_404(property_id)
    return jsonify(prop.to_dict())
