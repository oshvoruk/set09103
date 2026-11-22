from dataclasses import asdict, dataclass

from flask import Blueprint, jsonify

from app.db import get_db

sites_bp = Blueprint("sites", __name__, url_prefix="/api/sites")


@dataclass(frozen=True, slots=True)
class Site:
    id: int
    name: str
    latitude: float
    longitude: float
    watercourse: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=int(row["id"]),
            name=str(row["name"]),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            watercourse=str(row["watercourse"]),
        )


@sites_bp.get("/")
def sites():
    rows = (
        get_db()
        .execute("""
            SELECT
                site.id,
                site.name,
                site.latitude,
                site.longitude,
                watercourse.name AS watercourse
            FROM site
            JOIN watercourse
                ON site.watercourse_id = watercourse.id
            ORDER BY watercourse.name, site.name
        """)
        .fetchall()
    )
    return jsonify([asdict(Site.from_row(row)) for row in rows])
