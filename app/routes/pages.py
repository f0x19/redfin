from __future__ import annotations

from flask import Blueprint, render_template, request

from ..extensions import db
from ..models import Property

pages_bp = Blueprint("pages", __name__)


@pages_bp.get("/")
def home():
    """Server-rendered home page with search UI."""
    # Initial load shows recent properties
    per_page = int(request.args.get("per_page") or 12)
    page = int(request.args.get("page") or 1)

    query = Property.query.order_by(Property.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "home.html",
        properties=pagination.items,
        pagination=pagination,
        search_params={},
    )


@pages_bp.get("/properties/<int:property_id>")
def property_detail(property_id: int):
    prop = Property.query.get_or_404(property_id)
    return render_template("detail.html", property=prop)
