from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import sys # Importado para logar erros detalhados

app = Flask(__name__)

# --- CONFIGURAÇÃO DO BANCO DE DADOS (Substitua pelos seus dados!) ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'labinfo'
app.config['MYSQL_DB'] = 'autopercepcao_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)

# -------------------------------------------------------------------

@app.route('/')
def index():
    # RF01: Disponibilizar questionários sobre bem-estar
    return render_template('questionario.html')

@app.route('/enviar_respostas', methods=['POST'])
def Enviar_respostas():
    if request.method == 'POST':
        # 1. Coletar respostas do formulário
        # ATENÇÃO: Use um sistema de autenticação real para obter o ID do usuário!
        usuario_id = 'user_teste@email.com' 
        
        try:
            # Coleta os dados do formulário e garante que são inteiros
            q1 = int(request.form['resposta_q1'])
            q2 = int(request.form['resposta_q2'])
            q3 = int(request.form['resposta_q3'])
            q4 = int(request.form['resposta_q4'])
            q5 = int(request.form['resposta_q5'])
            q6 = int(request.form['resposta_q6'])
            q7 = int(request.form['resposta_q7'])
        except (KeyError, ValueError) as e:
            print(f"Erro ao coletar dados do formulário: {e}", file=sys.stderr)
            return "Erro: Respostas inválidas ou faltando. Verifique os nomes dos campos no HTML.", 400

        # 2. RF03: Calcular pontuações automaticamente
        pontuacao_total = q1 + q2 + q3 + q4+ q5 + q6 + q7
        
        # 3. RF04 (Base para o feedback)
        if pontuacao_total >= 10:
            nivel_bem_estar = 'Ótimo'
        elif pontuacao_total >= 5:
            nivel_bem_estar = 'Satisfatório'
        else:
            nivel_bem_estar = 'Atenção'

        # 4. RF02: Coletar e salvar respostas no banco de dados
        try:
            cur = mysql.connection.cursor()
            
            # Comando SQL de inserção
            sql_query = """
                INSERT INTO RespostasQuestionario (
                    usuario_id, resposta_q1, resposta_q2, resposta_q3, resposta_q4, 
                    resposta_q5, resposta_q6, resposta_q7, pontuacao_total, nivel_bem_estar
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            valores = (
                usuario_id, q1, q2, q3, q4, q5, q6, q7, pontuacao_total, nivel_bem_estar
            )
            
            # Execução corrigida (string SQL e tuple de valores separados por vírgula)
            cur.execute(sql_query, valores) 
            
            # Confirma a transação
            mysql.connection.commit()
            cur.close()

            # Redireciona para a tela de resultados
            return redirect(url_for('resultado', user_id=usuario_id))

        except Exception as e:
            print(f"Erro detalhado ao salvar no banco de dados: {e}", file=sys.stderr)
            return f"Erro ao salvar no banco de dados: {e}", 500

@app.route('/resultado')
def resultado():
    # RF04: Exibir feedback e relatório de resultados ao usuário
    user_id = request.args.get('user_id')
    
    if not user_id:
        return redirect(url_for('index'))

    try:
        cur = mysql.connection.cursor()
        
        cur.execute("""
            SELECT pontuacao_total, nivel_bem_estar
            FROM RespostasQuestionario
            WHERE usuario_id = %s
            LIMIT 1
        """, [user_id])
        
        resultado = cur.fetchone()
        cur.close()

        if resultado:
            return render_template('resultado.html', resultado=resultado)
        else:
            return "Nenhum resultado encontrado para este usuário."
    
    except Exception as e:
        print(f"Erro detalhado ao buscar resultado: {e}", file=sys.stderr)
        return f"Erro ao buscar resultado: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
