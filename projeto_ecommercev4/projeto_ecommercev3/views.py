from flask import render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Unauthorized

from ecommerce import app, db
from models import Produtos, Usuarios, Admins
from uploads import UPLOAD_FOLDER, salvar_imagem
import os


@app.route('/')
def inicio():
    return render_template('tela_inicial.html')

@app.route('/loja')
def loja():
    produtos = Produtos.query.all()
    return render_template('loja.html', produtos=produtos)

@app.route('/about')
def about():
    produtos = Produtos.query.all()
    return render_template('about.html', produtos=produtos)

@app.route('/produto/<int:id>')
def detalhes_produto(id):
    produto = Produtos.query.get(id)
    return render_template('produtos_descricao.html', produto=produto)

#parte carrinho
@app.route('/carrinho')
def carrinho():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    
    carrinho = []
    total = 0
    

    if 'carrinho' in session:
        for item in session['carrinho']:
            produto = Produtos.query.get(item['id']) 
            if produto:
                subtotal = float(produto.preco) * item['quantidade']
                total += subtotal 
                carrinho.append({
                    'id': produto.id,
                    'nome': produto.nome,
                    'quantidade': item['quantidade'],
                    'preco': float(produto.preco),  
                    'total': subtotal
                })

    return render_template('carrinho.html', carrinho=carrinho, total=total)

@app.route('/add-to-cart/<int:produto_id>', methods=['POST'])
def add_to_cart(produto_id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        flash('Você precisa estar logado para adicionar itens ao carrinho!', 'error')
        return redirect(url_for('login'))

    produto = Produtos.query.get(produto_id)
    if not produto:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('loja'))

   
    try:
        quantidade = int(request.form.get('quantidade', 1))
    except ValueError:
        flash('Quantidade inválida!', 'error')
        return redirect(url_for('loja'))

    
    if quantidade > produto.quantidade:  
        flash(f'Quantidade indisponível! Apenas {produto.quantidade} unidades restantes.', 'error')
        return redirect(url_for('loja'))

    
    if 'carrinho' not in session:
        session['carrinho'] = []

    
    for item in session['carrinho']:
        if item['id'] == produto_id:
            item['quantidade'] += quantidade  
            break
    else:
        session['carrinho'].append({'id': produto_id, 'quantidade': quantidade})

    session.modified = True  

    flash(f'{produto.nome} foi adicionado ao carrinho!', 'success')
    return redirect(url_for('carrinho'))

@app.route('/remover-item/<int:produto_id>', methods=['POST'])
def remover_item(produto_id):
    if 'carrinho' in session:
    
        session['carrinho'] = [item for item in session['carrinho'] if item['id'] != produto_id]
        session.modified = True  
    return redirect(url_for('carrinho'))

# Parte login

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)  
    flash('Logout realizado com sucesso!', 'success') 
    return redirect(url_for('login')) 

@app.route('/autenticar', methods=['POST'])
def autenticar():
    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = Usuarios.query.filter_by(email=email).first()
    admin = Admins.query.filter_by(email=email).first()

    if usuario and check_password_hash(usuario.senha, senha):
        session['usuario_logado'] = usuario.email
        flash(f"{usuario.nome} logado com sucesso!")
        return redirect(request.form.get('proxima', url_for('loja')))
    elif admin and check_password_hash(admin.senha, senha):
        session['usuario_logado'] = admin.email
        flash(f"Admin {admin.nome} logado com sucesso!")
        return redirect(url_for('admin_menu'))
    else:
        flash("Email ou senha incorretos!")
        return redirect(url_for('login'))

# Parte referente aos admins

def verifica_admin():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        flash("Faça login para acessar esta página.")
        return redirect(url_for('login'))
    
    admin = Admins.query.filter_by(email=session.get('usuario_logado')).first()
    if not admin:
        raise Unauthorized()


@app.route('/admin')
def admin_menu():
    resposta = verifica_admin()
    if resposta: return resposta
    return render_template('menu_admin.html')


@app.route('/usuarios')
def lista_usuarios():
    resposta = verifica_admin()
    if resposta: return resposta
    usuarios = Usuarios.query.all()
    return render_template('lista_usuarios.html', usuarios=usuarios)


@app.route('/admins')
def lista_admins():
    resposta = verifica_admin()
    if resposta: return resposta
    admins = Admins.query.all()
    return render_template('lista_admin.html', admins=admins)


@app.route('/lista')
def lista():
    resposta = verifica_admin()
    if resposta: return resposta
    produtos = Produtos.query.all()
    return render_template('lista.html', titulo='Lista', produtos=produtos)


@app.route('/novo')
def novo():
    resposta = verifica_admin()
    if resposta: return resposta
    return render_template('novo.html', titulo='Novo Produto')

