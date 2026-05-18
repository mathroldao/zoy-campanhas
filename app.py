import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Zoy Campanhas",
    page_icon="🚀",
    layout="wide"
)

# Inicialização
if "campanhas" not in st.session_state:
    st.session_state.campanhas = []

# Sidebar
st.sidebar.title("ZOY")
pagina = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Nova Campanha"]
)

# DASHBOARD
if pagina == "Dashboard":
    st.title("Dashboard de Campanhas")

    total_campanhas = len(st.session_state.campanhas)

    campanhas_ativas = len([
        c for c in st.session_state.campanhas
        if c["status"] != "Finalizado"
    ])

    campanhas_finalizadas = len([
        c for c in st.session_state.campanhas
        if c["status"] == "Finalizado"
    ])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Campanhas Totais", total_campanhas)

    with col2:
        st.metric("Campanhas Ativas", campanhas_ativas)

    with col3:
        st.metric("Finalizadas", campanhas_finalizadas)

    st.divider()

    if st.session_state.campanhas:
        df = pd.DataFrame(st.session_state.campanhas)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhuma campanha cadastrada ainda.")

# NOVA CAMPANHA
elif pagina == "Nova Campanha":
    st.title("Cadastrar Nova Campanha")

    with st.form("nova_campanha"):
        cliente = st.text_input("Cliente")
        nome = st.text_input("Nome da Campanha")
        responsavel = st.text_input("Responsável")
        data_inicio = st.date_input("Data de Início")
        data_fim = st.date_input("Data Final")

        status = st.selectbox(
            "Status",
            [
                "Briefing recebido",
                "Mapeamento",
                "Negociação",
                "Contrato enviado",
                "Conteúdo pendente",
                "Conteúdo em aprovação",
                "Postado",
                "Relatório pendente",
                "Finalizado"
            ]
        )

        salvar = st.form_submit_button("Salvar Campanha")

        if salvar:
            st.session_state.campanhas.append({
                "cliente": cliente,
                "campanha": nome,
                "responsavel": responsavel,
                "inicio": str(data_inicio),
                "fim": str(data_fim),
                "status": status
            })

            st.success("Campanha cadastrada com sucesso!")
