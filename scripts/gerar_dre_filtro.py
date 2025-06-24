import pandas as pd

# === Passo 1: Ler toda a base com todos os meses ===
df = pd.read_csv('./data/dre_exemplo_2024_janeiro.csv')

# === Passo 2: Perguntar ao usuário o Ano e o Mês ===
ano = int(input("Digite o ANO (ex: 2024): "))
mes = int(input("Digite o MÊS (1 a 12): "))

# === Passo 3: Perguntar o Nível que o usuário deseja visualizar ===
print("\nEscolha o nível de detalhe:")
print("1 - Apenas Nível 1 (totalizadores)")
print("2 - Apenas Nível 2 (detalhes)")
print("0 - Todos os níveis")
nivel_opcao = int(input("Digite sua escolha: "))

# === Passo 4: Filtrar os dados pelo período ===
filtro = df[(df['Ano'] == ano) & (df['Mês'] == mes)]

# === Passo 5: Filtrar pelos níveis selecionados ===
if nivel_opcao == 1:
    filtro = filtro[filtro['Nível'] == 1]
elif nivel_opcao == 2:
    filtro = filtro[filtro['Nível'] == 2]
# Se for 0, mantém todos os níveis

# === Passo 6: Exibir a DRE filtrada ===
print(f"\n======= DRE - {mes}/{ano} - Nível {nivel_opcao if nivel_opcao else 'Todos'} =======\n")
for index, row in filtro.iterrows():
    print(f"{row['Conta']:<35} R$ {row['Valor']:,.2f}")

# === Passo 7: Calcular Indicadores somente se houver Nível 1 ===
if any(filtro['Conta'] == 'Receita Líquida'):
    receita_liquida = filtro.loc[filtro['Conta'] == 'Receita Líquida', 'Valor'].values[0]
    lucro_bruto = filtro.loc[filtro['Conta'] == 'Lucro Bruto', 'Valor'].values[0]
    ebitda = filtro.loc[filtro['Conta'] == 'EBITDA', 'Valor'].values[0]
    ebit = filtro.loc[filtro['Conta'] == 'EBIT', 'Valor'].values[0]
    lucro_liquido = filtro.loc[filtro['Conta'] == 'Lucro Líquido', 'Valor'].values[0]

    indicadores = {
        'Margem Bruta (%)': (lucro_bruto / receita_liquida) * 100,
        'Margem EBITDA (%)': (ebitda / receita_liquida) * 100,
        'Margem EBIT (%)': (ebit / receita_liquida) * 100,
        'Margem Líquida (%)': (lucro_liquido / receita_liquida) * 100,
    }

    print("\n======= Indicadores Financeiros =======\n")
    for nome, valor in indicadores.items():
        print(f"{nome:<25} {valor:.2f}%")
else:
    print("\n(Não foi possível calcular indicadores. Filtro atual não contém as contas principais.)")
