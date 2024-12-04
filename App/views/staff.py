from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, make_response
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.database import db
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime

from App.models import Student, Staff, User, IncidentReport
from App.controllers import (
    jwt_authenticate, create_incident_report, get_student_by_UniId,
    get_student_by_id, get_staff_by_id, get_students_by_faculty,
    get_staff_by_id, get_transcript, analyze_sentiment,
    get_total_As, get_student_for_ir, create_review, get_karma,)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')
'''
Page/Action Routes
'''

@staff_views.route('/StaffHome', methods=['GET'])
def get_StaffHome_page():
  staff_id = current_user.get_id()
  staff=get_staff_by_id(staff_id)
  return render_template('Staff-Home.html', staff=staff)


@staff_views.route('/staffhome', methods=['GET'])
def get_staffHome_page():
  staff_id = current_user.get_id()
  if (current_user.user_type == "admin"):
    return render_template('Admin-Home.html')
  return render_template('Staff-Home.html')


@staff_views.route('/incidentReport', methods=['GET'])
def staff_ir_page():
  return render_template('IncidentReport.html')


@staff_views.route('/get_student_name', methods=['POST'])
def get_student_name():
  student_id = request.json['studentID']
  student = get_student_by_UniId(student_id)
  fullname = None
  if student:
    fullname = student.firstname + ' ' + student.lastname

  return jsonify({'studentName': fullname})


@staff_views.route('/studentSearch', methods=['GET'])
def student_search_page():
  return render_template('StudentSearch.html')


@staff_views.route('/reviewSearch', methods=['GET'])
def review_search_page():
  return render_template('ReviewSearch.html')


@staff_views.route('/mainReviewPage', methods=['GET'])
def mainReviewPage():
  return render_template('CreateReview.html')
  
@staff_views.route('/createReview', methods=['POST'])
def createReview():
  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id)

  data = request.form
  studentID = data['studentID']
  studentName = data['name']
  course = data['course']
  points = int(data['points'])
  num = data['num']
  personalReview = data['manual-review']
  details = data['selected-details']
  student = get_student_by_UniId(studentID)

  if personalReview:
    details += f"{num}. {personalReview}"
    nltk_points = analyze_sentiment(personalReview)
    rounded_nltk_points = round(float(nltk_points))
    points += int(rounded_nltk_points)

  positive = points > 0

  if student:
    review = create_review(staff, student, course, positive, points, details)
    message = f"You have created a review on Student: {studentName}"
    return render_template('Stafflandingpage.html', message=message)
  else:
    message = f"Error creating review on Student: {studentName}"
    return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/newIncidentReport', methods=['POST'])
@login_required
def newIncidentReport():
  data = request.form
  staff_id = current_user.get_id()

  student_id = data['studentID']
  student_name = data['name']
  course = data['course']
  fullname = student_name.split(' ')
  firstname = fullname[0]
  lastname = fullname[-1]
  student = get_student_for_ir(firstname, lastname, student_id)

  topic = data['topic']
  details = data['details']
  points = data['points-dropdown']

  incidentReport = create_incident_report(student_id, staff_id, course, topic, details, points)

  if incidentReport:
    message = f"You have created an incident report on the student {student_name} with a topic of {topic} !"

    return render_template('Stafflandingpage.html', message=message)
  else:
    message = f"Error creating incident report on the student {student_name} with a topic of {topic} !"
    return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/searchStudent', methods=['GET'])
@login_required
def studentSearch():
  name = request.args.get('name')
  studentID = request.args.get('studentID')
  faculty = request.args.get('faculty')
  degree = request.args.get('degree')

  query = Student.query

  if name:
    # Check if the name contains both a first name and a last name
    name_parts = name.split()
    firstname = " ".join(name_parts[0:-1])
    if len(name_parts) > 1:
      # If it contains both first name and last name, filter by full name
      query = query.filter_by(firstname=firstname,lastname=name_parts[-1])
    else:
      # If it contains only one name, filter by either first name or last name
      query = query.filter(or_(Student.firstname.ilike(f'%{name}%'), Student.lastname.ilike(f'%{name}%')))

  if studentID:
    query = query.filter_by(UniId=studentID)

  if faculty:
    query = query.filter_by(faculty=faculty)

  if degree:
    query = query.filter_by(degree=degree)

  students = query.all()

  if students:
    return render_template('ssresult.html', students=students)
  else:
    message = "No students found"
    return render_template('StudentSearch.html', message=message)

@staff_views.route('/view-all-student-reviews/<string:uniID>', methods=['GET'])
@login_required
def view_all_student_reviews(uniID):
  student = get_student_by_UniId(uniID)
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllStudentReviews.html', student=student,user=user)


@staff_views.route('/view-all-student-incidents/<string:uniID>', methods=['GET'])
@login_required
def view_all_student_incidents(uniID):
  student = get_student_by_UniId(uniID)
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllStudentIncidents.html', student=student,user=user)


@staff_views.route('/getStudentProfile/<string:uniID>', methods=['GET'])
@login_required
def getStudentProfile(uniID):
  student = Student.query.filter_by(UniId=uniID).first()

  if student is None:
    student = Student.query.filter_by(ID=uniID).first()

  user = User.query.filter_by(ID=student.ID).first()
  karma = get_karma(student.ID)
  transcripts = get_transcript(student.UniId)
  numAs = get_total_As(student.UniId)

  if current_user.user_type == "admin":
    return render_template('Student-Profile-forAdmin.html', student=student, user=user, transcripts=transcripts, numAs=numAs, karma=karma)
  
  return render_template('Student-Profile-forStaff.html', student=student, user=user, transcripts=transcripts, numAs=numAs, karma=karma)