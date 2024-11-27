from flask import Flask, send_file
import pandas as pd
import plotly.graph_objects as go
import glob

app = Flask(__name__)

# Funções para gerar gráficos
def grafico_temperatura(caminho_temperatura, saida_html):
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
    file_paths = glob.glob(f'{pasta_plantas}/*.csv')
    dataframes = [pd.read_csv(file_path) for file_path in file_paths]
    dados_plantas = pd.concat(dataframes, ignore_index=True)
    dados_plantas['data_pas'] = pd.to_datetime(dados_plantas['data_pas'])
    dados_plantas['ano'] = dados_plantas['data_pas'].dt.year

    contagem_por_ano = dados_plantas.groupby('ano')['id_bdq'].count().reset_index()
    contagem_por_ano.rename(columns={'id_bdq': 'quantidade_plantas'}, inplace=True)
    media_plantas_geral = contagem_por_ano['quantidade_plantas'].mean()
    contagem_por_ano['anomalia_plantas'] = contagem_por_ano['quantidade_plantas'] - media_plantas_geral

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=contagem_por_ano['ano'],
        y=contagem_por_ano['anomalia_plantas'],
        mode='lines+markers',
        name='Anomalia de Plantas',
        line=dict(color='green')
    ))
    fig.update_layout(
        title='Anomalia de Plantas por Ano',
        xaxis_title='Ano',
        yaxis_title='Anomalia de Plantas',
        template='plotly_white',
        hovermode='x'
    )
    fig.write_html(saida_html)


def grafico_precipitacao_e_plantas(caminho_precipitacao, pasta_plantas, saida_html):
    dados_precipitacao = pd.read_csv(caminho_precipitacao, skiprows=4)
    dados_precipitacao['Date'] = pd.to_datetime(dados_precipitacao['Date'], format='%Y%m')
    dados_precipitacao['ano'] = dados_precipitacao['Date'].dt.year
    precipitacao_por_ano = dados_precipitacao.groupby('ano')['Anomaly'].mean().reset_index()
    precipitacao_por_ano.rename(columns={'Anomaly': 'anomalia_precipitacao'}, inplace=True)

    file_paths = glob.glob(f'{pasta_plantas}/*.csv')
    dataframes = [pd.read_csv(file_path) for file_path in file_paths]
    dados_plantas = pd.concat(dataframes, ignore_index=True)
    dados_plantas['data_pas'] = pd.to_datetime(dados_plantas['data_pas'])
    dados_plantas['ano'] = dados_plantas['data_pas'].dt.year

    contagem_por_ano = dados_plantas.groupby('ano')['id_bdq'].count().reset_index()
    contagem_por_ano.rename(columns={'id_bdq': 'quantidade_plantas'}, inplace=True)
    media_plantas_geral = contagem_por_ano['quantidade_plantas'].mean()
    contagem_por_ano['anomalia_plantas'] = contagem_por_ano['quantidade_plantas'] - media_plantas_geral

    dados_combinados = pd.merge(contagem_por_ano, precipitacao_por_ano, on='ano', how='inner')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dados_combinados['ano'],
        y=dados_combinados['anomalia_plantas'],
        mode='lines+markers',
        name='Anomalia de Plantas',
        line=dict(color='blue', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=dados_combinados['ano'],
        y=dados_combinados['anomalia_precipitacao'],
        mode='lines+markers',
        name='Anomalia de Precipitação',
        line=dict(color='green', width=2)
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


# Rotas Flask
@app.route('/grafico-temperatura')
def serve_grafico_temperatura():
    output_file = 'grafico_temperatura.html'
    grafico_temperatura('data_temperatura.csv', output_file)
    return send_file(output_file)


@app.route('/grafico-plantas')
def serve_grafico_plantas():
    output_file = 'grafico_plantas.html'
    grafico_plantas('plantas', output_file)
    return send_file(output_file)


@app.route('/grafico-precipitacao-e-plantas')
def serve_grafico_precipitacao_e_plantas():
    output_file = 'plantas_precipitacao_por_ano.html'
    grafico_precipitacao_e_plantas('data_precipitacao.csv', 'plantas', output_file)
    return send_file(output_file)


if __name__ == '__main__':
    app.run(debug=True)
