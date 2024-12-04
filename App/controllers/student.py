from App.models import Student
from App.observer.events import Event
from App.database import db

def create_student(UniId, firstname, lastname, email, faculty, admittedTerm, degree, gpa=0.0):
  newStudent = Student(UniId, firstname, lastname, email, faculty, admittedTerm, degree, gpa)
  db.session.add(newStudent)

  try:
    db.session.commit()
    from .karma import create_karma
    create_karma(newStudent.ID)
    return True
  except Exception as e:
    print(
        "[student.create_student] Error occurred while creating new student: ",
        str(e))
    db.session.rollback()
    return False


def create_student_from_transcript(transcript_data, student_data):
  from App.observer.initialize import subject
  try:
    UniId = transcript_data.get('id')
    gpa = transcript_data.get('gpa')
    faculty = transcript_data.get('faculty')
    admittedTerm = transcript_data.get('admittedTerm')

    #updating student
    student = get_student_by_id(student_data.ID)
    if not student:
      print(f"Student with ID {student.ID} already exists in database from controller!")
      return False
    else:
      update_from_transcript(student_data.ID, admittedTerm, UniId, gpa, faculty)
      print(f"Added row: UniId: {UniId}, GPA: {gpa}, Faculty: {faculty}, Admitted Term: {admittedTerm}")
      print("Student data stored in database from controller!")
      event = Event(name="new_academic", student_id=student.ID) # Send event to observer
      subject.notify(event)
      return True
  except Exception as e:
    print("[transcript.create_transcript] Error occurred while creating new Student: ", str(e))
    db.session.rollback()
    return False

def get_all_students():
  return Student.query.all()

def get_student_by_id(id):
  return Student.query.get(id)


def get_student_by_UniId(UniId):
  return Student.query.filter_by(UniId=UniId).first()

def get_students_by_faculty(faculty):
  return Student.query.filter_by(faculty=faculty).all()

def get_student_for_ir(firstname, lastname, UniId):
  student = Student.query.filter_by(firstname=firstname, lastname=lastname, UniId=UniId).first()
  if student:
    return student
  else:
    return []


def get_student_by_name(firstname, lastname):
  return Student.query.filter_by(firstname=firstname,  lastname=lastname).all()

def get_full_name_by_student_id(student_id):
  student = Student.query.filter_by(UniId=student_id).first()
  if student:
    return f"{student.firstname} {student.lastname}"
  return None


def get_students_by_degree(degree):
  students = Student.query.filter_by(degree=degree).all()
  if students:
    return students
  else:
    return []


def get_students_by_ids(student_ids):
  students = Student.query.filter(Student.ID.in_(student_ids)).all()
  return students

def get_all_students_json():
  students = Student.query.all()
  if not students:
    return []

  students_json = []
  for student in students:
    student_data = {
        'id': student.ID,
        'UniId': student.UniId,
        'firstname': student.firstname,
        'lastname': student.lastname,
        'email': student.email,
        'faculty': student.faculty, 
        'degree': student.degree,
        'admittedTerm': student.admittedTerm,
        'gpa': student.gpa,
    }
    students_json.append(student_data)

  return students_json

def update_from_transcript(ID, newAdmittedTerm, newUniId, newGpa, newFaculty):
  student = get_student_by_id(ID)
  if student:
    student.admittedTerm = newAdmittedTerm
    student.UniId = newUniId
    student.gpa = newGpa
    student.faculty = newFaculty
    #student.fullname = newFullname
    try:
      db.session.commit()
      return True
    except Exception as e:
      print(
          "[student.update_from_transcript] Error occurred while updating student admittedTerm, No student with ID:",
          ID, "was found!", str(e))
      db.session.rollback()
      return False