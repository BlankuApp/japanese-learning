import os
import sys
import csv
import flask as fl

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
    kanji, hiragana, definition, jlpt = get_line_content('static/N3Kanjies.csv', 1)
    question = definition + "\n" + hiragana + "\n" + jlpt
    return fl.render_template('hello.html', question=question, answer=kanji, totalnumber=str(N3_KANJI_COUNT))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    number = int(fl.request.form.get("number")) +1
    kanji, hiragana, definition, jlpt = get_line_content('static/N3Kanjies.csv', number)
    question = definition + "\n" + hiragana + "\n" + jlpt
    return fl.jsonify({"question": question, "answer": f"{kanji}", "number": f"{number}", "totalnumber": str(N3_KANJI_COUNT)})

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)), debug=True)
