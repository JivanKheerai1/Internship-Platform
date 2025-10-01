from .user import create_user
from App.database import db
from App.models.Employer import Employer
from App.models.Staff import Staff
from App.models.Student import Student



def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')

    employer1 = Employer(employerName='Jack', employerID=1001, companyName ='State Enterprise')
    employer2 = Employer(employerName='Luna', employerID=1002, companyName = 'Global Market')

    staff1 = Staff(staffName='Richie', staffID=1001)
    staff2 = Staff(staffName='Angel', staffID=1002)

    student1 = Student(studentName='Poppy', studentID=1001, gpa=3, degree='BSc Computer Science')
    student2 = Student(studentName='Daisy', studentID=1002, gpa=1, degree='BSc Engineering')


    db.session.add(employer1)
    db.session.add(employer2)
    db.session.add(staff1)
    db.session.add(staff2)
    db.session.add(student1)
    db.session.add(student2)
    db.session.commit()
