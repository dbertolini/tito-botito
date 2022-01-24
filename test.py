from flask import request, Response, Flask

app = Flask(__name__)
app.config["DEBUG"] = True

def mio():
    print("soy mio")

@app.route("/first")
def first_route():      # http://localhost/first
    print("Soy la primera ruta")
    #return "Soy First"
    mio()
    return Response("Soy respuesta", status=200)

@app.route("/manzana/<int:numero>")
def get_manzana(numero):
    return "Soy la manzana " + str(numero)

@app.route("/<int:pera_id>/comer")
def comer_pera(pera_id):
    return "Comiendo pera " + str(pera_id)

@app.route("/<fruta>/comer/<int:fruta_id>")
def comer_fruta(fruta, fruta_id):
    return "Comiendo " + fruta + " id " + str(fruta_id)

@app.route("/second", methods=['PUT', 'POST'])
def second_route():
    if request.method == "POST":
        print("Hizo POST")
    elif request.method == "PUT":
        print("Hizo PUT")

    print(request.remote_addr)
    return "second"

if __name__ == "__main__":
    print("Escuchando...")
    app.run('0.0.0.0')
