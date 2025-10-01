from App.database import db

#bridge table
class Application(db.Model):
    __tablename__ = "application"
    applicationID = db.Column(db.Integer, primary_key=True)
    positionID = db.Column(db.Integer, db.ForeignKey("position.positionID"))
    positionName = db.Column(db.String(20), db.ForeignKey("position.positionName"))
    studentID = db.Column(db.Integer, db.ForeignKey("student.studentID"))
    status = db.Column(db.Boolean, nullable=False)
    student = db.relationship("Student", back_populates="applications", foreign_keys=[studentID])
    position = db.relationship("Position", back_populates="applications", foreign_keys=[positionID])