from flask import Flask, render_template, request
import random
import decimal

app = Flask(__name__)

op_setting = tal1 = tal2 = 0
operator = [" + ", " - ", " * ", " / "]
resultat = ""


def num_gen1():
    return random.randrange(-9, 9)


def num_gen2():
    return random.randrange(-99, 99)


def num_gen3():
    return random.randrange(-999, 999)


def gen_pu():
    global op_setting, tal1, tal2
    op_setting = 0
    tal1 = num_gen3()
    tal2 = num_gen3()


def gen_mi():
    global op_setting, tal1, tal2
    op_setting = 1
    tal1 = num_gen3()
    tal2 = num_gen3()


def gen_mu():
    global op_setting, tal1, tal2
    op_setting = 2
    tal1 = num_gen3()
    tal2 = num_gen2()


def gen_di():
    global op_setting, tal1, tal2
    op_setting = 3
    tal1 = num_gen3()
    tal2 = num_gen2()
    if tal2 == 0:
        tal2 += 1


def generate():
    if op_setting == 0:
        gen_pu()
    elif op_setting == 1:
        gen_mi()
    elif op_setting == 2:
        gen_mu()
    elif op_setting == 3:
        gen_di()


def comma_dot(x):
    swap = x.maketrans(",", ".")
    return x.translate(swap)


def dot_comma(x):
    swap = x.maketrans(".", ",")
    return x.translate(swap)


@app.route("/", methods=["GET", "POST"])
def home():
    global resultat
    resultat = ""
    # generer nyt regnestykke ved skift af operator
    if request.method == "POST":
        if request.form.get("pl") == "Plus":
            gen_pu()
        elif request.form.get("mi") == "Minus":
            gen_mi()
        elif request.form.get("mu") == "Multiplikation":
            gen_mu()
        elif request.form.get("di") == "Division":
            gen_di()
        # læs svar og tjek imod facit
        elif request.form.get("sv_btn") == "Svar":
            svar = request.form["sv"]
            if svar == "":
                svar = 0.0
            # tjek om svar er et tal
            try:
                svar = round(float(comma_dot(str(svar))), 1)
            except ValueError:
                resultat = "Svaret skal være et tal."
            else:
                regnestykke = f"tal1{operator[op_setting]}tal2"
                facit = eval(regnestykke)
                d = decimal.Decimal(facit)
                decimaler = abs(d.as_tuple().exponent)
                if svar == round(facit, 1):
                    resultat = "Rigtigt!"
                    generate()
                else:
                    # hvis tallet er blevet rundet: ≈
                    if decimaler > 1:
                        resultat = "Forkert! " + str(tal1) + operator[op_setting] + str(tal2) + " ≈ " + \
                               dot_comma(str(round(facit, 1))) + "."
                    else:
                        resultat = "Forkert! " + str(tal1) + operator[op_setting] + str(tal2) + " = " + \
                               dot_comma(str(facit)) + "."
        # giv nyt regnestykke ved tryk på "Ny"
        elif request.form.get("ny_btn") == "Ny":
            generate()
    # opdater side med nye værdier
    return render_template("MatQuiz.html", t1=tal1, op=operator[op_setting], t2=tal2, re=resultat)


# kør app
if __name__ == "__main__":
    gen_pu()
    app.run()
