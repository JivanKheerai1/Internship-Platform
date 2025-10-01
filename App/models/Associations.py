from App.database import db

shortlist_table = db.Table(
    "shortlist",
    db.Column("position_id", db.Integer, db.ForeignKey("position.positionID"), primary_key=True),
    db.Column("student_id", db.Integer, db.ForeignKey("student.studentID"), primary_key=True)
)

#association tables
staff_student = db.Table(
    'staff_student',
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.staffID'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.studentID'), primary_key=True)
)