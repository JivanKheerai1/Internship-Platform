from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

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

#association tables
staff_student = db.Table(
    'staff_student',
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.staffID'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.studentID'), primary_key=True)
)

shortlist_table = db.Table(
    "shortlist",
    db.Column("position_id", db.Integer, db.ForeignKey("position.positionID"), primary_key=True),
    db.Column("student_id", db.Integer, db.ForeignKey("student.studentID"), primary_key=True)
)


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

