import sqlite3
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

st.markdown("""
<style>
header[data-testid="stHeader"] { display: none !important; }

.stApp {
    background: #FFFFFF;
    color: #111827;
}

.main .block-container {
    padding-top: 3rem;
    padding-left: 4rem;
    padding-right: 4rem;
    max-width: 1650px;
}

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid rgba(17,24,39,0.10);
}

section[data-testid="stSidebar"] * {
    color: #111827 !important;
}

h1, h2, h3, h4, h5, h6, p, span, label {
    color: #111827 !important;
}

label,
.stTextInput label,
.stTextArea label,
.stNumberInput label,
.stSelectbox label {
    color: #111827 !important;
    font-weight: 700 !important;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid rgba(124,58,237,0.18);
    padding: 22px;
    border-radius: 22px;
    box-shadow: 0 10px 30px rgba(17,24,39,0.05);
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 29px !important;
}

[data-testid="stMetricLabel"] {
    color: #7C3AED !important;
    font-weight: 800 !important;
}

.stButton button,
div[data-testid="stForm"] button,
div[data-testid="stLinkButton"] a {
    background: linear-gradient(90deg, #7C3AED, #A855F7) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 10px 22px !important;
    font-weight: 800 !important;
    text-decoration: none !important;
}

.stButton button:hover,
div[data-testid="stForm"] button:hover,
div[data-testid="stLinkButton"] a:hover {
    background: linear-gradient(90deg, #6D28D9, #9333EA) !important;
    color: white !important;
    border: none !important;
}

div[data-testid="stLinkButton"] a p {
    color: white !important;
}

.card {
    background: #FFFFFF;
    border: 1px solid rgba(17,24,39,0.10);
    border-radius: 24px;
    padding: 26px;
    margin-bottom: 18px;
    box-shadow: 0 10px 30px rgba(17,24,39,0.05);
}

.card-purple {
    background: linear-gradient(145deg, rgba(168,85,247,0.10), #FFFFFF);
    border: 1px solid rgba(168,85,247,0.25);
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 10px 30px rgba(17,24,39,0.05);
}

.mini-card {
    background: #FFFFFF;
    border: 1px solid rgba(17,24,39,0.10);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
    box-shadow: 0 8px 22px rgba(17,24,39,0.04);
}

.sub {
    color: #6B7280 !important;
    margin-top: -10px;
    margin-bottom: 28px;
}

.purple {
    color: #7C3AED !important;
}

.info-line {
    font-size: 17px;
    margin-bottom: 15px;
}

hr {
    border-color: rgba(17,24,39,0.08);
}

div[data-baseweb="input"],
div[data-baseweb="select"],
textarea {
    background: #F9FAFB !important;
    border-radius: 14px !important;
    border: 1px solid rgba(17,24,39,0.12) !important;
}

input, textarea {
    color: #111827 !important;
}

input::placeholder,
textarea::placeholder {
    color: #9CA3AF !important;
    opacity: 1 !important;
}

div[data-baseweb="select"] * {
    color: #111827 !important;
}

div[data-baseweb="input"] * {
    color: #111827 !important;
}

.stDataFrame {
    border-radius: 16px;
    overflow: hidden;
}

.status-pill {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(168,85,247,0.12);
    color: #7C3AED !important;
    font-weight: 800;
    font-size: 14px;
    border: 1px solid rgba(168,85,247,0.25);
}

.value-big {
    font-size: 34px;
    font-weight: 950;
    color: #7C3AED !important;
}

.small-muted {
    color: #6B7280 !important;
    font-size: 14px;
}

.big-number {
    font-size: 42px;
    font-weight: 950;
    color: #111827 !important;
    line-height: 1;
}

.card-title {
    color: #7C3AED !important;
    font-size: 14px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .7px;
}

.logo-wrapper {
    margin-bottom: 22px;
}

.sidebar-caption {
    color: #6B7280 !important;
    font-size: 13px;
    margin-top: -5px;
    margin-bottom: 14px;
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
    background: rgba(168,85,247,0.08) !important;
}

div[role="radiogroup"] label:has(input:checked) {
    background: rgba(168,85,247,0.12) !important;
    border-left: 4px solid #7C3AED !important;
}

.danger-note {
    color: #DC2626 !important;
    font-size: 13px;
}

.soft-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(124,58,237,0.18), rgba(17,24,39,0.04));
    margin: 24px 0;
}
</style>
""", unsafe_allow_html=True)


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
    CREATE TABLE IF NOT EXISTS influenciadores_base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arroba TEXT UNIQUE
    )
    """)

    try:
        cursor.execute("ALTER TABLE campanhas ADD COLUMN prazo_pagamento TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE campanhas ADD COLUMN marca TEXT")
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
    UPDATE campanhas
    SET status = 'Mapeamento', progresso = 10
    WHERE status = 'Briefing recebido'
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO influenciadores_base (arroba)
    SELECT DISTINCT arroba FROM influenciadores
    WHERE arroba IS NOT NULL AND arroba != ''
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


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def normalizar_arroba(arroba):
    arroba = (arroba or "").strip()
    if arroba and not arroba.startswith("@"):
        arroba = "@" + arroba
    return arroba


def salvar_influenciador_base(arroba):
    arroba = normalizar_arroba(arroba)
    if not arroba:
        return

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO influenciadores_base (arroba) VALUES (?)", (arroba,))
    conn.commit()
    conn.close()


def buscar_influenciadores_base():
    conn = conectar()
    df = pd.read_sql_query("SELECT arroba FROM influenciadores_base ORDER BY arroba ASC", conn)
    conn.close()
    return df["arroba"].tolist() if not df.empty else []


def salvar_campanha(cliente, marca, campanha, responsavel, valor, inicio, prazo_pagamento, status, drive, briefing, observacoes):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO campanhas (
        cliente, marca, campanha, responsavel, valor, inicio, fim, prazo_pagamento,
        status, progresso, drive, briefing, observacoes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cliente, marca, campanha, responsavel, valor, inicio, "", prazo_pagamento,
        status, calcular_progresso(status), drive, briefing, observacoes
    ))

    campanha_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return campanha_id


def buscar_campanhas():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM campanhas ORDER BY id DESC", conn)
    conn.close()

    if "prazo_pagamento" not in df.columns:
        df["prazo_pagamento"] = ""
    if "marca" not in df.columns:
        df["marca"] = ""

    return df


def buscar_influenciadores():
    conn = conectar()
    df = pd.read_sql_query("""
        SELECT 
            influenciadores.id,
            influenciadores.campanha_id,
            campanhas.campanha,
            campanhas.cliente,
            campanhas.marca,
            campanhas.responsavel,
            campanhas.prazo_pagamento,
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

    if "marca" not in df.columns:
        df["marca"] = ""

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


