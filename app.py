import sqlite3
from datetime import date
import pandas as pd
import streamlit as st
import plotly.express as px

DB_NAME = "zoy_campanhas.db"

st.set_page_config(
    page_title="Zoy Campanhas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
header[data-testid="stHeader"] {
    display: none !important;
}

.stApp {
    background: #000000;
    color: #F8FAFC;
}

.main .block-container {
    padding-top: 3rem;
    padding-left: 4rem;
    padding-right: 4rem;
    max-width: 1650px;
}

section[data-testid="stSidebar"] {
    background: #020204;
    border-right: 1px solid rgba(168,85,247,0.35);
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

h1, h2, h3, h4, h5, h6, p, span, label {
    color: #F8FAFC !important;
}

label,
.stTextInput label,
.stTextArea label,
.stDateInput label,
.stNumberInput label,
.stSelectbox label {
    color: #E2E8F0 !important;
    font-weight: 600 !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #070707, #111111);
    border: 1px solid rgba(168,85,247,0.38);
    padding: 22px;
    border-radius: 22px;
    box-shadow: 0 0 30px rgba(168,85,247,0.08);
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 29px !important;
}

[data-testid="stMetricLabel"] {
    color: #C084FC !important;
    font-weight: 800 !important;
}

.stButton button,
div[data-testid="stForm"] button {
    background: linear-gradient(90deg, #7C3AED, #A855F7) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 10px 22px !important;
    font-weight: 800 !important;
}

.stButton button:hover,
div[data-testid="stForm"] button:hover {
    background: linear-gradient(90deg, #6D28D9, #9333EA) !important;
    color: white !important;
    border: none !important;
}

.card {
    background: linear-gradient(145deg, #050505, #0C0C0F);
    border: 1px solid rgba(168,85,247,0.26);
    border-radius: 24px;
    padding: 26px;
    margin-bottom: 18px;
    box-shadow: 0 0 35px rgba(168,85,247,0.06);
}

.card-purple {
    background: linear-gradient(145deg, rgba(124,58,237,0.22), rgba(3,3,3,1));
    border: 1px solid rgba(168,85,247,0.50);
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 18px;
}

.mini-card {
    background: #050505;
    border: 1px solid rgba(168,85,247,0.30);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}

.sub {
    color: #94A3B8 !important;
    margin-top: -10px;
    margin-bottom: 28px;
}

.purple {
    color: #A855F7 !important;
}

.info-line {
    font-size: 17px;
    margin-bottom: 15px;
}

hr {
    border-color: rgba(168,85,247,0.20);
}

div[data-baseweb="input"],
div[data-baseweb="select"],
textarea {
    background: #101010 !important;
    border-radius: 14px !important;
    border-color: rgba(168,85,247,0.25) !important;
}

input, textarea {
    color: #FFFFFF !important;
}

.stDataFrame {
    border-radius: 16px;
    overflow: hidden;
}

div[data-testid="stDataFrame"] {
    background: #050505 !important;
}

.status-pill {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(168,85,247,0.18);
    color: #C084FC !important;
    font-weight: 800;
    font-size: 14px;
    border: 1px solid rgba(168,85,247,0.35);
}

.value-big {
    font-size: 34px;
    font-weight: 950;
    color: #A855F7 !important;
}

.small-muted {
    color: #94A3B8 !important;
    font-size: 14px;
}

.big-number {
    font-size: 42px;
    font-weight: 950;
    color: #FFFFFF !important;
    line-height: 1;
}

.card-title {
    color: #C084FC !important;
    font-size: 14px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .7px;
}

.logo-wrapper {
    margin-bottom: 22px;
}

.sidebar-caption {
    color: #94A3B8 !important;
    font-size: 13px;
    margin-top: -5px;
    margin-bottom: 28px;
}

div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

div[role="radiogroup"] label {
    background: transparent !important;
    border-radius: 14px !important;
    padding: 12px 14px !important;
    margin-bottom: 4px !important;
}

div[role="radiogroup"] label:hover {
    background: rgba(168,85,247,0.14) !important;
}

div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, rgba(124,58,237,0.38), rgba(168,85,247,0.12)) !important;
    border-left: 4px solid #A855F7 !important;
}

</style>
""", unsafe_allow_html=True)


# =========================
# DATABASE
# =========================
def conectar():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS campanhas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        campanha TEXT,
        responsavel TEXT,
        valor REAL,
        inicio TEXT,
        fim TEXT,
        status TEXT,
        progresso INTEGER,
        drive TEXT,
        briefing TEXT,
        observacoes TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS influenciadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campanha_id INTEGER,
        nome TEXT,
        arroba TEXT,
        valor REAL,
        entregaveis TEXT,
        postagem TEXT,
        status_conteudo TEXT,
        status_contrato TEXT,
        observacoes TEXT,
        FOREIGN KEY(campanha_id) REFERENCES campanhas(id)
    )
    """)

    cursor.execute("""
    UPDATE campanhas
    SET status = 'Mapeamento', progresso = 10
    WHERE status = 'Briefing recebido'
    """)

    conn.commit()
    conn.close()


STATUS_CAMPANHA = [
    "Mapeamento",
    "Atendimento Iniciado",
    "Contrato Enviado",
    "Conteúdo Pendente",
    "Conteúdo em Aprovação",
    "Ajuste Solicitado",
    "Aprovado",
    "Postado",
    "Relatório Pendente",
    "Finalizado",
    "Cancelado"
]


STATUS_CONTEUDO = [
    "Pendente",
    "Recebido",
    "Em aprovação",
    "Ajuste solicitado",
    "Aprovado",
    "Postado",
    "Finalizado"
]


STATUS_CONTRATO = [
    "Não enviado",
    "Enviado",
    "Assinado"
]


def calcular_progresso(status):
    mapa = {
        "Mapeamento": 10,
        "Atendimento Iniciado": 20,
        "Contrato Enviado": 35,
        "Conteúdo Pendente": 50,
        "Conteúdo em Aprovação": 65,
        "Ajuste Solicitado": 70,
        "Aprovado": 80,
        "Postado": 90,
        "Relatório Pendente": 95,
        "Finalizado": 100,
        "Cancelado": 0
    }
    return mapa.get(status, 0)


def salvar_campanha(cliente, campanha, responsavel, valor, inicio, fim, status, drive, briefing, observacoes):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO campanhas (
        cliente, campanha, responsavel, valor, inicio, fim, status, progresso, drive, briefing, observacoes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cliente, campanha, responsavel, valor, str(inicio), str(fim), status,
        calcular_progresso(status), drive, briefing, observacoes
    ))

    campanha_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return campanha_id


def buscar_campanhas():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM campanhas ORDER BY id DESC", conn)
    conn.close()
    return df


def atualizar_status_campanha(campanha_id, novo_status):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE campanhas 
    SET status = ?, progresso = ?
    WHERE id = ?
    """, (novo_status, calcular_progresso(novo_status), campanha_id))

    conn.commit()
    conn.close()


def salvar_influenciador(campanha_id, nome, arroba, valor, entregaveis, postagem, status_conteudo, status_contrato, observacoes):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO influenciadores (
        campanha_id, nome, arroba, valor, entregaveis, postagem,
        status_conteudo, status_contrato, observacoes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        campanha_id, nome, arroba, valor, entregaveis, str(postagem),
        status_conteudo, status_contrato, observacoes
    ))

    conn.commit()
    conn.close()


def buscar_influenciadores():
    conn = conectar()
    df = pd.read_sql_query("""
        SELECT 
            influenciadores.id,
            campanhas.campanha,
            campanhas.cliente,
            influenciadores.nome,
            influenciadores.arroba,
            influenciadores.valor,
            influenciadores.entregaveis,
            influenciadores.postagem,
            influenciadores.status_conteudo,
            influenciadores.status_contrato,
            influenciadores.observacoes
        FROM influenciadores
        LEFT JOIN campanhas ON influenciadores.campanha_id = campanhas.id
        ORDER BY influenciadores.id DESC
    """, conn)
    conn.close()
    return df


def buscar_influenciadores_por_campanha(campanha_id):
    conn = conectar()
    df = pd.read_sql_query("""
        SELECT * FROM influenciadores
        WHERE campanha_id = ?
        ORDER BY id DESC
    """, conn, params=(campanha_id,))
    conn.close()
    return df


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


criar_tabelas()


# =========================
# SIDEBAR
# =========================
st.sidebar.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
st.sidebar.image("logo_zoy.png", width=115)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-caption">CAMPAIGN OS</div>', unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Nova Campanha",
        "Campanhas",
        "Detalhe da Campanha",
        "Squads",
        "Relatórios"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Zoy Campaign OS · V5")


# =========================
# DASHBOARD
# =========================
if pagina == "Dashboard":
    campanhas_df = buscar_campanhas()
    influ_df = buscar_influenciadores()

    st.title("Dashboard de Campanhas")
    st.markdown('<div class="sub">Central executiva de acompanhamento das campanhas da Agência Zoy</div>', unsafe_allow_html=True)

    total = len(campanhas_df)
    ativas = len(campanhas_df[~campanhas_df["status"].isin(["Finalizado", "Cancelado"])]) if total > 0 else 0
    investimento = campanhas_df["valor"].sum() if total > 0 else 0
    contratos_pendentes = len(influ_df[influ_df["status_contrato"] != "Assinado"]) if not influ_df.empty else 0
    conteudos_pendentes = len(influ_df[influ_df["status_conteudo"].isin(["Pendente", "Recebido", "Em aprovação", "Ajuste solicitado"])]) if not influ_df.empty else 0
    relatorios_pendentes = len(campanhas_df[campanhas_df["status"] == "Relatório Pendente"]) if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Campanhas Ativas", ativas)
    col2.metric("Investimento Total", formatar_moeda(investimento))
    col3.metric("Influenciadores Ativos", len(influ_df))

    col4, col5, col6 = st.columns(3)
    col4.metric("Contratos Pendentes", contratos_pendentes)
    col5.metric("Conteúdos Pendentes", conteudos_pendentes)
    col6.metric("Relatórios Pendentes", relatorios_pendentes)

    st.markdown("---")

    col_status, col_atendimento = st.columns([1, 1])

    with col_status:
        st.subheader("Visão geral por status")

        if campanhas_df.empty:
            st.info("Nenhuma campanha cadastrada ainda.")
        else:
            status_df = (
                campanhas_df.groupby("status")
                .size()
                .reset_index(name="quantidade")
                .sort_values("quantidade", ascending=False)
            )

            fig = px.pie(
                status_df,
                names="status",
                values="quantidade",
                hole=0.55,
                color_discrete_sequence=[
                    "#A855F7", "#7C3AED", "#C084FC", "#9333EA",
                    "#6D28D9", "#DDD6FE", "#8B5CF6", "#581C87",
                    "#E9D5FF", "#4C1D95", "#2E1065"
                ]
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                marker=dict(line=dict(color="#000000", width=2))
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F8FAFC", size=12),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=0.95,
                    font=dict(color="#E2E8F0", size=11)
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                height=280
            )

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_atendimento:
        st.subheader("Visão geral por atendimento")

        if campanhas_df.empty or "responsavel" not in campanhas_df.columns:
            st.info("Nenhum responsável cadastrado ainda.")
        else:
            resp_df = (
                campanhas_df[campanhas_df["responsavel"].fillna("") != ""]
                .groupby("responsavel")
                .size()
                .reset_index(name="campanhas")
                .sort_values("campanhas", ascending=False)
            )

            if resp_df.empty:
                st.info("Nenhum responsável cadastrado ainda.")
            else:
                for _, r in resp_df.iterrows():
                    st.markdown('<div class="mini-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-title">{r["responsavel"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="big-number">{int(r["campanhas"])}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="small-muted">campanha(s) sob responsabilidade</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Campanhas recentes")

    if not campanhas_df.empty:
        df_view = campanhas_df[["cliente", "campanha", "responsavel", "valor", "inicio", "fim", "status"]].copy()
        df_view["valor"] = df_view["valor"].apply(formatar_moeda)
        st.dataframe(df_view, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma campanha cadastrada ainda.")


# =========================
# NOVA CAMPANHA
# =========================
elif pagina == "Nova Campanha":
    st.title("Nova Campanha")
    st.markdown('<div class="sub">Cadastre uma campanha nova e já monte o squad inicial</div>', unsafe_allow_html=True)

    with st.form("form_campanha"):
        st.markdown('<div class="card">', unsafe_allow_html=True)

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
            status = st.selectbox("Status da campanha", STATUS_CAMPANHA)

        briefing = st.text_area("Resumo do briefing")
        observacoes = st.text_area("Observações internas")

        st.markdown("---")
        st.subheader("Influenciadores da campanha")

        tipo_campanha = st.radio(
            "Essa campanha é individual ou squad?",
            ["Individual", "Squad"],
            horizontal=True
        )

        qtd_influenciadores = 1
        if tipo_campanha == "Squad":
            qtd_influenciadores = st.number_input(
                "Quantidade de influenciadores no squad",
                min_value=1,
                max_value=20,
                value=2,
                step=1
            )

        influenciadores_temp = []

        for i in range(int(qtd_influenciadores)):
            st.markdown(f"#### Influenciador {i + 1}")

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                nome_influ = st.text_input(f"Nome do influenciador {i + 1}", key=f"nome_influ_{i}")
                arroba_influ = st.text_input(f"@ do influenciador {i + 1}", key=f"arroba_influ_{i}")

            with col_b:
                valor_influ = st.number_input(f"Cachê {i + 1}", min_value=0.0, step=100.0, key=f"valor_influ_{i}")
                entregaveis_influ = st.text_input(
                    f"Entregáveis {i + 1}",
                    placeholder="Ex: 1 Reels + 2 combos de stories",
                    key=f"entregaveis_influ_{i}"
                )

            with col_c:
                postagem_influ = st.date_input(f"Data prevista {i + 1}", value=date.today(), key=f"postagem_influ_{i}")
                status_contrato_influ = st.selectbox(
                    f"Status contrato {i + 1}",
                    STATUS_CONTRATO,
                    key=f"contrato_influ_{i}"
                )
                status_conteudo_influ = st.selectbox(
                    f"Status conteúdo {i + 1}",
                    STATUS_CONTEUDO,
                    key=f"conteudo_influ_{i}"
                )

            obs_influ = st.text_area(f"Observações do influenciador {i + 1}", key=f"obs_influ_{i}")

            influenciadores_temp.append({
                "nome": nome_influ,
                "arroba": arroba_influ,
                "valor": valor_influ,
                "entregaveis": entregaveis_influ,
                "postagem": postagem_influ,
                "status_contrato": status_contrato_influ,
                "status_conteudo": status_conteudo_influ,
                "observacoes": obs_influ
            })

            st.markdown("---")

        salvar = st.form_submit_button("Salvar campanha")

        st.markdown('</div>', unsafe_allow_html=True)

        if salvar:
            if not cliente or not campanha:
                st.error("Preencha pelo menos Cliente e Nome da campanha.")
            else:
                campanha_id = salvar_campanha(
                    cliente, campanha, responsavel, valor, inicio, fim,
                    status, drive, briefing, observacoes
                )

                for influ in influenciadores_temp:
                    if influ["nome"]:
                        salvar_influenciador(
                            campanha_id,
                            influ["nome"],
                            influ["arroba"],
                            influ["valor"],
                            influ["entregaveis"],
                            influ["postagem"],
                            influ["status_conteudo"],
                            influ["status_contrato"],
                            influ["observacoes"]
                        )

                st.success("Campanha cadastrada com sucesso.")


# =========================
# CAMPANHAS
# =========================
elif pagina == "Campanhas":
    campanhas_df = buscar_campanhas()

    st.title("Campanhas")
    st.markdown('<div class="sub">Acompanhe status, progresso, squad e responsáveis</div>', unsafe_allow_html=True)

    if campanhas_df.empty:
        st.info("Nenhuma campanha cadastrada ainda.")
    else:
        for _, c in campanhas_df.iterrows():
            st.markdown('<div class="card">', unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.subheader(c["campanha"])
                st.write(f"**Cliente:** {c['cliente']}")
                st.write(f"**Responsável:** {c['responsavel']}")
                st.write(f"**Período:** {c['inicio']} até {c['fim']}")

            with col2:
                st.write("**Status**")
                st.markdown(f'<span class="status-pill">{c["status"]}</span>', unsafe_allow_html=True)
                st.write("")
                st.progress(int(c["progresso"]) / 100)

            with col3:
                st.write("**Valor**")
                st.subheader(formatar_moeda(c["valor"]))

                if c["drive"]:
                    st.link_button("Abrir Drive", c["drive"])

            with st.expander("Ver detalhes rápidos"):
                squad_df = buscar_influenciadores_por_campanha(int(c["id"]))

                if squad_df.empty:
                    st.info("Nenhum influenciador cadastrado nesta campanha ainda.")
                else:
                    squad_view = squad_df[["nome", "arroba", "valor", "entregaveis", "postagem", "status_conteudo", "status_contrato"]].copy()
                    squad_view["valor"] = squad_view["valor"].apply(formatar_moeda)
                    st.dataframe(squad_view, use_container_width=True, hide_index=True)

            st.markdown('</div>', unsafe_allow_html=True)


# =========================
# DETALHE DA CAMPANHA
# =========================
elif pagina == "Detalhe da Campanha":
    campanhas_df = buscar_campanhas()

    st.title("Detalhe da Campanha")
    st.markdown('<div class="sub">Visão completa da campanha, squad e operação</div>', unsafe_allow_html=True)

    if campanhas_df.empty:
        st.info("Nenhuma campanha cadastrada ainda.")
    else:
        campanhas_dict = {
            f"{row['campanha']} | {row['cliente']}": int(row["id"])
            for _, row in campanhas_df.iterrows()
        }

        escolha = st.selectbox("Selecione a campanha", list(campanhas_dict.keys()))
        campanha_id = campanhas_dict[escolha]

        campanha = campanhas_df[campanhas_df["id"] == campanha_id].iloc[0]
        squad_df = buscar_influenciadores_por_campanha(campanha_id)

        st.markdown('<div class="card-purple">', unsafe_allow_html=True)

        col1, col2 = st.columns([1.4, 1])

        with col1:
            st.header(campanha["campanha"])
            st.markdown(f'<div class="info-line"><span class="purple">Cliente:</span> {campanha["cliente"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="purple">Responsável:</span> {campanha["responsavel"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="purple">Período:</span> {campanha["inicio"]} até {campanha["fim"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="purple">Status:</span> <span class="status-pill">{campanha["status"]}</span></div>', unsafe_allow_html=True)

            st.write("**Progresso**")
            st.progress(int(campanha["progresso"]) / 100)
            st.caption(f"{int(campanha['progresso'])}% concluído")

        with col2:
            st.markdown('<div class="small-muted">Valor total</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="value-big">{formatar_moeda(campanha["valor"])}</div>', unsafe_allow_html=True)

            st.write("")
            st.write("**Link do Drive**")
            if campanha["drive"]:
                st.link_button("Abrir pasta no Drive", campanha["drive"])
            else:
                st.caption("Nenhum link cadastrado.")

            st.write("**Resumo do briefing**")
            st.write(campanha["briefing"] if campanha["briefing"] else "-")

            st.write("**Observações internas**")
            st.write(campanha["observacoes"] if campanha["observacoes"] else "-")

        st.markdown('</div>', unsafe_allow_html=True)

        col_squad, col_status = st.columns([1.3, 1])

        with col_squad:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Squad da Campanha")

            if squad_df.empty:
                st.info("Nenhum influenciador cadastrado nesta campanha ainda.")
            else:
                df_squad = squad_df[["nome", "arroba", "valor", "entregaveis", "postagem", "status_conteudo", "status_contrato"]].copy()
                df_squad["valor"] = df_squad["valor"].apply(formatar_moeda)
                st.dataframe(df_squad, use_container_width=True, hide_index=True)

            with st.expander("Adicionar influenciador nesta campanha"):
                with st.form("form_influ_detalhe"):
                    nome = st.text_input("Nome do influenciador")
                    arroba = st.text_input("@ do influenciador")
                    valor = st.number_input("Cachê", min_value=0.0, step=100.0)
                    entregaveis = st.text_input("Entregáveis", placeholder="Ex: 1 Reels + 2 combos de stories")
                    postagem = st.date_input("Data prevista de postagem")
                    status_conteudo = st.selectbox("Status do conteúdo", STATUS_CONTEUDO)
                    status_contrato = st.selectbox("Status do contrato", STATUS_CONTRATO)
                    observacoes = st.text_area("Observações")

                    salvar = st.form_submit_button("Salvar influenciador")

                    if salvar:
                        if not nome:
                            st.error("Preencha o nome do influenciador.")
                        else:
                            salvar_influenciador(
                                campanha_id, nome, arroba, valor, entregaveis,
                                postagem, status_conteudo, status_contrato, observacoes
                            )
                            st.success("Influenciador adicionado ao squad.")
                            st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        with col_status:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Atualizar status da campanha")

            novo_status = st.selectbox(
                "Novo status",
                STATUS_CAMPANHA,
                index=STATUS_CAMPANHA.index(campanha["status"]) if campanha["status"] in STATUS_CAMPANHA else 0
            )

            if st.button("Salvar novo status"):
                atualizar_status_campanha(campanha_id, novo_status)
                st.success("Status atualizado.")
                st.rerun()

            st.markdown("---")
            st.subheader("Checklist operacional")

            checklist = [
                ("Mapeamento", campanha["progresso"] >= 10),
                ("Atendimento Iniciado", campanha["progresso"] >= 20),
                ("Contrato Enviado", campanha["progresso"] >= 35),
                ("Conteúdo Pendente", campanha["progresso"] >= 50),
                ("Conteúdo em Aprovação", campanha["progresso"] >= 65),
                ("Aprovado", campanha["progresso"] >= 80),
                ("Postado", campanha["progresso"] >= 90),
                ("Relatório Pendente", campanha["progresso"] >= 95),
                ("Finalizado", campanha["progresso"] >= 100),
            ]

            for item, feito in checklist:
                st.write(f"{'✓' if feito else '○'} {item}")

            st.markdown('</div>', unsafe_allow_html=True)


# =========================
# SQUADS
# =========================
elif pagina == "Squads":
    campanhas_df = buscar_campanhas()

    st.title("Squads")
    st.markdown('<div class="sub">Cadastre influenciadores por campanha e acompanhe entregas</div>', unsafe_allow_html=True)

    if campanhas_df.empty:
        st.warning("Cadastre uma campanha antes de adicionar influenciadores.")
    else:
        campanhas_dict = {
            f"{row['campanha']} | {row['cliente']}": int(row["id"])
            for _, row in campanhas_df.iterrows()
        }

        with st.form("form_influ"):
            col1, col2 = st.columns(2)

            with col1:
                campanha_escolhida = st.selectbox("Campanha", list(campanhas_dict.keys()))
                nome = st.text_input("Nome do influenciador")
                arroba = st.text_input("@ do influenciador")
                valor = st.number_input("Cachê", min_value=0.0, step=100.0)

            with col2:
                entregaveis = st.text_input("Entregáveis", placeholder="Ex: 1 Reels + 2 combos de stories")
                postagem = st.date_input("Data prevista de postagem")
                status_conteudo = st.selectbox("Status do conteúdo", STATUS_CONTEUDO)
                status_contrato = st.selectbox("Status do contrato", STATUS_CONTRATO)

            observacoes = st.text_area("Observações")

            salvar = st.form_submit_button("Salvar influenciador")

            if salvar:
                if not nome:
                    st.error("Preencha o nome do influenciador.")
                else:
                    campanha_id = campanhas_dict[campanha_escolhida]
                    salvar_influenciador(
                        campanha_id, nome, arroba, valor, entregaveis,
                        postagem, status_conteudo, status_contrato, observacoes
                    )
                    st.success("Influenciador cadastrado com sucesso.")

        st.markdown("---")
        st.subheader("Influenciadores cadastrados")

        influ_df = buscar_influenciadores()

        if influ_df.empty:
            st.info("Nenhum influenciador cadastrado ainda.")
        else:
            influ_view = influ_df.copy()
            influ_view["valor"] = influ_view["valor"].apply(formatar_moeda)
            st.dataframe(influ_view, use_container_width=True, hide_index=True)


# =========================
# RELATÓRIOS
# =========================
elif pagina == "Relatórios":
    campanhas_df = buscar_campanhas()

    st.title("Relatórios")
    st.markdown('<div class="sub">Visão simples para acompanhar relatórios pendentes e finalizados</div>', unsafe_allow_html=True)

    if campanhas_df.empty:
        st.info("Nenhuma campanha cadastrada ainda.")
    else:
        relatorios = []

        for _, c in campanhas_df.iterrows():
            if c["status"] == "Finalizado":
                status_relatorio = "Finalizado"
            elif c["status"] == "Relatório Pendente":
                status_relatorio = "Pendente"
            else:
                status_relatorio = "Não iniciado"

            relatorios.append({
                "campanha": c["campanha"],
                "cliente": c["cliente"],
                "responsavel": c["responsavel"],
                "status_campanha": c["status"],
                "relatorio": status_relatorio
            })

        df_rel = pd.DataFrame(relatorios)
        st.dataframe(df_rel, use_container_width=True, hide_index=True)
