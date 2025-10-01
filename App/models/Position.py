from App.database import db
from .Application import Application
from App.models.Associations import shortlist_table



#created by employer
class Position(db.Model):
    __tablename__ = "position"
    positionID = db.Column(db.Integer, primary_key=True)
    positionName =  db.Column(db.String(20), nullable=False)
    employerID = db.Column(db.Integer, db.ForeignKey("employer.employerID"))
    shortlist = db.relationship(
        "Student",
        secondary=shortlist_table,
        back_populates="shortlisted_positions"
    )
    applications = db.relationship("Application", back_populates="position", foreign_keys=[Application.positionID])
    staffID = db.Column(db.Integer, db.ForeignKey("staff.staffID"), nullable=False)