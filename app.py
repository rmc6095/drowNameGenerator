from flask import *
import drow_name_gen as dng

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    name = str(dng.generate_name())
    name = name.split('\n')
    return render_template("DrowNameGenerator.html", drow_string=name[0], trans_string=name[1])


@app.route('/gen', methods=['GET', 'POST'])
def generate():
    gender = request.form['gender']
    match gender:
        case "F":
            gender = 0
        case "M":
            gender = 1
        case "N":
            gender = 2
    length = request.form['length']
    match length:
        case "n":
            mid = False
            end = True
        case "l":
            mid = True
            end = True
        case "s":
            mid = False
            end = False
    order = request.form['order']
    match order:
        case "True":
            order = True
        case "False":
            order = False
        case "None":
            order = None
    vowels = int(request.form['vowels'])
    consonants = int(request.form['consonants'])
    name = str(dng.generate_name(gender, mid, end, order, vowels, consonants))
    name = name.split('\n')
    return render_template("DrowNameGenerator.html", drow_string=name[0], trans_string=name[1])


if __name__ == '__main__':
    app.debug
    app.run()
