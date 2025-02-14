# Gráfico de Preço do Ethereum atualizado.
# Seleção de períodos para análise.
# Métricas chave sobre o preço do Ethereum.

import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title='Ethereum ',
    page_icon=':chart_with_upwards_trend:',
    layout='wide'
)

# Título do dashboard
st.title('Ethereum ')
st.markdown("###")

# Função para buscar os dados do preço do Ethereum
def get_ethereum_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "ethereum",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params).json()
    return response.get("ethereum", {}).get("usd")

# Obtendo o preço atual do Ethereum
eth_price = get_ethereum_price()
if eth_price:
    st.metric(label='Preço Atual do Ethereum (USD)', value=f'${eth_price:,.2f}')
else:
    st.error("Falha ao obter dados do preço do Ethereum")

# Obtendo dados históricos do Ethereum
@st.cache_data
def get_historical_data():
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "30",
        "interval": "daily"
    }
    response = requests.get(url, params=params).json()
    df = pd.DataFrame(response['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

df = get_historical_data()

# Criando o gráfico interativo
fig = px.line(df, x='timestamp', y='price', title='Preço do Ethereum nos Últimos 30 Dias', labels={'price': 'Preço (USD)', 'timestamp': 'Data'})
st.plotly_chart(fig, use_container_width=True)

st.markdown("Fonte: [CoinGecko](https://www.coingecko.com/)")
