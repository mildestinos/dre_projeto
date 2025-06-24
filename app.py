from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

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

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/dre_resultado', methods=['POST'])
def dre_resultado():
    ano = int(request.form['ano'])
    mes = int(request.form['mes'])
    nivel = int(request.form['nivel'])

    df = consolidar_dados()
    df_periodo = df[(df['Ano'] == ano) & (df['Mês'] == mes)]

    if nivel == 1:
        df_periodo = df_periodo[df_periodo['Nível'] == 1]
    elif nivel == 2:
        df_periodo = df_periodo[df_periodo['Nível'] == 2]

    indicadores = calcular_indicadores(df_periodo)
    linhas = df_periodo.to_dict(orient='records')

    return render_template('dre_resultado.html', ano=ano, mes=mes, nivel=nivel, dre=linhas, indicadores=indicadores)

@app.route('/dre_consolidado_anual', methods=['GET', 'POST'])
def dre_consolidado_anual():
    df = consolidar_dados()
    anos_disponiveis = sorted(df['Ano'].unique())

    if request.method == 'POST':
        ano = int(request.form['ano'])
        df_ano = df[(df['Ano'] == ano) & (df['Nível'] == 1)]

        tabela = df_ano.pivot_table(
            index='Conta',
            columns='Mês',
            values='Valor',
            aggfunc='sum',
            fill_value=0
        )

        meses_map = {
            1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
        }
        tabela.rename(columns=meses_map, inplace=True)

        tabela['Total Ano'] = tabela.sum(axis=1)

        tabela = tabela.reset_index()
        colunas = tabela.columns.tolist()
        linhas = tabela.to_dict(orient='records')

        return render_template('dre_consolidado_anual.html', colunas=colunas, linhas=linhas, ano=ano, anos=anos_disponiveis)

    return render_template('dre_consolidado_anual.html', colunas=None, linhas=None, ano=None, anos=anos_disponiveis)

if __name__ == '__main__':
    app.run(debug=True)
