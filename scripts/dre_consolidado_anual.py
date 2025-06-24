import pandas as pd
import os

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

def gerar_dre_anual(df, ano):
    df_ano = df[(df['Ano'] == ano) & (df['Nível'] == 1)]

    tabela = df_ano.pivot_table(
        index='Conta',
        columns='Mês',
        values='Valor',
        aggfunc='sum',
        fill_value=0
    )

    # Nome dos meses
    meses_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    tabela.rename(columns=meses_map, inplace=True)

    # Adicionar coluna Total
    tabela['Total'] = tabela.sum(axis=1)

    # Formatar como moeda
    def formatar(valor):
        return f" R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    print("\n======= 🐍DRE Consolidado Anual =======\n")
    print(f"{'Conta':<30}", end='')
    for col in tabela.columns:
        print(f"{col:<12}", end='')
    print()

    print("-" * (30 + 13 * len(tabela.columns)))

    for conta, linha in tabela.iterrows():
        print(f"{conta:<30}", end='')
        for valor in linha:
            print(f"{formatar(valor):<12}", end='')
        print()

if __name__ == "__main__":
    df_dre = consolidar_dados()
    ano = int(input("Digite o ANO para o consolidado (ex: 2024): "))
    gerar_dre_anual(df_dre, ano)
