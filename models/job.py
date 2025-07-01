from sqlalchemy.dialects.postgresql import UUID
import datetime
from extensions import db
import uuid

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    salary = db.Column(db.Numeric(10,2), nullable=True)
    job_type = db.Column(db.Enum('full_time', 'part_time', 'internship', 'contract', name='job_type_enum'), nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "company_id": str(self.company_id),
            "title": self.title,
            "description": self.description,
            "salary": float(self.salary) if self.salary is not None else None,
            "job_type": self.job_type,
            "posted_at": self.posted_at.isoformat()
        } 