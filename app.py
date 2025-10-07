from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'chave_super_segura' 

# Configurações do Banco de Dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'labinfo' 
app.config['MYSQL_DB'] = 'autopercepcao_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index_page():
    """Renders the login page."""
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Handles user login without password hashing (INSECURE)."""
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha'] 

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
            usuario = cur.fetchone()
            cur.close()

            if usuario:
                session['usuario_id'] = usuario['id']
                session['nome'] = usuario['nome']
                # Remoção da limpeza de sessão obsoleta
                return redirect(url_for('quest1'))
            else:
                return "Usuário ou senha inválidos."
        except Exception as e:
            print(f"Erro durante o login: {e}")
            return "Erro ao tentar conectar com o banco de dados.", 500
            
    return render_template('login.html')

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    """Registers a new user, storing the password in plaintext (INSECURE)."""
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha'] 

    try:
        cur = mysql.connection.cursor()
        # Verificar se o e-mail já existe
        cur.execute("SELECT id FROM usuarios WHERE email = %s", [email])
        if cur.fetchone():
            cur.close()
            return "Este e-mail já está registrado. Tente fazer login.", 409
            
        cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login_page'))
    except Exception as e:
        print(f"Erro durante o registro: {e}")
        return "Erro ao registrar o usuário.", 500

@app.route('/quest1')
def quest1():
    """Renders the single questionnaire page containing all 7 questions."""
    if 'usuario_id' not in session:
        return redirect(url_for('login_page'))
    # Assumimos que 'quest1.html' é o arquivo que contém todas as 7 perguntas.
    return render_template('quest1.html')

# A rota /processar_quest1 foi removida.
# A rota /quest2 foi removida.

@app.route('/enviar_respostas', methods=['POST'])
def enviar_respostas():
    """
    Recebe as 7 respostas diretamente do formulário, calcula o score e salva no banco de dados.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login_page'))
        
    # 1. Coleta Direta das Respostas (Questionário em uma única página)
    # Todos os dados do formulário chegam aqui
    respostas = request.form.to_dict() 
    pontuacao_total = 0
    
    # Defina o número de perguntas de acordo com o seu DB (7 perguntas)
    NUM_PERGUNTAS = 7 
    MAX_SCORE_POR_PERGUNTA = 5  # Assumindo que a pontuação máxima por pergunta é 5
    MAX_SCORE = NUM_PERGUNTAS * MAX_SCORE_POR_PERGUNTA # 7 * 5 = 35

    respostas_individuais = [] 

    # 2. Lógica de Cálculo do Score (Itera de 1 a 7)
    for i in range(1, NUM_PERGUNTAS + 1): 
        key = f'pergunta{i}'
        try:
            # Pega o valor da resposta (garantindo que seja um int)
            # Se o campo não for encontrado, assume 0 (o que pode indicar que o usuário pulou uma questão)
            resposta = int(respostas.get(key, 0))
            pontuacao_total += resposta
            respostas_individuais.append(resposta)
        except ValueError:
            print(f"Valor não numérico recebido para {key}. Contando como 0.")
            respostas_individuais.append(0)
            continue 
        
        # Log para debug:
        print(f"Resposta {key}: {resposta}, Total parcial: {pontuacao_total}")

    # 3. Cálculo da Pontuação Percentual e Nível de Bem-Estar
    pontuacao_percentual = round((pontuacao_total / MAX_SCORE) * 100, 2) if MAX_SCORE > 0 else 0

    if pontuacao_percentual >= 80:
        nivel_bem_estar = "Ótimo"
    elif pontuacao_percentual >= 50:
        nivel_bem_estar = "Bom"
    else:
        nivel_bem_estar = "Atenção"
        
    print(f"Pontuação Total: {pontuacao_total}, Percentual: {pontuacao_percentual}%, Nível: {nivel_bem_estar}")

    # 4. Inserção no Banco de Dados
    try:
        cur = mysql.connection.cursor()
        
    
        valores = [usuario_id] + respostas_individuais + [pontuacao_total, pontuacao_percentual, nivel_bem_estar]

       
        sql = """
            INSERT INTO respostasquestionario (
                usuario_id, resposta_q1, resposta_q2, resposta_q3, resposta_q4, 
                resposta_q5, resposta_q6, resposta_q7, pontuacao_total, 
                pontuacao_percentual, nivel_bem_estar
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, tuple(valores))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('fim_page'))

    except MySQLdb.Error as e:
        print(f"❌ Erro ao salvar as respostas no banco de dados (MySQL): {e}")

        return f"Erro ao salvar respostas: {e}. Verifique se a estrutura da sua tabela está correta (11 colunas).", 500


@app.route('/fim')
def fim_page():
    """Displays the final questionnaire result."""
    if 'usuario_id' not in session:
        return redirect(url_for('login_page'))

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT pontuacao_total, pontuacao_percentual, nivel_bem_estar, data_submissao
            FROM respostasquestionario
            WHERE usuario_id = %s
            ORDER BY data_submissao DESC
            LIMIT 1
        """, [session['usuario_id']])
        resultado = cur.fetchone()
        cur.close()

        if not resultado:
            return "Nenhum resultado encontrado para este usuário. Por favor, complete o questionário.", 404

        return render_template('fim.html', resultado=resultado)
    except Exception as e:
        print(f"Erro ao buscar resultados finais: {e}")
        return "Erro ao buscar seus resultados.", 500

@app.route('/test_db')
def test_db():
    """Tests the database connection by listing tables."""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SHOW TABLES;")
        tabelas = cur.fetchall()
        cur.close()
        return f" Conexão bem-sucedida! Tabelas encontradas: {tabelas}"
    except Exception as e:
        return f" Erro de Conexão com o Banco de Dados: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)