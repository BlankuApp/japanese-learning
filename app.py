import os
import sys
import csv
import flask as fl
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
  return line.split(",")

N3_KANJI_COUNT = count_lines_in_csv('static/N3Kanjies.csv')

app = fl.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    number = int(fl.request.cookies.get('number', 1))
    order = fl.request.cookies.get('order', 'inorder')
    from_number = int(fl.request.cookies.get('from-number', 1))
    to_number = int(fl.request.cookies.get('to-number', N3_KANJI_COUNT))
    kanji, hiragana, definition, jlpt = get_line_content('static/N3Kanjies.csv', number)
    question = definition + "\n" + hiragana + "\n" + jlpt
    resp = fl.make_response(fl.render_template('hello.html', question=question, answer=kanji, totalnumber=str(N3_KANJI_COUNT), number=number, order=order, from_number=from_number, to_number=to_number))
    return resp

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    radio = fl.request.form.get("radio")
    from_number = int(fl.request.form.get("from-number"))
    to_number = int(fl.request.form.get("to-number"))
    if radio == "inorder":
      number = int(fl.request.form.get("number")) +1
    else:
      number = random.randint(from_number, to_number)
    kanji, hiragana, definition, jlpt = get_line_content('static/N3Kanjies.csv', number)
    question = definition + "\n" + hiragana + "\n" + jlpt

    resp = fl.jsonify({"question": f"{question.strip()}", "answer": f"{kanji}", "number": f"{number}", "totalnumber": str(N3_KANJI_COUNT)})
    resp.set_cookie('number', str(number))
    resp.set_cookie('order', radio)
    resp.set_cookie('from-number', str(from_number))
    resp.set_cookie('to-number', str(to_number))
    return resp

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)), debug=True)
