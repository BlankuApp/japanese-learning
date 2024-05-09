import os
import sys
import csv
from flask import Flask, request, render_template, jsonify, session, redirect, url_for, make_response
import random

def count_lines_in_csv(filename):
  with open(filename, 'r') as csv_file:
    reader = csv.reader(csv_file)
    num_lines = 0
    for row in reader:
      num_lines += 1
  return num_lines

def get_line_content(filename, line_number):
  with open(filename, 'r') as csv_file:
    for _ in range(line_number-1):
      csv_file.readline()
    line = csv_file.readline()
  return line.split("|")

N3_KANJI_COUNT = count_lines_in_csv('static/N3Kanjies.csv')
N3_VOCAB_COUNT = count_lines_in_csv('static/N3Vocabs.csv')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRETKEY')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    if request.form['username'] == username and request.form['password'] == password:
      session['logged_in'] = True
      return redirect(url_for('admin'))
    else:
      return "Invalid credentials!"
  return render_template('login.html')

@app.route('/admin')
def admin():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  with open('static/N3Kanjies.csv', 'r') as file:
    n3kanjies = file.read()
  with open('static/N3Vocabs.csv', 'r') as file:
    n3vocabs = file.read()
  return make_response(render_template('admin.html', n3kanjies=n3kanjies, n3vocabs=n3vocabs))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route('/n3kanjies', methods=['GET'])
def n3kanjies():
    number = int(request.cookies.get('n3kanjies-number', 1))
    order = request.cookies.get('n3kanjies-order', 'inorder')
    from_number = int(request.cookies.get('n3kanjies-from-number', 1))
    to_number = int(request.cookies.get('n3kanjies-to-number', N3_KANJI_COUNT))
    _, kanji, hiragana, definition, jlpt = get_line_content('static/N3Kanjies.csv', number)
    resp = make_response(render_template('n3kanjies.html', definition=definition, hiragana=hiragana, jlpt=jlpt, kanji=kanji, totalnumber=str(N3_KANJI_COUNT), number=number, order=order, from_number=from_number, to_number=to_number))
    return resp

@app.route('/submitn3kanjies', methods=['GET', 'POST'])
def submitN3Kanjies():
  content = request.form['n3kanjies']
  with open('static/N3Kanjies.csv', 'w') as csv_file:
    index = 1
    for line in content.split('\n'):
      if not "," in line:
        continue
      res = line[line.index(',') + 1:].strip()
      csv_file.write(str(index) + ',' + res + '\n')
      index += 1
  global N3_KANJI_COUNT
  N3_KANJI_COUNT = count_lines_in_csv('static/N3Kanjies.csv')
  return redirect(url_for('admin'))


@app.route('/nextn3kanji', methods=['GET', 'POST'])
def nextn3kanji():
    radio = request.form.get("radio")
    from_number = int(request.form.get("from-number"))
    to_number = int(request.form.get("to-number"))
    if radio == "inorder":
      number = int(request.form.get("number")) +1
    else:
      number = random.randint(from_number, to_number)
    _, kanji, hiragana, definition, jlpt = get_line_content('static/N3Kanjies.csv', number)

    resp = jsonify({"kanji": f"{kanji}", "definition": f"{definition}", "hiragana": f"{hiragana}", "jlpt": f"{jlpt}", "number": f"{number}", "totalnumber": str(N3_KANJI_COUNT)})
    resp.set_cookie('n3kanjies-number', str(number))
    resp.set_cookie('n3kanjies-order', radio)
    resp.set_cookie('n3kanjies-from-number', str(from_number))
    resp.set_cookie('n3kanjies-to-number', str(to_number))
    return resp
  
@app.route('/n3vocabs', methods=['GET'])
def n3vocabs():
  number = int(request.cookies.get('n3vocab-number', 1))
  order = request.cookies.get('n3vocab-order', 'inorder')
  from_number = int(request.cookies.get('from-number', 1))
  to_number = int(request.cookies.get('to-number', N3_VOCAB_COUNT))
  _, kanji, hiragana, definition = get_line_content('static/N3Vocabs.csv', number)
  resp = make_response(render_template('n3vocabs.html', definition=definition, hiragana=hiragana, kanji=kanji, totalnumber=str(N3_VOCAB_COUNT), number=number, order=order, from_number=from_number, to_number=to_number))
  return resp

@app.route('/submitn3vocabs', methods=['GET', 'POST'])
def submitn3vocabs():
  content = request.form['n3vocabs']
  with open('static/N3Vocabs.csv', 'w') as file:
    index = 1
    for line in content.split('\n'):
      if not "|" in line:
        continue
      res = line[line.index('|') + 1:].strip()
      file.write(str(index) + '|' + res + '\n')
      index += 1
  global N3_VOCAB_COUNT
  N3_VOCAB_COUNT = count_lines_in_csv('static/N3Vocabs.csv')
  return redirect(url_for('admin'))

@app.route('/nextn3vocab', methods=['GET', 'POST'])
def nextn3vocab():
  radio = request.form.get("radio")
  from_number = int(request.form.get("from-number"))
  to_number = int(request.form.get("to-number"))
  if radio == "inorder":
    number = int(request.form.get("number")) +1
  else:
    number = random.randint(from_number, to_number)
  _, kanji, hiragana, definition = get_line_content('static/N3Vocabs.csv', number)

  resp = jsonify({"kanji": f"{kanji}", "definition": f"{definition}", "hiragana": f"{hiragana}", "number": f"{number}", "totalnumber": str(N3_VOCAB_COUNT)})
  resp.set_cookie('n3vocab-number', str(number))
  resp.set_cookie('n3vocab-order', radio)
  resp.set_cookie('n3vocab-from-number', str(from_number))
  resp.set_cookie('n3vocab-to-number', str(to_number))
  return resp

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)), debug=True)
