
#Dashboard Streamlit -- Desafio Data Scientist, Gil Vicente FC (v2, design)


import glob
import os

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from mplsoccer import Pitch


# Paleta de cores oficial do Gil Vicente FC

COR_VERMELHO = "#D52929"
COR_AZUL_MARINHO = "#083363"
COR_BRANCO = "#FFFFFF"
COR_VERMELHO_ESCURO = "#521C19"
COR_DOURADO = "#9EA85E"
COR_CINZA_CLARO = "#D9D9D9"
COR_FUNDO_CAMPO = "#F5F3EE"
COR_LINHAS_CAMPO = "#000000"

st.set_page_config(page_title="Gil Vicente FC — Análise IMPECT", layout="wide", page_icon="⚽")


# CSS global

def html(bloco):
    """Remove indentação e linhas em branco de um bloco HTML multi-linha.
    Necessário porque o Markdown do Streamlit interpreta linhas em branco
    seguidas de indentação como um bloco de código (ou HTML solto), o que
    faz o HTML aparecer como texto em vez de ser aplicado/renderizado.
    Junta as linhas com espaço (não string vazia) para não colar palavras
    quando uma frase está dividida em várias linhas no código-fonte -- o
    HTML colapsa espaços a mais, por isso isto é seguro visualmente."""
    linhas = [linha.strip() for linha in bloco.strip().splitlines() if linha.strip() != ""]
    return " ".join(linhas)


st.markdown(
    html(f"""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background-color: {COR_BRANCO}; }}
    .block-container {{ padding-top: 3.2rem; padding-bottom: 2rem; max-width: 1300px; }}
    h1, h2, h3 {{ color: {COR_AZUL_MARINHO}; font-weight: 700; }}
    h3 {{ font-size: 23px !important; margin-top: 0.2rem !important; margin-bottom: 0.6rem !important; }}
    h4 {{ font-size: 18px !important; margin-bottom: 0.4rem !important; }}

    .stTabs [data-baseweb="tab"] {{ font-weight: 600; color: {COR_AZUL_MARINHO}; padding-top: 4px; padding-bottom: 4px; }}
    .stTabs [aria-selected="true"] {{ color: {COR_VERMELHO} !important; }}
    .stTabs [data-baseweb="tab-highlight"] {{ background-color: {COR_VERMELHO} !important; }}

    .card-row {{ display: flex; gap: 12px; margin-bottom: 14px; flex-wrap: wrap; }}
    .metric-card {{
        flex: 1; min-width: 170px;
        background: {COR_BRANCO};
        border: 1px solid {COR_CINZA_CLARO};
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 2px 8px rgba(8, 51, 99, 0.06);
        border-top: 4px solid {COR_VERMELHO};
    }}
    .metric-card.navy {{ border-top-color: {COR_AZUL_MARINHO}; }}
    .metric-card.gold {{ border-top-color: {COR_DOURADO}; }}
    .metric-label {{
        font-size: 13px; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.05em; color: {COR_AZUL_MARINHO}; opacity: 0.8; margin-bottom: 4px;
        display: flex; align-items: center; gap: 7px;
    }}
    .metric-label i {{ font-size: 17px; opacity: 1; color: {COR_VERMELHO}; }}
    .metric-card.navy .metric-label i {{ color: {COR_AZUL_MARINHO}; }}
    .metric-card.gold .metric-label i {{ color: {COR_DOURADO}; }}
    .metric-value {{ font-size: 28px; font-weight: 800; color: {COR_VERMELHO_ESCURO}; line-height: 1.1; }}
    .metric-sub {{ font-size: 12.5px; color: #666; margin-top: 2px; }}

    .story-card {{
        background: {COR_FUNDO_CAMPO};
        border-left: 4px solid {COR_AZUL_MARINHO};
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0 14px 0;
        font-size: 14px; line-height: 1.5; color: #222;
    }}
    .story-card b {{ color: {COR_AZUL_MARINHO}; }}

    .insight-card {{
        background: {COR_BRANCO};
        border: 1px solid {COR_CINZA_CLARO};
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 2px 8px rgba(8, 51, 99, 0.06);
        margin-bottom: 10px;
        font-size: 14px; line-height: 1.5;
    }}
    .insight-card h4 {{
        color: {COR_VERMELHO}; margin-top: 0 !important; font-size: 15px !important; text-transform: uppercase;
        letter-spacing: 0.04em; display: flex; align-items: center; gap: 8px;
    }}
    .insight-card h4 i {{ font-size: 18px; }}

    .legend-pill {{
        display: inline-block; padding: 3px 12px; border-radius: 20px;
        font-size: 12px; font-weight: 600; color: white; margin-right: 6px;
    }}

    .step-list {{ list-style: none; padding-left: 0; margin: 0; }}
    .step-list li {{
        padding: 5px 9px; border-radius: 7px; margin-bottom: 3px; font-size: 13px;
    }}

    .chart-header {{
        display: flex; align-items: center; gap: 10px; margin: 4px 0 4px 0;
    }}
    .chart-header i {{ font-size: 27px; color: {COR_VERMELHO}; }}
    .chart-header span {{ font-size: 21px; font-weight: 700; color: {COR_AZUL_MARINHO}; }}

    .hero-stat {{
        text-align: center; padding: 14px; background: {COR_FUNDO_CAMPO};
        border-radius: 12px; margin-bottom: 12px;
    }}
    .hero-stat .valor {{ font-size: 36px; font-weight: 800; color: {COR_VERMELHO}; }}
    .hero-stat .texto {{ font-size: 14px; color: {COR_AZUL_MARINHO}; font-weight: 600; margin-top: 2px; }}
    </style>
    """),
    unsafe_allow_html=True,
)


def icone_html(classe_bi, cor=None):
    estilo = f'style="color:{cor};"' if cor else ""
    return f'<i class="bi {classe_bi}" {estilo}></i>'


def chart_header(texto, classe_bi):
    st.markdown(
        html(f'<div class="chart-header"><i class="bi {classe_bi}"></i><span>{texto}</span></div>'),
        unsafe_allow_html=True,
    )


def metric_card(label, value, sub="", classe="", icone_bi=""):
    prefixo = f'<i class="bi {icone_bi}"></i>' if icone_bi else ""
    return html(f"""
    <div class="metric-card {classe}">
        <div class="metric-label">{prefixo}{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """)


def cards_row(cards_html):
    st.markdown(html(f'<div class="card-row">{"".join(cards_html)}</div>'), unsafe_allow_html=True)


