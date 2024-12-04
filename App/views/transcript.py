from flask import Blueprint, redirect, render_template, request, url_for, jsonify, session
#from App.controllers.transcript import *
import os
from flask_login import login_required, login_user, current_user, logout_user
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import requests

from App.controllers.transcript import create_transcript
from App.controllers.student import *

transcript_views = Blueprint('transcript_views', __name__)

@transcript_views.route('/checkPDF/<string:uniID>')
def checkPDF(uniID):
  message = session.get('message')
  return render_template('landingpage.html', message=message)

@transcript_views.route('/upload-transcript/<string:uniID>', methods=['GET'])
@login_required
def student_profile(uniID):
  student = Student.query.filter_by(UniId=uniID).first()
  return render_template('uploadtranscript.html',student=student)

@login_required
@transcript_views.route('/upload_transcript/<string:uniID>', methods=['POST'])
def upload_transcript(uniID):
  student = Student.query.filter_by(UniId=uniID).first()
  if student is None:
    return jsonify({'error': 'Invalid Student ID'})

  if 'file' not in request.files:
    return jsonify({'error': 'No file part'})

  file = request.files['file']
  if file.filename == '':
    return jsonify({'error': 'No selected file'})

  if file and file.filename.endswith('.pdf'):
    filename = secure_filename(file.filename)
    file_path = os.path.join(
        'App', 'Transcript', filename
    )  # Assuming 'App/Transcript' is the path to save transcript files
    file.save(file_path)

    try:
      print('trying_to_parse_transcript')
      transcript_data = parse_transcript(file_path)

      if transcript_data and transcript_data.get('id') == student.UniId:
        success = create_transcript(transcript_data)
        if success:
          print("transcript data stored in database from view!")
          successStudent = create_student_from_transcript(transcript_data, student)
          if successStudent:
            os.remove(file_path)
            print("Student data stored in database Correctly!")
            session['message'] = f"Transcript: '{filename}' uploaded successfully !!"
            return f"Transcript: '{filename}' uploaded successfully !!"
          else:
            os.remove(file_path)
            print("failed to store student data in database from view!")
            session['message'] = f"Transcript: '{filename}' upload failed !!"
            return f"Transcript: '{filename}' upload failed !!"
        else:
          os.remove(file_path)
          print("failed to store transcript data in database from view!")
          session['message'] = f"Transcript: '{filename}' upload failed !!"
          return f"Transcript: '{filename}' upload failed !!"
      else:
        os.remove(file_path)
        print("student uniid invalid or transcript parsing failed from view!")
        print("student uniid: ", student.UniId, "transcript id: ", transcript_data.get('id'))
        session['message'] = f"Transcript: '{filename}' upload failed !!"
        return f"Transcript: '{filename}' upload failed !!"
    except Exception as e:
      os.remove(file_path)
      print("failed to create transcript from view")
      print(str(e))
      session['message'] = f"Transcript: '{filename}' upload failed !!"
      return f"Transcript: '{filename}' upload failed !!"
  else:
    print("invalid file format!")
    session['message'] = "Transcript upload failed. Invalid format !!"
    return f"Transcript upload failed !!"


# Function to parse transcript using external service
def parse_transcript(file_path):
  # API endpoint for transcript parser service
  parser_url = 'https://parser-service.onrender.com/parse'

  # Prepare file for uploading
  files = {'file': open(file_path, 'rb')}

  # Make POST request to transcript parser service
  response = requests.post(parser_url, files=files)

  # Check if request was successful and return parsed data
  if response.status_code == 200:
    parsed_data = response.json(
    )  # Assuming response contains parsed transcript data
    #print("parsed transcript data from API: ")
    #print(parsed_data)
    return parsed_data
  else:
    return None
