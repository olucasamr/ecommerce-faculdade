from ecommerce import db

class Produtos(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    url_imagem = db.Column(db.String(500))

    def __repr__(self):
        return f"<Produtos name={self.name}>"

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Usuarios name={self.name}>"

class Admins(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Admins name={self.name}>"
