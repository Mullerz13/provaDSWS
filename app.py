from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# -----------------------------
#  BANCO DE DADOS - SQLITE
# -----------------------------
DB_NAME = "alunos.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            disciplina TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

init_db()

def add_student(nome, disciplina):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO alunos (nome, disciplina) VALUES (?, ?)", (nome, disciplina))
    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT nome, disciplina FROM alunos")
    rows = cur.fetchall()
    conn.close()
    return rows

# -----------------------------
#  ROTAS
# -----------------------------

@app.route("/")
def index():
    data = datetime.now().strftime('%B %d, %Y %I:%M %p')
    return render_template("index.html", data=data)


# Rotas que devem mostrar “Não disponível”
nao_disp = ["/professores", "/disciplinas", "/cursos", "/ocorrencias"]

for r in nao_disp:
    def handler(route=r):
        return render_template("nao_disponivel.html",
                               data=datetime.now().strftime('%B %d, %Y %I:%M %p'))
    app.add_url_rule(r, view_func=handler)


@app.route("/alunos", methods=["GET", "POST"])
def alunos():
    if request.method == "POST":
        nome = request.form.get("nome")
        disciplina = request.form.get("disciplina")
        if nome and disciplina:
            add_student(nome, disciplina)
        return redirect(url_for("alunos"))

    lista = get_students()

    return render_template("alunos.html", alunos=lista)


if __name__ == "__main__":
    app.run(debug=True)
