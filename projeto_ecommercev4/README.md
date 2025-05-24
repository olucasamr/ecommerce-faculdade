# E-Commerce QUBE

---

## Descrição do Projeto
Uma breve e clara descrição do que o seu projeto faz. Pense em uma ou duas frases que capturem a essência.
*Exemplo:* "Este projeto é uma aplicação web de gerenciamento de tarefas que permite aos usuários criar, editar e excluir tarefas de forma intuitiva."

---

## Funcionalidades

    * Cadastro e login de usuários e administradores
    * Criação e visualização de produtos para a loja
    * Edição e exclusão de informações existentes

---

## Tecnologias Utilizadas

    * **Frontend:** Javascript, CSS, HTML
    * **Backend:** Python, Flask
    * **Banco de Dados:** MySQL

---

## Pré-requisitos
Depêndencias e pré-requisitos para o projeto rodar normalmente
    * Flask (3.1.0)
    * Werkzeug(3.1.3)
    * MySQL local

---

## Instalação e Configuração
Passos detalhados para clonar o repositório, instalar as dependências e configurar o projeto para rodar localmente.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-projeto.git](https://github.com/seu-usuario/seu-projeto.git)
    cd seu-projeto
    ```

2.  **Instale as dependências do backend:**
    Importante instalar as dependências dentro da pasta onde estão os arquivos do projeto (geralmente "src")
    ```bash
    cd ../src
    pip install Flask
    pip install mysql-connector-python
    pip install Flask-SQLAlchemy
    ```

3.  **Configuração das variáveis de ambiente:**
    Não criamos um arquivo `.env` na raiz do diretório, fica aqui um desafio caso queiram agregar no projeto. Porém para conectar com o banco lembre-se de configurar as variáveis em config.py e prepara_banco.py.

## Como Rodar o Projeto
Instruções sobre como iniciar o projeto após a instalação.

1.  **Inicie o projeto:**

    Certifique-se de criar um banco de dados no MySQL configurado com o mesmo nome e variáveis do arquivo "prepara_banco.py";

    Na pasta `rojeto_rcommercev3`:
    ```bash
    python ecommerce.py 
    ```
    O servidor estará rodando em `http://localhost:5000` (ou a porta que você configurou).

    Após isso basta segurar CTRL e clicar no link que aparecerá no terminal.