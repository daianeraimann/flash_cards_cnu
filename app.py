from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import random
from random import shuffle

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Chave secreta para gerar sessões

acertos = 0
erros = 0

# Função para conectar ao banco de dados
def get_db():
    db = sqlite3.connect('cards.db')
    db.row_factory = sqlite3.Row
    return db

# Página inicial
@app.route('/')
def index():
    tema = request.args.get('tema')
    card = selecionar_flashcard_aleatorio([tema])
    # Verifica se o usuário está autenticado (verifica se há um ID de usuário na sessão)
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Conecta com o banco de dados
    with get_db() as conn:
        cursor = conn.cursor()
        #seleciona os temas da tabela de cards e imprime uma vez cada um, sem repetir
        cursor.execute("SELECT DISTINCT tema FROM flash_cards")
        themes = [row['tema'] for row in cursor.fetchall()]
    
    if card is None:
        # Se nenhum flashcard for retornado, você pode lidar com isso aqui
        # Por exemplo, pode definir um valor padrão para card
        card = {'id': None, 'tema': 'Nenhum tema encontrado', 'termo': 'Nenhum termo encontrado', 'definicao': 'Nenhuma definição encontrada'}
    
    return render_template('index.html', card=card, themes=themes)


@app.route('/flashcards')
def show_flashcards():
    temas_selecionados = request.args.getlist('tema')

    # Verifica se algum tema foi selecionado
    if not temas_selecionados:
        # Redireciona de volta para a página inicial ou exibe uma mensagem de erro
        return "Nenhum tema selecionado. Por favor, selecione pelo menos um tema."

    # Obtém todos os flashcards dos temas selecionados
    flashcards = []
    for tema in temas_selecionados:
        flashcards += selecionar_flashcards_por_tema(tema)

    if not flashcards:
        return "Nenhum flashcard encontrado para os temas selecionados."

    # Embaralha os flashcards para exibição aleatória
    shuffle(flashcards)

    # Retorna o primeiro flashcard para exibição
    card = flashcards.pop(0)

    return render_template('flashcards.html', flashcards=flashcards, card=card, temas_selecionados=temas_selecionados, card_id=card['id'])
    

def selecionar_flashcards_por_tema(tema):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, tema, termo, definicao FROM flash_cards WHERE tema = ?", (tema,))
        flashcards = cursor.fetchall()

    return flashcards
    
def selecionar_flashcard_aleatorio(temas):
    

    with get_db() as conn:
        cursor = conn.cursor()
        # Inicializa uma lista para armazenar os flashcards de todos os temas
        flashcards = []


        for tema in temas:
            # Constrói a consulta SQL para o tema atual
            query = "SELECT id, tema, termo, definicao FROM flash_cards WHERE tema = ? ORDER BY RANDOM() LIMIT 1"
            cursor.execute(query, (tema,))
            # Adiciona o resultado à lista de flashcards
            flashcards.extend(cursor.fetchall())

        # Verifica se algum flashcard foi encontrado
        if flashcards:
            # Seleciona um flashcard aleatório dentre todos os temas
            return random.choice(flashcards)
        else:
            # Retorna None se nenhum flashcard foi encontrado
            return None


# Rota para registrar a resposta do usuário
@app.route('/register_answer/<answer>/<card_id>', methods=['GET'])
def register_answer(answer, card_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Conecta com o banco de dados
    with get_db() as conn:
        cursor = conn.cursor()

        if answer == 'acertou':
            # Atualiza o campo 'acertou' para True
            cursor.execute("UPDATE flash_cards SET acertou = 1 WHERE id = ?", (card_id,))
        elif answer == 'errou':
            # Atualiza o campo 'acertou' para False
            cursor.execute("UPDATE flash_cards SET acertou = 0 WHERE id = ?", (card_id,))

        # Atualiza o campo 'data_hora_revisao' para a data e hora atuais
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE flash_cards SET data_hora_revisao = ? WHERE id = ?", (current_datetime, card_id))

    return redirect(url_for('show_flashcards'))

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

def zerarJogo():
    
    # Conecta-se ao banco de dados e redefine os valores de acertos e erros para zero
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE flash_cards SET acertou = NULL")
        conn.commit()

@app.route('/novo_jogo')
def novoJogo():
    zerarJogo()
    return redirect(url_for('index'))

# Rota para finalizar a sessão de revisão
@app.route('/finalizar')
def finalizar():
    # Conectar ao banco de dados para obter o número de acertos e erros
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM flash_cards WHERE acertou = 1")
        acertos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM flash_cards WHERE acertou = 0")
        erros = cursor.fetchone()[0]
    
    # Renderizar a página finalizar.html com os resultados
    return render_template('finalizar.html', acertos=acertos, erros=erros)

if __name__ == '__main__':
    app.run(debug=True)
