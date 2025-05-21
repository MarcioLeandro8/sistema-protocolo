from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Criação do banco de dados
def criar_banco():
    if not os.path.exists("protocolo.db"):
        conn = sqlite3.connect("protocolo.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS protocolos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT NOT NULL,
                setor TEXT NOT NULL,
                assunto TEXT NOT NULL,
                data TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect("protocolo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM protocolos")
    protocolos = cursor.fetchall()
    conn.close()
    return render_template("index.html", protocolos=protocolos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    numero = request.form['numero']
    setor = request.form['setor']
    assunto = request.form['assunto']
    data = request.form['data']

    conn = sqlite3.connect("protocolo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO protocolos (numero, setor, assunto, data) VALUES (?, ?, ?, ?)",
                   (numero, setor, assunto, data))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    conn = sqlite3.connect("protocolo.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM protocolos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

