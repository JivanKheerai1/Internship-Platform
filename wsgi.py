import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from App.database import db, get_migrate
from App.models import User, Position, Application
from App.models.Employer import Employer
from App.models.Staff import Staff
from App.models.Student import Student
from App.models.Position import Position
from App.models.Application import Application
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from flask_cors import CORS


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

@app.cli.command("create-position")
@click.argument("employerid", type=int)
@click.argument("positionname")
@click.argument("staffid", type=int)
def create_position(employerid, positionname, staffid):
    employer = Employer.query.get(employerid)
    if not employer:
        click.echo(f" Employer with ID {employerid} not found")
        return
    
    new_position = employer.create_position(positionname, staffid)
    db.session.commit()
    click.echo(f" Created position '{new_position.positionName}' by employer {employerid} for management by staff {staffid}")

@app.cli.command("add-student")
@click.argument("positionid", type=int)
@click.argument("studentid", nargs=-1, type=int)
@click.option("--status", default=False, type=bool, help="Initial status for applications")
def add_students_cli(positionid, studentid, status):
    """Add multiple students to a position and create application records."""
    position = Position.query.get(positionid)
    if not position:
        click.echo(f"Position with ID {positionid} not found.")
        return

    students = Student.query.filter(Student.studentID.in_(studentid)).all()
    if not students:
        click.echo("No valid students found with the provided IDs.")
        return

    for student in students:
        existing_application = Application.query.filter_by(
            studentID=student.studentID,
            positionID=position.positionID
        ).first()

        if not existing_application:
            new_application = Application(
                studentID=student.studentID,
                positionID=position.positionID,
                status=status
            )
            db.session.add(new_application)

    db.session.commit()
    click.echo(f"Added {len(students)} student(s) to position {position.positionName}.")

@app.cli.command("update-status")
@click.argument("studentid", type=int)
@click.argument("applicationid", type=int)
def update_status_cli(studentid, applicationid):
    """Update the status of an application based on the student's GPA."""
    student = Student.query.get(studentid)
    if not student:
        click.echo(f"Student with ID {studentid} not found.")
        return

    application = Application.query.get(applicationid)
    if not application:
        click.echo(f"Application with ID {applicationid} not found.")
        return

    # Update status
    application.status = student.gpa > 2
    db.session.commit()
    click.echo(f"Application {applicationid} status updated to {application.status}.")

@app.cli.command("view-applications")
@click.argument("studentid", type=int)
def view_applications_cli(studentid):
    """View all applications for a given employer."""
    student = Student.query.get(studentid)
    if not student:
        click.echo(f"Student with ID {studentid} not found.")
        return

    applications = student.applications 
    if not applications:
        click.echo("No applications found for this student.")
        return

    for app in applications:
        student = Student.query.get(app.studentID)
        position = Position.query.get(app.positionID)
        click.echo(f"Application ID: {app.applicationID}, Student: {student.studentName}, "
                   f"Position: {position.positionName}, Status: {app.status}")
