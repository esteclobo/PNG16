from flask import Flask, url_for, render_template, request, redirect, g, session 
from random import choice
from os import urandom
from string import ascii_letters

app = Flask(__name__)
wsgi_app = app.wsgi_app
app.secret_key = urandom(24)

##GERAR A SENHA DO PROFESSOR

def gerachar ():
    return choice(ascii_letters)
password = gerachar() + gerachar() + gerachar() + gerachar() + gerachar()
print (password)

#/#

##FUNÇÕES DE DATABASE:
def get_allquestions():
    with open('db/questoes.txt') as q:
        txt=q.read()
        questoes=txt.replace('\n','').split('$$')
        listquests=[]
        for item in questoes:
            listquests.append(item.split('//')[0])
        return listquests

def get_question(n):
    with open('db/questoes.txt') as q:
        txt=q.read()
        questoes=txt.replace('\n','').split('$$')
        listquests=[]
        listresps= []
        for item in questoes:
            listquests.append(item.split('//')[0])
            listresps.append(tuple(item.split('//')[1].split(';;')))
        return listquests[n], listresps[n]

def next_question():
    with open ('db/currentquest.txt', 'r+') as w:
        current = int(w.readline())
        w.seek(0)
        w.truncate()
        w.write(str(current + 1))
def check_reset ():
    with open('db/resetvotes.txt', 'r') as c:
        if int(c.readline()):
            session['votou'] = 0
def make_reset ():
    with open('db/resetvotes.txt', 'w') as w:
        w.seek(0)
        w.truncate()
        w.write('1')
            
            
#/#

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
    check_reset()

@app.route('/', methods=['GET','POST'])
def home():
    session.pop('user', None)
    if request.method == 'POST':
        if request.form['persona'] == 'aluno':
            session['user'] = request.remote_addr
            try:
                if session['votou']:
                    pass
            except:
                session['votou'] = 0
            return redirect (url_for('questao'))
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
        if request.form['codigo'] == 'banan':
            session['user'] = 'admin'
            return redirect(url_for('admin'))
        return render_template('professor.html', status = 'código inválido.')
    return render_template('professor.html', status = status)


@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        with open('db/currentquest.txt', 'w') as w:
            w.truncate()
            w.write(request.form['opcao'])
        return redirect(url_for('questao'))
    else:
        if g.user == 'admin':
            session['votou'] = 0
            return render_template('admin.html', quests=get_allquestions())
        else:
            return redirect(url_for('home'))



@app.route('/questao', methods=['GET', 'POST'])
def questao():
    if request.method == 'POST':
        if session['user'] == 'admin':
            next_question()
            make_reset()
            return redirect('questao')
        if session['votou']:
            return render_template('wait.html')
        return render_template('questao.html')
    with open('db/currentquest.txt', 'r') as c:
        numero = c.readline()
    try:
        respostas=get_question(int(numero))[1]
    except IndexError:
        return render_template('fim.html')
    if session['votou'] :
        return render_template('wait.html')
    if session['user'] == 'admin':
        return render_template('questaoprof.html', questao= get_question(int(numero))[0],respostas=respostas,)
    return render_template('questao.html', questao= get_question(int(numero))[0],respostas=respostas,)

"""

@app.route('/questao/')
def q():
    try:
        return redirect(url_for('questao', numero=session['number']))
    except:
        return render_template('wait.html')

@app.route('/questao/<numero>', methods=['GET', 'POST'])
def questao(numero):
    print ('nmr',numero, 'sess',session['number'])
    if numero == session['number']:
        respostas=get_question(int(numero))[1]
        if session['votou'] :
            return render_template('wait.html')
        else:
            if session['user'] == 'admin':
                if request.method == 'POST':
                    session['number'] = int(session['number']) + 1
                    print ('ennnnnnnnnnnneee ps', str(session['number']))
                    return redirect(url_for('q'))
                return render_template('questaoprof.html', questao= get_question(int(numero))[0],respostas=respostas,)
            return render_template('questao.html', questao= get_question(int(numero))[0],respostas=respostas,)
    else:
        return render_template('wait.html')
        
"""
    



@app.route('/confirmed')
def confirmed():
    if not session['votou']:
        vote = request.args.get('opcao')
        session['votou'] = 1
        with open('db/resultados.txt', 'a') as f:
            f.write(vote + '\n')
        return render_template("confirmed.html", vote=vote)
    else:
        return render_template('wait.html')

##

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run (HOST,PORT)
    
