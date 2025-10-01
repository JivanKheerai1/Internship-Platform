from App.database import db
from .Position import Position


class Employer(db.Model):
    __tablename__ = "employer"
    employerID = db.Column(db.Integer, primary_key=True)
    employerName =  db.Column(db.String(20), nullable=False, unique=True)
    companyName =  db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, employerID, employerName, companyName):
        self.employerID = employerID
        self.employerName = employerName
        self.companyName = companyName

    def create_position(self, positionName, staffID):
        new_position = Position(
            positionName = positionName,
            employerID = self.employerID,
            staffID = staffID
        )
        db.session.add(new_position)
        db.session.commit()
        return new_position

    def updateStatus(self, student, application):
        application.status = student.gpa > 2
        db.session.commit()
        return application.status        

