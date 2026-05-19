import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

DB_NAME = "zoy_campanhas.db"

st.set_page_config(
    page_title="Campaign OS",
    page_icon="🟣",
    layout="wide"
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

.card:empty,
.card-purple:empty,
.mini-card:empty {
    display: none !important;
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

.soft-divider {
    height: 1px;
    background: linear-gradient(
        90deg,
        rgba(124,58,237,0),
        rgba(124,58,237,0.55),
        rgba(168,85,247,0.35),
        rgba(124,58,237,0)
    );
    margin: 32px 0;
    border-radius: 999px;
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        senha TEXT,
        ativo INTEGER DEFAULT 1
    )
    """)

    usuarios_padrao = [
        ("jean@agenciazoy.com", "zoy2026"),
        ("rafaela@agenciazoy.com", "zoy2026"),
        ("taila@agenciazoy.com", "zoy2026"),
        ("camila@agenciazoy.com", "zoy2026"),
        ("contato@agenciazoy.com", "zoy2026"),
        ("matheus@agenciazoy.com", "zoy2026"),
        ("financeiro@agenciazoy.com", "zoy2026"),
    ]

    for email, senha in usuarios_padrao:
        cursor.execute("""
        INSERT OR IGNORE INTO usuarios (email, senha, ativo)
        VALUES (?, ?, 1)
        """, (email, senha))
        
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

def validar_login(email, senha):
    email = (email or "").strip().lower()
    senha = (senha or "").strip()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT email FROM usuarios
    WHERE email = ?
    AND senha = ?
    AND ativo = 1
    """, (email, senha))

    usuario = cursor.fetchone()
    conn.close()

    return usuario is not None
    
criar_tabelas()

if "qtd_influ_squad" not in st.session_state:
    st.session_state.qtd_influ_squad = 2

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = ""

if "tipo_campanha_atual" not in st.session_state:
    st.session_state.tipo_campanha_atual = "Individual"

if "pagina_ativa" not in st.session_state:
    st.session_state.pagina_ativa = "Dashboard"

if not st.session_state.logado:

    st.markdown(
        "<h1 style='text-align:center;'>Zoy Influence Hub</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#6B7280;'>Agência Zoy</p>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 2, 1.2])

with col2:
    email_login = st.text_input("E-mail")
    senha_login = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):
        if validar_login(email_login, senha_login):
            st.session_state.logado = True
            st.session_state.usuario_logado = email_login
            st.rerun()
        else:
            st.error("Login ou senha inválidos.")

    st.stop()

    st.markdown(
        "<p style='text-align:center;color:#6B7280;'>Acesso interno Agência Zoy</p>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    email_login = st.text_input("E-mail")
    senha_login = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):
        if validar_login(email_login, senha_login):
            st.session_state.logado = True
            st.session_state.usuario_logado = email_login
            st.rerun()
        else:
            st.error("Login ou senha inválidos.")

    st.stop()
st.sidebar.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
st.sidebar.image("logo_zoy_dark.png", width=115)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-caption">ZOY INFLUENCE HUB<</div>', unsafe_allow_html=True)

st.sidebar.caption(f"Logado como: {st.session_state.usuario_logado}")

if st.sidebar.button("Sair", use_container_width=True):
    st.session_state.logado = False
    st.session_state.usuario_logado = ""
    st.rerun()
    
if st.sidebar.button("+ Nova Campanha", use_container_width=True):
    st.session_state.pagina_ativa = "Nova Campanha"

menu_opcoes = [
    "Dashboard",
    "Nova Campanha",
    "Campanhas",
    "Detalhe da Campanha",
    "Squads",
    "Contratos",
    "Relatórios"
]

pagina = st.sidebar.radio(
    "Menu",
    menu_opcoes,
    index=menu_opcoes.index(st.session_state.pagina_ativa) if st.session_state.pagina_ativa in menu_opcoes else 0
)

st.session_state.pagina_ativa = pagina

st.sidebar.markdown("---")
st.sidebar.caption("Zoy Influence Hub · V12")

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
        valor = st.number_input(
            f"Cachê {i + 1}",
            min_value=0.0,
            step=100.0,
            key=f"{prefixo}_valor_influ_{i}"
        )
        entregaveis = st.text_input(
            f"Entregáveis {i + 1}",
            placeholder="Ex: 1 Reels + 2 combos de stories",
            key=f"{prefixo}_entregaveis_influ_{i}"
        )

    with col_c:
        status_contrato = st.selectbox(
            f"Status contrato {i + 1}",
            STATUS_CONTRATO,
            key=f"{prefixo}_contrato_influ_{i}"
        )
        status_conteudo = st.selectbox(
            f"Status conteúdo {i + 1}",
            STATUS_CONTEUDO,
            key=f"{prefixo}_conteudo_influ_{i}"
        )

    observacoes = st.text_area(f"Observações do influenciador {i + 1}", key=f"{prefixo}_obs_influ_{i}")

    return {
        "arroba": arroba,
        "valor": valor,
        "entregaveis": entregaveis,
        "status_contrato": status_contrato,
        "status_conteudo": status_conteudo,
        "observacoes": observacoes
    }


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

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

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
                    "#7C3AED", "#A855F7", "#C084FC", "#DDD6FE",
                    "#8B5CF6", "#6D28D9", "#E9D5FF", "#4C1D95"
                ]
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                marker=dict(line=dict(color="#FFFFFF", width=2))
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#111827", size=12),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=0.95,
                    font=dict(color="#111827", size=11)
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

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
    st.subheader("Campanhas recentes")

    if not campanhas_df.empty:
        df_view = campanhas_df[["cliente", "marca", "campanha", "responsavel", "valor", "inicio", "prazo_pagamento", "status"]].copy()
        df_view = df_view.rename(columns={"cliente": "cliente/agência", "inicio": "mês_inicio"})
        df_view["valor"] = df_view["valor"].apply(formatar_moeda)
        st.dataframe(df_view, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma campanha cadastrada ainda.")


elif pagina == "Nova Campanha":
    st.title("Nova Campanha")
    st.markdown('<div class="sub">Cadastre uma campanha nova e já monte o squad inicial</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        cliente = st.text_input("Cliente/Agência", key="nova_cliente")
        marca = st.text_input("Marca", key="nova_marca")
        campanha = st.text_input("Nome da campanha", key="nova_campanha")
        responsavel = st.text_input("Responsável interno", key="nova_responsavel")
        valor = st.number_input("Valor total da campanha", min_value=0.0, step=100.0, key="nova_valor")

    with col2:
        mes_inicio = st.text_input("Mês de início da campanha", placeholder="Ex: Maio/2026", key="nova_mes_inicio")
        prazo_pagamento = st.text_input("Prazo de pagamento", placeholder="Ex: 45 dias após postagem", key="nova_prazo")
        drive = st.text_input("Link da pasta do Drive", key="nova_drive")
        status = st.selectbox("Status da campanha", STATUS_CAMPANHA, key="nova_status")

    briefing = st.text_area("Resumo do briefing", key="nova_briefing")
    observacoes = st.text_area("Observações internas", key="nova_observacoes")

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
    st.subheader("Influenciadores da campanha")

    tipo_campanha = st.radio(
        "Essa campanha é individual ou squad?",
        ["Individual", "Squad"],
        horizontal=True,
        key="tipo_campanha_radio"
    )

    if tipo_campanha != st.session_state.tipo_campanha_atual:
        st.session_state.tipo_campanha_atual = tipo_campanha
        st.session_state.qtd_influ_squad = 1 if tipo_campanha == "Individual" else 2
        st.rerun()

    qtd_influenciadores = 1 if tipo_campanha == "Individual" else st.session_state.qtd_influ_squad
    influenciadores_temp = []

    for i in range(int(qtd_influenciadores)):
        st.markdown(f"### Influenciador {i + 1}")
        influenciadores_temp.append(campo_influenciador(i, "nova"))
        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    if tipo_campanha == "Squad":
        col_add, col_remove, col_space = st.columns([1.2, 1.2, 4])

        with col_add:
            if st.button("+ Deseja cadastrar mais influenciadores?"):
                st.session_state.qtd_influ_squad += 1
                st.rerun()

        with col_remove:
            if st.session_state.qtd_influ_squad > 2:
                if st.button("Remover último influenciador"):
                    st.session_state.qtd_influ_squad -= 1
                    st.rerun()

    salvar = st.button("Salvar campanha")

    st.markdown('</div>', unsafe_allow_html=True)

    if salvar:
        if not cliente or not campanha:
            st.error("Preencha pelo menos Cliente/Agência e Nome da campanha.")
        else:
            campanha_id = salvar_campanha(
                cliente, marca, campanha, responsavel, valor, mes_inicio,
                prazo_pagamento, status, drive, briefing, observacoes
            )

            for influ in influenciadores_temp:
                if influ["arroba"]:
                    salvar_influenciador(
                        campanha_id,
                        influ["arroba"],
                        influ["valor"],
                        influ["entregaveis"],
                        influ["status_conteudo"],
                        influ["status_contrato"],
                        influ["observacoes"]
                    )

            st.session_state.qtd_influ_squad = 2
            st.session_state.tipo_campanha_atual = "Individual"

            st.success("Campanha cadastrada com sucesso.")


elif pagina == "Campanhas":
    campanhas_df = buscar_campanhas()

    st.title("Campanhas")
    st.markdown('<div class="sub">Acompanhe status, progresso, squad e responsáveis</div>', unsafe_allow_html=True)

    if campanhas_df.empty:
        st.info("Nenhuma campanha cadastrada ainda.")
    else:
        responsaveis = sorted(
            campanhas_df["responsavel"]
            .fillna("")
            .replace("", "Sem responsável")
            .unique()
            .tolist()
        )

        filtro_responsavel = st.selectbox(
            "Filtrar por responsável",
            ["Todos"] + responsaveis
        )

        if filtro_responsavel != "Todos":
            if filtro_responsavel == "Sem responsável":
                campanhas_df = campanhas_df[
                    campanhas_df["responsavel"].fillna("").str.strip() == ""
                ]
            else:
                campanhas_df = campanhas_df[
                    campanhas_df["responsavel"] == filtro_responsavel
                ]

        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

        if campanhas_df.empty:
            st.info("Nenhuma campanha encontrada para esse responsável.")
        else:
            for _, c in campanhas_df.iterrows():

                st.markdown('<div class="card">', unsafe_allow_html=True)

                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.subheader(c["campanha"])
                    st.write(f"**Cliente/Agência:** {c['cliente']}")
                    st.write(f"**Marca:** {c['marca'] if c['marca'] else '-'}")
                    st.write(f"**Responsável:** {c['responsavel']}")
                    st.write(f"**Mês de início:** {c['inicio']}")
                    st.write(f"**Prazo de pagamento:** {c['prazo_pagamento'] if c['prazo_pagamento'] else '-'}")

                with col2:
                    st.write("**Status**")
                    st.markdown(
                        f'<span class="status-pill">{c["status"]}</span>',
                        unsafe_allow_html=True
                    )
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
                        squad_view = squad_df[
                            ["arroba", "valor", "entregaveis", "status_conteudo", "status_contrato"]
                        ].copy()

                        squad_view["valor"] = squad_view["valor"].apply(formatar_moeda)

                        st.dataframe(
                            squad_view,
                            use_container_width=True,
                            hide_index=True
                        )

                st.markdown('</div>', unsafe_allow_html=True)

elif pagina == "Detalhe da Campanha":
    campanhas_df = buscar_campanhas()

    st.title("Detalhe da Campanha")
    st.markdown('<div class="sub">Visão completa da campanha, squad e operação</div>', unsafe_allow_html=True)

    if campanhas_df.empty:
        st.info("Nenhuma campanha cadastrada ainda.")
    else:
        campanhas_dict = {
            f"{row['campanha']} | {row['marca'] if row['marca'] else row['cliente']}": int(row["id"])
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
            st.markdown(f'<div class="info-line"><span class="purple">Cliente/Agência:</span> {campanha["cliente"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="purple">Marca:</span> {campanha["marca"] if campanha["marca"] else "-"}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="purple">Responsável:</span> {campanha["responsavel"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="purple">Mês de início:</span> {campanha["inicio"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-line"><span class="purple">Prazo de pagamento:</span> {campanha["prazo_pagamento"] if campanha["prazo_pagamento"] else "-"}</div>', unsafe_allow_html=True)
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

            with st.expander("Ler resumo do briefing"):
                st.write(campanha["briefing"] if campanha["briefing"] else "-")

            with st.expander("Ler observações internas"):
                st.write(campanha["observacoes"] if campanha["observacoes"] else "-")

        st.markdown('</div>', unsafe_allow_html=True)

        col_squad, col_status = st.columns([1.3, 1])

        with col_squad:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Squad da Campanha")

            if squad_df.empty:
                st.info("Nenhum influenciador cadastrado nesta campanha ainda.")
            else:
                df_squad = squad_df[["arroba", "valor", "entregaveis", "status_conteudo", "status_contrato"]].copy()
                df_squad["valor"] = df_squad["valor"].apply(formatar_moeda)
                st.dataframe(df_squad, use_container_width=True, hide_index=True)

            with st.expander("Adicionar influenciador nesta campanha"):
                base_influs = buscar_influenciadores_base()
                opcoes = ["Cadastrar novo"] + base_influs

                escolha_influ = st.selectbox("Influenciador", opcoes, key="detalhe_select_influ")

                if escolha_influ == "Cadastrar novo":
                    arroba = st.text_input("@ do influenciador", key="detalhe_novo_arroba")
                else:
                    arroba = escolha_influ
                    st.caption(f"Selecionado: {arroba}")

                valor = st.number_input("Cachê", min_value=0.0, step=100.0, key="detalhe_valor_influ")
                entregaveis = st.text_input("Entregáveis", placeholder="Ex: 1 Reels + 2 combos de stories", key="detalhe_entregaveis")
                status_conteudo = st.selectbox("Status do conteúdo", STATUS_CONTEUDO, key="detalhe_status_conteudo")
                status_contrato = st.selectbox("Status do contrato", STATUS_CONTRATO, key="detalhe_status_contrato")
                observacoes = st.text_area("Observações", key="detalhe_obs_influ")

                if st.button("Salvar influenciador"):
                    if not arroba:
                        st.error("Preencha o @ do influenciador.")
                    else:
                        salvar_influenciador(
                            campanha_id, arroba, valor, entregaveis,
                            status_conteudo, status_contrato, observacoes
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

            st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
            st.subheader("Configurações da campanha")

            with st.expander("Editar campanha"):
                with st.form("form_editar_campanha"):
                    edit_cliente = st.text_input("Cliente/Agência", value=campanha["cliente"])
                    edit_marca = st.text_input("Marca", value=campanha["marca"] if campanha["marca"] else "")
                    edit_campanha = st.text_input("Nome da campanha", value=campanha["campanha"])
                    edit_responsavel = st.text_input("Responsável interno", value=campanha["responsavel"])
                    edit_valor = st.number_input("Valor total", min_value=0.0, step=100.0, value=float(campanha["valor"]))
                    edit_mes = st.text_input("Mês de início", value=campanha["inicio"])
                    edit_prazo = st.text_input("Prazo de pagamento", value=campanha["prazo_pagamento"] if campanha["prazo_pagamento"] else "")
                    edit_status = st.selectbox(
                        "Status",
                        STATUS_CAMPANHA,
                        index=STATUS_CAMPANHA.index(campanha["status"]) if campanha["status"] in STATUS_CAMPANHA else 0
                    )
                    edit_drive = st.text_input("Link do Drive", value=campanha["drive"] if campanha["drive"] else "")
                    edit_briefing = st.text_area("Resumo do briefing", value=campanha["briefing"] if campanha["briefing"] else "")
                    edit_obs = st.text_area("Observações internas", value=campanha["observacoes"] if campanha["observacoes"] else "")

                    salvar_edicao = st.form_submit_button("Salvar alterações")

                    if salvar_edicao:
                        atualizar_campanha(
                            campanha_id, edit_cliente, edit_marca, edit_campanha, edit_responsavel,
                            edit_valor, edit_mes, edit_prazo, edit_status,
                            edit_drive, edit_briefing, edit_obs
                        )
                        st.success("Campanha atualizada.")
                        st.rerun()

            with st.expander("Excluir campanha"):
                st.markdown('<div class="danger-note">Essa ação apaga a campanha e todos os influenciadores vinculados.</div>', unsafe_allow_html=True)
                confirmar = st.text_input("Digite EXCLUIR para confirmar")

                if st.button("Excluir campanha definitivamente"):
                    if confirmar == "EXCLUIR":
                        excluir_campanha(campanha_id)
                        st.success("Campanha excluída.")
                        st.rerun()
                    else:
                        st.error("Confirmação incorreta. Digite EXCLUIR.")

            st.markdown('</div>', unsafe_allow_html=True)


elif pagina == "Squads":
    campanhas_df = buscar_campanhas()

    st.title("Squads")
    st.markdown('<div class="sub">Cadastre influenciadores por campanha e acompanhe entregas</div>', unsafe_allow_html=True)

    if campanhas_df.empty:
        st.warning("Cadastre uma campanha antes de adicionar influenciadores.")
    else:
        campanhas_dict = {
            f"{row['campanha']} | {row['marca'] if row['marca'] else row['cliente']}": int(row["id"])
            for _, row in campanhas_df.iterrows()
        }

        st.markdown('<div class="card">', unsafe_allow_html=True)

        campanha_escolhida = st.selectbox("Campanha", list(campanhas_dict.keys()))

        base_influs = buscar_influenciadores_base()
        opcoes = ["Cadastrar novo"] + base_influs

        escolha_influ = st.selectbox("Influenciador", opcoes)

        if escolha_influ == "Cadastrar novo":
            arroba = st.text_input("@ do influenciador")
        else:
            arroba = escolha_influ
            st.caption(f"Selecionado: {arroba}")

        col1, col2 = st.columns(2)

        with col1:
            valor = st.number_input("Cachê", min_value=0.0, step=100.0)
            entregaveis = st.text_input("Entregáveis", placeholder="Ex: 1 Reels + 2 combos de stories")

        with col2:
            status_conteudo = st.selectbox("Status do conteúdo", STATUS_CONTEUDO)
            status_contrato = st.selectbox("Status do contrato", STATUS_CONTRATO)

        observacoes = st.text_area("Observações")

        if st.button("Salvar influenciador"):
            if not arroba:
                st.error("Preencha o @ do influenciador.")
            else:
                campanha_id = campanhas_dict[campanha_escolhida]
                salvar_influenciador(
                    campanha_id, arroba, valor, entregaveis,
                    status_conteudo, status_contrato, observacoes
                )
                st.success("Influenciador cadastrado com sucesso.")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
        st.subheader("Influenciadores cadastrados")

        influ_df = buscar_influenciadores()

        if influ_df.empty:
            st.info("Nenhum influenciador cadastrado ainda.")
        else:
            influ_view = influ_df[["campanha", "cliente", "marca", "arroba", "valor", "entregaveis", "status_conteudo", "status_contrato", "observacoes"]].copy()
            influ_view["valor"] = influ_view["valor"].apply(formatar_moeda)
            st.dataframe(influ_view, use_container_width=True, hide_index=True)


elif pagina == "Contratos":
    influ_df = buscar_influenciadores()

    st.title("Contratos")
    st.markdown('<div class="sub">Visão para jurídico e administrativo acompanharem o status dos contratos</div>', unsafe_allow_html=True)

    if influ_df.empty:
        st.info("Nenhum influenciador cadastrado ainda.")
    else:
        total_contratos = len(influ_df)
        assinados = len(influ_df[influ_df["status_contrato"] == "Assinado"])
        enviados = len(influ_df[influ_df["status_contrato"] == "Enviado"])
        nao_enviados = len(influ_df[influ_df["status_contrato"] == "Não enviado"])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", total_contratos)
        col2.metric("Assinados", assinados)
        col3.metric("Enviados", enviados)
        col4.metric("Não enviados", nao_enviados)

        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

        filtro_status = st.selectbox("Filtrar por status", ["Todos"] + STATUS_CONTRATO)

        contratos_df = influ_df[[
            "campanha",
            "cliente",
            "marca",
            "responsavel",
            "arroba",
            "status_contrato",
            "prazo_pagamento",
            "entregaveis"
        ]].copy()

        if filtro_status != "Todos":
            contratos_df = contratos_df[contratos_df["status_contrato"] == filtro_status]

        st.dataframe(contratos_df, use_container_width=True, hide_index=True)


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
                "cliente/agência": c["cliente"],
                "marca": c["marca"] if c["marca"] else "-",
                "responsavel": c["responsavel"],
                "mês_inicio": c["inicio"],
                "prazo_pagamento": c["prazo_pagamento"] if c["prazo_pagamento"] else "-",
                "status_campanha": c["status"],
                "relatorio": status_relatorio
            })

        df_rel = pd.DataFrame(relatorios)
        st.dataframe(df_rel, use_container_width=True, hide_index=True)
