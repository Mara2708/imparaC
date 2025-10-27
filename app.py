from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "supersegreto"  # Necessario per la sessione

# --- Connessione a MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["imparaC_db"]
utenti = db["utenti"]
risultati = db["risultati"]

# -------------------------------------------
# HOME
# -------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")

# -------------------------------------------
# TEORIA
# -------------------------------------------
@app.route("/teoria")
def teoria():
    return render_template("teoria.html")

# -------------------------------------------
# PROFILO
# -------------------------------------------
@app.route("/profilo", methods=["GET", "POST"])
def profilo():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        corso = request.form["corso"].strip()

        if not nome:
            return render_template("profilo.html", errore="⚠️ Inserisci il tuo nome prima di salvare.")

        utente = {"nome": nome, "corso": corso}
        session["utente"] = utente
        utenti.update_one({"nome": nome}, {"$set": utente}, upsert=True)

        return render_template("profilo.html", utente=utente, messaggio="✅ Profilo salvato correttamente!")
    else:
        utente = session.get("utente")
        return render_template("profilo.html", utente=utente)

# -------------------------------------------
# CANCELLA PROFILO
# -------------------------------------------
@app.route("/cancella_profilo", methods=["GET", "POST"])
def cancella_profilo():
    utente = session.get("utente")
    if utente:
        utenti.delete_one({"nome": utente["nome"]})
        session.pop("utente", None)
    return redirect(url_for("profilo"))

# -------------------------------------------
# LIVELLI
# -------------------------------------------
@app.route("/livelli")
def livelli():
    utente = session.get("utente")
    if not utente:
        return render_template("livelli.html", livelli_sbloccati={}, session=session)

    record = risultati.find_one({"nome": utente["nome"]})
    if not record:
        livelli_sbloccati = {"intermedio": False, "avanzato": False}
    else:
        punti = record.get("punteggio", 0)
        livelli_sbloccati = {
            "intermedio": punti >= 20,
            "avanzato": punti >= 50
        }

    return render_template("livelli.html", livelli_sbloccati=livelli_sbloccati, session=session)

# -------------------------------------------
# QUIZ
# -------------------------------------------
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    quiz_db = {
        "principiante": [
            {"id": 1, "tipo": "mcq", "testo": "Quale funzione stampa testo in C?", "opzioni": ["echo", "printf", "cout"], "risposta": 1},
            {"id": 2, "tipo": "testo", "testo": "Come si chiama la funzione principale in un programma C?", "risposta": "main"},
            {"id": 3, "tipo": "mcq", "testo": "Quale simbolo si usa per terminare un’istruzione in C?", "opzioni": [".", ";", ":"], "risposta": 1},
            {"id": 4, "tipo": "mcq", "testo": "Quale parola chiave serve per dichiarare una variabile intera?", "opzioni": ["int", "integer", "num"], "risposta": 0}
        ],
        "intermedio": [
            {"id": 5, "tipo": "mcq", "testo": "Quale ciclo è usato per iterazioni note?", "opzioni": ["while", "for", "if"], "risposta": 1},
            {"id": 6, "tipo": "mcq", "testo": "Quale istruzione serve per uscire da un ciclo?", "opzioni": ["continue", "exit", "break"], "risposta": 2},
            {"id": 7, "tipo": "testo", "testo": "Quale funzione si usa per leggere un input da tastiera in C?", "risposta": "scanf"},
            {"id": 8, "tipo": "mcq", "testo": "Quale tipo di dato rappresenta un singolo carattere?", "opzioni": ["char", "string", "byte"], "risposta": 0}
        ],
        "avanzato": [
            {"id": 9, "tipo": "mcq", "testo": "Come si libera la memoria allocata dinamicamente in C?", "opzioni": ["delete()", "free()", "dispose()"], "risposta": 1},
            {"id": 10, "tipo": "mcq", "testo": "Quale libreria serve per l’allocazione dinamica?", "opzioni": ["<math.h>", "<stdlib.h>", "<stdio.h>"], "risposta": 1},
            {"id": 11, "tipo": "testo", "testo": "Quale operatore serve per accedere a un elemento di un array?", "risposta": "[]"},
            {"id": 12, "tipo": "mcq", "testo": "Cosa restituisce malloc() se l’allocazione fallisce?", "opzioni": ["0", "NULL", "-1"], "risposta": 1},
            {"id": 13, "tipo": "mcq", "testo": "Quale parola chiave serve per definire una funzione che non restituisce nulla?", "opzioni": ["none", "null", "void"], "risposta": 2}
        ]
    }

# ---Quando l’utente seleziona un livello

    if request.method == "POST":
        livello = request.form.get("livello")
        session["livello"] = livello
        session["indice"] = 0  # inizia dalla prima domanda

    livello = session.get("livello")
    indice = session.get("indice", 0)

    if not livello:
        return redirect(url_for("livelli"))

    domande = quiz_db[livello]
    if indice >= len(domande):
        return redirect(url_for("risultati_finali"))

    domanda = domande[indice]
    numero_domanda = indice + 1
    totale_domande = len(domande)

    return render_template(
        "quiz.html",
        livello_nome=livello,
        domanda=domanda,
        numero_domanda=numero_domanda,
        totale_domande=totale_domande
    )