def salvar_influenciador(campanha_id, arroba, valor, entregaveis, status_conteudo, status_contrato, observacoes):
    arroba = normalizar_arroba(arroba)
    salvar_influenciador_base(arroba)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO influenciadores (
        campanha_id, nome, arroba, valor, entregaveis, postagem,
        status_conteudo, status_contrato, observacoes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        campanha_id, "", arroba, valor, entregaveis, "",
        status_conteudo, status_contrato, observacoes
    ))

    conn.commit()
    conn.close()


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


def atualizar_campanha(campanha_id, cliente, marca, campanha, responsavel, valor, inicio, prazo_pagamento, status, drive, briefing, observacoes):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE campanhas
    SET cliente = ?,
        marca = ?,
        campanha = ?,
        responsavel = ?,
        valor = ?,
        inicio = ?,
        prazo_pagamento = ?,
        status = ?,
        progresso = ?,
        drive = ?,
        briefing = ?,
        observacoes = ?
    WHERE id = ?
    """, (
        cliente, marca, campanha, responsavel, valor, inicio, prazo_pagamento,
        status, calcular_progresso(status), drive, briefing, observacoes, campanha_id
    ))

    conn.commit()
    conn.close()


def excluir_campanha(campanha_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM influenciadores WHERE campanha_id = ?", (campanha_id,))
    cursor.execute("DELETE FROM campanhas WHERE id = ?", (campanha_id,))

    conn.commit()
    conn.close()


criar_tabelas()

if "qtd_influ_squad" not in st.session_state:
    st.session_state.qtd_influ_squad = 2

if "tipo_campanha_atual" not in st.session_state:
    st.session_state.tipo_campanha_atual = "Individual"

if "pagina_ativa" not in st.session_state:
    st.session_state.pagina_ativa = "Dashboard"


st.sidebar.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
st.sidebar.image("logo_zoy.png", width=115)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-caption">CAMPAIGN OS</div>', unsafe_allow_html=True)

if st.sidebar.button("+ Nova Campanha", use_container_width=True):
    st.session_state.pagina_ativa = "Nova Campanha"

menu_opcoes = [
    "Dashboard",
    "Campanhas",
    "Detalhe da Campanha",
    "Squads",
    "Contratos",
    "Relatórios"
]

pagina_radio = st.sidebar.radio(
    "Menu",
    menu_opcoes,
    index=menu_opcoes.index(st.session_state.pagina_ativa) if st.session_state.pagina_ativa in menu_opcoes else 0
)

if st.session_state.pagina_ativa == "Nova Campanha":
    pagina = "Nova Campanha"
else:
    pagina = pagina_radio
    st.session_state.pagina_ativa = pagina_radio

st.sidebar.markdown("---")
st.sidebar.caption("Zoy Campaign OS · V10")


def campo_influenciador(i, prefixo="nova"):
    base_influs = buscar_influenciadores_base()
    opcoes = ["Cadastrar novo"] + base_influs

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        escolha = st.selectbox(
            f"Influenciador {i + 1}",
            opcoes,
            key=f"{prefixo}_select_influ_{i}"
        )

        if escolha == "Cadastrar novo":
            arroba = st.text_input(f"@ do influenciador {i + 1}", key=f"{prefixo}_arroba_influ_{i}")
        else:
            arroba = escolha
            st.caption(f"Selecionado: {arroba}")

    with col_b:
        valor = st.number_input(f"Cachê {i + 1}", min_value=0.0, step=100.0, key=f"{
