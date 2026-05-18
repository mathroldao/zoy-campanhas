import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Zoy Campanhas",
    page_icon="⚡",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>
.stApp {
    background: #070A12;
    color: #F8FAFC;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090D18 0%, #111827 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #111827, #0B1020);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

[data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 34px !important;
}

.stButton button {
    background: linear-gradient(90deg, #7C3AED, #A855F7);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: 700;
}

.stButton button:hover {
    background: linear-gradient(90deg, #6D28D9, #9333EA);
    color: white;
}

.card {
    background: linear-gradient(145deg, #111827, #0B1020);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 18px;
}

.zoy-logo {
    font-size: 38px;
    font-weight: 900;
    letter-spacing: -2px;
    color: white;
    margin-bottom: 20px;
}

.sub {
    color: #94A3B8;
    margin-top: -10px;
    margin-bottom: 25px;
}

.status {
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    display: inline-block;
}

.status-ok { background: rgba(34,197,94,.15); color: #4ADE80; }
.status-alert { background: rgba(245,158,11,.15); color: #FBBF24; }
.status-danger { background: rgba(239,68,68,.15); color: #F87171; }
.status-info { background: rgba(59,130,246,.15); color: #60A5FA; }
.status-purple { background: rgba(168,85,247,.15); color: #C084FC; }

hr {
    border-color: rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

if "campanhas" not in st.session_state:
    st.session_state.campanhas = []

if "influenciadores" not in st.session_state:
    st.session_state.influenciadores = []

# =========================
# SIDEBAR
# =========================

st.sidebar.markdown('<div class="zoy-logo">ZOY</div>', unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Nova Campanha",
        "Campanhas",
        "Influenciadores",
        "Relatórios"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Zoy Campaign OS · V1")

# =========================
# HELPERS
# =========================

def status_class(status):
    if status in ["Finalizado", "Aprovado", "Postado"]:
        return "status-ok"
    if status in ["Conteúdo em aprovação", "Relatório pendente", "Ajuste solicitado"]:
        return "status-alert"
    if status in ["Atrasado", "Cancelado"]:
        return "status-danger"
    if status in ["Mapeamento", "Briefing recebido"]:
        return "status-info"
    return "status-purple"

def calcular_progresso(status):
    mapa = {
        "Briefing recebido": 10,
        "Mapeamento": 20,
        "Casting enviado": 30,
        "Negociação": 40,
        "Contrato enviado": 50,
        "Conteúdo pendente": 60,
        "Conteúdo em aprovação": 70,
        "Aprovado": 80,
        "Postado": 90,
        "Relatório pendente": 95,
        "Finalizado": 100
    }
    return mapa.get(status, 0)

# =========================
# DASHBOARD
# =========================

if pagina == "Dashboard":
    st.title("Dashboard de Campanhas")
    st.markdown('<div class="sub">Visão geral das campanhas ativas da Agência Zoy</div>', unsafe_allow_html=True)

    total = len(st.session_state.campanhas)
    ativas = len([c for c in st.session_state.campanhas if c["status"] != "Finalizado"])
    finalizadas = len([c for c in st.session_state.campanhas if c["status"] == "Finalizado"])
    pendentes = len([c for c in st.session_state.campanhas if c["status"] in ["Conteúdo pendente", "Conteúdo em aprovação", "Relatório pendente"]])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Campanhas totais", total)
    col2.metric("Campanhas ativas", ativas)
    col3.metric("Pendências", pendentes)
    col4.metric("Finalizadas", finalizadas)

    st.markdown("---")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.subheader("Campanhas recentes")

        if st.session_state.campanhas:
            df = pd.DataFrame(st.session_state.campanhas)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma campanha cadastrada ainda.")

    with col_b:
        st.subheader("Alertas")

        if pendentes > 0:
            st.warning(f"{pendentes} campanha(s) precisam de atenção.")
        else:
            st.success("Nenhum alerta no momento.")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Resumo rápido**")
        st.write(f"Campanhas ativas: {ativas}")
        st.write(f"Campanhas finalizadas: {finalizadas}")
        st.write(f"Influenciadores cadastrados: {len(st.session_state.influenciadores)}")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# NOVA CAMPANHA
# =========================

elif pagina == "Nova Campanha":
    st.title("Nova Campanha")
    st.markdown('<div class="sub">Cadastre uma campanha nova para acompanhamento interno</div>', unsafe_allow_html=True)

    with st.form("form_campanha"):
        col1, col2 = st.columns(2)

        with col1:
            cliente = st.text_input("Cliente")
            campanha = st.text_input("Nome da campanha")
            responsavel = st.text_input("Responsável interno")
            valor = st.number_input("Valor total da campanha", min_value=0.0, step=100.0)

        with col2:
            inicio = st.date_input("Data de início", value=date.today())
            fim = st.date_input("Data final", value=date.today())
            drive = st.text_input("Link da pasta do Drive")
            status = st.selectbox(
                "Status da campanha",
                [
                    "Briefing recebido",
                    "Mapeamento",
                    "Casting enviado",
                    "Negociação",
                    "Contrato enviado",
                    "Conteúdo pendente",
                    "Conteúdo em aprovação",
                    "Aprovado",
                    "Postado",
                    "Relatório pendente",
                    "Finalizado"
                ]
            )

        briefing = st.text_area("Resumo do briefing")
        obs = st.text_area("Observações internas")

        salvar = st.form_submit_button("Salvar campanha")

        if salvar:
            nova = {
                "cliente": cliente,
                "campanha": campanha,
                "responsavel": responsavel,
                "valor": valor,
                "inicio": str(inicio),
                "fim": str(fim),
                "status": status,
                "progresso": calcular_progresso(status),
                "drive": drive,
                "briefing": briefing,
                "observacoes": obs
            }

            st.session_state.campanhas.append(nova)
            st.success("Campanha cadastrada com sucesso.")

# =========================
# CAMPANHAS
# =========================

elif pagina == "Campanhas":
    st.title("Campanhas")
    st.markdown('<div class="sub">Acompanhe status, progresso e responsáveis</div>', unsafe_allow_html=True)

    if not st.session_state.campanhas:
        st.info("Nenhuma campanha cadastrada ainda.")
    else:
        for i, c in enumerate(st.session_state.campanhas):
            st.markdown('<div class="card">', unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.subheader(c["campanha"])
                st.write(f"**Cliente:** {c['cliente']}")
                st.write(f"**Responsável:** {c['responsavel']}")
                st.write(f"**Período:** {c['inicio']} até {c['fim']}")

            with col2:
                st.write("**Status**")
                st.markdown(
                    f'<span class="status {status_class(c["status"])}">{c["status"]}</span>',
                    unsafe_allow_html=True
                )
                st.write("")
                st.progress(c["progresso"] / 100)

            with col3:
                st.write("**Valor**")
                st.subheader(f"R$ {c['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                if c["drive"]:
                    st.link_button("Abrir Drive", c["drive"])

            with st.expander("Ver detalhes"):
                st.write("**Briefing:**")
                st.write(c["briefing"] if c["briefing"] else "Sem briefing cadastrado.")

                st.write("**Observações:**")
                st.write(c["observacoes"] if c["observacoes"] else "Sem observações.")

                novo_status = st.selectbox(
                    "Atualizar status",
                    [
                        "Briefing recebido",
                        "Mapeamento",
                        "Casting enviado",
                        "Negociação",
                        "Contrato enviado",
                        "Conteúdo pendente",
                        "Conteúdo em aprovação",
                        "Aprovado",
                        "Postado",
                        "Relatório pendente",
                        "Finalizado"
                    ],
                    index=[
                        "Briefing recebido",
                        "Mapeamento",
                        "Casting enviado",
                        "Negociação",
                        "Contrato enviado",
                        "Conteúdo pendente",
                        "Conteúdo em aprovação",
                        "Aprovado",
                        "Postado",
                        "Relatório pendente",
                        "Finalizado"
                    ].index(c["status"]),
                    key=f"status_{i}"
                )

                if st.button("Salvar novo status", key=f"btn_status_{i}"):
                    st.session_state.campanhas[i]["status"] = novo_status
                    st.session_state.campanhas[i]["progresso"] = calcular_progresso(novo_status)
                    st.success("Status atualizado.")
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

# =========================
# INFLUENCIADORES
# =========================

elif pagina == "Influenciadores":
    st.title("Influenciadores")
    st.markdown('<div class="sub">Cadastre influenciadores por campanha e acompanhe entregas</div>', unsafe_allow_html=True)

    if not st.session_state.campanhas:
        st.warning("Cadastre uma campanha antes de adicionar influenciadores.")
    else:
        campanhas_nomes = [c["campanha"] for c in st.session_state.campanhas]

        with st.form("form_influ"):
            col1, col2 = st.columns(2)

            with col1:
                campanha_ref = st.selectbox("Campanha", campanhas_nomes)
                nome = st.text_input("Nome do influenciador")
                arroba = st.text_input("@ do influenciador")
                valor = st.number_input("Cachê", min_value=0.0, step=100.0)

            with col2:
                entregaveis = st.text_input("Entregáveis", placeholder="Ex: 1 Reels + 2 combos de stories")
                data_postagem = st.date_input("Data prevista de postagem")
                status_conteudo = st.selectbox(
                    "Status do conteúdo",
                    [
                        "Pendente",
                        "Recebido",
                        "Em aprovação",
                        "Ajuste solicitado",
                        "Aprovado",
                        "Postado",
                        "Finalizado"
                    ]
                )
                status_contrato = st.selectbox(
                    "Status do contrato",
                    [
                        "Não enviado",
                        "Enviado",
                        "Assinado"
                    ]
                )

            obs = st.text_area("Observações")

            salvar_influ = st.form_submit_button("Salvar influenciador")

            if salvar_influ:
                st.session_state.influenciadores.append({
                    "campanha": campanha_ref,
                    "nome": nome,
                    "arroba": arroba,
                    "valor": valor,
                    "entregaveis": entregaveis,
                    "postagem": str(data_postagem),
                    "status_conteudo": status_conteudo,
                    "status_contrato": status_contrato,
                    "observacoes": obs
                })

                st.success("Influenciador cadastrado com sucesso.")

        st.markdown("---")
        st.subheader("Influenciadores cadastrados")

        if st.session_state.influenciadores:
            df_influ = pd.DataFrame(st.session_state.influenciadores)
            st.dataframe(df_influ, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum influenciador cadastrado ainda.")

# =========================
# RELATÓRIOS
# =========================

elif pagina == "Relatórios":
    st.title("Relatórios")
    st.markdown('<div class="sub">Visão simples para acompanhar relatórios pendentes e finalizados</div>', unsafe_allow_html=True)

    if not st.session_state.campanhas:
        st.info("Nenhuma campanha cadastrada ainda.")
    else:
        relatorios = []

        for c in st.session_state.campanhas:
            relatorios.append({
                "campanha": c["campanha"],
                "cliente": c["cliente"],
                "responsavel": c["responsavel"],
                "status": c["status"],
                "relatorio": "Pendente" if c["status"] == "Relatório pendente" else "Não iniciado" if c["status"] != "Finalizado" else "Finalizado"
            })

        df_rel = pd.DataFrame(relatorios)
        st.dataframe(df_rel, use_container_width=True, hide_index=True)