# -------------------------------------------
# RISPOSTA QUIZ
# -------------------------------------------
@app.route("/rispondi", methods=["POST"])
def rispondi():
    livello = session.get("livello")
    indice = session.get("indice", 0)
    if not livello:
        return redirect(url_for("livelli"))

    risposta = request.form.get("risposta")
 
    quiz_db = {
        "principiante": [
            {"id": 1, "tipo": "mcq", "testo": "Quale funzione stampa testo in C?", "opzioni": ["echo", "printf", "cout"], "risposta": 1},
            {"id": 2, "tipo": "testo", "testo": "Come si chiama la funzione principale in un programma C?", "risposta": "main"},
            {"id": 3, "tipo": "mcq", "testo": "Quale simbolo si usa per terminare un’istruzione in C?", "opzioni": [".", ";", ":"], "risposta": 1},
            {"id": 4, "tipo": "mcq", "testo": "Quale parola chiave serve per dichiarare una variabile intera?", "opzioni": ["int", "integer", "num"], "risposta": 0}
        ],
        "intermedio": [
            {"id": 5, "tipo": "mcq", "testo": "Quale ciclo è usato per iterazioni note?", "opzioni": ["while", "for", "if"], "risposta": 1},
            {"id": 6, "tipo": "mcq", "testo": "Quale istruzione serve per uscire da un ciclo?", "opzioni": ["continue", "exit", "break"], "risposta": 2},
            {"id": 7, "tipo": "testo", "testo": "Quale funzione si usa per leggere un input da tastiera in C?", "risposta": "scanf"},
            {"id": 8, "tipo": "mcq", "testo": "Quale tipo di dato rappresenta un singolo carattere?", "opzioni": ["char", "string", "byte"], "risposta": 0}
        ],
        "avanzato": [
            {"id": 9, "tipo": "mcq", "testo": "Come si libera la memoria allocata dinamicamente in C?", "opzioni": ["delete()", "free()", "dispose()"], "risposta": 1},
            {"id": 10, "tipo": "mcq", "testo": "Quale libreria serve per l’allocazione dinamica?", "opzioni": ["<math.h>", "<stdlib.h>", "<stdio.h>"], "risposta": 1},
            {"id": 11, "tipo": "testo", "testo": "Quale operatore serve per accedere a un elemento di un array?", "risposta": "[]"},
            {"id": 12, "tipo": "mcq", "testo": "Cosa restituisce malloc() se l’allocazione fallisce?", "opzioni": ["0", "NULL", "-1"], "risposta": 1},
            {"id": 13, "tipo": "mcq", "testo": "Quale parola chiave serve per definire una funzione che non restituisce nulla?", "opzioni": ["none", "null", "void"], "risposta": 2}
        ]
    }


    domande = quiz_db[livello]
    domanda = domande[indice]

# --- Controllo risposta ---
    if domanda["tipo"] == "mcq":
        corretto = int(risposta) == domanda["risposta"]
    else:
        corretto = risposta.strip().lower() == domanda["risposta"]

    punteggio = 10 if corretto else 0

# --- Aggiorna punteggio nel database ---
    utente = session.get("utente")
    if utente:
        update_data = {"$inc": {"punteggio": punteggio}}
        if not corretto: 
           update_data["$inc"]["errori"] = 1  # conteggio errori
        risultati.update_one({"nome": utente["nome"]}, update_data, upsert=True)
        
    session["indice"] = indice + 1
    if session["indice"] >= len(domande):
        return redirect(url_for("risultati_finali"))

#--- Mostra domanda successiva
    prossima = domande[session["indice"]]
    numero_domanda = session["indice"] + 1
    totale_domande = len(domande)
    messaggio = "✅ Corretto! +10 punti 🎉" if corretto else "❌ Sbagliato 😢"

    return render_template(
        "quiz.html",
        livello_nome=livello,
        domanda=prossima,
        numero_domanda=numero_domanda,
        totale_domande=totale_domande,
        messaggio=messaggio
    )

   
# -------------------------------------------
# RISULTATI FINALI
# -------------------------------------------
@app.route("/risultati")
def risultati_finali():
    utente = session.get("utente")
    if not utente:
        return redirect(url_for("profilo"))

    record = risultati.find_one({"nome": utente["nome"]})
    punteggio = record.get("punteggio", 0) if record else 0
    errori = record.get("errori", 0) if record else 0

    if punteggio < 20:
        livello_nome = "Principiante"
    elif punteggio < 50:
        livello_nome = "Intermedio"
    else:
        livello_nome = "Avanzato"

    progresso = min(int((punteggio / 100) * 100), 100)

    return render_template(
        "risultati.html",
        nome=utente["nome"],
        corso=utente.get("corso", ""),
        punteggio=punteggio,
        livello_nome=livello_nome,
        progresso=progresso,
        errori=errori
    )

# -------------------------------------------
# ESPORTAZIONE DATI (CSV)
# -------------------------------------------
from flask import Response

@app.route("/esporta_dati")
def esporta_dati():
    utenti_data = list(utenti.find({}, {"_id": 0}))
    
    # se non hai la collection 'risultati', salta questa parte in sicurezza
    try:
        risultati_data = list(risultati.find({}, {"_id": 0}))
    except:
        risultati_data = []

    output = "nome,corso,punteggio,errori\n"
    for utente in utenti_data:
        nome = utente.get("nome", "")
        corso = utente.get("corso", "")
        # cerca il punteggio corrispondente, se esiste
        record = next((r for r in risultati_data if r.get("nome") == nome), {})
        punteggio = record.get("punteggio", 0)
        errori = record.get("errori", 0)
        output += f"{nome},{corso},{punteggio},{errori}\n"

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=risultati_imparaC.csv"}
    )

# -------------------------------------------
# AVVIO
# -------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
