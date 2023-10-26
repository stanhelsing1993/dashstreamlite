import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Configuração do banco de dados MySQL
def conectar_mysql():
    cursor_mysql = mysql.connector.connect(
        host='10.61.176.114',
        user='pwd',
        password='vUyEth8y',
        database='auto_oss',
        charset='utf8'
    )
    return cursor_mysql



st.set_page_config(page_title= "Automacao- Sustentação OSS")

with st.container():
    st.subheader("Automacao- Sustentação OSS")
    st.title("Automação -  Envio Timeout CRM")
    st.write("Rotina responsavel por reenvio de requisições com timeout ao CRM")


@st.cache_data
def carregar_dados_timeout_crm():
    conn = conectar_mysql()
    query = "SELECT count(Pedido) as Pedidos,DATE_FORMAT (data_tratamento,'%d/%m/%Y') as Data FROM automacao where rotina = 'REENVIO TIMEOUT CRM' group by Data"
    timeout_crm = pd.read_sql_query(query, conn)
    tabela = timeout_crm
    return tabela

@st.cache_data
def carregar_dados_erro_null():
    conn = conectar_mysql()
    query = "SELECT count(Pedido) as Pedidos,DATE_FORMAT (data_tratamento,'%d/%m/%Y') as Data FROM automacao where rotina = 'SISTEMA FORA - ERRO NULL' group by Data"
    Sistema_Fora_erro_Null = pd.read_sql_query(query, conn)
    tabela = Sistema_Fora_erro_Null
    return tabela

@st.cache_data
def carregar_dados_sistema_fora():
    conn = conectar_mysql()
    query = "SELECT count(Pedido) as Pedidos,DATE_FORMAT (data_tratamento,'%d/%m/%Y') as Data FROM automacao where rotina = 'SISTEMA_FORA' group by Data;"
    Sistema_Fora_erro_Null = pd.read_sql_query(query, conn)
    tabela = Sistema_Fora_erro_Null
    return tabela

@st.cache_data
def carregar_dados_derivacao_hierarquia():
    conn = conectar_mysql()
    query = "SELECT count(Pedido) as Pedidos, DATE_FORMAT (data_tratamento,'%d/%m/%Y') as Data FROM automacao where rotina = 'REENVIO_DERIVACAO_HIERARQUIA' group by Data;"
    derivacao_hierarquia = pd.read_sql_query(query, conn)
    tabela = derivacao_hierarquia
    return tabela


#Timeout CRM
with st.container():
    st.write("---")
    qtd_dias = st.selectbox("Selecione o Periodo", ["1D", "7D", "15D", "30D", "60D", "90D"])
    num_dias = int(qtd_dias.replace("D", ""))
    dados = carregar_dados_timeout_crm()
    dados = dados[-num_dias:]
    st.area_chart(dados, x="Data", y="Pedidos")

#Erro null
with st.container():
    st.title("Automação -  Erro Null")
    st.write("Rotina Responsavel por adicionar os pedidos com erro null ao usuario para realizar o reenvio")


with st.container():
    st.write("---")
    dados = carregar_dados_erro_null()
    dados = dados[-num_dias:]
    st.area_chart(dados, x="Data", y="Pedidos")


# Sistema Fora
with st.container():
    st.title("Automação -  Sistema Fora")
    st.write("Rotina Responsavel por adicionar os pedidos com erro Sistema fora ao usuario para realizar o reenvio")


with st.container():
    st.write("---")
    dados = carregar_dados_sistema_fora()
    dados = dados[-num_dias:]
    st.area_chart(dados, x="Data", y="Pedidos")


#REENVIO_DERIVACAO_HIERARQUIA
with st.container():
    st.title("Automação -  Derivação Hierarquia")
    st.write("Rotina responsavel por reenviar eventos com erro de derivação de hierarquia com o click")


with st.container():
    st.write("---")
    dados = carregar_dados_derivacao_hierarquia()
    dados = dados[-num_dias:]
    st.area_chart(dados, x="Data", y="Pedidos")