#CRUD(produtos)
@app.route('/adicionar_produto', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        imagem = request.files['imagem']

        imagem_url = salvar_imagem(imagem)

        if imagem_url:
            novo_produto = Produtos(
                nome=nome,
                preco=preco,
                descricao=descricao,
                quantidade=quantidade,
                url_imagem=imagem_url
            )

            db.session.add(novo_produto)
            db.session.commit()

            flash(f'Produto "{nome}" salvo com sucesso! URL da imagem: {imagem_url}', 'success')
            return redirect(url_for('adicionar_produto'))

        flash('Erro: Arquivo enviado não é uma imagem válida.', 'danger')
        return redirect(url_for('adicionar_produto'))

    produtos = Produtos.query.all()
    return render_template('lista.html', titulo='Lista', produtos=produtos)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    produto = Produtos.query.get_or_404(id)

    if request.method == 'POST':

        produto.nome = request.form['nome']
        produto.preco = request.form['preco']
        produto.descricao = request.form['descricao']
        produto.quantidade = request.form['quantidade']


        nova_imagem = request.files.get('imagem')
        if nova_imagem:

            if produto.url_imagem:
                try:
                    caminho_imagem_antiga = os.path.join(UPLOAD_FOLDER, os.path.basename(produto.url_imagem))
                    if os.path.exists(caminho_imagem_antiga):
                        os.remove(caminho_imagem_antiga)
                except Exception as e:
                    print(f"Erro ao apagar imagem antiga: {e}")


            produto.url_imagem = salvar_imagem(nova_imagem)

        db.session.commit()
        flash(f"Produto '{produto.nome}' atualizado com sucesso!")
        return redirect(url_for('lista'))

    return render_template('editar.html', titulo='Editar Produto', produto=produto)
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    produto = Produtos.query.get_or_404(id)

    if produto.url_imagem:
        try:
            caminho_imagem = os.path.join(UPLOAD_FOLDER, os.path.basename(produto.url_imagem))
            if os.path.exists(caminho_imagem):
                os.remove(caminho_imagem)
                print(f"Imagem '{produto.url_imagem}' foi removida.")
            else:
                print(f"Imagem '{produto.url_imagem}' não encontrada.")
        except Exception as e:
            print(f"Erro ao tentar excluir a imagem: {e}")

    db.session.delete(produto)
    db.session.commit()

    flash(f"Produto '{produto.nome}' excluído com sucesso!")
    return redirect(url_for('lista'))


#CRUD usuarios


@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        
        nova_senha = request.form.get('senha')
        if nova_senha:  
            usuario.senha = generate_password_hash(nova_senha)

        db.session.commit()
        flash(f"Usuário '{usuario.nome}' atualizado com sucesso!", 'success')
        return redirect(url_for('lista_usuarios'))

    return render_template('editar_usuario.html', titulo='Editar Usuário', usuario=usuario)

@app.route('/deletar_usuario/<int:id>', methods=['POST'])
def deletar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    flash(f"Usuário '{usuario.nome}' excluído com sucesso!", 'success')
    return redirect(url_for('lista_usuarios'))


# CRUD (Administradores)

@app.route('/editar_admin/<int:id>', methods=['GET', 'POST'])
def editar_admin(id):
    admin = Admins.query.get_or_404(id)

    if request.method == 'POST':
        admin.nome = request.form['nome']
        admin.email = request.form['email']
        
        nova_senha = request.form.get('senha')
        if nova_senha: 
            admin.senha = generate_password_hash(nova_senha)

        db.session.commit()
        flash(f"Administrador '{admin.nome}' atualizado com sucesso!", 'success')
        return redirect(url_for('lista_admins'))

    return render_template('editar_admin.html', titulo='Editar Administrador', admin=admin)

@app.route('/deletar_admin/<int:id>', methods=['POST'])
def deletar_admin(id):
    admin = Admins.query.get_or_404(id)

    db.session.delete(admin)
    db.session.commit()

    flash(f"Administrador '{admin.nome}' excluído com sucesso!", 'success')
    return redirect(url_for('lista_admins'))

#cadastro(usuarios)
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not nome or not email or not senha:
        flash('Todos os campos são obrigatórios!', 'error')
        return redirect(url_for('cadastro'))

   
    usuario_existente = Usuarios.query.filter_by(email=email).first()
    if usuario_existente:
        flash('Este e-mail já está cadastrado! Tente outro.', 'error')
        return redirect(url_for('cadastro'))

    
    senha_hash = generate_password_hash(senha)
    novo_usuario = Usuarios(nome=nome, email=email, senha=senha_hash)

    db.session.add(novo_usuario)
    db.session.commit()

    flash(f'Usuário "{nome}" cadastrado com sucesso!', 'success')
    return redirect(url_for('login'))

#cadastro admin
@app.route('/cadastro_admin')
def cadastro_admin():
    return render_template('cadastro_admin.html')

@app.route('/cadastrar_admin', methods=['POST'])
def cadastrar_admin():
    nome = request.form.get('nome')
    email = request.form.get('email') 
    senha = request.form.get('senha')

    admin_existente = Admins.query.filter_by(email=email).first()
    if admin_existente:
        flash('Este e-mail já está cadastrado! Tente outro.', 'error')
        return redirect(url_for('cadastro_admin'))
    
    if nome and email and senha:
        senha_hash = generate_password_hash(senha)
        novo_admin = Admins(nome=nome, email=email, senha=senha_hash)

        db.session.add(novo_admin)
        db.session.commit()

        flash(f'Administrador "{nome}" cadastrado com sucesso!', 'success')
        return redirect(url_for('lista_admins'))  

    return "Erro ao cadastrar administrador", 400


@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        flash('Você precisa estar logado para finalizar a compra!', 'error')
        return redirect(url_for('login'))

    if 'carrinho' not in session or not session['carrinho']:
        flash('Seu carrinho está vazio!', 'error')
        return redirect(url_for('carrinho'))

 
    for item in session['carrinho']:
        produto = Produtos.query.get(item['id'])
        
        if not produto:
            flash(f'O produto {item["id"]} não foi encontrado!', 'error')
            continue
        
        
        if produto.quantidade < item['quantidade']:
            flash(f'Estoque insuficiente para {produto.nome}.', 'error')
            return redirect(url_for('carrinho'))

       
        produto.quantidade -= item['quantidade']
        db.session.commit()  


    session.pop('carrinho', None)
    
    flash('Compra finalizada com sucesso!', 'success')
    return redirect(url_for('loja'))

