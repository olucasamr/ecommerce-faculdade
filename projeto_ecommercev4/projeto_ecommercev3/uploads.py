import os
from werkzeug.utils import secure_filename
from flask import url_for

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def extensao_permitida(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def salvar_imagem(imagem):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


    if imagem and extensao_permitida(imagem.filename):
        filename = secure_filename(imagem.filename)
        caminho = os.path.join(UPLOAD_FOLDER, filename)
        imagem.save(caminho)

        
        return url_for('static', filename=f'uploads/{filename}')
    return None
