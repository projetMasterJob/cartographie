from sqlalchemy.dialects.postgresql import UUID
import datetime
from extensions import db
import uuid

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = db.Column(db.Enum('company', 'job', name='entity_type_enum'), nullable=False)
    entity_id = db.Column(UUID(as_uuid=True), nullable=False)
    latitude = db.Column(db.Numeric(9,6), nullable=False)
    longitude = db.Column(db.Numeric(9,6), nullable=False)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('entity_type', 'entity_id', name='uix_entity_type_id'),)

    def to_dict(self):
        return {
            "id": str(self.id),
            "entity_type": self.entity_type,
            "entity_id": str(self.entity_id),
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "address": self.address,
            "created_at": self.created_at.isoformat()
        } 