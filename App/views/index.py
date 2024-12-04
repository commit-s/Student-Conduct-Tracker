from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db, Student, Karma
from App.controllers import (
    create_user,
    create_student,
    create_staff,
    create_admin,
    create_karma,
    get_staff_by_id,
    get_student_by_UniId,
    create_review,
)
from flask_login import login_required, login_user, current_user, logout_user

index_views = Blueprint('index_views',
                        __name__,
                        template_folder='../templates')


@index_views.route('/', methods=['GET'])
def index_page():
  return render_template('login.html')


@index_views.route('/hello')
def hello_world():
  return 'Hello, World!'


@index_views.route('/admin', methods=['GET'])
@login_required
def admin_page():
  return render_template('Admin-Home.html')


@index_views.route('/studentcsv', methods=['GET'])
def indexs_page():
  return render_template('StudentCSV.html')


@index_views.route('/staffcsv', methods=['GET'])
def csvStaffPage():
  return render_template('StaffCSV.html')


@index_views.route('/init', methods=['GET'])
def init():
  db.drop_all()
  db.create_all()

  create_student(
                UniId='816031609',
                 firstname="Brian",
                 lastname="Cheruiyot",
                 email="brian.cheruiyot@my.uwi.edu",
                 faculty="FST",
                 admittedTerm="2021/2022",
                 degree="Bachelor of Computer Science (General)",
                 gpa="")

  #Creating staff
  create_staff(
                UniId="816032312",
                firstname="Tim",
                lastname="Long",
                email="tim.long@sta.uwi.edu",
                password="timpass",
                faculty="FST")

  create_staff(
              UniId="816032313",
              firstname="Vijayanandh",
              lastname="Rajamanickam",
              email="vijayanandh.rajamanickam@sta.uwi.edu",
              password="vijaypass",
              faculty="FST")

  create_staff(
              UniId="816032314",
              firstname="Permanand",
              lastname="Mohan",
              email="permanand.mohan@sta.uwi.edu",
              password="permpass",
              faculty="FST")

  
  staff = get_staff_by_id(2)
  student1 = get_student_by_UniId(816031609)
  create_review(staff, student1, True, 5, "Behaves very well in class!")

  create_admin(
              UniId="8160332315",
              firstname="Admin",
              lastname="Main",
              email="admin@sta.uwi.com",
              password="password",
              faculty="FST")

  return jsonify(message='db initialized!')


@index_views.route('/health', methods=['GET'])
def health_check():
  return jsonify({'status': 'healthy'})


@index_views.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
  return send_from_directory('/workspaces/Info3604_Project/images', filename)