def plotly_layout_base(fig, altura=300):
    fig.update_layout(
        paper_bgcolor=COR_BRANCO,
        plot_bgcolor=COR_BRANCO,
        font=dict(family="Inter", color="#333", size=12),
        margin=dict(l=10, r=20, t=45, b=10),
        showlegend=False,
        height=altura,
    )
    fig.update_xaxes(showgrid=True, gridcolor="#F0EFEA", zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig



# Carregamento e normalização dos dados

st.sidebar.title("⚙️ Configuração")
pasta_dados = st.sidebar.text_input("Pasta com os ficheiros .pkl IMPECT", value="./dados")


@st.cache_data(show_spinner="A carregar e normalizar os dados...")
def carregar_dados(pasta):
    ficheiros = sorted(glob.glob(os.path.join(pasta, "*.pkl")))
    if not ficheiros:
        return None
    dfs = [pd.read_pickle(f) for f in ficheiros]
    data = pd.concat(dfs, ignore_index=True).sort_values(["matchId", "gameTimeInSec"]).reset_index(drop=True)

    remates_gv = data[(data["squadName"] == "Gil Vicente FC") & (data["actionType"] == "SHOT")]
    sinal = (
        remates_gv.groupby(["matchId", "periodId"])["startCoordinatesX"]
        .mean().apply(lambda x: 1 if x < 0 else -1).rename("multiplicador").reset_index()
    )
    data = data.merge(sinal, on=["matchId", "periodId"], how="left")
    data["multiplicador"] = data["multiplicador"].fillna(1)
    for col in ["startCoordinatesX", "startCoordinatesY", "endCoordinatesX", "endCoordinatesY",
                "opponentCoordinatesX", "opponentCoordinatesY"]:
        if col in data.columns:
            data[col] = data[col] * data["multiplicador"]
    return data


data = carregar_dados(pasta_dados)

if data is None:
    st.error(f"Não encontrei ficheiros `.pkl` em `{pasta_dados}`. Ajusta o caminho na barra lateral.")
    st.stop()

mapa_adversario = (
    data[(data["squadName"] != "Gil Vicente FC").fillna(False)][["matchId", "squadName"]]
    .drop_duplicates().dropna().groupby("matchId")["squadName"].first().to_dict()
)


# Cabeçalho

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

colunas_cabecalho = st.columns([1, 9])
with colunas_cabecalho[0]:
    caminho_escudo = os.path.join(PASTA_SCRIPT, "assets", "escudo_gvfc.png")
    if os.path.exists(caminho_escudo):
        st.image(caminho_escudo, width=64)
    else:
        st.markdown('<div style="font-size:34px; color:' + COR_VERMELHO + ';"><i class="bi bi-shield-fill"></i></div>', unsafe_allow_html=True)
with colunas_cabecalho[1]:
    st.markdown(
        html(f"""
        <div style="font-size:28px; font-weight:800; color:{COR_AZUL_MARINHO}; margin-top:6px;">
        Gil Vicente FC — Desafio Data Scientist</div>
        <div style="font-size:14px; color:#777;">
        Análise de Dados IMPECT - 8 jogos - Época 2025/26</div>
        """),
        unsafe_allow_html=True,
    )
st.markdown(
    f'<hr style="border:none; border-top:2px solid {COR_CINZA_CLARO}; margin:10px 0 14px 0;">',
    unsafe_allow_html=True,
)

n_jogos = data["matchId"].nunique()
golos_gv = int((data[(data["squadName"] == "Gil Vicente FC")]["GOALS"] > 0).sum())
golos_sofridos = int(
    ((data["actionType"] == "GOAL") & (data["squadName"] != "Gil Vicente FC") & data["squadName"].notna()).sum()
)

cards_row([
    metric_card("Jogos analisados", n_jogos, "época 2025/26", "navy", "bi-calendar3"),
    metric_card("Golos marcados", golos_gv, "", "", "bi-trophy"),
    metric_card("Golos sofridos", golos_sofridos, "", "gold", "bi-shield-exclamation"),
])

tab_insight1, tab_insight2, tab_metodologia = st.tabs(
    ["Insight 1 — Lançamento Lateral", "Insight 2 — Cruzamentos", "Metodologia & Limitações"]
)


# INSIGHT 1

with tab_insight1:
    st.markdown("### O lançamento lateral como arma ofensiva de bola parada")

    chart_header("O porquê de ter explorado as bolas paradas primeiro", "bi-fire")

    ordem_fases = ["SET_PIECE", "ATTACKING_TRANSITION", "SECOND_BALL", "IN_POSSESSION"]
    nomes_fases = {"SET_PIECE": "Bola parada", "ATTACKING_TRANSITION": "Transição",
                   "SECOND_BALL": "Segunda bola", "IN_POSSESSION": "Jogo organizado"}
    fase_pxt = data[data["squadName"] == "Gil Vicente FC"].groupby("phase")["pxTTeam"].mean()
    fase_pxt = fase_pxt.reindex(ordem_fases).reset_index()
    fase_pxt["label"] = fase_pxt["phase"].map(nomes_fases)

    pxt_sp = fase_pxt.loc[fase_pxt["phase"] == "SET_PIECE", "pxTTeam"].values[0]
    pxt_pos = fase_pxt.loc[fase_pxt["phase"] == "IN_POSSESSION", "pxTTeam"].values[0]
    razao = pxt_sp / pxt_pos

    fig0 = go.Figure(go.Bar(
        x=fase_pxt["label"], y=fase_pxt["pxTTeam"],
        marker_color=[COR_VERMELHO if f == "SET_PIECE" else COR_CINZA_CLARO for f in fase_pxt["phase"]],
        text=[f"{v:.4f}" for v in fase_pxt["pxTTeam"]], textposition="outside", cliponaxis=False,
        width=0.45,
    ))
    fig0 = plotly_layout_base(fig0, altura=340)
    fig0.update_layout(margin=dict(l=10, r=20, t=55, b=10))
    fig0.update_yaxes(title="pxT médio por evento (ameaça ofensiva)", range=[0, fase_pxt["pxTTeam"].max() * 1.3])
    st.plotly_chart(fig0, use_container_width=True)

    st.markdown(
        html(f"""
        <div class="story-card">
        Este foi o gráfico que motivou toda a análise seguinte: por evento, uma ação em bola parada gera 
        <b> {razao:.1f}x mais pxT</b> (ameaça ofensiva, métrica nativa do IMPECT) do que uma ação em jogo
        organizado. Foi este contraste que me levou a decompor as bolas paradas por tipo, e a descobrir que
        o lançamento lateral, não os cantos, é onde essa ameaça se converte mesmo em golo.
        </div>
        """),
        unsafe_allow_html=True,
    )

    todos_golos_gv = data[(data["squadName"] == "Gil Vicente FC") & (data["GOALS"] > 0)]
    golos_sp = todos_golos_gv[todos_golos_gv["phase"] == "SET_PIECE"]
    n_throwin = len(golos_sp[golos_sp["setPieceCategory"] == "THROW_IN"])
    n_total_golos_gv = len(todos_golos_gv)
    n_corner_livre = len(golos_sp) - n_throwin
    n_organizado = n_total_golos_gv - len(golos_sp)

    st.markdown(
        html(f"""
        <div class="hero-stat">
        <div class="valor">{n_throwin} de {n_total_golos_gv}</div>
        <div class="texto"><i class="bi bi-hand-index-thumb"></i>&nbsp; golos do Gil Vicente vieram de lançamento lateral ({n_throwin/n_total_golos_gv:.0%})</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.1, 1])

    with col1:
        chart_header(f"Origem dos {n_total_golos_gv} golos do Gil Vicente", "bi-trophy")
        # lançamento lateral ao lado de jogo organizado, para contraste direto;
        # cantos + livres (zero golos) fica de fora
        ordem_cat = ["Lançamento lateral", "Jogo organizado", "Cantos + livres"]
        valores_cat = [n_throwin, n_organizado, n_corner_livre]
        cores_cat = [COR_VERMELHO, COR_AZUL_MARINHO, COR_DOURADO]
        fig = go.Figure(go.Bar(
            x=ordem_cat, y=valores_cat,
            marker_color=cores_cat,
            text=valores_cat,
            textposition="outside", cliponaxis=False,
            width=0.35,
        ))
        fig = plotly_layout_base(fig, altura=340)
        fig.update_layout(margin=dict(l=10, r=20, t=55, b=10))
        fig.update_yaxes(title="Nº de golos", range=[0, max(valores_cat) * 1.3])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        chart_header("pxT médio por tipo de bola parada", "bi-flag")
        gv_setpiece = data[(data["squadName"] == "Gil Vicente FC") & (data["phase"] == "SET_PIECE")]
        resumo_tipo = gv_setpiece.groupby("setPieceCategory").agg(
            n_eventos=("pxTTeam", "count"), pxt_medio=("pxTTeam", "mean"), golos=("GOALS", "sum")
        ).sort_values("pxt_medio", ascending=False).reset_index()

        fig2 = go.Figure(go.Bar(
            y=resumo_tipo["setPieceCategory"],
            x=resumo_tipo["pxt_medio"],
            orientation="h",
            marker_color=COR_AZUL_MARINHO,
            text=[f"{v:.4f}" for v in resumo_tipo["pxt_medio"]],
            textposition="outside", cliponaxis=False,
            width=0.5,
        ))
        fig2 = plotly_layout_base(fig2)
        fig2.update_xaxes(title="pxT médio / evento")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        html("""
        <div class="story-card">
        Metade dos golos do Gil Vicente nesta amostra vieram de <b> lançamento lateral</b> — mais do que
        cantos e livres combinados, apesar destes somarem muito mais volume de eventos. Os cantos têm o
        maior <b> pxT</b> médio por evento (métrica nativa do IMPECT), mas <b> zero golos</b> nos 8 jogos.
        </div>
        """),
        unsafe_allow_html=True,
    )

    chart_header("Padrão individual — quem lança", "bi-person-arms-up")

    @st.cache_data(show_spinner="A calcular taxa de perigo por lançador...")
    def calcular_taxa_lancador(_data):
        c1 = (_data["squadName"] == "Gil Vicente FC").fillna(False)
        c2 = (_data["actionType"] == "THROW_IN").fillna(False)
        lancamentos = _data[c1 & c2]

        registos = []
        for _, lanc in lancamentos.iterrows():
            match_id, t_lanc, lancador = lanc["matchId"], lanc["gameTimeInSec"], lanc["playerName"]
            c1b = (_data["matchId"] == match_id).fillna(False)
            c2b = (_data["gameTimeInSec"] > t_lanc).fillna(False)
            c3b = (_data["gameTimeInSec"] <= t_lanc + 15).fillna(False)
            janela = _data[c1b & c2b & c3b]
            c4b = (janela["actionType"] == "SHOT").fillna(False)
            c5b = (janela["squadName"] == "Gil Vicente FC").fillna(False)
            remates = janela[c4b & c5b]
            registos.append({"lancador": lancador, "houve_remate": len(remates) > 0})
        res = pd.DataFrame(registos)
        resumo = res.groupby("lancador").agg(
            n_lancamentos=("houve_remate", "count"), taxa_remate=("houve_remate", "mean")
        ).sort_values("n_lancamentos", ascending=False)
        return resumo[resumo["n_lancamentos"] >= 5].reset_index()

    resumo_lancador = calcular_taxa_lancador(data)

    fig_l = go.Figure(go.Bar(
        x=resumo_lancador["lancador"], y=resumo_lancador["taxa_remate"],
        marker_color=[COR_VERMELHO if l == "Santi García" else COR_CINZA_CLARO for l in resumo_lancador["lancador"]],
        text=[f"{v:.1%}" for v in resumo_lancador["taxa_remate"]], textposition="outside", cliponaxis=False,
        width=0.4,
    ))
    fig_l = plotly_layout_base(fig_l, altura=330)
    fig_l.update_layout(margin=dict(l=10, r=20, t=55, b=10))
    fig_l.update_yaxes(title="Taxa de remate por lançamento", tickformat=".0%", range=[0, resumo_lancador["taxa_remate"].max() * 1.35])
    st.plotly_chart(fig_l, use_container_width=True)

    st.markdown(
        html("""
        <div class="story-card">
        O <b> Santi García</b> converte 31% dos seus lançamentos em remate nos 15s seguintes — quase 9x mais
        que o Ghislain Konan (3.4%), o lançador mais utilizado. Os 3 golos de lançamento do Santi García
        vieram de 3 jogos diferentes, o que dá alguma confiança apesar da amostra modesta (29 lançamentos).
        Uma equipa adversária pode ajustar a marcação especificamente nos lançamentos em que ele é o
        executante.
        </div>
        """),
        unsafe_allow_html=True,
    )

    chart_header("Lançamentos longos: qualidade, não volume", "bi-rulers")

    LIMIAR_LONGO = 24.5
    JANELA_LONGO = 15

    @st.cache_data(show_spinner="A comparar lançamentos longos com os adversários...")
    def analisar_longos_todos(_data):
        mapa_adv = (
            _data[(_data["squadName"] != "Gil Vicente FC").fillna(False)][["matchId", "squadName"]]
            .drop_duplicates().dropna().groupby("matchId")["squadName"].first().to_dict()
        )

        def analisar_equipa(nome_equipa, subset_jogos=None):
            c1 = (_data["squadName"] == nome_equipa).fillna(False)
            c2 = (_data["actionType"] == "THROW_IN").fillna(False)
            if subset_jogos is not None:
                c3 = _data["matchId"].isin(subset_jogos)
                lancamentos = _data[c1 & c2 & c3]
            else:
                lancamentos = _data[c1 & c2]

            total = len(lancamentos)
            longos = lancamentos[lancamentos["passDistance"] > LIMIAR_LONGO]
            n_longos = len(longos)
            pct_longos = n_longos / total if total > 0 else None

            n_com_remate = 0
            for _, lanc in longos.iterrows():
                match_id, t_lanc = lanc["matchId"], lanc["gameTimeInSec"]
                c1b = (_data["matchId"] == match_id).fillna(False)
                c2b = (_data["gameTimeInSec"] > t_lanc).fillna(False)
                c3b = (_data["gameTimeInSec"] <= t_lanc + JANELA_LONGO).fillna(False)
                janela = _data[c1b & c2b & c3b]
                c4b = (janela["actionType"] == "SHOT").fillna(False)
                c5b = (janela["squadName"] == nome_equipa).fillna(False)
                if (c4b & c5b).any():
                    n_com_remate += 1
            taxa_conversao = n_com_remate / n_longos if n_longos > 0 else None

            return {"equipa": nome_equipa, "total_lancamentos": total, "n_longos": n_longos,
                    "pct_longos": pct_longos, "taxa_conversao_longos": taxa_conversao}

        resultados = [analisar_equipa("Gil Vicente FC")]
        for match_id, nome in mapa_adv.items():
            resultados.append(analisar_equipa(nome, subset_jogos=[match_id]))
        return pd.DataFrame(resultados)

    res_longos = analisar_longos_todos(data)
    gv_longos = res_longos[res_longos["equipa"] == "Gil Vicente FC"].iloc[0]
    adv_longos = res_longos[res_longos["equipa"] != "Gil Vicente FC"]
    media_pct_volume = adv_longos["pct_longos"].mean()
    media_taxa_qualidade = adv_longos["taxa_conversao_longos"].mean()

    col_v, col_q = st.columns(2)
    with col_v:
        st.markdown(
            html(f"""
            <div class="metric-card navy">
                <div class="metric-label"><i class="bi bi-graph-up"></i>Volume — % lançamentos longos</div>
                <div class="metric-value">{gv_longos['pct_longos']:.1%}</div>
                <div class="metric-sub">GV vs. {media_pct_volume:.1%} de média dos adversários — abaixo da média</div>
            </div>
            """),
            unsafe_allow_html=True,
        )
    with col_q:
        st.markdown(
            html(f"""
            <div class="metric-card">
                <div class="metric-label"><i class="bi bi-bullseye"></i>Qualidade — conversão dos longos</div>
                <div class="metric-value">{gv_longos['taxa_conversao_longos']:.1%}</div>
                <div class="metric-sub">Gil Vicente vs. {media_taxa_qualidade:.1%} de média dos adversários — {gv_longos['taxa_conversao_longos']/media_taxa_qualidade:.1f}x acima</div>
            </div>
            """),
            unsafe_allow_html=True,
        )

    # tabela comparativa
    tabela_html = """
    <table style="width:100%; border-collapse:collapse; margin-top:14px; font-size:13.5px;">
    <thead>
    <tr style="border-bottom:2px solid #D9D9D9;">
        <th style="text-align:left; padding:8px;">Equipa</th>
        <th style="text-align:right; padding:8px;">Lançamentos</th>
        <th style="text-align:right; padding:8px;">Longos (>24.5m)</th>
        <th style="text-align:right; padding:8px;">% longos (volume)</th>
        <th style="text-align:right; padding:8px;">Conversão longos (qualidade)</th>
    </tr>
    </thead>
    <tbody>
    """
    res_longos_sorted = res_longos.sort_values("equipa", key=lambda s: s == "Gil Vicente FC", ascending=False)
    for _, row in res_longos_sorted.iterrows():
        destaque = row["equipa"] == "Gil Vicente FC"
        cor_fundo = COR_FUNDO_CAMPO if destaque else COR_BRANCO
        peso = "700" if destaque else "400"
        cor_texto = COR_VERMELHO_ESCURO if destaque else "#333"
        pct_txt = f"{row['pct_longos']:.1%}" if pd.notna(row["pct_longos"]) else "—"
        taxa_txt = f"{row['taxa_conversao_longos']:.1%}" if pd.notna(row["taxa_conversao_longos"]) else "—"
        tabela_html += (
            f'<tr style="background:{cor_fundo}; font-weight:{peso}; color:{cor_texto};">'
            f'<td style="padding:7px 8px;">{row["equipa"]}</td>'
            f'<td style="text-align:right; padding:7px 8px;">{row["total_lancamentos"]}</td>'
            f'<td style="text-align:right; padding:7px 8px;">{row["n_longos"]}</td>'
            f'<td style="text-align:right; padding:7px 8px;">{pct_txt}</td>'
            f'<td style="text-align:right; padding:7px 8px;">{taxa_txt}</td>'
            f'</tr>'
        )
    tabela_html += "</tbody></table>"
    st.markdown(html(tabela_html), unsafe_allow_html=True)

    st.markdown(
        html(f"""
        <div class="story-card">
        O Gil Vicente tenta proporcionalmente <b> menos</b> lançamentos longos do que a média dos adversários
        ({gv_longos['pct_longos']:.1%} vs. {media_pct_volume:.1%}) — não é uma questão de insistirem mais
        nisso. Mas quando lançam longo, convertem em remate a uma taxa {gv_longos['taxa_conversao_longos']/media_taxa_qualidade:.1f}x
        superior à média dos adversários. Os golos de lançamento lateral do Gil Vicente não vêm de tentarem
        muitas vezes — vêm de o fazerem bem.
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.markdown("#### As 4 jogadas de golo")

    golos_info = [
        {"matchId": 210999, "setPieceSubPhaseId": 90536463.0, "jogo": "Gil Vicente vs AFS"},
        {"matchId": 210999, "setPieceSubPhaseId": 90536483.0, "jogo": "Gil Vicente vs AFS"},
        {"matchId": 211045, "setPieceSubPhaseId": 90700672.0, "jogo": "Tondela vs Gil Vicente (Penálti)"},
        {"matchId": 211053, "setPieceSubPhaseId": 91199882.0, "jogo": "Gil Vicente vs Casa Pia"},
    ]

    def agrupar_pontos_proximos(pontos, limiar_metros=2.0):
        grupos = [[0]]
        for j in range(1, len(pontos)):
            i_ref = grupos[-1][0]
            mesma_equipa = pontos.loc[j, "squadName"] == pontos.loc[i_ref, "squadName"]
            dist = ((pontos.loc[j, "startCoordinatesX"] - pontos.loc[i_ref, "startCoordinatesX"]) ** 2
                    + (pontos.loc[j, "startCoordinatesY"] - pontos.loc[i_ref, "startCoordinatesY"]) ** 2) ** 0.5
            if mesma_equipa and dist <= limiar_metros:
                grupos[-1].append(j)
            else:
                grupos.append([j])
        return grupos

    def desenhar_jogada_fig(seq):
        pontos = seq[["startCoordinatesX", "startCoordinatesY", "squadName", "playerName", "action"]] \
            .dropna(subset=["startCoordinatesX", "startCoordinatesY"]).reset_index(drop=True)
        grupos = agrupar_pontos_proximos(pontos, limiar_metros=2.0)

        fig, ax_campo = plt.subplots(figsize=(7.5, 6.5))
        pitch = Pitch(pitch_type="skillcorner", pitch_length=105, pitch_width=68,
                      pitch_color=COR_FUNDO_CAMPO, line_color=COR_LINHAS_CAMPO, half=False)
        pitch.draw(ax=ax_campo)

        coords_grupos = [(pontos.loc[g, "startCoordinatesX"].mean(), pontos.loc[g, "startCoordinatesY"].mean()) for g in grupos]
        for g_idx, grupo in enumerate(grupos):
            x0, y0 = coords_grupos[g_idx]
            equipa = pontos.loc[grupo[0], "squadName"]
            cor = COR_VERMELHO if equipa == "Gil Vicente FC" else COR_AZUL_MARINHO
            ax_campo.scatter(x0, y0, color=cor, s=200, zorder=4, edgecolors="black", linewidths=1)
            rotulo = str(grupo[0] + 1) if len(grupo) == 1 else f"{grupo[0]+1}-{grupo[-1]+1}"
            ax_campo.annotate(rotulo, (x0, y0), color="white", fontsize=9, ha="center", va="center", zorder=5, fontweight="bold")
            if g_idx < len(grupos) - 1:
                x1, y1 = coords_grupos[g_idx + 1]
                pitch.arrows(x0, y0, x1, y1, color=cor, ax=ax_campo, width=2.2, alpha=0.7, headwidth=7)

        ultimo = pontos.iloc[-1]
        ax_campo.scatter(ultimo["startCoordinatesX"], ultimo["startCoordinatesY"], color=COR_DOURADO, s=280,
                          zorder=6, marker="*", edgecolors="black", linewidths=0.8)
        if ultimo["startCoordinatesX"] < 0:
            ax_campo.set_xlim(-56, -10)
        else:
            ax_campo.set_xlim(10, 56)
        ax_campo.set_ylim(-36, 36)
        fig.patch.set_facecolor(COR_FUNDO_CAMPO)
        plt.tight_layout()
        return fig, pontos

    colX, colY = st.columns([1, 2])
    with colX:
        escolha = st.radio("Escolhe a jogada:", [g["jogo"] for g in golos_info], label_visibility="collapsed")

    info_escolhida = next(g for g in golos_info if g["jogo"] == escolha)
    seq = data[
        (data["matchId"] == info_escolhida["matchId"])
        & (data["setPieceSubPhaseId"] == info_escolhida["setPieceSubPhaseId"])
    ].sort_values("gameTimeInSec")

    with colY:
        if len(seq) > 0:
            fig, pontos = desenhar_jogada_fig(seq)
            c_campo, c_legenda = st.columns([1.6, 1])
            with c_campo:
                st.pyplot(fig)
            with c_legenda:
                pills = (
                    f'<span class="legend-pill" style="background:{COR_VERMELHO}">Gil Vicente</span>'
                    f'<span class="legend-pill" style="background:{COR_AZUL_MARINHO}">Adversário</span>'
                )
                st.markdown(pills, unsafe_allow_html=True)
                itens = "".join(
                    f'<li style="background:{COR_FUNDO_CAMPO}; border-left:3px solid '
                    f'{COR_VERMELHO if pontos.loc[j, "squadName"] == "Gil Vicente FC" else COR_AZUL_MARINHO};">'
                    f'<b> {j+1}.</b> {pontos.loc[j, "playerName"]} — {pontos.loc[j, "action"]}</li>'
                    for j in range(len(pontos))
                )
                st.markdown(f'<ul class="step-list">{itens}</ul>', unsafe_allow_html=True)
        else:
            st.info("Sequência não encontrada nos dados carregados.")


# INSIGHT 2

with tab_insight2:
    st.markdown("### Análise dos Cruzamentos e Remates Sofridos")

    chart_header("Identificação da Zona Central Defensiva", "bi-bullseye")

    @st.cache_data(show_spinner="A localizar remates e golos sofridos...")
    def calcular_remates_golos_zona(_data):
        c1 = (_data["actionType"] == "SHOT").fillna(False)
        c2 = (_data["squadName"] != "Gil Vicente FC").fillna(False)
        c3 = _data["squadName"].notna()
        remates = _data[c1 & c2 & c3].copy()

        c1g = (_data["actionType"] == "GOAL").fillna(False)
        golos_eventos = _data[c1g & c2 & c3].copy()

        remates_que_marcaram = []
        for _, golo in golos_eventos.iterrows():
            match_id, t_golo, jogador = golo["matchId"], golo["gameTimeInSec"], golo["playerName"]
            candidatos = remates[
                (remates["matchId"] == match_id) & (remates["playerName"] == jogador)
                & (remates["gameTimeInSec"] < t_golo) & (remates["gameTimeInSec"] >= t_golo - 5)
            ]
            if len(candidatos) > 0:
                remates_que_marcaram.append(candidatos.sort_values("gameTimeInSec").iloc[-1])
        remates_que_marcaram = pd.DataFrame(remates_que_marcaram) if remates_que_marcaram else pd.DataFrame()

        def classificar_corredor_zona(y):
            if pd.isna(y):
                return None
            if y < -11.33:
                return "ESQUERDA"
            elif y > 11.33:
                return "DIREITA"
            return "CENTRO"

        remates["corredor"] = remates["startCoordinatesY"].apply(classificar_corredor_zona)
        n_remates_zona = ((remates["startCoordinatesX"] > 35) & (remates["corredor"] == "CENTRO")).sum()

        return remates, remates_que_marcaram, n_remates_zona

    remates, remates_que_marcaram, n_remates_zona = calcular_remates_golos_zona(data)

    fig_zona, ax_zona = plt.subplots(figsize=(8, 6.3))
    pitch = Pitch(pitch_type="skillcorner", pitch_length=105, pitch_width=68,
                  pitch_color=COR_FUNDO_CAMPO, line_color="#000000", half=False)
    pitch.draw(ax=ax_zona)

    zona_patch = Rectangle((35, -11.33), 52.5 - 35, 22.66, facecolor=COR_DOURADO, alpha=0.28, zorder=1,
                            edgecolor=COR_DOURADO, linewidth=2)
    ax_zona.add_patch(zona_patch)

    indices_golo = remates_que_marcaram.index if len(remates_que_marcaram) > 0 else []
    remates_sem_golo = remates[~remates.index.isin(indices_golo)]
    ax_zona.scatter(remates_sem_golo["startCoordinatesX"], remates_sem_golo["startCoordinatesY"], marker="x", s=55,
                     color=COR_AZUL_MARINHO, linewidths=1.5, zorder=3, label=f"Remates sofridos (n={len(remates)})")
    if len(remates_que_marcaram) > 0:
        ax_zona.scatter(remates_que_marcaram["startCoordinatesX"], remates_que_marcaram["startCoordinatesY"],
                         marker="*", s=240, color=COR_VERMELHO, edgecolors="black", linewidths=1, zorder=4,
                         label=f"Remate que resultou em golo (n={len(remates_que_marcaram)})")
    ax_zona.set_xlim(10, 56)
    ax_zona.set_ylim(-36, 36)
    ax_zona.legend(loc="upper left", frameon=True, facecolor=COR_FUNDO_CAMPO, fontsize=8.5)
    fig_zona.patch.set_facecolor(COR_FUNDO_CAMPO)
    plt.tight_layout()

    col_mapa, col_stats = st.columns([1.5, 1])
    with col_mapa:
        st.pyplot(fig_zona)
    with col_stats:
        st.markdown(
            html(f"""
            <div class="metric-card">
                <div class="metric-label"><i class="bi bi-crosshair"></i>Remates a partir desta zona</div>
                <div class="metric-value">{n_remates_zona}</div>
                <div class="metric-sub">de {len(remates)} remates sofridos no total ({n_remates_zona/len(remates):.0%})</div>
            </div>
            """),
            unsafe_allow_html=True,
        )
        st.markdown(
            html("""
            <div class="story-card" style="margin-top:12px;">
            Quase metade dos remates sofridos pelo Gil Vicente partem desta zona — a área diretamente à
            frente da própria baliza. É por isso que comecei a investigação aqui.
            </div>
            """),
            unsafe_allow_html=True,
        )

    chart_header("De onde vêm as bolas que chegam a esta zona", "bi-diagram-3")

    origem_zona_dados = pd.DataFrame({
        "origem": ["Bola parada", "Cruzamento", "Outro", "Bola longa/diagonal", "Drible do adversário"],
        "pct": [46.9, 34.4, 12.5, 3.1, 3.1],
    })
    fig_origem = go.Figure(go.Bar(
        x=origem_zona_dados["pct"], y=origem_zona_dados["origem"], orientation="h",
        marker_color=[COR_CINZA_CLARO, COR_VERMELHO, COR_CINZA_CLARO, COR_CINZA_CLARO, COR_CINZA_CLARO],
        text=[f"{v:.1f}%" for v in origem_zona_dados["pct"]], textposition="outside", cliponaxis=False,
    ))
    fig_origem = plotly_layout_base(fig_origem, altura=260)
    fig_origem.update_xaxes(title="% das disputas nesta zona")
    fig_origem.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_origem, use_container_width=True)

    st.markdown(
        html("""
        <div class="story-card">
        A bola parada é a fonte individual mais comum (46.9%) — já coberta, do lado ofensivo, no insight 1.
        Logo a seguir vem o <b> cruzamento</b> (34.4%), o principal vetor de entrega em <b> jogo corrido </b>
        para esta zona. Foi por isso que decidi investigar especificamente os cruzamentos a seguir, não por serem o tema mais óbvio, mas por serem o mecanismo não-redundante mais relevante que os dados apontavam.
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.markdown("### Contenção de Cruzamentos: onde o Gil Vicente é comparativamente forte")

    st.markdown(
        html("""
        <div class="story-card">
        Testei primeiro se o Gil Vicente tinha uma <b> fraqueza</b> na disputa física direta desta zona — a taxa de vitória em duelos rondava valores altos (cerca de 89%), mas ao comparar com os 8 adversários nas suas próprias zonas equivalentes, o Gil Vicente não se distinguia: é um padrão universal do futebol, não um ponto forte específico. 
        Por isso virei a pergunta ao contrário: sabendo que o cruzamento é o principal
        vetor de perigo em jogo corrido, onde é que o Gil Vicente responde <b> bem</b> a essa ameaça?
        </div>
        """),
        unsafe_allow_html=True,
    )

    excluir_sporting = st.toggle("Excluir o Sporting CP da comparação (teste de robustez)", value=False)
    MATCH_SPORTING = 211082
    JANELA_CRUZAMENTO = 10

    def taxa_contencao(cruzamentos_df, data, janela=JANELA_CRUZAMENTO):
        n_contidos = 0
        for _, cruz in cruzamentos_df.iterrows():
            match_id, t_cruz = cruz["matchId"], cruz["gameTimeInSec"]
            equipa_atacante = cruz["squadName"]
            c1 = (data["matchId"] == match_id).fillna(False)
            c2 = (data["gameTimeInSec"] >= t_cruz).fillna(False)
            c3 = (data["gameTimeInSec"] <= t_cruz + janela).fillna(False)
            janela_df = data[c1 & c2 & c3]
            c4 = (janela_df["actionType"] == "SHOT").fillna(False)
            c5 = (janela_df["squadName"] == equipa_atacante).fillna(False)
            if not (c4 & c5).any():
                n_contidos += 1
        return n_contidos, len(cruzamentos_df)

    @st.cache_data(show_spinner="A calcular taxas de contenção...")
    def calcular_contencao_todos(_data, excluir_sporting):
        c1 = _data["action"].isin(["HIGH_CROSS", "LOW_CROSS"]).fillna(False)
        c2 = (_data["squadName"] != "Gil Vicente FC").fillna(False)
        c3 = _data["squadName"].notna()
        cruzamentos_adv = _data[c1 & c2 & c3]
        if excluir_sporting:
            cruzamentos_adv = cruzamentos_adv[cruzamentos_adv["matchId"] != MATCH_SPORTING]
        n_gv, total_gv = taxa_contencao(cruzamentos_adv, _data)

        resultados = []
        for match_id, nome in mapa_adversario.items():
            if excluir_sporting and match_id == MATCH_SPORTING:
                continue
            c1b = (_data["matchId"] == match_id).fillna(False)
            c2b = _data["action"].isin(["HIGH_CROSS", "LOW_CROSS"]).fillna(False)
            c3b = (_data["squadName"] == "Gil Vicente FC").fillna(False)
            cruz_gv_jogo = _data[c1b & c2b & c3b]
            n, total = taxa_contencao(cruz_gv_jogo, _data)
            resultados.append({"adversario": nome, "n_contidos": n, "n_total": total,
                                "taxa": n / total if total > 0 else None})
        return n_gv, total_gv, pd.DataFrame(resultados)

    n_gv, total_gv, res_cruz_df = calcular_contencao_todos(data, excluir_sporting)
    taxa_gv = n_gv / total_gv
    taxa_media_adv = res_cruz_df["n_contidos"].sum() / res_cruz_df["n_total"].sum()

    cards_row([
        metric_card("Contenção do Gil Vicente", f"{taxa_gv:.1%}", f"{total_gv} cruzamentos sofridos", "", "bi-shield-check"),
        metric_card("Média dos adversários", f"{taxa_media_adv:.1%}", "8 jogos, 1 por adversário", "navy", "bi-bar-chart-line"),
        metric_card("Diferença", f"{(taxa_gv - taxa_media_adv)*100:+.1f} pp", "a favor do Gil Vicente", "gold", "bi-graph-up-arrow"),
    ])

    res_plot = res_cruz_df.copy()
    res_plot.loc[len(res_plot)] = ["Gil Vicente FC", n_gv, total_gv, taxa_gv]
    res_plot = res_plot.sort_values("taxa")
    cores_barras = [COR_VERMELHO if e == "Gil Vicente FC" else COR_AZUL_MARINHO for e in res_plot["adversario"]]

    titulo_grafico = "Contenção de cruzamentos — Gil Vicente vs. adversários"
    titulo_grafico += " · sem Sporting CP" if excluir_sporting else ""
    chart_header(titulo_grafico, "bi-shield-check")

    fig = go.Figure(go.Bar(
        y=res_plot["adversario"], x=res_plot["taxa"], orientation="h",
        marker_color=cores_barras,
        text=[f"{v:.1%}" for v in res_plot["taxa"]], textposition="outside", cliponaxis=False,
    ))
    fig.add_vline(x=taxa_media_adv, line_dash="dash", line_color="#888",
                  annotation_text=f"Média adversários ({taxa_media_adv:.1%})", annotation_position="top")
    fig = plotly_layout_base(fig, altura=340)
    fig.update_xaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        html(f"""
        <div class="insight-card">
        <h4><i class="bi bi-rulers"></i> Definição de "contido"</h4>
        Um cruzamento conta como contido se a equipa que cruzou <b> não</b> conseguir rematar nos
        {JANELA_CRUZAMENTO}s seguintes — independentemente de o Gil Vicente ter vencido ou não a disputa física
        inicial. É uma medida de resultado coletivo, não de processo individual.
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.markdown(
        html(f"""
        <div style="display:flex; align-items:center; gap:18px; margin:22px 0 18px 0;">
            <div style="flex:1; height:2px; background:{COR_CINZA_CLARO};"></div>
            <div style="display:flex; align-items:center; gap:8px; background:{COR_VERMELHO}; color:white;
                        padding:8px 22px; border-radius:24px; font-weight:800; font-size:16px; white-space:nowrap;">
                <i class="bi bi-arrow-down-circle-fill"></i> MAS
            </div>
            <div style="flex:1; height:2px; background:{COR_CINZA_CLARO};"></div>
        </div>
        <div style="text-align:center; font-size:13px; color:#666; margin-bottom:6px;">
        ao decompor a força geral por tipo de entrega, aparece uma exceção clara
        </div>
        """),
        unsafe_allow_html=True,
    )

    chart_header("Apesar disso: o cruzamento rasteiro é uma fraqueza", "bi-exclamation-diamond")

    st.markdown(
        html("""
        <div class="story-card">
        A força geral em cruzamentos não é uniforme por tipo de entrega. Decompondo por <b> cruzamento alto</b> vs. <b> cruzamento rasteiro</b>, aparece uma inversão clara.
        </div>
        """),
        unsafe_allow_html=True,
    )

    tipo_cruzamento_dados = pd.DataFrame({
        "tipo": ["Cruzamento alto", "Cruzamento rasteiro"],
        "gv": [83.6, 85.7],
        "adversarios": [71.5, 93.8],
    })
    fig_tipo = go.Figure()
    fig_tipo.add_trace(go.Bar(x=tipo_cruzamento_dados["tipo"], y=tipo_cruzamento_dados["gv"],
                               name="Gil Vicente", marker_color=COR_VERMELHO, width=0.32,
                               text=[f"{v:.1f}%" for v in tipo_cruzamento_dados["gv"]], textposition="outside", cliponaxis=False))
    fig_tipo.add_trace(go.Bar(x=tipo_cruzamento_dados["tipo"], y=tipo_cruzamento_dados["adversarios"],
                               name="Média adversários", marker_color=COR_AZUL_MARINHO, width=0.32,
                               text=[f"{v:.1f}%" for v in tipo_cruzamento_dados["adversarios"]], textposition="outside", cliponaxis=False))
    fig_tipo = plotly_layout_base(fig_tipo, altura=360)
    fig_tipo.update_layout(showlegend=True, legend=dict(orientation="h", y=1.25), margin=dict(l=10, r=20, t=95, b=10))
    fig_tipo.update_yaxes(title="Taxa de contenção", tickformat=".0f", ticksuffix="%", range=[0, 125])
    st.plotly_chart(fig_tipo, use_container_width=True)

    st.markdown(
        html("""
        <div class="story-card">
        No cruzamento <b> alto</b>, o Gil Vicente está bem acima da média (+12.1pp) — a vantagem geral vem quase toda
        daqui. No cruzamento <b> rasteiro</b>, o Gil Vicente fica <b> abaixo</b> da média dos adversários (-8.1pp).
        Faz sentido: um cruzamento alto dá tempo à equipa para se reorganizar coletivamente; o rasteiro,
        mais rápido e direto, não dá esse tempo. Amostra pequena (28 cruzamentos rasteiros) — tratar como
        direção plausível, não certeza estatística.
        </div>
        """),
        unsafe_allow_html=True,
    )

    col_lado, col_prof = st.columns(2)
    with col_lado:
        st.markdown(
            html("""
            <div class="insight-card">
            <h4><i class="bi bi-arrow-left-right"></i> De que lado?</h4>
            Os cruzamentos rasteiros vindos do <b> flanco esquerdo do Gil Vicente</b> são muito mais perigosos
            (25.0% de taxa de remate, xG total 0.52) do que os da direita (6.2%, xG total 0.05). A força aérea do lateral esquerdo não se estende a este tipo de entrega mais rápida e rasteira.
            </div>
            """),
            unsafe_allow_html=True,
        )
    with col_prof:
        st.markdown(
            html("""
            <div class="insight-card">
            <h4><i class="bi bi-rulers"></i> De que profundidade?</h4>
            Cruzamentos batidos <b> mesmo da linha de fundo</b> (até 5.4m de profundidade) geram 0% de
            remates — muito bem controlados. Os batidos de uma <b> zona mais recuada</b> (mais de 12.1m de
            profundidade) são os mais perigosos (30.0% de taxa de remate) — mais difíceis de antecipar do
            que a entrega clássica. Medida como distância pura no eixo de profundidade à linha de fundo
            (não a distância euclidiana à baliza, que mistura profundidade com largura).
            </div>
            """),
            unsafe_allow_html=True,
        )

    tabela_lado_prof = pd.DataFrame([
        {"grupo": "Lado", "categoria": "Esquerda", "n": 12, "taxa_remate": 25.0, "xg_total": 0.52},
        {"grupo": "Lado", "categoria": "Direita", "n": 16, "taxa_remate": 6.2, "xg_total": 0.05},
        {"grupo": "Profundidade", "categoria": "Linha de fundo (≤ 5.4m)", "n": 9, "taxa_remate": 0.0, "xg_total": 0.00},
        {"grupo": "Profundidade", "categoria": "Zona intermédia (5.4–12.1m)", "n": 9, "taxa_remate": 11.1, "xg_total": 0.05},
        {"grupo": "Profundidade", "categoria": "Mais recuado (> 12.1m)", "n": 10, "taxa_remate": 30.0, "xg_total": 0.52},
    ])

    tabela_html_lp = """
    <table style="width:100%; border-collapse:collapse; margin-top:14px; font-size:13px;">
    <thead>
    <tr style="border-bottom:2px solid #D9D9D9;">
        <th style="text-align:left; padding:7px 8px;">Dimensão</th>
        <th style="text-align:left; padding:7px 8px;">Categoria</th>
        <th style="text-align:right; padding:7px 8px;">Nº de casos</th>
        <th style="text-align:right; padding:7px 8px;">Taxa de remate</th>
        <th style="text-align:right; padding:7px 8px;">xG total</th>
    </tr>
    </thead>
    <tbody>
    """
    grupo_anterior = None
    for _, row in tabela_lado_prof.iterrows():
        destaque = row["taxa_remate"] == tabela_lado_prof[tabela_lado_prof["grupo"] == row["grupo"]]["taxa_remate"].max()
        cor_fundo = COR_FUNDO_CAMPO if destaque else COR_BRANCO
        peso = "700" if destaque else "400"
        cor_texto = COR_VERMELHO_ESCURO if destaque else "#333"
        grupo_txt = row["grupo"] if row["grupo"] != grupo_anterior else ""
        grupo_anterior = row["grupo"]
        tabela_html_lp += (
            f'<tr style="background:{cor_fundo}; font-weight:{peso}; color:{cor_texto};">'
            f'<td style="padding:6px 8px; color:{COR_AZUL_MARINHO}; font-weight:600;">{grupo_txt}</td>'
            f'<td style="padding:6px 8px;">{row["categoria"]}</td>'
            f'<td style="text-align:right; padding:6px 8px;">{row["n"]}</td>'
            f'<td style="text-align:right; padding:6px 8px;">{row["taxa_remate"]:.1f}%</td>'
            f'<td style="text-align:right; padding:6px 8px;">{row["xg_total"]:.2f}</td>'
            f'</tr>'
        )
    tabela_html_lp += "</tbody></table>"
    st.markdown(html(tabela_html_lp), unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:11px; color:#999; margin-top:4px;">Linha destacada = maior taxa de remate dentro de cada dimensão. Amostra pequena (28 cruzamentos rasteiros) — tratar como direção plausível.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        html("""
        <div class="story-card">
        <b> Recomendação:</b> ao chegar a zona de cruzamento, priorizar o cruzamento rasteiro em vez do alto
        — de preferência a partir do flanco esquerdo do Gil Vicente e de uma zona a mais de 12.1m de profundidade da
        linha de fundo (não colada à linha). Metade destas situações surgem em jogo organizado (não só em
        transição), por isso a equipa pode procurar criar esta situação deliberadamente, não só aproveitá-la
        de forma oportunista.
        </div>
        """),
        unsafe_allow_html=True,
    )


# METODOLOGIA

with tab_metodologia:
    st.markdown("### Metodologia, definições e limitações")

    st.markdown(
        html("""
        <div class="insight-card">
        <h4><i class="bi bi-book"></i> Definições operacionais</h4>
        <b> Bola solta (LOOSE_BALL_REGAIN)</b>: momento em que um jogador ganha o controlo de uma bola sem
        dono claro. Definição inferida do nome da coluna, não confirmada com documentação oficial.<br><br>
        <b> Cruzamento contido</b>: cruzamento que não resulta em remate da equipa atacante nos  10s seguintes.<br><br>
        <b> Terço/corredor</b>: campo dividido em 3 terços (X) e 3 corredores (Y), usando coordenada normalizada.
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.markdown(
        html("""
        <div class="insight-card">
        <h4><i class="bi bi-tools"></i> Correções técnicas relevantes</h4>
        <b> Offset de tempo entre partes</b>: a 2ª parte começa com um offset fixo de 10000s em todos os jogos
        — corrigido com um tempo normalizado contínuo.<br><br>
        <b> Orientação das coordenadas</b>: absolutas no campo real, com troca de lado ao intervalo —
        normalizadas para negativo = baliza adversária (o Gil Vicente ataca), positivo = baliza do
        Gil Vicente (o adversário ataca). Confirmado com a posição real dos golos marcados/sofridos.<br><br>
        <b> Duelos terrestres</b>: a coluna result está vazia para GROUND_DUEL; o vencedor é
        identificado via WON_GROUND_DUELS e duelPlayerName.
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.markdown(
        html("""
        <div class="insight-card">
        <h4><i class="bi bi-exclamation-triangle"></i> Limitações gerais</h4>
        Amostra de 8 jogos — qualquer teste estatístico aqui é indicativo, não conclusivo. Dados do adversário mais limitados em volume total (densidade por jogo comparável ao Gil Vicente). Métricas nativas do
        IMPECT (pxT, zonas pré-classificadas) usadas como estão, sem verificação da fórmula exata do
        fornecedor.
        </div>
        """),
        unsafe_allow_html=True,
    )

st.markdown(
    f'<hr style="border:none; border-top:1px solid {COR_CINZA_CLARO}; margin:32px 0 12px 0;">',
    unsafe_allow_html=True,
)
st.markdown(
    html(f"""
    <div style="text-align:center; font-size:12.5px; color:#999; padding-bottom:14px;">
    Trabalho realizado por: Ricardo Bonança
    </div>
    """),
    unsafe_allow_html=True,
)