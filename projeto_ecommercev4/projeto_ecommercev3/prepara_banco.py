import mysql.connector
from mysql.connector import errorcode
from werkzeug.security import generate_password_hash

try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password=''
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `ecommerce`;")

cursor.execute("CREATE DATABASE `ecommerce`;")

cursor.execute("USE `ecommerce`;")

# criando tabelas
TABLES = {}
TABLES['Produtos'] = ('''
      CREATE TABLE `produtos` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `preco` decimal(10, 2) NOT NULL,                
      `descricao` text,  
      `quantidade` int NOT NULL,
      `url_imagem` varchar(500),                
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nome` varchar(20) NOT NULL,
      `email` varchar(40) NOT NULL,
      `senha` varchar(255) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Admins'] = ('''
      CREATE TABLE `admins` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nome` varchar(20) NOT NULL,
      `email` varchar(40) NOT NULL,
      `senha` varchar(255) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Lucas Amaral", "lucas@gmail.com", generate_password_hash("1234")),
      ("Douglas", "douglas@gmail.com", generate_password_hash("4321")),
]            
cursor.executemany(usuario_sql, usuarios)


# inserindo admins

usuario_sql = 'INSERT INTO admins (nome, email, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Bruno Firmino Torres", "bruno@gmail.com", generate_password_hash("12345")),
      ("Fernando", "fernando@gmail.com", generate_password_hash("5321")),
]            
cursor.executemany(usuario_sql, usuarios)

# inserindo produtos(para salvar imagens:http://localhost:5000/static/uploads/nome_da_imagem.jpg)
produtos_sql = 'INSERT INTO produtos (nome, preco, descricao, quantidade, url_imagem) VALUES (%s, %s, %s, %s, %s)'
produtos = [
    ('PC GAMER', '4000', 'Roda tudo', '40', 'http://localhost:5000/static/uploads/pc_gamer_01.jpg'),
    ('PC MAIS GAMER AINDA', '7000', 'Roda até a NASA', '4', 'http://localhost:5000/static/uploads/pc_gamer_02.jpg'),
    ('PC Casual', '1000', 'roda o Google', '20', 'http://localhost:5000/static/uploads/pc_casual_01.jpg'),
    ('PC Vintage', '10000', 'Esse é raridade', '1', 'http://localhost:5000/static/uploads/computador_vintage_01.jpg')
    
      
]
cursor.executemany(produtos_sql, produtos)



cursor.execute('select * from ecommerce.produtos')
print(' -------------  Produtos:  -------------')
for produtos in cursor.fetchall():
    print(produtos[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
