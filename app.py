import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

DB_NAME = "zoy_campanhas.db"

st.set_page_config(
    page_title="Zoy Hub",
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
    CREATE TABLE IF NOT EXISTS observacoes_campanha (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campanha_id INTEGER,
        usuario TEXT,
        observacao TEXT,
        data TEXT,
        FOREIGN KEY(campanha_id) REFERENCES campanhas(id)
    )
    
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS observacoes_contrato (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        influenciador_id INTEGER,
        usuario TEXT,
        observacao TEXT,
        data TEXT,
        FOREIGN KEY(influenciador_id) REFERENCES influenciadores(id)
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agenda_entregas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campanha_id INTEGER,
        tipo TEXT,
        data TEXT,
        horario TEXT,
        responsavel TEXT,
        influenciador TEXT,
        descricao TEXT,
        status TEXT DEFAULT 'Pendente',
        FOREIGN KEY(campanha_id) REFERENCES campanhas(id)
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
    "Roteiro Pendente",
    "Roteiro em Aprovação",
    "Conteúdo Pendente",
    "Conteúdo em Aprovação",
    "Ajuste Solicitado",
    "Aprovado",
    "Postado",
    "Relatório Pendente",
    "Campanha Pausada",
    "Campanha Declinada",
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

EMAIL_RESPONSAVEIS = {
    "jean": "jean@agenciazoy.com",
    "rafaela": "rafaela@agenciazoy.com",
    "taila": "taila@agenciazoy.com",
    "camila": "camila@agenciazoy.com",
    "matheus": "matheus@agenciazoy.com",
    "financeiro": "financeiro@agenciazoy.com",
    "contato": "contato@agenciazoy.com",
}

RESPONSAVEIS_FIXOS = ["Jean", "Rafaela", "Taila", "Camila", "Financeiro", "Matheus"]


def calcular_progresso(status):
    mapa = {
        "Mapeamento": 10,
        "Atendimento Iniciado": 20,
        "Contrato Enviado": 30,
        "Roteiro Pendente": 40,
        "Roteiro em Aprovação": 50,
        "Conteúdo Pendente": 60,
        "Conteúdo em Aprovação": 70,
        "Ajuste Solicitado": 75,
        "Aprovado": 80,
        "Postado": 90,
        "Relatório Pendente": 95,
        "Campanha Pausada": 50,
        "Campanha Declinada": 0,
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


def restaurar_backup(campanhas_file, influenciadores_file):
    conn = conectar()
    cursor = conn.cursor()

    campanhas_df = pd.read_csv(campanhas_file)
    influ_df = pd.read_csv(influenciadores_file)

    cursor.execute("DELETE FROM influenciadores")
    cursor.execute("DELETE FROM campanhas")

    for _, row in campanhas_df.iterrows():
        cursor.execute("""
            INSERT INTO campanhas (
                id, cliente, campanha, responsavel, valor, inicio, fim,
                status, progresso, drive, briefing, observacoes,
                prazo_pagamento, marca
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(row["id"]),
            row["cliente"] if "cliente" in row and pd.notna(row["cliente"]) else "",
            row["campanha"] if "campanha" in row and pd.notna(row["campanha"]) else "",
            row["responsavel"] if "responsavel" in row and pd.notna(row["responsavel"]) else "",
            float(row["valor"]) if "valor" in row and pd.notna(row["valor"]) else 0,
            row["inicio"] if "inicio" in row and pd.notna(row["inicio"]) else "",
            row["fim"] if "fim" in row and pd.notna(row["fim"]) else "",
            row["status"] if "status" in row and pd.notna(row["status"]) else "",
            int(row["progresso"]) if "progresso" in row and pd.notna(row["progresso"]) else 0,
            row["drive"] if "drive" in row and pd.notna(row["drive"]) else "",
            row["briefing"] if "briefing" in row and pd.notna(row["briefing"]) else "",
            row["observacoes"] if "observacoes" in row and pd.notna(row["observacoes"]) else "",
            row["prazo_pagamento"] if "prazo_pagamento" in row and pd.notna(row["prazo_pagamento"]) else "",
            row["marca"] if "marca" in row and pd.notna(row["marca"]) else ""
        ))

    for _, row in influ_df.iterrows():
        cursor.execute("""
            INSERT INTO influenciadores (
                id, campanha_id, nome, arroba, valor, entregaveis,
                postagem, status_conteudo, status_contrato, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(row["id"]),
            int(row["campanha_id"]),
            row["nome"] if "nome" in row and pd.notna(row["nome"]) else "",
            row["arroba"] if "arroba" in row and pd.notna(row["arroba"]) else "",
            float(row["valor"]) if "valor" in row and pd.notna(row["valor"]) else 0,
            row["entregaveis"] if "entregaveis" in row and pd.notna(row["entregaveis"]) else "",
            row["postagem"] if "postagem" in row and pd.notna(row["postagem"]) else "",
            row["status_conteudo"] if "status_conteudo" in row and pd.notna(row["status_conteudo"]) else "",
            row["status_contrato"] if "status_contrato" in row and pd.notna(row["status_contrato"]) else "",
            row["observacoes"] if "observacoes" in row and pd.notna(row["observacoes"]) else ""
        ))

    cursor.execute("DELETE FROM influenciadores_base")
    cursor.execute("""
    INSERT OR IGNORE INTO influenciadores_base (arroba)
    SELECT DISTINCT arroba FROM influenciadores
    WHERE arroba IS NOT NULL AND arroba != ''
    """)

    conn.commit()
    conn.close()

def salvar_observacao(campanha_id, usuario, observacao):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    from datetime import datetime
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    cursor.execute("""
        INSERT INTO observacoes_campanha (campanha_id, usuario, observacao, data)
        VALUES (?, ?, ?, ?)
    """, (campanha_id, usuario, observacao, data))

    conn.commit()
    conn.close()


def buscar_observacoes(campanha_id):
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query("""
        SELECT usuario, observacao, data
        FROM observacoes_campanha
        WHERE campanha_id = ?
        ORDER BY id DESC
    """, conn, params=(campanha_id,))

    conn.close()
    return df


def salvar_item_agenda(campanha_id, tipo, data, horario, responsavel, influenciador, descricao, status):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agenda_entregas (
            campanha_id, tipo, data, horario, responsavel, influenciador, descricao, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        campanha_id, tipo, data, horario, responsavel, influenciador, descricao, status
    ))

    conn.commit()
    conn.close()


def buscar_agenda_campanha(campanha_id):
    conn = conectar()

    df = pd.read_sql_query("""
        SELECT *
        FROM agenda_entregas
        WHERE campanha_id = ?
        ORDER BY data ASC, horario ASC
    """, conn, params=(campanha_id,))

    conn.close()
    return df


def buscar_agenda_hoje():
    from datetime import date

    hoje = date.today().strftime("%Y-%m-%d")

    conn = conectar()

    df = pd.read_sql_query("""
        SELECT 
            agenda_entregas.id,
            agenda_entregas.tipo,
            agenda_entregas.data,
            agenda_entregas.horario,
            agenda_entregas.responsavel,
            agenda_entregas.influenciador,
            agenda_entregas.descricao,
            agenda_entregas.status,
            campanhas.campanha,
            campanhas.cliente,
            campanhas.marca
        FROM agenda_entregas
        LEFT JOIN campanhas ON agenda_entregas.campanha_id = campanhas.id
        WHERE agenda_entregas.data = ?
        ORDER BY agenda_entregas.horario ASC
    """, conn, params=(hoje,))

    conn.close()
    return df


def concluir_item_agenda(item_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE agenda_entregas
        SET status = 'Concluído'
        WHERE id = ?
    """, (item_id,))

    conn.commit()
    conn.close()


def resolver_email_responsavel(responsavel):
    responsavel = (responsavel or "").strip()

    if "@" in responsavel:
        return responsavel

    chave = responsavel.lower().split()[0] if responsavel else ""
    return EMAIL_RESPONSAVEIS.get(chave)


def enviar_email_nova_campanha(cliente, marca, campanha, responsavel, inicio, prazo_pagamento, status, drive):
    destinatario = resolver_email_responsavel(responsavel)

    if not destinatario:
        return False, "Responsável sem e-mail configurado."

    try:
        config_email = st.secrets.get("email", {})
        remetente = config_email.get("remetente")
        senha_app = config_email.get("senha_app")
        smtp_server = config_email.get("smtp_server", "smtp.gmail.com")
        smtp_port = int(config_email.get("smtp_port", 587))
        link_hub = config_email.get("link_hub", "")

        if not remetente or not senha_app:
            return False, "E-mail não configurado no Streamlit Secrets."

        assunto = f"Nova campanha atribuída no Zoy Hub: {campanha}"

        corpo = f"""
Olá!

Uma nova campanha foi cadastrada no Zoy Hub sob sua responsabilidade.

Campanha: {campanha}
Cliente/Agência: {cliente}
Marca: {marca if marca else '-'}
Mês de início: {inicio if inicio else '-'}
Prazo de pagamento: {prazo_pagamento if prazo_pagamento else '-'}
Status inicial: {status}

Acesse o Zoy Hub para acompanhar os detalhes, squad, contratos, agenda e observações.
{link_hub}

Zoy Hub
"""

        msg = MIMEMultipart()
        msg["From"] = remetente
        msg["To"] = destinatario
        msg["Subject"] = assunto
        msg.attach(MIMEText(corpo, "plain", "utf-8"))

        servidor = smtplib.SMTP(smtp_server, smtp_port)
        servidor.starttls()
        servidor.login(remetente, senha_app)
        servidor.sendmail(remetente, destinatario, msg.as_string())
        servidor.quit()

        return True, f"E-mail enviado para {destinatario}."

    except Exception as erro:
        return False, f"Não foi possível enviar o e-mail: {erro}"


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



def atualizar_status_contrato(influenciador_id, novo_status):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE influenciadores
        SET status_contrato = ?
        WHERE id = ?
    """, (novo_status, influenciador_id))

    conn.commit()
    conn.close()


def salvar_observacao_contrato(influenciador_id, usuario, observacao):
    conn = conectar()
    cursor = conn.cursor()

    from datetime import datetime
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    cursor.execute("""
        INSERT INTO observacoes_contrato (influenciador_id, usuario, observacao, data)
        VALUES (?, ?, ?, ?)
    """, (influenciador_id, usuario, observacao, data))

    conn.commit()
    conn.close()


def buscar_observacoes_contrato(influenciador_id, limite=2):
    conn = conectar()

    df = pd.read_sql_query("""
        SELECT usuario, observacao, data
        FROM observacoes_contrato
        WHERE influenciador_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, conn, params=(influenciador_id, limite))

    conn.close()
    return df


def contar_observacoes_contrato(influenciador_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM observacoes_contrato
        WHERE influenciador_id = ?
    """, (influenciador_id,))
    total = cursor.fetchone()[0]
    conn.close()
    return total


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
        "<h1 style='text-align:center;'>Zoy Hub</h1>",
        unsafe_allow_html=True
    )

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
st.sidebar.markdown('<div class="sidebar-caption">Zoy Hub</div>', unsafe_allow_html=True)

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
st.sidebar.caption("Zoy Hub")


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

    agenda_hoje_df = buscar_agenda_hoje()

    st.subheader("Entregas e postagens de hoje")

    if agenda_hoje_df.empty:
        st.info("Nenhuma entrega ou postagem prevista para hoje.")
    else:
        for _, item in agenda_hoje_df.iterrows():
            st.markdown('<div class="mini-card">', unsafe_allow_html=True)
            st.write(f"**{item['horario'] if item['horario'] else '-'} | {item['tipo']}**")
            st.write(f"**Campanha:** {item['campanha']}")
            st.write(f"**Marca:** {item['marca'] if item['marca'] else '-'}")
            st.write(f"**Influenciador:** {item['influenciador'] if item['influenciador'] else '-'}")
            st.write(f"**Responsável:** {item['responsavel'] if item['responsavel'] else '-'}")
            st.write(f"**Status:** {item['status']}")

            if item["descricao"]:
                st.caption(item["descricao"])

            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

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
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Ferramentas administrativas")

    admin1, admin2, admin3 = st.columns([1, 1, 6])

    with admin1:
        st.download_button(
            label="Backup campanhas",
            data=campanhas_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="backup_campanhas_zoy.csv",
            mime="text/csv"
        )

    with admin2:
        st.download_button(
            label="Backup influenciadores",
            data=influ_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="backup_influenciadores_zoy.csv",
            mime="text/csv"
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    with st.expander("Restaurar backup"):
        st.caption("Use esta área somente para recuperar dados a partir dos arquivos CSV de backup.")

        backup_campanhas = st.file_uploader(
            "Arquivo CSV de campanhas",
            type=["csv"],
            key="upload_backup_campanhas"
        )

        backup_influenciadores = st.file_uploader(
            "Arquivo CSV de influenciadores",
            type=["csv"],
            key="upload_backup_influenciadores"
        )

        if st.button("Restaurar backup agora"):
            if backup_campanhas is None or backup_influenciadores is None:
                st.error("Envie os dois arquivos de backup antes de restaurar.")
            else:
                restaurar_backup(backup_campanhas, backup_influenciadores)
                st.success("Backup restaurado com sucesso.")
                st.rerun()

elif pagina == "Nova Campanha":
    st.title("Nova Campanha")
    st.markdown('<div class="sub">Cadastre uma campanha nova e já monte o squad inicial</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        cliente = st.text_input("Cliente/Agência", key="nova_cliente")
        marca = st.text_input("Marca", key="nova_marca")
        campanha = st.text_input("Nome da campanha", key="nova_campanha")
        responsavel = st.selectbox(
            "Responsável interno",
            RESPONSAVEIS_FIXOS,
            key="nova_responsavel"
        )
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

            email_enviado, mensagem_email = enviar_email_nova_campanha(
                cliente,
                marca,
                campanha,
                responsavel,
                mes_inicio,
                prazo_pagamento,
                status,
                drive
            )

            if email_enviado:
                st.info(mensagem_email)
            else:
                st.warning(mensagem_email)

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
            "Filtrar campanhas por responsável",
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
        responsaveis = sorted(
            campanhas_df["responsavel"]
            .fillna("")
            .replace("", "Sem responsável")
            .unique()
            .tolist()
        )

        filtro_responsavel_detalhe = st.selectbox(
            "Filtrar por responsável",
            ["Todos"] + responsaveis,
            key="filtro_responsavel_detalhe"
        )

        if filtro_responsavel_detalhe != "Todos":
            if filtro_responsavel_detalhe == "Sem responsável":
                campanhas_df = campanhas_df[
                    campanhas_df["responsavel"].fillna("").str.strip() == ""
                ]
            else:
                campanhas_df = campanhas_df[
                    campanhas_df["responsavel"] == filtro_responsavel_detalhe
                ]

        if campanhas_df.empty:
            st.info("Nenhuma campanha encontrada para esse responsável.")

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
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Observações da Campanha")

        nova_observacao = st.text_area(
            "Adicionar atualização",
            placeholder="Ex: Cliente pediu ajuste no roteiro / conteúdo enviado para aprovação / aguardando retorno...",
            key=f"obs_campanha_{campanha_id}"
        )

        if st.button("Salvar observação", key=f"salvar_obs_{campanha_id}"):
            if nova_observacao.strip():
                salvar_observacao(
                    campanha_id,
                    st.session_state.usuario_logado if "usuario_logado" in st.session_state else "Equipe Zoy",
                    nova_observacao
                )
                st.success("Observação salva.")
                st.rerun()
            else:
                st.error("Digite uma observação antes de salvar.")

        obs_df = buscar_observacoes(campanha_id)

        if obs_df.empty:
            st.info("Nenhuma observação registrada ainda.")
        else:
            for _, obs in obs_df.iterrows():
                st.markdown(
                    f"""
                    <div class="mini-card">
                        <div class="small-muted">{obs['data']} • {obs['usuario']}</div>
                        <div style="margin-top:8px;">{obs['observacao']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Agenda da Campanha")

        with st.expander("Adicionar item na agenda"):
            col_ag1, col_ag2 = st.columns(2)

            with col_ag1:
                tipo_agenda = st.selectbox(
                    "Tipo",
                    ["Postagem", "Entrega de roteiro", "Entrega de conteúdo", "Reunião", "Aprovação", "Outro"],
                    key=f"tipo_agenda_{campanha_id}"
                )

                data_agenda = st.date_input(
                    "Data",
                    key=f"data_agenda_{campanha_id}"
                )

                horario_agenda = st.text_input(
                    "Horário",
                    placeholder="Ex: 14:00",
                    key=f"horario_agenda_{campanha_id}"
                )

            with col_ag2:
                responsavel_agenda = st.text_input(
                    "Responsável",
                    value=campanha["responsavel"] if campanha["responsavel"] else "",
                    key=f"responsavel_agenda_{campanha_id}"
                )

                influenciador_agenda = st.text_input(
                    "Influenciador",
                    placeholder="Ex: @influenciador",
                    key=f"influ_agenda_{campanha_id}"
                )

                status_agenda = st.selectbox(
                    "Status",
                    ["Pendente", "Concluído", "Atrasado"],
                    key=f"status_agenda_{campanha_id}"
                )

            descricao_agenda = st.text_area(
                "Descrição",
                placeholder="Ex: Postagem do Reels / envio do roteiro / prazo de aprovação",
                key=f"descricao_agenda_{campanha_id}"
            )

            if st.button("Salvar item na agenda", key=f"salvar_agenda_{campanha_id}"):
                salvar_item_agenda(
                    campanha_id,
                    tipo_agenda,
                    str(data_agenda),
                    horario_agenda,
                    responsavel_agenda,
                    influenciador_agenda,
                    descricao_agenda,
                    status_agenda
                )
                st.success("Item adicionado na agenda.")
                st.rerun()

        agenda_df = buscar_agenda_campanha(campanha_id)

        if agenda_df.empty:
            st.info("Nenhum item cadastrado na agenda desta campanha ainda.")
        else:
            for _, item in agenda_df.iterrows():
                st.markdown('<div class="mini-card">', unsafe_allow_html=True)

                st.write(f"**{item['data']} | {item['horario'] if item['horario'] else '-'} | {item['tipo']}**")
                st.write(f"**Influenciador:** {item['influenciador'] if item['influenciador'] else '-'}")
                st.write(f"**Responsável:** {item['responsavel'] if item['responsavel'] else '-'}")
                st.write(f"**Status:** {item['status']}")

                if item["descricao"]:
                    st.caption(item["descricao"])

                if item["status"] != "Concluído":
                    if st.button("Marcar como concluído", key=f"concluir_agenda_{item['id']}"):
                        concluir_item_agenda(int(item["id"]))
                        st.success("Item concluído.")
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

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
                    responsavel_atual = campanha["responsavel"] if campanha["responsavel"] in RESPONSAVEIS_FIXOS else RESPONSAVEIS_FIXOS[0]
                    edit_responsavel = st.selectbox(
                        "Responsável interno",
                        RESPONSAVEIS_FIXOS,
                        index=RESPONSAVEIS_FIXOS.index(responsavel_atual),
                        key=f"edit_responsavel_{campanha_id}"
                    )
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
    st.markdown('<div class="sub">Organize os contratos por status, em formato de quadro</div>', unsafe_allow_html=True)

    if influ_df.empty:
        st.info("Nenhum influenciador cadastrado ainda.")
    else:
        total_contratos = len(influ_df)
        assinados = len(influ_df[influ_df["status_contrato"] == "Assinado"])
        enviados = len(influ_df[influ_df["status_contrato"] == "Enviado"])
        nao_enviados = len(influ_df[influ_df["status_contrato"] == "Não enviado"])

        resumo1, resumo2, resumo3, resumo4 = st.columns(4)
        resumo1.metric("Total", total_contratos)
        resumo2.metric("Não enviados", nao_enviados)
        resumo3.metric("Enviados", enviados)
        resumo4.metric("Assinados", assinados)

        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        colunas_status = {
            "Não enviado": {
                "coluna": col1,
                "cor": "#F59E0B",
                "bg": "rgba(245,158,11,0.08)",
                "border": "rgba(245,158,11,0.28)",
                "icone": "Pendente"
            },
            "Enviado": {
                "coluna": col2,
                "cor": "#2563EB",
                "bg": "rgba(37,99,235,0.07)",
                "border": "rgba(37,99,235,0.22)",
                "icone": "Enviado"
            },
            "Assinado": {
                "coluna": col3,
                "cor": "#16A34A",
                "bg": "rgba(22,163,74,0.07)",
                "border": "rgba(22,163,74,0.22)",
                "icone": "Assinado"
            }
        }

        def texto_seguro(item, campo):
            valor = item[campo] if campo in item.index else ""
            if pd.isna(valor) or valor == "":
                return "-"
            return str(valor)

        def texto_curto(valor, limite=58):
            valor = str(valor or "-")
            if valor == "nan":
                return "-"
            return valor if len(valor) <= limite else valor[:limite - 3] + "..."

        for status_nome, config in colunas_status.items():
            coluna = config["coluna"]
            cor = config["cor"]
            bg = config["bg"]
            border = config["border"]

            with coluna:
                df_status = influ_df[influ_df["status_contrato"] == status_nome]

                st.markdown(
                    f"""
                    <div style="
                        background:{bg};
                        border:1px solid {border};
                        border-radius:22px;
                        padding:16px 16px 12px 16px;
                        margin-bottom:14px;
                    ">
                        <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
                            <div style="font-size:21px; font-weight:950; color:{cor};">{status_nome}</div>
                            <div style="
                                background:white;
                                border:1px solid {border};
                                color:{cor};
                                border-radius:999px;
                                padding:4px 10px;
                                font-weight:900;
                                font-size:13px;
                            ">{len(df_status)}</div>
                        </div>
                        <div style="font-size:13px; color:#6B7280; margin-top:4px;">contrato(s)</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if df_status.empty:
                    st.info("Nenhum contrato aqui.")
                else:
                    for _, item in df_status.iterrows():
                        influ_id = int(item["id"])
                        obs_total = contar_observacoes_contrato(influ_id)
                        obs_label = f" • {obs_total} obs" if obs_total else ""

                        st.markdown(
                            f"""
                            <div style="
                                background:#FFFFFF;
                                border:1px solid rgba(17,24,39,0.10);
                                border-left:5px solid {cor};
                                border-radius:18px;
                                padding:14px 14px 12px 14px;
                                margin-bottom:8px;
                                box-shadow:0 8px 20px rgba(17,24,39,0.045);
                            ">
                                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
                                    <div style="font-size:17px; font-weight:950; color:#111827;">{texto_seguro(item, 'arroba')}</div>
                                    <span style="
                                        background:{bg};
                                        color:{cor};
                                        border:1px solid {border};
                                        border-radius:999px;
                                        padding:3px 8px;
                                        font-size:11px;
                                        font-weight:900;
                                        white-space:nowrap;
                                    ">{status_nome}</span>
                                </div>
                                <div style="font-size:13px; color:#374151; margin-top:8px; line-height:1.45;">
                                    <b>{texto_seguro(item, 'campanha')}</b> • {texto_seguro(item, 'cliente')}<br>
                                    {texto_curto(texto_seguro(item, 'entregaveis'), 70)}
                                </div>
                                <div style="font-size:12px; color:#6B7280; margin-top:8px;">
                                    Resp.: {texto_seguro(item, 'responsavel')}{obs_label}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        with st.expander("Ver mais", expanded=False):
                            st.markdown(
                                f"""
                                <div style="font-size:14px; line-height:1.7; color:#111827;">
                                    <b>Campanha:</b> {texto_seguro(item, 'campanha')}<br>
                                    <b>Cliente:</b> {texto_seguro(item, 'cliente')}<br>
                                    <b>Marca:</b> {texto_seguro(item, 'marca')}<br>
                                    <b>Responsável:</b> {texto_seguro(item, 'responsavel')}<br>
                                    <b>Entregáveis:</b> {texto_seguro(item, 'entregaveis')}<br>
                                    <b>Prazo:</b> {texto_seguro(item, 'prazo_pagamento')}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            novo_status = st.selectbox(
                                "Status do contrato",
                                STATUS_CONTRATO,
                                index=STATUS_CONTRATO.index(item["status_contrato"]) if item["status_contrato"] in STATUS_CONTRATO else 0,
                                key=f"contrato_status_{influ_id}"
                            )

                            col_btn1, col_btn2 = st.columns([1, 1])

                            with col_btn1:
                                if st.button("Salvar", key=f"salvar_status_contrato_{influ_id}"):
                                    atualizar_status_contrato(influ_id, novo_status)
                                    st.success("Status atualizado.")
                                    st.rerun()

                            with col_btn2:
                                if item["status_contrato"] != "Assinado":
                                    if st.button("Assinado", key=f"assinar_contrato_{influ_id}"):
                                        atualizar_status_contrato(influ_id, "Assinado")
                                        st.success("Contrato marcado como assinado.")
                                        st.rerun()

                            st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
                            st.caption("Observações do contrato")

                            nova_obs = st.text_area(
                                "Adicionar observação",
                                placeholder="Ex: contrato enviado / aguardando assinatura / ajuste solicitado...",
                                height=70,
                                key=f"nova_obs_contrato_{influ_id}"
                            )

                            if st.button("Salvar observação", key=f"salvar_obs_contrato_{influ_id}"):
                                if nova_obs.strip():
                                    salvar_observacao_contrato(
                                        influ_id,
                                        st.session_state.usuario_logado if "usuario_logado" in st.session_state else "Equipe Zoy",
                                        nova_obs.strip()
                                    )
                                    st.success("Observação salva.")
                                    st.rerun()
                                else:
                                    st.error("Digite uma observação antes de salvar.")

                            obs_df = buscar_observacoes_contrato(influ_id, limite=2)

                            if obs_df.empty:
                                st.caption("Nenhuma observação ainda.")
                            else:
                                for _, obs in obs_df.iterrows():
                                    st.markdown(
                                        f"""
                                        <div style="
                                            background:#F9FAFB;
                                            border:1px solid rgba(17,24,39,0.08);
                                            border-radius:14px;
                                            padding:10px 12px;
                                            margin-top:8px;
                                        ">
                                            <div style="font-size:12px; color:#6B7280; font-weight:700;">{obs['data']} • {obs['usuario']}</div>
                                            <div style="font-size:13px; color:#111827; margin-top:4px;">{obs['observacao']}</div>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )

                        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

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
