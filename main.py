from flask import Flask, url_for, render_template, request, redirect, g, session 
from random import choice
from os import urandom
import redis
from string import ascii_uppercase

app = Flask(__name__)
wsgi_app = app.wsgi_app
app.secret_key = urandom(24)

##GERAR A SENHA DO PROFESSOR
"""
def gerachar ():
    return choice(ascii_uppercase)
password = gerachar() + gerachar() + gerachar() + gerachar()
"""
#/#

##FUNÇÃO QUE LÊ AS QUESTÕES:
def get_question(n):
    with open('questoes.txt') as q:
        txt=q.read()
        questoes=txt.replace('\n','').split('$$')
        listquests=[]
        listresps= []
        for item in questoes:
            listquests.append(item.split('//')[0])
            listresps.append(tuple(item.split('//')[1].split(';;')))
        print (listquests,listresps)
        return listquests[n], listresps[n]
#/#

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/', methods=['GET','POST'])
def home():
    session.pop('user', None)
    if request.method == 'POST':
        if request.form['persona'] == 'aluno':
            session['user'] = request.remote_addr
            return render_template('wait.html', cu = request.remote_addr)
        return redirect(url_for('professor'))
    return render_template('home.html')

    
"""       if request.form['submit'] == 'aluno':
            return render_template('wait.html')
        if request.form['submit'] == 'aluno':
            return render_template('professor.html')
"""


@app.route('/professor', methods=['GET','POST'])
def professor ():
    status = ''
    if request.method == 'POST':
        if request.form['codigo'] == 'banana':
            session['user'] = 'admin'
            return redirect(url_for('admin'))
        return render_template('professor.html', status = 'código inválido.')
    return render_template('professor.html', status = status)


@app.route('/admin')
def admin():
    if g.user == 'admin':
        return render_template('admin.html')
    else:
        return redirect(url_for('home'))


@app.route('/questao/<numero>')
def questao(numero):
    respostas=get_question(int(numero))[1]
    
    if numero == 'wait':
        return render_template('wait.html')
    else:
        return render_template('questao.html', questao= get_question(int(numero))[0],respostas=respostas,)
    
        

    



@app.route('/confirmed')
def confirmed():
    vote = request.args.get('opcao')
    with open('resultados.txt', 'a') as f:
        f.write(vote + '\n')
    return render_template("confirmed.html", vote=vote)


##

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run (HOST,PORT)
    
