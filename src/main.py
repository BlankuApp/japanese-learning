import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import flask as fl
from markupsafe import Markup
from src.utilities import count_lines_in_csv, get_line_content

app = fl.Flask(__name__)

N3_KANJI_COUNT = count_lines_in_csv('src/static/N3Kanjies.csv')

@app.route('/', methods=['GET', 'POST'])
def main():
    kanji, hiragana, definition, jlpt = get_line_content('src/static/N3Kanjies.csv', 1)
    question = definition + "\n" + hiragana + "\n" + jlpt
    return fl.render_template('hello.html', question=question, answer=kanji, totalnumber=str(N3_KANJI_COUNT))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    number = int(fl.request.form.get("number")) +1
    kanji, hiragana, definition, jlpt = get_line_content('src/static/N3Kanjies.csv', number)
    question = definition + "\n" + hiragana + "\n" + jlpt
    return fl.jsonify({"question": question, "answer": f"{kanji}", "number": f"{number}", "totalnumber": str(N3_KANJI_COUNT)})

if __name__ == "__main__":
    N3_KANJI_COUNT = count_lines_in_csv('src/static/N3Kanjies.csv')
    app.run(port=int(os.environ.get('PORT', 80)), debug=True)

