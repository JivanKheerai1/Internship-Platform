from App.database import db
from .Application import Application
from App.models.Associations import staff_student

class Staff(db.Model):
    __tablename__ = "staff"
    staffID = db.Column(db.Integer, primary_key=True)
    staffName =  db.Column(db.String(20), nullable=False, unique=True)
    students = db.relationship("Student", backref="staff", lazy=True)
    position = db.relationship("Position", backref="staff", lazy=True)

    students = db.relationship("Student", secondary=staff_student, back_populates="staffs")
    
    def __init__(self, staffID, staffName):
        self.staffID = staffID
        self.staffName = staffName
    
    def add_student(self, position, students, status=False):
        for student in students:
            # position.shortlist.append(student)
            # Check if an application already exists for this student/position
            existing_application = Application.query.filter_by(
                studentID=student.studentID,
                positionID=position.positionID
            ).first()

            if not existing_application:
                # Create a new application record
                new_application = Application(
                    studentID=student.studentID,
                    positionID=position.positionID,
                    status=status
                )
                db.session.add(new_application)

        # Commit all new applications to the database
        db.session.commit()



