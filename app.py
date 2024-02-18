from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Chave secreta para gerar sessões

# Função para conectar ao banco de dados
def get_db():
    db = sqlite3.connect('cards.db')
    db.row_factory = sqlite3.Row
    return db

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Verifica se o email já existe na base de dados
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                error = 'Este email já está registrado.'
            else:
                # Insere o novo usuário na base de dados
                cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
                conn.commit()  # Confirma a transação

                # Redireciona para a página de login após o registro bem-sucedido
                return redirect(url_for('login'))
    
    return render_template('register.html', error=error)

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Verifica se o email e senha existem no banco de dados
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()
        
        if user:
            # Login bem-sucedido, armazena o ID do usuário na sessão
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            # Login falhou
            error = 'Email ou senha incorretos'
    
    return render_template('login.html', error=error)

# Página de logout
@app.route('/logout')
def logout():
    # Remove o ID do usuário da sessão (logout)
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Página inicial
@app.route('/')
def index():
    # Verifica se o usuário está autenticado (verifica se há um ID de usuário na sessão)
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Conecta com o banco de dados
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Seleciona um flashcard aleatório
        cursor.execute("SELECT tema, termo, definicao FROM flash_cards ORDER BY RANDOM() LIMIT 1")
        card = cursor.fetchone()
    
    return render_template('index.html', tema=card[0], termo=card[1], definicao=card[2])



if __name__ == '__main__':
    app.run(debug=True)
