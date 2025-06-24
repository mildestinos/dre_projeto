from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__, template_folder='../templates')

def consolidar_dados():
    pasta_data = './data/'
    arquivos = [f for f in os.listdir(pasta_data) if f.endswith('.csv')]

    lista_dfs = []
    for arquivo in arquivos:
        caminho = os.path.join(pasta_data, arquivo)
        df_temp = pd.read_csv(caminho)
        lista_dfs.append(df_temp)

    return pd.concat(lista_dfs, ignore_index=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ano = int(request.form['ano'])
        mes = int(request.form['mes'])
        nivel = int(request.form['nivel'])

        df = consolidar_dados()
        df_periodo = df[(df['Ano'] == ano) & (df['Mês'] == mes)]

        if nivel == 1:
            df_periodo = df_periodo[df_periodo['Nível'] == 1]
        elif nivel == 2:
            df_periodo = df_periodo[df_periodo['Nível'] == 2]

        indicadores = {}
        if any(df_periodo['Conta'] == 'Receita Líquida'):
            receita_liquida = df_periodo.loc[df_periodo['Conta'] == 'Receita Líquida', 'Valor'].values[0]
            lucro_bruto = df_periodo.loc[df_periodo['Conta'] == 'Lucro Bruto', 'Valor'].values[0]
            ebitda = df_periodo.loc[df_periodo['Conta'] == 'EBITDA', 'Valor'].values[0]
            ebit = df_periodo.loc[df_periodo['Conta'] == 'EBIT', 'Valor'].values[0]
            lucro_liquido = df_periodo.loc[df_periodo['Conta'] == 'Lucro Líquido', 'Valor'].values[0]

            indicadores = {
                'Margem Bruta (%)': (lucro_bruto / receita_liquida) * 100,
                'Margem EBITDA (%)': (ebitda / receita_liquida) * 100,
                'Margem EBIT (%)': (ebit / receita_liquida) * 100,
                'Margem Líquida (%)': (lucro_liquido / receita_liquida) * 100,
            }

        return render_template('dre_resultado.html', dre=df_periodo.to_dict(orient='records'), indicadores=indicadores, ano=ano, mes=mes, nivel=nivel)

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
