SECRET_KEY = 'fecaf'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'your-password',
        servidor = 'localhost',
        database = 'ecommerce'
    )