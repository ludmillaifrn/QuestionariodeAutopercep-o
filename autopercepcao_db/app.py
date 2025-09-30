from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL 
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'labinfo'
app.config['MYSQL_DB'] = 'autopercepcao_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/aprof')
def aprof_page():
    return render_template('aprof.html')

@app.route('/quest1')
def quest1():
    return render_template('quest1.html')

@app.route('/quest2')
def quest2():
    return render_template('quest2.html')


@app.route('/enviar_respostas', methods=['POST'])
def enviar_respostas():
    usuario_id = 'user_teste@email.com'

    pesos = {
        "resposta_q1": {"A": 0, "B": 20, "C": 60, "D": 100},
        "resposta_q2": {"A": 0, "B": 15, "C": 45, "D": 90},
        "resposta_q3": {"A": 0, "B": 10, "C": 50, "D": 80},
        "resposta_q4": {"A": 0, "B": 25, "C": 55, "D": 95},
        "resposta_q5": {"A": 0, "B": 30, "C": 60, "D": 90},
        "resposta_q6": {"A": 0, "B": 35, "C": 70, "D": 100},
        "resposta_q7": {"A": 0, "B": 40, "C": 80, "D": 100}
    }

    try:
        respostas_raw = {}       
        respostas_valores = {}   
        pontuacao_total = 0

        for i in range(1, 8):
            campo = f'resposta_q{i}'
            letra = request.form.get(campo)

            if letra not in pesos[campo]:
                return f"Erro: Resposta inválida para a questão {i}.", 400

            valor = pesos[campo][letra]
            respostas_raw[campo] = letra
            respostas_valores[campo] = valor
            pontuacao_total += valor


        if pontuacao_total >= 550:
            nivel_bem_estar = 'Ótimo'
        elif pontuacao_total >= 300:
            nivel_bem_estar = 'Satisfatório'
        else:
            nivel_bem_estar = 'Atenção'

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO respostasquestionario (
                usuario_id,
                resposta_q1, resposta_q2, resposta_q3,
                resposta_q4, resposta_q5, resposta_q6, resposta_q7,
                pontuacao_total, nivel_bem_estar
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            usuario_id,
            respostas_valores['resposta_q1'],
            respostas_valores['resposta_q2'],
            respostas_valores['resposta_q3'],
            respostas_valores['resposta_q4'],
            respostas_valores['resposta_q5'],
            respostas_valores['resposta_q6'],
            respostas_valores['resposta_q7'],
            pontuacao_total,
            nivel_bem_estar
        ))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('fim_page', user_id=usuario_id))

    except Exception as e:
        return f"Erro ao processar ou salvar respostas: {e}", 500


@app.route('/fim') 
def fim_page(): 
    user_id = request.args.get('user_id')
    
    if not user_id:
        return redirect(url_for('index_page')) 

    try:
        cur = mysql.connection.cursor()
        
        cur.execute("""
            SELECT pontuacao_total, nivel_bem_estar, data_submissao
            FROM respostasquestionario
            WHERE usuario_id = %s
            ORDER BY data_submissao DESC
            LIMIT 1
        """, [user_id])
        
        resultado = cur.fetchone()
        cur.close()

        if resultado:
            return render_template('fim.html', resultado=resultado) 
        else:
            return "Nenhum resultado encontrado para este usuário."
    
    except Exception as e:
        return f"Erro ao buscar resultados: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)

