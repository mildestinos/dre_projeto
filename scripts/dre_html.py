import pandas as pd
import os
from datetime import datetime

def consolidar_dados():
    pasta_data = './data/'
    arquivos = [f for f in os.listdir(pasta_data) if f.endswith('.csv')]

    lista_dfs = []
    for arquivo in arquivos:
        caminho = os.path.join(pasta_data, arquivo)
        df_temp = pd.read_csv(caminho)
        lista_dfs.append(df_temp)

    df_consolidado = pd.concat(lista_dfs, ignore_index=True)
    return df_consolidado

def gerar_dre_html(df, ano, mes):
    df_periodo = df[(df['Ano'] == ano) & (df['Mês'] == mes)]

    html = f"""
    <html>
    <head>
        <title>DRE - {mes}/{ano}</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            h1, h2 {{ text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: right; }}
            th {{ background-color: #f2f2f2; }}
            td.conta {{ text-align: left; }}
        </style>
    </head>
    <body>
        <h1>Empresa XYZ</h1>
        <h2>Demonstração de Resultados - DRE</h2>
        <h3>Período: {mes}/{ano}</h3>

        <table>
            <tr>
                <th>Código</th>
                <th>Conta</th>
                <th>Valor (R$)</th>
            </tr>
    """

    for _, row in df_periodo.iterrows():
        html += f"""
            <tr>
                <td>{row['Código_Conta']}</td>
                <td class='conta'>{row['Conta']}</td>
                <td>{row['Valor']:,.2f}</td>
            </tr>
        """

    # Calcular indicadores se houver Receita Líquida
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

        html += """
        </table>
        <h2>Indicadores Financeiros</h2>
        <table>
            <tr><th>Indicador</th><th>Valor (%)</th></tr>
        """
        for nome, valor in indicadores.items():
            html += f"<tr><td class='conta'>{nome}</td><td>{valor:.2f}%</td></tr>"

    html += f"""
        </table>
        <p>Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </body>
    </html>
    """

    # Salvar
    with open('./output/dre_{0}_{1}.html'.format(ano, mes), 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ Arquivo HTML gerado: ./output/dre_{ano}_{mes}.html")

if __name__ == "__main__":
    df_dre = consolidar_dados()
    ano = int(input("Digite o ANO (ex: 2024): "))
    mes = int(input("Digite o MÊS (1 a 12): "))
    gerar_dre_html(df_dre, ano, mes)
