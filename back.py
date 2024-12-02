import pandas as pd
import plotly.graph_objects as go
import glob


def grafico_temperatura(caminho_temperatura, saida_html):
    """Cria e salva o gráfico de anomalias de temperatura."""
    dados_temperatura = pd.read_csv(caminho_temperatura, skiprows=4)
    dados_temperatura['Date'] = pd.to_datetime(dados_temperatura['Date'], format='%Y%m')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dados_temperatura['Date'],
        y=dados_temperatura['Anomaly'],
        mode='lines',
        name='Anomalia de Temperatura',
        line=dict(color='royalblue')
    ))
    fig.update_layout(
        title='Anomalias de Temperatura Global',
        xaxis_title='Ano',
        yaxis_title='Anomalia (°C)',
        template='plotly_white',
        hovermode='x'
    )
    fig.write_html(saida_html)


def grafico_plantas(pasta_plantas, saida_html):
    """Cria e salva o gráfico de anomalias de plantas."""
    
    # Processar dados das plantas
    file_paths = glob.glob(f'{pasta_plantas}/*.csv')
    dataframes = [pd.read_csv(file_path) for file_path in file_paths]
    dados_plantas = pd.concat(dataframes, ignore_index=True)
    dados_plantas['data_pas'] = pd.to_datetime(dados_plantas['data_pas'])
    dados_plantas['ano'] = dados_plantas['data_pas'].dt.year
    
    contagem_por_ano = dados_plantas.groupby('ano')['id_bdq'].count().reset_index()
    contagem_por_ano.rename(columns={'id_bdq': 'quantidade_plantas'}, inplace=True)
    media_plantas_geral = contagem_por_ano['quantidade_plantas'].mean()
    contagem_por_ano['anomalia_plantas'] = contagem_por_ano['quantidade_plantas'] - media_plantas_geral
    
    # dados_precipitacao = pd.read_csv(caminho_precipitacao, skiprows=4)
    # dados_precipitacao['Date'] = pd.to_datetime(dados_precipitacao['Date'], format='%Y%m')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dados_plantas['municipio'],
        y=contagem_por_ano['anomalia_plantas'],
        mode='lines+markers',
        name='Anomalia de Plantas',
        line=dict(color='green')
    ))
    fig.update_layout(
        title='Anomalia de Plantas por Região',
        xaxis_title='Região',
        yaxis_title='Anomalia de Plantas',
        template='plotly_white',
        hovermode='x'
    )
    fig.write_html(saida_html)


def grafico_precipitacao_e_plantas(caminho_precipitacao, pasta_plantas, saida_html):
    """Cria e salva o gráfico combinado de precipitação e anomalia de plantas."""
    # Processar dados de precipitação
    dados_precipitacao = pd.read_csv(caminho_precipitacao, skiprows=4)
    dados_precipitacao['Date'] = pd.to_datetime(dados_precipitacao['Date'], format='%Y%m')
    dados_precipitacao['ano'] = dados_precipitacao['Date'].dt.year
    precipitacao_por_ano = dados_precipitacao.groupby('ano')['Anomaly'].mean().reset_index()
    precipitacao_por_ano.rename(columns={'Anomaly': 'anomalia_precipitacao'}, inplace=True)

    # Processar dados das plantas
    file_paths = glob.glob(f'{pasta_plantas}/*.csv')
    dataframes = [pd.read_csv(file_path) for file_path in file_paths]
    dados_plantas = pd.concat(dataframes, ignore_index=True)
    dados_plantas['data_pas'] = pd.to_datetime(dados_plantas['data_pas'])
    dados_plantas['ano'] = dados_plantas['data_pas'].dt.year

    contagem_por_ano = dados_plantas.groupby('ano')['id_bdq'].count().reset_index()
    contagem_por_ano.rename(columns={'id_bdq': 'quantidade_plantas'}, inplace=True)
    media_plantas_geral = contagem_por_ano['quantidade_plantas'].mean()
    contagem_por_ano['anomalia_plantas'] = contagem_por_ano['quantidade_plantas'] - media_plantas_geral

    # Combinar dados
    dados_combinados = pd.merge(contagem_por_ano, precipitacao_por_ano, on='ano', how='inner')

    # Criar gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dados_combinados['ano'],
        y=dados_combinados['anomalia_plantas'],
        mode='lines+markers',
        name='Anomalia de Plantas',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))
    fig.add_trace(go.Scatter(
        x=dados_combinados['ano'],
        y=dados_combinados['anomalia_precipitacao'],
        mode='lines+markers',
        name='Anomalia de Precipitação',
        line=dict(color='green', width=2),
        marker=dict(size=6)
    ))
    fig.update_layout(
        title='Anomalias de Plantas e Precipitação por Ano',
        xaxis_title='Ano',
        yaxis_title='Anomalias',
        template='plotly_white',
        xaxis=dict(dtick=1),
        hovermode='x',
        legend_title='Variáveis'
    )
    fig.write_html(saida_html)


# Função principal para executar o fluxo
def main():
    grafico_temperatura('data_temperatura.csv', 'grafico_temperatura.html')
    grafico_plantas('plantas', 'grafico_plantas.html')
    grafico_precipitacao_e_plantas('data_precipitacao.csv', 'plantas', 'plantas_precipitacao_por_ano.html')


if __name__ == '__main__':
    main()
