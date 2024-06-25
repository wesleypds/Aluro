from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/cursos'
app.config['UPLOAD_FOLDER'] = 'C:/Users/mathe/OneDrive/Documentos/Trabalho Faculdade/static/uploads'

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Modelo de Curso
class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    imagem = db.Column(db.String(255), nullable=False)  # Caminho para a imagem

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username, password=password).first()
        if user:
            # Aqui você pode adicionar lógica para autenticar o usuário
            return "Login realizado com sucesso!"
        else:
            return "Usuário ou senha incorretos. Tente novamente."
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = Usuario(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return "Cadastro realizado com sucesso!"
    return render_template('cadastro.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

#Rota para adicionar um curso
@app.route('/admin/curso/add', methods=['POST'])
def add_curso():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    categoria = request.form['categoria']
    imagem = request.files['imagem']

    # Salvar a imagem no sistema de arquivos
    nome_imagem = secure_filename(imagem.filename)
    imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_imagem))

    # Criando uma nova instância de Curso
    novo_curso = Curso(titulo=titulo, descricao=descricao, categoria=categoria, imagem=nome_imagem)

    # Adicionando ao banco de dados
    db.session.add(novo_curso)
    db.session.commit()

    return 'Curso adicionado com sucesso!'


if __name__ == '__main__':
    app.run(debug=True)
