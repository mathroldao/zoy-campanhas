import sqlite3
from datetime import date
import pandas as pd
import streamlit as st

DB_NAME = "zoy_campanhas.db"

st.set_page_config(page_title="Zoy Campanhas", page_icon="⚡", layout="wide")


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

h1, h2, h3, h4, p, span {
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
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -2px;
    color: white;
    margin-bottom: 20px;
}

.sub {
    color: #94A3B8 !important;
    margin-top: -10px;
    margin-bottom: 25px;
}

hr {
    border-color: rgba(255,255,255,0.08);
}

div[data-baseweb="input"],
div[data-baseweb="select"],
textarea {
    border-radius: 14px !important;
}

.stDataFrame {
    border-radius: 16px;
    overflow: hidden;
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

    conn.commit()
    conn.close()


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

    conn.commit()
    conn.close()


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


criar_tabelas()


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
st.sidebar.caption("Zoy Campaign OS · SQLite V1")


# =========================
# DASHBOARD
# =========================
if pagina == "Dashboard":
    campanhas_df = buscar_campanhas()
    influ_df = buscar_influenciadores()

    st.title("Dashboard de Campanhas")
    st.markdown('<div class="sub">Visão geral das campanhas ativas da Agência Zoy</div>', unsafe_allow_html=True)

    total = len(campanhas_df)
    ativas = len(campanhas_df[campanhas_df["status"] != "Finalizado"]) if total > 0 else 0
    finalizadas = len(campanhas_df[campanhas_df["status"] == "Finalizado"]) if total > 0 else 0
    pendentes = len(campanhas_df[campanhas_df["status"].isin(["Conteúdo pendente", "Conteúdo em aprovação", "Relatório pendente"])]) if total > 0 else 0
    investimento = campanhas_df["valor"].sum() if total > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Campanhas totais", total)
    col2.metric("Campanhas ativas", ativas)
    col3.metric("Pendências", pendentes)
    col4.metric("Finalizadas", finalizadas)
    col5.metric("Investimento total", f"R$ {investimento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.markdown("---")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.subheader("Campanhas recentes")

        if not campanhas_df.empty:
            st.dataframe(
                campanhas_df[["cliente", "campanha", "responsavel", "valor", "inicio", "fim", "status", "progresso"]],
                use_container_width=True,
                hide_index=True
            )
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
        st.write(f"Influenciadores cadastrados: {len(influ_df)}")
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
        observacoes = st.text_area("Observações internas")

        salvar = st.form_submit_button("Salvar campanha")

        if salvar:
            if not cliente or not campanha:
                st.error("Preencha pelo menos Cliente e Nome da campanha.")
            else:
                salvar_campanha(cliente, campanha, responsavel, valor, inicio, fim, status, drive, briefing, observacoes)
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
                st.write(c["status"])
                st.progress(int(c["progresso"]) / 100)

            with col3:
                valor_formatado = f"R$ {c['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                st.write("**Valor**")
                st.subheader(valor_formatado)

                if c["drive"]:
                    st.link_button("Abrir Drive", c["drive"])

            with st.expander("Ver detalhes da campanha"):
                st.write("**Briefing:**")
                st.write(c["briefing"] if c["briefing"] else "Sem briefing cadastrado.")

                st.write("**Observações:**")
                st.write(c["observacoes"] if c["observacoes"] else "Sem observações.")

                st.markdown("---")
                st.write("**Squad da campanha:**")

                squad_df = buscar_influenciadores_por_campanha(int(c["id"]))

                if squad_df.empty:
                    st.info("Nenhum influenciador cadastrado nesta campanha ainda.")
                else:
                    st.dataframe(
                        squad_df[["nome", "arroba", "valor", "entregaveis", "postagem", "status_conteudo", "status_contrato"]],
                        use_container_width=True,
                        hide_index=True
                    )

                st.markdown("---")

                opcoes_status = [
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

                novo_status = st.selectbox(
                    "Atualizar status",
                    opcoes_status,
                    index=opcoes_status.index(c["status"]) if c["status"] in opcoes_status else 0,
                    key=f"status_{c['id']}"
                )

                if st.button("Salvar novo status", key=f"btn_status_{c['id']}"):
                    atualizar_status_campanha(int(c["id"]), novo_status)
                    st.success("Status atualizado.")
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)


# =========================
# INFLUENCIADORES
# =========================
elif pagina == "Influenciadores":
    campanhas_df = buscar_campanhas()

    st.title("Influenciadores")
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
            st.dataframe(influ_df, use_container_width=True, hide_index=True)


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
            elif c["status"] == "Relatório pendente":
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
