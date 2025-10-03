from __future__ import annotations

from typing import Any, Dict, Optional

from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import and_, or_  # noqa: F401

from ..extensions import db
from ..models import Property

api_bp = Blueprint("properties", __name__)


@api_bp.get("/properties")
def list_properties():
    """List/search properties with filters and pagination.

    Query params:
    - q: free text matches title, city, state, zipcode
    - min_price, max_price
    - min_bed, max_bed
    - min_bath, max_bath
    - city, state, zipcode
    - type: property_type
    - sort: price_asc|price_desc|newest
    - page, per_page
    """
    args = request.args

    page = int(args.get("page") or 1)
    per_page = int(args.get("per_page") or current_app.config.get("PER_PAGE", 12))

    query = Property.query

    text = (args.get("q") or "").strip()
    if text:
        like = f"%{text}%"
        query = query.filter(
            or_(
                Property.title.ilike(like),
                Property.city.ilike(like),
                Property.state.ilike(like),
                Property.zipcode.ilike(like),
                Property.address_line.ilike(like),
            )
        )

    def int_arg(name: str) -> Optional[int]:
        try:
            return int(args.get(name)) if args.get(name) is not None else None
        except ValueError:
            return None

    def float_arg(name: str) -> Optional[float]:
        try:
            return float(args.get(name)) if args.get(name) is not None else None
        except ValueError:
            return None

    min_price, max_price = int_arg("min_price"), int_arg("max_price")
    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    if max_price is not None:
        query = query.filter(Property.price <= max_price)

    min_bed, max_bed = int_arg("min_bed"), int_arg("max_bed")
    if min_bed is not None:
        query = query.filter(Property.bedrooms >= min_bed)
    if max_bed is not None:
        query = query.filter(Property.bedrooms <= max_bed)

    min_bath, max_bath = float_arg("min_bath"), float_arg("max_bath")
    if min_bath is not None:
        query = query.filter(Property.bathrooms >= min_bath)
    if max_bath is not None:
        query = query.filter(Property.bathrooms <= max_bath)

    if args.get("city"):
        query = query.filter(Property.city.ilike(args.get("city")))
    if args.get("state"):
        query = query.filter(Property.state.ilike(args.get("state")))
    if args.get("zipcode"):
        query = query.filter(Property.zipcode.ilike(args.get("zipcode")))

    if args.get("type"):
        query = query.filter(Property.property_type == args.get("type"))

    sort = args.get("sort") or "newest"
    if sort == "price_asc":
        query = query.order_by(Property.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Property.price.desc())
    else:
        query = query.order_by(Property.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(
        {
            "items": [p.to_dict() for p in pagination.items],
            "page": pagination.page,
            "pages": pagination.pages,
            "total": pagination.total,
            "per_page": pagination.per_page,
        }
    )


@api_bp.get("/properties/<int:property_id>")
def get_property(property_id: int):
    prop = Property.query.get_or_404(property_id)
    return jsonify(prop.to_dict(include_images=True))
