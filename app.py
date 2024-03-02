from flask import *
import drow_name_gen as dng

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    name = str(dng.generate_name())
    name = name.split('\n')
    return render_template("DrowNameGenerator.html", drow_string=name[0], trans_string=name[1], last_g="", last_gender='Choose Here', last_l="", last_length='Choose Here', last_o='', last_order='Choose Here', last_vowel='75', last_consonant='50')


@app.route('/gen', methods=['GET', 'POST'])
def generate():
    gender = request.form['gender']
    match gender:
        case "F":
            gender = 0
            last_g = 'F'
            last_gender = 'Feminine'
        case "M":
            gender = 1
            last_g = 'M'
            last_gender = 'Masculine'
        case "N":
            gender = 2
            last_g = 'N'
            last_gender = 'Neutral'
    length = request.form['length']
    match length:
        case "n":
            mid = False
            end = True
            last_l = 'n'
            last_length = 'Standard'
        case "l":
            mid = True
            end = True
            last_l = 'l'
            last_length = 'Longer'
        case "s":
            mid = False
            end = False
            last_l = 's'
            last_length = 'Shorter'
    order = request.form['order']
    match order:
        case "True":
            order = True
            last_o = 'True'
            last_order = 'Yes'
        case "False":
            order = False
            last_o = 'False'
            last_order = 'No'
        case "None":
            order = None
            last_o = 'None'
            last_order = 'Either'
    vowels = int(request.form['vowels'])
    consonants = int(request.form['consonants'])
    name = str(dng.generate_name(gender, mid, end, order, vowels, consonants))
    name = name.split('\n')
    return render_template("DrowNameGenerator.html", drow_string=name[0], trans_string=name[1],last_g=last_g, last_gender=last_gender, last_l=last_l, last_length=last_length, last_o=last_o, last_order=last_order, last_vowels=str(vowels), last_consonants=str(consonants))

if __name__ == '__main__':
    app.debug
    app.run()
