import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Carrega dados do banco
conn = sqlite3.connect('eventos_hidrograficos.db')
df = pd.read_sql_query('SELECT * FROM eventos_hidrograficos', conn)
conn.close()

# Converte data para datetime
if 'data' in df.columns:
    df['data'] = pd.to_datetime(df['data'])

# 1. Histograma de precipitação por intensidade
plt.figure(figsize=(8,5))
sns.histplot(data=df[df['tipo_evento']=='chuva'], x='precipitacao_mm', hue='intensidade', multiple='stack', bins=20)
plt.title('Distribuição da Precipitação por Intensidade de Chuva')
plt.xlabel('Precipitação (mm)')
plt.ylabel('Frequência')
plt.tight_layout()
plt.savefig('grafico_histograma_precipitacao.png')
plt.close()

# 2. Boxplot de precipitação por bairro
plt.figure(figsize=(12,6))
sns.boxplot(data=df[df['tipo_evento']=='chuva'], x='bairro', y='precipitacao_mm')
plt.title('Boxplot de Precipitação por Bairro')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_boxplot_bairro.png')
plt.close()

# 3. Série temporal de eventos de chuva
plt.figure(figsize=(10,5))
df_chuva = df[df['tipo_evento']=='chuva'].groupby('data').size()
df_chuva.plot()
plt.title('Frequência de Eventos de Chuva ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Número de Eventos')
plt.tight_layout()
plt.savefig('grafico_serie_temporal_chuva.png')
plt.close()

# 4. Matriz de correlação entre variáveis numéricas
plt.figure(figsize=(6,5))
num_cols = ['precipitacao_mm']
correlacao = df[num_cols].corr()
sns.heatmap(correlacao, annot=True, cmap='Blues')
plt.title('Matriz de Correlação')
plt.tight_layout()
plt.savefig('grafico_correlacao.png')
plt.close()

print('Gráficos gerados: histograma, boxplot, série temporal e correlação.')
