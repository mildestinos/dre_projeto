import pandas as pd

# === Passo 1: Ler o CSV a partir da raiz ===
df = pd.read_csv('./data/dre_exemplo_2024_janeiro.csv')

# === Passo 2: Exibir a DRE no terminal ===
print("\n======= DRE Janeiro/2024 =======\n")
for index, row in df.iterrows():
    print(f"{row['Conta']:<35} R$ {row['Valor']:,.2f}")

# === Passo 3: Calcular Indicadores ===
print("\n======= Indicadores Financeiros =======\n")

# Captura valores principais
receita_liquida = df.loc[df['Conta'] == 'Receita Líquida', 'Valor'].values[0]
lucro_bruto = df.loc[df['Conta'] == 'Lucro Bruto', 'Valor'].values[0]
ebitda = df.loc[df['Conta'] == 'EBITDA', 'Valor'].values[0]
ebit = df.loc[df['Conta'] == 'EBIT', 'Valor'].values[0]
lucro_liquido = df.loc[df['Conta'] == 'Lucro Líquido', 'Valor'].values[0]

# Cálculos
indicadores = {
    'Margem Bruta (%)': (lucro_bruto / receita_liquida) * 100,
    'Margem EBITDA (%)': (ebitda / receita_liquida) * 100,
    'Margem EBIT (%)': (ebit / receita_liquida) * 100,
    'Margem Líquida (%)': (lucro_liquido / receita_liquida) * 100,
}

# Exibir resultados
for nome, valor in indicadores.items():
    print(f"{nome:<25} {valor:.2f}%")
