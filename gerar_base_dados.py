import sqlite3
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Bairros de São Vicente
bairros_insular = [
    'Centro', 'Gonzaguinha', 'Itararé', 'Boa Vista', 'Parque Bitaru', 'Vila Valença',
    'Vila Margarida', 'Vila Voturuá', 'Catiapoã', 'Jockey Clube', 'Vila São Jorge', 'Vila Ponte Nova'
]
bairros_continental = [
    'Jardim Rio Branco', 'Parque das Bandeiras', 'Quarentenário', 'Samaritá',
    'Jardim Humaitá', 'Jardim Guassu', 'Jardim Irmã Dolores', 'Jardim Independência', 'Jardim Pompeba'
]

bairros = [(b, 'insular') for b in bairros_insular] + [(b, 'continental') for b in bairros_continental]
tipos_evento = ['chuva', 'maré', 'rio']
intensidades = ['leve', 'moderada', 'severa']
rios_sao_vicente = ['Rio Branco', 'Rio dos Sales', 'Rio Santo Antônio', 'Rio Jurubatuba']

fake = Faker('pt_BR')

# Cria conexão SQLite
db_name = 'eventos_hidrograficos.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()

# Cria tabela
c.execute('''
CREATE TABLE IF NOT EXISTS eventos_hidrograficos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE,
    bairro TEXT,
    regiao TEXT,
    tipo_evento TEXT,
    descricao TEXT,
    intensidade TEXT
)
''')
conn.commit()

# Gera dados sintéticos
eventos = []
for _ in range(1000):
    bairro, regiao = random.choice(bairros)
    tipo_evento = random.choice(tipos_evento)
    intensidade = random.choice(intensidades)
    dias_atras = random.randint(0, 365*3)  # últimos 3 anos
    data = (datetime.now() - timedelta(days=dias_atras)).date()
    if tipo_evento == 'chuva':
        descricao = f"Chuva {intensidade} causou alagamento em {bairro}."
    elif tipo_evento == 'maré':
        descricao = f"Maré alta provocou inundação em {bairro}."
    else:
        rio = random.choice(rios_sao_vicente)
        descricao = f"O {rio} transbordou próximo ao bairro {bairro}."
    eventos.append((str(data), bairro, regiao, tipo_evento, descricao, intensidade))

# Insere dados na tabela
c.executemany('''
INSERT INTO eventos_hidrograficos (data, bairro, regiao, tipo_evento, descricao, intensidade)
VALUES (?, ?, ?, ?, ?, ?)
''', eventos)
conn.commit()

print(f"Base de dados '{db_name}' criada com {len(eventos)} registros.")
conn.close()
