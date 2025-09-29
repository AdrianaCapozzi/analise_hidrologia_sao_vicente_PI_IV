import pandas as pd

df = pd.DataFrame({
    'data': pd.date_range('2025-01-01', periods=12, freq='M'),
    'bairro': ['Centro', 'Praia', 'Jardim', 'Vila'] * 3,
    'precipitacao': [120, 80, 95, 110, 130, 70, 100, 105, 115, 90, 85, 125],
    'nivel_mare': [1.2, 1.5, 1.1, 1.3, 1.4, 1.6, 1.2, 1.3, 1.5, 1.4, 1.3, 1.2],
    'inundacao': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    'temperatura': [28, 30, 27, 29, 28, 31, 26, 30, 29, 32, 27, 28]
})

df.to_json('dados_graficos.json', orient='records', date_format='iso')