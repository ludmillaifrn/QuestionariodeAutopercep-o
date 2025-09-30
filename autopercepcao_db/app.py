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


def aprof_page():
   
    return render_template('aprof.html')


@app.route('/quest1')
def quest1()
    return render_template('quest1.html')


@app.route('/quest2')
def quest2():
   
    return render_template('quest2.html')



@app.route('/enviar_respostas', methods=['POST'])
def enviar_respostas():
    usuario_id = 'user_teste@email.com'

    if request.method == 'POST':
    
        try:
            # 1. Coletar respostas do formulário
            q1 = int(request.form['resposta_q1'])
            q2 = int(request.form['resposta_q2'])
            q3 = int(request.form['resposta_q3'])
        except (KeyError, ValueError):
            return "Erro: O formulário final (quest2) precisa enviar os campos 'resposta_q1', 'resposta_q2' e 'resposta_q3'.", 400

       
        pontuacao_total = q1 + q2 + q3
        
        
        if pontuacao_total >= 10:
            nivel_bem_estar = 'Ótimo'
        elif pontuacao_total >= 5:
            nivel_bem_estar = 'Satisfatório'
        else:
            nivel_bem_estar = 'Atenção'

       
        cur = None
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO RespostasQuestionario (usuario_id, resposta_q1, resposta_q2, resposta_q3, pontuacao_total, nivel_bem_estar)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (usuario_id, q1, q2, q3, pontuacao_total, nivel_bem_estar))
            
            mysql.connection.commit()

        except Exception as e:
            return f"Erro ao salvar no banco de dados: {e}", 500
        
        finally:
            if cur:
                cur.close()

       
        return redirect(url_for('fim_page', user_id=usuario_id))



@app.route('/fim') 
def fim_page(): # Mudei o nome da função para 'fim_page' para evitar conflito com 'resultados'
    user_id = request.args.get('user_id')
    
    if not user_id:
       
        return redirect(url_for('index_page')) 

    try:
        cur = mysql.connection.cursor()
        
        cur.execute("""
            SELECT pontuacao_total, nivel_bem_estar, data_submissao
            FROM RespostasQuestionario
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


