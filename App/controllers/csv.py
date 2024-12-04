import csv
import secrets
import string
from flask import current_app
from App.models import *
from App.controllers.student import create_student, get_student_by_UniId
from App.database import db  

def populate_db_from_csv(csv_file_path):
  try:
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        firstname = row.get('First name')
        lastname = row.get('Last name')
        UniId = row.get('ID number')
        email = row.get('Email address')
        faculty = row.get('Faculty')
        degree = row.get('Degree')
        admittedTerm = row.get('Admitted Term')

        if None in [firstname, lastname, UniId, email, faculty, email, admittedTerm]:
          print("Some values in the row are None.")
          continue

        #check if student exists in db
        student = get_student_by_UniId(UniId)
        #if not student:
        if student:
          print ('student already exist')
          return
        
        new_student = create_student(
            UniId=UniId,
            firstname=firstname,
            lastname=lastname,
            email=email,
            faculty=faculty,
            admittedTerm=admittedTerm,
            degree=degree,
            gpa=0.0,
        )

        if new_student:
          print(f"Student created: {firstname} {lastname}")
        else:
          print(f"Failed to create user: {firstname} {lastname}")
  except Exception as e:
    print(f"An error occurred while processing the CSV file: {str(e)}")
