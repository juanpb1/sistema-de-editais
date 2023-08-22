import sqlite3
import os

banco = os.path.join("banco de dados", "Database.sqlite3")

conn = sqlite3.connect(banco)
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

def criar_tabela_aluno():
    c.execute('''CREATE TABLE ALUNO (
                    matricula INTEGER PRIMARY KEY,
                    nome TEXT,
                    nacionalidade TEXT,
                    cpf TEXT,
                    sexo TEXT,
                    email TEXT,
                    telefone TEXT,
                    data_nasc DATE
                 )''')
    conn.commit()

def criar_tabela_edital():
    c.execute('''CREATE TABLE EDITAL (
                    numero INTEGER PRIMARY KEY,
                    titulo TEXT,
                    descricao TEXT,
                    n_vagas INTEGER,
                    data_inicial DATE,
                    data_final DATE
                 )''')
    conn.commit()

def criar_tabela_edital_aluno():
    c.execute('''CREATE TABLE EDITAL_ALUNO (
                    aluno_mat INTEGER,
                    edital_num INTEGER,
                    status TEXT,
                    PRIMARY KEY (aluno_mat, edital_num),
                    FOREIGN KEY (aluno_mat) REFERENCES ALUNO(matricula),
                    FOREIGN KEY (edital_num) REFERENCES EDITAL(numero)
                 )''')
    conn.commit()

def criar_tabela_professor():
    c.execute('''CREATE TABLE PROFESSOR (
                    matricula INTEGER PRIMARY KEY,
                    nome TEXT,
                    nacionalidade TEXT,
                    cpf TEXT,
                    sexo TEXT,
                    email TEXT,
                    telefone TEXT,
                    data_nasc DATE,
                    graduacao TEXT
                 )''')
    conn.commit()

def criar_tabela_projeto():
    c.execute('''CREATE TABLE PROJETO (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    data_de_inicio DATE,
                    data_de_fim DATE,
                    professor INTEGER,
                    FOREIGN KEY (professor) REFERENCES PROFESSOR(matricula)
                 )''')
    conn.commit()

def criar_tabela_relatorio():
    c.execute('''CREATE TABLE RELATORIO (
                    id INTEGER PRIMARY KEY,
                    status TEXT,
                    projeto_id INTEGER,
                    FOREIGN KEY (projeto_id) REFERENCES PROJETO(id)
                 )''')
    conn.commit()

def criar_tabelas():
    criar_tabela_aluno()
    criar_tabela_edital()
    criar_tabela_professor()
    criar_tabela_edital_aluno()
    criar_tabela_projeto()
    criar_tabela_relatorio()

criar_tabelas()
