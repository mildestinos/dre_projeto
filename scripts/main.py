import pandas as pd
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def consolidar_dados():
    pasta_data = './data/'
    arquivos = [f for f in os.listdir(pasta_data) if f.endswith('.csv')]
    lista_dfs = []
    for arquivo in arquivos:
        df_temp = pd.read_csv(os.path.join(pasta_data, arquivo))
        lista_dfs.append(df_temp)
    return pd.concat(lista_dfs, ignore_index=True)

def calcular_indicadores(df):
    try:
        receita_liquida = df.loc[df['Conta'] == 'Receita Líquida', 'Valor'].values[0]
        lucro_bruto = df.loc[df['Conta'] == 'Lucro Bruto', 'Valor'].values[0]
        ebitda = df.loc[df['Conta'] == 'EBITDA', 'Valor'].values[0]
        ebit = df.loc[df['Conta'] == 'EBIT', 'Valor'].values[0]
        lucro_liquido = df.loc[df['Conta'] == 'Lucro Líquido', 'Valor'].values[0]

        return {
            'Margem Bruta (%)': (lucro_bruto / receita_liquida) * 100,
            'Margem EBITDA (%)': (ebitda / receita_liquida) * 100,
            'Margem EBIT (%)': (ebit / receita_liquida) * 100,
            'Margem Líquida (%)': (lucro_liquido / receita_liquida) * 100,
        }
    except:
        return {}

def gerar_html(df, ano, mes, nivel):
    df_periodo = df[(df['Ano'] == ano) & (df['Mês'] == mes)]

    if nivel == 1:
        df_periodo = df_periodo[df_periodo['Nível'] == 1]
    elif nivel == 2:
        df_periodo = df_periodo[df_periodo['Nível'] == 2]

    indicadores = calcular_indicadores(df_periodo)
    linhas = df_periodo.to_dict(orient='records')

    env = Environment(loader=FileSystemLoader('./scripts/templates'))
    template = env.get_template('dre_resultado.html')

    html_output = template.render(
        mes=mes,
        ano=ano,
        nivel=nivel,
        dre=linhas,
        indicadores=indicadores
    )

    output_file = f'./output/dre_{ano}_{mes}.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"✅ HTML gerado com sucesso: {output_file}")

if __name__ == "__main__":
    df_dre = consolidar_dados()

    print("\n======= Geração de DRE (Somente HTML) =======")
    ano = int(input("Ano (ex: 2024): "))
    mes = int(input("Mês (1 a 12): "))
    print("\nNível: 1-Nível 1 | 2-Nível 2 | 0-Todos")
    nivel = int(input("Digite: "))

    gerar_html(df_dre, ano, mes, nivel)
