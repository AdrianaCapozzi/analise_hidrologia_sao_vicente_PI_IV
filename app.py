from flask import Flask, request, jsonify, send_from_directory
import os
import sqlite3
import pandas as pd

app = Flask(__name__)
@app.route('/')
def index():
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)), 'index.html')
DB_PATH = 'eventos_hidrograficos.db'

# Função para buscar dados filtrados
def get_eventos(data_ini=None, data_fim=None, bairro=None, tipo_evento=None):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM eventos_hidrograficos WHERE 1=1"
    params = []
    if data_ini:
        query += " AND data >= ?"
        params.append(data_ini)
    if data_fim:
        query += " AND data <= ?"
        params.append(data_fim)
    if bairro:
        query += " AND bairro = ?"
        params.append(bairro)
    if tipo_evento:
        query += " AND tipo_evento = ?"
        params.append(tipo_evento)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    # Garante que o campo precipitacao_mm está presente
    if 'precipitacao_mm' not in df.columns:
        df['precipitacao_mm'] = None
    return df

@app.route('/api/eventos', methods=['GET'])
def api_eventos():
    data_ini = request.args.get('data_ini')
    data_fim = request.args.get('data_fim')
    bairro = request.args.get('bairro')
    tipo_evento = request.args.get('tipo_evento')
    df = get_eventos(data_ini, data_fim, bairro, tipo_evento)
    return df.to_json(orient='records', force_ascii=False)

@app.route('/api/bairros', methods=['GET'])
def api_bairros():
    conn = sqlite3.connect(DB_PATH)
    bairros = pd.read_sql_query("SELECT DISTINCT bairro, regiao FROM eventos_hidrograficos", conn)
    conn.close()
    return bairros.to_json(orient='records', force_ascii=False)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
