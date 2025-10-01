from App.database import db
from .Application import Application
from App.models.Associations import staff_student
from App.models.Associations import shortlist_table


class Student(db.Model):
    __tablename__ = "student"
    studentID = db.Column(db.Integer, primary_key=True)
    studentName =  db.Column(db.String(20), nullable=False, unique=True)
    degree = db.Column(db.String(20), nullable=False)
    gpa = db.Column(db.Integer, nullable=False)
    applications = db.relationship("Application", backref="student", lazy=True)

    staffs = db.relationship("Staff", secondary=staff_student, back_populates="students")
    applications = db.relationship("Application", back_populates="student", foreign_keys=[Application.studentID])
    shortlisted_positions = db.relationship(
        "Position",
        secondary=shortlist_table,
        back_populates="shortlist"
    )

    def __init__(self, studentID, gpa, studentName, degree):
        self.studentID = studentID
        self.gpa = gpa
        self.studentName = studentName
        self.degree = degree

    def view_all_applications(self):
        return self.applications

