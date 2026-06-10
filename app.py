
import streamlit as st
import pandas as pd
import numpy as np
import random
import hashlib
import json
import gzip
import base64
from itertools import combinations
from collections import defaultdict

st.set_page_config(
    page_title="Dashboard Copa 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS / DARK DASHBOARD
# =========================
def inject_css():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background: radial-gradient(circle at top left, #1b2a2f 0%, #090d10 42%, #050607 100%);
        color: #f2f2f2;
    }
    h1, h2, h3 {
        color: #f8d66d !important;
        letter-spacing: .3px;
    }
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #111820, #172228);
        border: 1px solid rgba(248,214,109,.35);
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,.28);
    }
    div[data-testid="stMetricLabel"] {
        color: #aeb9c2 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #39ff88 !important;
    }
    .card {
        background: linear-gradient(135deg, rgba(17,24,32,.98), rgba(9,13,16,.96));
        border: 1px solid rgba(248,214,109,.25);
        border-radius: 18px;
        padding: 18px;
        margin: 10px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,.35);
    }
    .match-card {
        background: #0e1419;
        border-left: 4px solid #39ff88;
        border-radius: 14px;
        padding: 14px;
        margin: 10px 0 16px 0;
    }
    .round-card {
        background: #101820;
        border: 1px solid rgba(57,255,136,.22);
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 14px;
    }
    .teamline {
        font-size: 1.05rem;
        font-weight: 700;
    }
    .muted {
        color: #9ba6af;
        font-size: .92rem;
    }
    .gold {
        color: #f8d66d;
        font-weight: 800;
    }
    .neon {
        color: #39ff88;
        font-weight: 800;
    }
    .stButton > button {
        background: linear-gradient(90deg, #1d7f4e, #39ff88);
        color: #06100a;
        border: 0;
        border-radius: 12px;
        font-weight: 800;
        padding: .55rem 1rem;
    }
    .stButton > button:hover {
        filter: brightness(1.10);
        color: #000;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(248,214,109,.20);
        border-radius: 14px;
        overflow: hidden;
    }
    [data-baseweb="tab-list"] {
        gap: 8px;
    }
    [data-baseweb="tab"] {
        background-color: #111820;
        border-radius: 12px 12px 0 0;
        color: #d9e0e5;
        border: 1px solid rgba(248,214,109,.14);
    }
    [aria-selected="true"] {
        color: #39ff88 !important;
        border-bottom: 2px solid #39ff88 !important;
    }

    /* GE-like dark readability fixes */
    input, textarea {
        color: #f9fafb !important;
        background-color: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        color: #f9fafb !important;
        border-color: #334155 !important;
    }
    .bracket-board {
        display: flex;
        gap: 14px;
        overflow-x: auto;
        padding: 12px 2px 20px 2px;
    }
    .bracket-round {
        min-width: 240px;
    }
    .bracket-title {
        color: #39ff88;
        font-weight: 900;
        margin-bottom: 10px;
        text-transform: uppercase;
        font-size: .88rem;
        letter-spacing: .08em;
    }
    .bracket-match {
        position: relative;
        background: linear-gradient(135deg, #0f172a, #111820);
        border: 1px solid rgba(57,255,136,.28);
        border-left: 4px solid #39ff88;
        border-radius: 14px;
        padding: 10px 12px;
        margin-bottom: 14px;
        color: #f8fafc;
        box-shadow: 0 8px 18px rgba(0,0,0,.25);
    }
    .bracket-team {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        font-size: .92rem;
        padding: 3px 0;
        border-bottom: 1px solid rgba(148,163,184,.12);
    }
    .bracket-team:last-child { border-bottom: 0; }
    .bracket-winner { color: #39ff88; font-weight: 900; }
    .small-chip {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 999px;
        background: rgba(57,255,136,.12);
        border: 1px solid rgba(57,255,136,.35);
        color: #d1fae5;
        font-size: .78rem;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# =========================
# DADOS FIXOS DO TORNEIO
# =========================
GROUPS = {
    "A": ["México", "África do Sul", "Coreia do Sul", "República Tcheca"],
    "B": ["Canadá", "Bósnia e Herzegovina", "Catar", "Suíça"],
    "C": ["Brasil", "Marrocos", "Haiti", "Escócia"],
    "D": ["Estados Unidos", "Paraguai", "Austrália", "Turquia"],
    "E": ["Alemanha", "Curaçao", "Costa do Marfim", "Equador"],
    "F": ["Países Baixos", "Japão", "Suécia", "Tunísia"],
    "G": ["Bélgica", "Egito", "Irã", "Nova Zelândia"],
    "H": ["Espanha", "Cabo Verde", "Arábia Saudita", "Uruguai"],
    "I": ["França", "Senegal", "Iraque", "Noruega"],
    "J": ["Argentina", "Argélia", "Áustria", "Jordânia"],
    "K": ["Portugal", "Colômbia", "Uzbequistão", "RD Congo"],
    "L": ["Inglaterra", "Croácia", "Gana", "Panamá"],
}

ALL_TEAMS = [team for teams in GROUPS.values() for team in teams]

FLAGS = {
    "México":"🇲🇽", "África do Sul":"🇿🇦", "Coreia do Sul":"🇰🇷", "República Tcheca":"🇨🇿",
    "Canadá":"🇨🇦", "Bósnia e Herzegovina":"🇧🇦", "Catar":"🇶🇦", "Suíça":"🇨🇭",
    "Brasil":"🇧🇷", "Marrocos":"🇲🇦", "Haiti":"🇭🇹", "Escócia":"🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Estados Unidos":"🇺🇸", "Paraguai":"🇵🇾", "Austrália":"🇦🇺", "Turquia":"🇹🇷",
    "Alemanha":"🇩🇪", "Curaçao":"🇨🇼", "Costa do Marfim":"🇨🇮", "Equador":"🇪🇨",
    "Países Baixos":"🇳🇱", "Japão":"🇯🇵", "Suécia":"🇸🇪", "Tunísia":"🇹🇳",
    "Bélgica":"🇧🇪", "Egito":"🇪🇬", "Irã":"🇮🇷", "Nova Zelândia":"🇳🇿",
    "Espanha":"🇪🇸", "Cabo Verde":"🇨🇻", "Arábia Saudita":"🇸🇦", "Uruguai":"🇺🇾",
    "França":"🇫🇷", "Senegal":"🇸🇳", "Iraque":"🇮🇶", "Noruega":"🇳🇴",
    "Argentina":"🇦🇷", "Argélia":"🇩🇿", "Áustria":"🇦🇹", "Jordânia":"🇯🇴",
    "Portugal":"🇵🇹", "Colômbia":"🇨🇴", "Uzbequistão":"🇺🇿", "RD Congo":"🇨🇩",
    "Inglaterra":"🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croácia":"🇭🇷", "Gana":"🇬🇭", "Panamá":"🇵🇦",
}

# Ranking mockado: quanto menor, mais forte.
FIFA_RANKING = {
    "Argentina": 1, "França": 2, "Espanha": 3, "Inglaterra": 4, "Brasil": 5, "Portugal": 6,
    "Países Baixos": 7, "Bélgica": 8, "Alemanha": 9, "Croácia": 10, "Uruguai": 11, "Colômbia": 12,
    "Marrocos": 13, "Suíça": 14, "Estados Unidos": 15, "México": 16, "Japão": 17, "Senegal": 18,
    "Equador": 19, "Áustria": 20, "Coreia do Sul": 21, "Austrália": 22, "Irã": 23, "Turquia": 24,
    "Suécia": 25, "Catar": 26, "Costa do Marfim": 27, "Paraguai": 28, "Canadá": 29, "Egito": 30,
    "Tunísia": 31, "Argélia": 32, "Noruega": 33, "Escócia": 34, "Arábia Saudita": 35, "Gana": 36,
    "África do Sul": 37, "Panamá": 38, "Uzbequistão": 39, "Cabo Verde": 40, "Iraque": 41, "Jordânia": 42,
    "Haiti": 43, "Nova Zelândia": 44, "Bósnia e Herzegovina": 45, "República Tcheca": 46, "RD Congo": 47, "Curaçao": 48
}

# =========================
# BASE REAL DO PDF EMBUTIDA
# 48 seleções x 26 atletas = 1.248 atletas
# Campos: team, fifa_code, pos, player_name, shirt_name, club, dob, height_cm
# =========================
PLAYER_BLOB = "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"

@st.cache_data(show_spinner=False)
def load_players() -> pd.DataFrame:
    raw = gzip.decompress(base64.b64decode(PLAYER_BLOB.encode("ascii"))).decode("utf-8")
    df = pd.DataFrame(json.loads(raw))
    df = df[df["team"].isin(ALL_TEAMS)].copy()
    df["ovr"] = df.apply(lambda r: generate_player_ovr(r["team"], r["pos"], r["player_name"], r["club"]), axis=1)
    df["display"] = df["player_name"] + " · " + df["pos"] + " · OVR " + df["ovr"].astype(str)
    return df

def stable_rand_int(seed: str, low: int, high: int) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    value = int(digest[:8], 16)
    return low + (value % (high - low + 1))

def generate_player_ovr(team: str, pos: str, name: str, club: str) -> int:
    rank = FIFA_RANKING.get(team, 48)
    # base mais alta para ranking melhor
    base = 88 - (rank - 1) * 0.43
    pos_bonus = {"GK": 0.2, "DF": 0.0, "MF": 0.4, "FW": 0.6}.get(pos, 0)
    club_bonus = 0
    elite_clubs = ["Real Madrid", "Barcelona", "Liverpool", "Manchester City", "Bayern", "Paris Saint-Germain",
                   "Arsenal", "Chelsea", "Internazionale", "Atlético", "Juventus", "Tottenham", "Leverkusen"]
    if any(c.lower() in club.lower() for c in elite_clubs):
        club_bonus += 2
    noise = stable_rand_int(team + name + club, -5, 5)
    return int(np.clip(round(base + pos_bonus + club_bonus + noise), 50, 96))

@st.cache_data(show_spinner=False)
def team_ovr_table(players: pd.DataFrame) -> pd.DataFrame:
    return (players.groupby("team", as_index=False)["ovr"]
            .mean()
            .rename(columns={"ovr":"OVR Médio"})
            .assign(**{"OVR Médio": lambda x: x["OVR Médio"].round(1)}))

def team_power(team: str, ovr_lookup: dict) -> float:
    rank = FIFA_RANKING.get(team, 48)
    rank_score = (49 - rank) / 48          # 0 a 1
    ovr_score = (ovr_lookup.get(team, 70) - 50) / 50
    return 0.56 * rank_score + 0.44 * ovr_score

# =========================
# SESSION STATE
# =========================
def make_group_matches():
    matches = []
    for group, teams in GROUPS.items():
        for i, (home, away) in enumerate(combinations(teams, 2), start=1):
            matches.append({
                "id": f"G{group}_{i}",
                "phase": "Grupos",
                "group": group,
                "home": home,
                "away": away
            })
    return matches

def init_state():
    if "group_matches" not in st.session_state:
        st.session_state.group_matches = make_group_matches()
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "events" not in st.session_state:
        st.session_state.events = {}
    if "fair_play" not in st.session_state:
        # Fair play começa zerado; cartões simulados/manualizados entram por partida.
        st.session_state.fair_play = {t: 0 for t in ALL_TEAMS}
    if "discipline" not in st.session_state:
        st.session_state.discipline = {}
    if "sim_wins" not in st.session_state:
        st.session_state.sim_wins = {t: 0 for t in ALL_TEAMS}
    if "sim_runs" not in st.session_state:
        st.session_state.sim_runs = 0
    if "knockout_rounds" not in st.session_state:
        st.session_state.knockout_rounds = {}
    if "team_stage" not in st.session_state:
        st.session_state.team_stage = {t: "Fase de Grupos" for t in ALL_TEAMS}
    if "champion" not in st.session_state:
        st.session_state.champion = None

init_state()
players_df = load_players()
ovr_df = team_ovr_table(players_df)
OVR_LOOKUP = dict(zip(ovr_df["team"], ovr_df["OVR Médio"]))

# =========================
# FUNÇÕES DE PARTIDA / TABELA
# =========================
def fair_play_totals():
    totals = {t: 0 for t in ALL_TEAMS}
    for match_cards in st.session_state.get("discipline", {}).values():
        for team, data in match_cards.items():
            totals[team] = totals.get(team, 0) + int(data.get("fp", 0))
    return totals

def empty_stats():
    fp_totals = fair_play_totals()
    return {t: dict(Time=t, Ranking=FIFA_RANKING[t], OVR=OVR_LOOKUP.get(t, 70), J=0, V=0, E=0, D=0, GP=0, GC=0, SG=0, Pts=0, FP=fp_totals.get(t, 0)) for t in ALL_TEAMS}

def simulate_cards_for_match(match_id: str, home: str, away: str):
    """Gera cartões com pontuação FIFA-like: amarelo=-1, 2A+V=-3, vermelho direto=-4."""
    cards = {}
    for team in [home, away]:
        # Times de menor ranking tendem a sofrer um pouco mais defensivamente.
        rank_factor = FIFA_RANKING.get(team, 48) / 48
        yellows = int(np.clip(np.random.poisson(1.35 + 0.55 * rank_factor), 0, 6))
        second_yellow_red = 1 if random.random() < (0.035 + 0.025 * rank_factor) else 0
        direct_red = 1 if random.random() < (0.025 + 0.025 * rank_factor) else 0
        yellow_direct_red = 1 if random.random() < 0.010 else 0
        fp = -1*yellows -3*second_yellow_red -4*direct_red -5*yellow_direct_red
        cards[team] = {
            "yellow": yellows,
            "second_yellow_red": second_yellow_red,
            "direct_red": direct_red,
            "yellow_direct_red": yellow_direct_red,
            "fp": fp,
        }
    st.session_state.discipline[match_id] = cards

def discipline_table():
    rows = []
    for match_id, cards in st.session_state.get("discipline", {}).items():
        for team, c in cards.items():
            rows.append({
                "Seleção": f"{FLAGS.get(team,'')} {team}",
                "Amarelos": c.get("yellow", 0),
                "Vermelho 2A": c.get("second_yellow_red", 0),
                "Vermelho direto": c.get("direct_red", 0),
                "Amarelo+VD": c.get("yellow_direct_red", 0),
                "Fair Play": c.get("fp", 0),
            })
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    return df.groupby("Seleção", as_index=False).sum().sort_values("Fair Play", ascending=True)

def register_match(stats, home, away, hg, ag):
    stats[home]["J"] += 1
    stats[away]["J"] += 1
    stats[home]["GP"] += hg
    stats[home]["GC"] += ag
    stats[away]["GP"] += ag
    stats[away]["GC"] += hg
    stats[home]["SG"] = stats[home]["GP"] - stats[home]["GC"]
    stats[away]["SG"] = stats[away]["GP"] - stats[away]["GC"]

    if hg > ag:
        stats[home]["V"] += 1; stats[away]["D"] += 1; stats[home]["Pts"] += 3
    elif ag > hg:
        stats[away]["V"] += 1; stats[home]["D"] += 1; stats[away]["Pts"] += 3
    else:
        stats[home]["E"] += 1; stats[away]["E"] += 1; stats[home]["Pts"] += 1; stats[away]["Pts"] += 1

def all_played_group_matches():
    return all(st.session_state.results.get(m["id"], {}).get("played", False) for m in st.session_state.group_matches)

def compute_group_tables():
    stats = empty_stats()
    for m in st.session_state.group_matches:
        r = st.session_state.results.get(m["id"])
        if r and r.get("played"):
            register_match(stats, m["home"], m["away"], int(r["home_goals"]), int(r["away_goals"]))

    tables = {}
    for group, teams in GROUPS.items():
        df = pd.DataFrame([stats[t] for t in teams])
        # Desempate RIGOROSO:
        # 1 pontos desc; 2 saldo desc; 3 gols pró desc; 4 menor FP asc; 5 ranking asc
        df = df.sort_values(["Pts", "SG", "GP", "FP", "Ranking"], ascending=[False, False, False, True, True]).reset_index(drop=True)
        df.insert(0, "Pos", range(1, len(df)+1))
        df["Seleção"] = df["Time"].map(lambda t: f"{FLAGS.get(t,'🏳️')} {t}")
        tables[group] = df[["Pos", "Seleção", "Time", "J", "V", "E", "D", "GP", "GC", "SG", "Pts", "FP", "Ranking", "OVR"]]
    return tables, pd.DataFrame(stats.values())

def qualified_teams():
    tables, _ = compute_group_tables()
    direct = []
    thirds = []
    for g, df in tables.items():
        direct += df.iloc[:2]["Time"].tolist()
        third = df.iloc[2].copy()
        third["Grupo"] = g
        thirds.append(third)
    thirds_df = pd.DataFrame(thirds)
    thirds_df = thirds_df.sort_values(["Pts", "SG", "GP", "FP", "Ranking"], ascending=[False, False, False, True, True]).reset_index(drop=True)
    best_thirds = thirds_df.head(8)["Time"].tolist()
    return direct, best_thirds, thirds_df

def highlight_group_rows(row):
    if row["Pos"] <= 2:
        return ["background-color: #064e3b; color: #ecfdf5; font-weight: 800"] * len(row)
    if row["Pos"] == 3:
        return ["background-color: #78350f; color: #fef3c7; font-weight: 800"] * len(row)
    return ["background-color: #111827; color: #e5e7eb"] * len(row)

def highlight_thirds(row):
    if row.name < 8:
        return ["background-color: #064e3b; color: #ecfdf5; font-weight: 800"] * len(row)
    return ["background-color: #7f1d1d; color: #fee2e2; font-weight: 800"] * len(row)

def simulate_score(home: str, away: str) -> tuple[int, int]:
    ph = team_power(home, OVR_LOOKUP)
    pa = team_power(away, OVR_LOOKUP)
    diff = ph - pa

    # Poisson com viés moderado. Evita placares absurdos.
    home_lambda = np.clip(1.20 + diff * 1.35, 0.25, 3.20)
    away_lambda = np.clip(1.05 - diff * 1.35, 0.25, 3.00)

    hg = int(np.random.poisson(home_lambda))
    ag = int(np.random.poisson(away_lambda))
    return min(hg, 6), min(ag, 6)

def store_simulated_match(m):
    """
    Simula uma partida da fase de grupos e sincroniza tudo que a interface usa:
    - resultado lógico da classificação;
    - inputs visuais do placar;
    - checkbox de jogo confirmado;
    - eventos automáticos de gols/assistências;
    - cartões/fair play.
    """
    mid = m["id"]
    home, away = m["home"], m["away"]
    hg, ag = simulate_score(home, away)

    st.session_state.results[mid] = {
        "home_goals": int(hg),
        "away_goals": int(ag),
        "played": True
    }

    # Estes são os estados dos widgets number_input/checkbox da tela.
    # Sem isso, a classificação muda, mas o placar visual fica 0x0.
    st.session_state[f"{mid}_hg"] = int(hg)
    st.session_state[f"{mid}_ag"] = int(ag)
    st.session_state[f"{mid}_played"] = True

    make_auto_events(mid, home, away, int(hg), int(ag))
    simulate_cards_for_match(mid, home, away)
    return int(hg), int(ag)


def team_players(team: str):
    df = players_df[players_df["team"] == team].sort_values(["pos", "player_name"])
    return ["Sem assistência"] + df["display"].tolist()

def pure_player_name(display: str) -> str:
    if display == "Sem assistência":
        return ""
    return display.split(" · ")[0]


def display_from_pure_name(team: str, pure_name: str) -> str:
    """
    Converte o nome puro salvo nos eventos para o texto completo usado no selectbox.
    Exemplo: "Neymar JR" -> "Neymar JR · FW · Santos FC".
    """
    if not pure_name:
        return "Sem assistência"

    options = team_players(team)
    for option in options:
        if option != "Sem assistência" and pure_player_name(option) == pure_name:
            return option
    return "Sem assistência"

def make_auto_events(match_id, home, away, hg, ag):
    """
    Sorteia automaticamente autores dos gols e assistentes.
    Além de salvar os eventos, preenche também os estados dos selectboxes,
    para que a interface mostre os jogadores sorteados após simular grupo/partida.
    """
    events = []

    for team, goals in [(home, hg), (away, ag)]:
        df = players_df[players_df["team"] == team].copy()

        # Atacantes e meias têm mais chance de participar de gols.
        weights = df["pos"].map({"FW": 5.0, "MF": 3.0, "DF": 1.2, "GK": 0.05}).fillna(1.0).to_numpy(dtype=float)
        weights = weights / weights.sum()
        names = df["display"].tolist()

        for goal_n in range(int(goals)):
            scorer_display = np.random.choice(names, p=weights)

            assist_options = ["Sem assistência"] + names
            assist_weights = [0.18] + list(weights * 0.82)
            assist_display = np.random.choice(assist_options, p=assist_weights)

            # Evita assistência para o próprio autor do gol.
            if assist_display == scorer_display:
                assist_display = "Sem assistência"

            scorer_pure = pure_player_name(scorer_display)
            assist_pure = pure_player_name(assist_display)

            events.append({"team": team, "scorer": scorer_pure, "assist": assist_pure})

            # Estados dos widgets selectbox já existentes.
            scorer_key = f"{match_id}_{team}_g{goal_n}_scorer"
            assist_key = f"{match_id}_{team}_g{goal_n}_assist"
            st.session_state[scorer_key] = scorer_display
            st.session_state[assist_key] = assist_display

    st.session_state.events[match_id] = events

def render_goal_selectors(match_id: str, home: str, away: str, hg: int, ag: int):
    """
    Renderiza os selectboxes de gols e assistências.
    Se a partida foi simulada, os campos já vêm preenchidos automaticamente.
    """
    total = int(hg) + int(ag)
    if total <= 0:
        st.session_state.events[match_id] = []
        return

    st.markdown("<span class='muted'>Eventos do jogo: escolha os autores dos gols e assistências.</span>", unsafe_allow_html=True)

    previous_events = st.session_state.events.get(match_id, [])
    updated_events = []
    cols = st.columns(2)

    for team, goals in [(home, int(hg)), (away, int(ag))]:
        with cols[0 if team == home else 1]:
            st.markdown(f"**{FLAGS.get(team,'')} {team}**")
            options = team_players(team)
            scorer_options = options[1:]

            team_previous_events = [ev for ev in previous_events if ev.get("team") == team]

            for goal_n in range(goals):
                scorer_key = f"{match_id}_{team}_g{goal_n}_scorer"
                assist_key = f"{match_id}_{team}_g{goal_n}_assist"

                # Se já existe evento salvo, usa-o como valor inicial do widget.
                if goal_n < len(team_previous_events):
                    old_event = team_previous_events[goal_n]
                    default_scorer = display_from_pure_name(team, old_event.get("scorer", ""))
                    default_assist = display_from_pure_name(team, old_event.get("assist", ""))

                    if default_scorer in scorer_options:
                        st.session_state.setdefault(scorer_key, default_scorer)
                    if default_assist in options:
                        st.session_state.setdefault(assist_key, default_assist)

                scorer = st.selectbox(f"Gol {goal_n+1} - marcador", scorer_options, key=scorer_key)
                assist = st.selectbox(f"Gol {goal_n+1} - assistência", options, key=assist_key)

                updated_events.append({
                    "team": team,
                    "scorer": pure_player_name(scorer),
                    "assist": pure_player_name(assist)
                })

    st.session_state.events[match_id] = updated_events

def render_match_input(m):
    mid = m["id"]
    home, away = m["home"], m["away"]
    current = st.session_state.results.get(mid, {"home_goals": 0, "away_goals": 0, "played": False})
    st.markdown(f"""
    <div class="match-card">
        <div class="teamline">{FLAGS.get(home,'')} {home} <span class="gold">vs</span> {FLAGS.get(away,'')} {away}</div>
        <div class="muted">Ranking: {home} #{FIFA_RANKING[home]} · OVR {OVR_LOOKUP.get(home,70):.1f} | {away} #{FIFA_RANKING[away]} · OVR {OVR_LOOKUP.get(away,70):.1f}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1.2, .8, .8, 1.2])
    with c1:
        if st.button("🎲 Simular partida", key=f"sim_one_{mid}"):
            store_simulated_match(m)
            st.rerun()
    current = st.session_state.results.get(mid, current)
    with c2:
        hg = st.number_input(f"Gols {home}", min_value=0, max_value=15, value=int(current["home_goals"]), key=f"{mid}_hg")
    with c3:
        ag = st.number_input(f"Gols {away}", min_value=0, max_value=15, value=int(current["away_goals"]), key=f"{mid}_ag")
    played = st.checkbox("Jogo confirmado", value=bool(current["played"]), key=f"{mid}_played")

    st.session_state.results[mid] = {"home_goals": int(hg), "away_goals": int(ag), "played": bool(played)}
    if played and mid not in st.session_state.discipline:
        st.session_state.discipline[mid] = {home: {"yellow": 0, "second_yellow_red": 0, "direct_red": 0, "yellow_direct_red": 0, "fp": 0}, away: {"yellow": 0, "second_yellow_red": 0, "direct_red": 0, "yellow_direct_red": 0, "fp": 0}}
    if played:
        render_goal_selectors(mid, home, away, int(hg), int(ag))

# =========================
# MATA-MATA
# =========================
ROUND_ORDER = ["16-avos", "Oitavas", "Quartas", "Semifinal", "Final"]
NEXT_ROUND = {"16-avos":"Oitavas", "Oitavas":"Quartas", "Quartas":"Semifinal", "Semifinal":"Final"}

STAGE_VALUE = {
    "Fase de Grupos": 1,
    "16-avos": 2,
    "Oitavas": 3,
    "Quartas": 4,
    "Semifinal": 5,
    "Vice-campeão": 6,
    "Campeão": 7,
}

def generate_round_of_32():
    direct, best_thirds, thirds_df = qualified_teams()
    teams = direct + best_thirds
    # Ordena os 32 classificados pelo desempenho na fase de grupos.
    tables, overall = compute_group_tables()
    group_perf = []
    for g, df in tables.items():
        for _, r in df.iterrows():
            if r["Time"] in teams:
                group_perf.append(r)
    seed_df = pd.DataFrame(group_perf).sort_values(["Pts","SG","GP","FP","Ranking"], ascending=[False,False,False,True,True]).reset_index(drop=True)
    seeds = seed_df["Time"].tolist()

    pair_indices = [(0,31),(15,16),(7,24),(8,23),(3,28),(12,19),(4,27),(11,20),
                    (1,30),(14,17),(6,25),(9,22),(2,29),(13,18),(5,26),(10,21)]
    matches = []
    for i, (a, b) in enumerate(pair_indices):
        matches.append({"id": f"KO_32_{i}", "phase": "16-avos", "home": seeds[a], "away": seeds[b]})
    st.session_state.knockout_rounds = {"16-avos": matches}
    for t in teams:
        st.session_state.team_stage[t] = "16-avos"

def get_match_winner(mid, home, away, hg, ag):
    if hg > ag:
        return home
    if ag > hg:
        return away
    return st.session_state.results.get(mid, {}).get("winner", home)

def render_knockout_match(m):
    mid, phase, home, away = m["id"], m["phase"], m["home"], m["away"]
    current = st.session_state.results.get(mid, {"home_goals": 0, "away_goals": 0, "played": False, "winner": home})
    st.markdown(f"""
    <div class="round-card">
        <strong>{FLAGS.get(home,'')} {home}</strong> <span class="gold">vs</span> <strong>{FLAGS.get(away,'')} {away}</strong><br>
        <span class="muted">{phase} · força: {team_power(home, OVR_LOOKUP):.2f} x {team_power(away, OVR_LOOKUP):.2f}</span>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,2])
    with c1:
        hg = st.number_input(f"{home}", min_value=0, max_value=15, value=int(current["home_goals"]), key=f"{mid}_ko_hg")
    with c2:
        ag = st.number_input(f"{away}", min_value=0, max_value=15, value=int(current["away_goals"]), key=f"{mid}_ko_ag")
    winner = home if hg > ag else away if ag > hg else current.get("winner", home)
    if hg == ag:
        with c3:
            winner = st.selectbox("Vencedor nos pênaltis/prorrogação", [home, away], index=0 if winner == home else 1, key=f"{mid}_winner")
    played = st.checkbox("Partida encerrada", value=bool(current["played"]), key=f"{mid}_ko_played")

    st.session_state.results[mid] = {"home_goals": int(hg), "away_goals": int(ag), "played": bool(played), "winner": winner}
    if played:
        render_goal_selectors(mid, home, away, int(hg), int(ag))

def current_round_complete(phase):
    matches = st.session_state.knockout_rounds.get(phase, [])
    return bool(matches) and all(st.session_state.results.get(m["id"], {}).get("played", False) for m in matches)

def advance_round(phase):
    matches = st.session_state.knockout_rounds.get(phase, [])
    winners = []
    for m in matches:
        r = st.session_state.results[m["id"]]
        winner = get_match_winner(m["id"], m["home"], m["away"], r["home_goals"], r["away_goals"])
        loser = m["away"] if winner == m["home"] else m["home"]
        winners.append(winner)
        if phase == "Final":
            st.session_state.team_stage[winner] = "Campeão"
            st.session_state.team_stage[loser] = "Vice-campeão"
            st.session_state.champion = winner
        else:
            st.session_state.team_stage[loser] = phase

    if phase == "Final":
        return

    next_phase = NEXT_ROUND[phase]
    next_matches = []
    for i in range(0, len(winners), 2):
        next_matches.append({"id": f"KO_{next_phase}_{i//2}", "phase": next_phase, "home": winners[i], "away": winners[i+1]})
    st.session_state.knockout_rounds[next_phase] = next_matches
    for w in winners:
        st.session_state.team_stage[w] = next_phase

def simulate_round(phase):
    for m in st.session_state.knockout_rounds.get(phase, []):
        hg, ag = simulate_score(m["home"], m["away"])
        if hg == ag:
            p_home = team_power(m["home"], OVR_LOOKUP)
            p_away = team_power(m["away"], OVR_LOOKUP)
            winner = random.choices([m["home"], m["away"]], weights=[p_home, p_away], k=1)[0]
        else:
            winner = m["home"] if hg > ag else m["away"]
        st.session_state.results[m["id"]] = {"home_goals": int(hg), "away_goals": int(ag), "played": True, "winner": winner}
        st.session_state[f"{m['id']}_ko_hg"] = int(hg)
        st.session_state[f"{m['id']}_ko_ag"] = int(ag)
        st.session_state[f"{m['id']}_ko_played"] = True
        st.session_state[f"{m['id']}_winner"] = winner
        make_auto_events(m["id"], m["home"], m["away"], int(hg), int(ag))
        simulate_cards_for_match(m["id"], m["home"], m["away"])

# =========================
# ESTATÍSTICAS E RANKING FINAL
# =========================
def tournament_team_stats():
    stats = empty_stats()
    # Fase de grupos
    for m in st.session_state.group_matches:
        r = st.session_state.results.get(m["id"])
        if r and r.get("played"):
            register_match(stats, m["home"], m["away"], int(r["home_goals"]), int(r["away_goals"]))
    # Mata-mata: não usa pontos como critério oficial, mas soma desempenho geral para ranking interno.
    for phase, matches in st.session_state.knockout_rounds.items():
        for m in matches:
            r = st.session_state.results.get(m["id"])
            if r and r.get("played"):
                register_match(stats, m["home"], m["away"], int(r["home_goals"]), int(r["away_goals"]))
    return pd.DataFrame(stats.values())

def event_tables():
    goals = defaultdict(int)
    assists = defaultdict(int)
    for events in st.session_state.events.values():
        for ev in events:
            if ev.get("scorer"):
                goals[(ev["scorer"], ev["team"])] += 1
            if ev.get("assist"):
                assists[(ev["assist"], ev["team"])] += 1
    goals_df = pd.DataFrame([{"Jogador": k[0], "Seleção": k[1], "Gols": v} for k, v in goals.items()])
    assists_df = pd.DataFrame([{"Jogador": k[0], "Seleção": k[1], "Assistências": v} for k, v in assists.items()])
    if not goals_df.empty:
        goals_df = goals_df.sort_values(["Gols", "Jogador"], ascending=[False, True]).reset_index(drop=True)
    if not assists_df.empty:
        assists_df = assists_df.sort_values(["Assistências", "Jogador"], ascending=[False, True]).reset_index(drop=True)
    return goals_df, assists_df

def final_ranking_table():
    df = tournament_team_stats()
    df["Fase alcançada"] = df["Time"].map(lambda t: st.session_state.team_stage.get(t, "Fase de Grupos"))
    df["Peso fase"] = df["Fase alcançada"].map(STAGE_VALUE).fillna(1)
    df["Bandeira"] = df["Time"].map(lambda t: FLAGS.get(t, "🏳️"))
    df = df.sort_values(["Peso fase","Pts","V","SG","GP","Ranking"], ascending=[False,False,False,False,False,True]).reset_index(drop=True)
    df.insert(0, "Posição", range(1, len(df)+1))
    df["Seleção"] = df["Bandeira"] + " " + df["Time"]
    return df[["Posição", "Seleção", "Fase alcançada", "J", "V", "E", "D", "GP", "GC", "SG", "Pts", "FP", "Ranking", "OVR"]]

# =========================
# CABEÇALHO
# =========================
st.markdown("""
<div class="card">
    <h1>🏆 Dashboard Simulador da Copa do Mundo FIFA 2026</h1>
    <p class="muted">48 seleções · 12 grupos fixos · 1.248 atletas · OVR por elenco · simulação probabilística · chaveamento visual</p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Seleções", "48")
m2.metric("Jogadores", f"{len(players_df):,}".replace(",", "."))
m3.metric("OVR médio geral", f"{players_df['ovr'].mean():.1f}")
m4.metric("Jogos da fase de grupos", "72")

tab_groups, tab_knockout, tab_stats, tab_simulations, tab_final, tab_squads = st.tabs(
    ["⚽ Fase de Grupos", "🏆 Mata-Mata", "📊 Estatísticas", "🧠 Simulações", "🌍 Classificação Final", "👥 Elencos/OVR"]
)

# =========================
# ABA: FASE DE GRUPOS
# =========================
with tab_groups:
    st.subheader("Fase de Grupos")
    c1, c2, c3 = st.columns([1.1, 1.1, 2.2])
    with c1:
        if st.button("🎲 Simular todos os jogos restantes"):
            for m in st.session_state.group_matches:
                if not st.session_state.results.get(m["id"], {}).get("played", False):
                    store_simulated_match(m)
            st.rerun()
    with c2:
        if st.button("🧹 Resetar torneio"):
            for key in ["results", "events", "knockout_rounds", "team_stage", "champion", "discipline", "fair_play"]:
                if key in st.session_state:
                    del st.session_state[key]
            init_state()
            st.rerun()
    with c3:
        st.info("Placares manuais são livres. Marque 'Jogo confirmado' para computar classificação e abrir seleção de gols/assistências.")

    tables, overall_stats = compute_group_tables()

    left, right = st.columns([1.35, 1])
    with left:
        for group, matches in [(g, [m for m in st.session_state.group_matches if m["group"] == g]) for g in GROUPS]:
            with st.expander(f"Grupo {group} — " + " · ".join([f"{FLAGS.get(t,'')} {t}" for t in GROUPS[group]]), expanded=(group in ["A","B"])):
                gc1, gc2 = st.columns([1, 4])
                with gc1:
                    if st.button(f"🎲 Simular grupo {group}", key=f"sim_group_{group}"):
                        for gm in matches:
                            if not st.session_state.results.get(gm["id"], {}).get("played", False):
                                store_simulated_match(gm)
                        st.rerun()
                st.dataframe(
                    tables[group].drop(columns=["Time"]).style.apply(highlight_group_rows, axis=1),
                    use_container_width=True,
                    hide_index=True
                )
                for m in matches:
                    render_match_input(m)

    with right:
        st.markdown("<div class='card'><h3>Melhores terceiros</h3><p class='muted'>Os 8 primeiros avançam aos 16-avos.</p></div>", unsafe_allow_html=True)
        direct, best_thirds, thirds_df = qualified_teams()
        show_thirds = thirds_df[["Grupo", "Seleção", "Time", "J", "V", "E", "D", "GP", "GC", "SG", "Pts", "FP", "Ranking", "OVR"]].copy()
        st.dataframe(
            show_thirds.drop(columns=["Time"]).style.apply(highlight_thirds, axis=1),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("<div class='card'><h3>Classificados provisórios</h3></div>", unsafe_allow_html=True)
        q = direct + best_thirds
        st.write(", ".join([f"{FLAGS.get(t,'')} {t}" for t in q]))

# =========================
# ABA: MATA-MATA
# =========================
with tab_knockout:
    st.subheader("Fase Mata-Mata")

    if not all_played_group_matches():
        st.warning("Finalize todos os 72 jogos da fase de grupos para gerar o mata-mata com segurança.")
    else:
        if not st.session_state.knockout_rounds:
            if st.button("Gerar chave de 16-avos de final"):
                generate_round_of_32()
                st.rerun()

    if st.session_state.champion:
        st.success(f"🏆 Campeão: {FLAGS.get(st.session_state.champion,'')} {st.session_state.champion}")

    if st.session_state.knockout_rounds:
        round_tabs = st.tabs([r for r in ROUND_ORDER if r in st.session_state.knockout_rounds or r == "16-avos"])
        for i, phase in enumerate([r for r in ROUND_ORDER if r in st.session_state.knockout_rounds]):
            with round_tabs[i]:
                st.markdown(f"### {phase}")
                b1, b2 = st.columns([1, 3])
                with b1:
                    if st.button(f"Simular {phase}", key=f"sim_{phase}"):
                        simulate_round(phase)
                        st.rerun()
                for m in st.session_state.knockout_rounds.get(phase, []):
                    render_knockout_match(m)
                if current_round_complete(phase):
                    if st.button(f"Avançar após {phase}", key=f"adv_{phase}"):
                        advance_round(phase)
                        st.rerun()

        st.markdown("### Chaveamento visual")
        phases = [r for r in ROUND_ORDER if r in st.session_state.knockout_rounds]
        html = ["<div class='bracket-board'>"]
        for phase in phases:
            html.append("<div class='bracket-round'>")
            html.append(f"<div class='bracket-title'>{phase}</div>")
            for m in st.session_state.knockout_rounds[phase]:
                r = st.session_state.results.get(m["id"], {})
                h_score = r.get("home_goals", "") if r.get("played") else ""
                a_score = r.get("away_goals", "") if r.get("played") else ""
                winner = r.get("winner", "") if r.get("played") else ""
                h_cls = "bracket-winner" if winner == m["home"] else ""
                a_cls = "bracket-winner" if winner == m["away"] else ""
                html.append("<div class='bracket-match'>")
                html.append(f"<div class='bracket-team {h_cls}'><span>{FLAGS.get(m['home'],'')} {m['home']}</span><strong>{h_score}</strong></div>")
                html.append(f"<div class='bracket-team {a_cls}'><span>{FLAGS.get(m['away'],'')} {m['away']}</span><strong>{a_score}</strong></div>")
                if winner:
                    html.append(f"<span class='small-chip'>Avança: {FLAGS.get(winner,'')} {winner}</span>")
                html.append("</div>")
            html.append("</div>")
        html.append("</div>")
        st.markdown("".join(html), unsafe_allow_html=True)

# =========================
# ABA: ESTATÍSTICAS
# =========================
with tab_stats:
    st.subheader("Estatísticas")
    goals_df, assists_df = event_tables()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='card'><h3>Artilharia</h3></div>", unsafe_allow_html=True)
        if goals_df.empty:
            st.info("Nenhum gol registrado ainda.")
        else:
            st.dataframe(goals_df, use_container_width=True, hide_index=True)
    with c2:
        st.markdown("<div class='card'><h3>Assistências</h3></div>", unsafe_allow_html=True)
        if assists_df.empty:
            st.info("Nenhuma assistência registrada ainda.")
        else:
            st.dataframe(assists_df, use_container_width=True, hide_index=True)

    st.markdown("<div class='card'><h3>Cartões e Fair Play</h3><p class='muted'>Fair Play negativo: amarelo=-1, vermelho 2A=-3, vermelho direto=-4, amarelo+VD=-5.</p></div>", unsafe_allow_html=True)
    cards_df = discipline_table()
    if cards_df.empty:
        st.info("Nenhum cartão registrado ainda. Jogos simulados geram cartões automaticamente; jogos manuais começam com fair play 0.")
    else:
        st.dataframe(cards_df, use_container_width=True, hide_index=True)

# =========================
# ABA: SIMULAÇÕES MASSIVAS
# =========================
def simulate_full_tournament_once():
    local_results = {}
    def local_register(stats, home, away, hg, ag):
        stats[home]["J"] += 1; stats[away]["J"] += 1
        stats[home]["GP"] += hg; stats[home]["GC"] += ag
        stats[away]["GP"] += ag; stats[away]["GC"] += hg
        stats[home]["SG"] = stats[home]["GP"] - stats[home]["GC"]
        stats[away]["SG"] = stats[away]["GP"] - stats[away]["GC"]
        if hg > ag:
            stats[home]["V"] += 1; stats[away]["D"] += 1; stats[home]["Pts"] += 3
        elif ag > hg:
            stats[away]["V"] += 1; stats[home]["D"] += 1; stats[away]["Pts"] += 3
        else:
            stats[home]["E"] += 1; stats[away]["E"] += 1; stats[home]["Pts"] += 1; stats[away]["Pts"] += 1
    stats = {t: dict(Time=t, Ranking=FIFA_RANKING[t], OVR=OVR_LOOKUP.get(t, 70), J=0, V=0, E=0, D=0, GP=0, GC=0, SG=0, Pts=0, FP=0) for t in ALL_TEAMS}
    for m in make_group_matches():
        hg, ag = simulate_score(m["home"], m["away"])
        local_register(stats, m["home"], m["away"], hg, ag)
    qualified = []
    third_rows = []
    for group, teams in GROUPS.items():
        df = pd.DataFrame([stats[t] for t in teams])
        df = df.sort_values(["Pts", "SG", "GP", "FP", "Ranking"], ascending=[False, False, False, True, True]).reset_index(drop=True)
        qualified += df.head(2)["Time"].tolist()
        third_rows.append(df.iloc[2])
    thirds = pd.DataFrame(third_rows).sort_values(["Pts", "SG", "GP", "FP", "Ranking"], ascending=[False, False, False, True, True]).head(8)["Time"].tolist()
    teams = qualified + thirds
    seed_df = pd.DataFrame([stats[t] for t in teams]).sort_values(["Pts","SG","GP","FP","Ranking"], ascending=[False,False,False,True,True]).reset_index(drop=True)
    seeds = seed_df["Time"].tolist()
    pair_indices = [(0,31),(15,16),(7,24),(8,23),(3,28),(12,19),(4,27),(11,20),(1,30),(14,17),(6,25),(9,22),(2,29),(13,18),(5,26),(10,21)]
    current = [(seeds[a], seeds[b]) for a,b in pair_indices]
    while len(current) >= 1:
        winners = []
        for home, away in current:
            hg, ag = simulate_score(home, away)
            if hg == ag:
                winner = random.choices([home, away], weights=[team_power(home, OVR_LOOKUP), team_power(away, OVR_LOOKUP)], k=1)[0]
            else:
                winner = home if hg > ag else away
            winners.append(winner)
        if len(winners) == 1:
            return winners[0]
        current = [(winners[i], winners[i+1]) for i in range(0, len(winners), 2)]

with tab_simulations:
    st.subheader("Simulações computacionais de campeão")
    st.markdown("<div class='card'><p class='muted'>Roda torneios completos em memória usando Ranking FIFA + OVR médio dos elencos. Serve para testar tendência de campeão sem alterar seu torneio principal.</p></div>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns([1,1,2])
    with s1:
        runs = st.number_input("Quantidade", min_value=10, max_value=1000, value=100, step=10)
    with s2:
        if st.button("🚀 Rodar simulações"):
            with st.spinner("Simulando torneios..."):
                for _ in range(int(runs)):
                    champ = simulate_full_tournament_once()
                    st.session_state.sim_wins[champ] = st.session_state.sim_wins.get(champ, 0) + 1
                    st.session_state.sim_runs += 1
            st.rerun()
    with s3:
        if st.button("🧹 Zerar histórico de simulações"):
            st.session_state.sim_wins = {t: 0 for t in ALL_TEAMS}
            st.session_state.sim_runs = 0
            st.rerun()

    sim_df = pd.DataFrame([{"Seleção": f"{FLAGS.get(t,'')} {t}", "Títulos simulados": v, "Probabilidade": (v / st.session_state.sim_runs * 100 if st.session_state.sim_runs else 0), "Ranking FIFA": FIFA_RANKING[t], "OVR": OVR_LOOKUP.get(t, 70)} for t, v in st.session_state.sim_wins.items()])
    sim_df = sim_df.sort_values(["Títulos simulados", "Probabilidade", "OVR"], ascending=[False, False, False]).reset_index(drop=True)
    sim_df["Probabilidade"] = sim_df["Probabilidade"].round(2).astype(str) + "%"
    st.metric("Torneios simulados", st.session_state.sim_runs)
    st.dataframe(sim_df, use_container_width=True, hide_index=True)

# =========================
# ABA: CLASSIFICAÇÃO FINAL
# =========================
with tab_final:
    st.subheader("Classificação Final Geral — 1º ao 48º")
    st.caption("Ordenação: fase alcançada, pontos, vitórias, saldo, gols pró e ranking FIFA.")
    final_df = final_ranking_table()
    st.dataframe(final_df, use_container_width=True, hide_index=True)

# =========================
# ABA: ELENCOS
# =========================
with tab_squads:
    st.subheader("Elencos e Overall")
    c1, c2 = st.columns([1, 2])
    with c1:
        selected_team = st.selectbox("Selecione uma seleção", ALL_TEAMS, format_func=lambda t: f"{FLAGS.get(t,'')} {t}")
        st.metric("Ranking FIFA mockado", FIFA_RANKING[selected_team])
        st.metric("OVR médio", f"{OVR_LOOKUP.get(selected_team, 0):.1f}")
    with c2:
        squad = players_df[players_df["team"] == selected_team][["pos","player_name","shirt_name","club","dob","height_cm","ovr"]]
        squad = squad.rename(columns={
            "pos":"Posição", "player_name":"Jogador", "shirt_name":"Nome na camisa",
            "club":"Clube", "dob":"Nascimento", "height_cm":"Altura", "ovr":"OVR"
        })
        st.dataframe(squad.sort_values(["Posição","OVR"], ascending=[True, False]), use_container_width=True, hide_index=True)

    st.markdown("<div class='card'><h3>Ranking de OVR médio por seleção</h3></div>", unsafe_allow_html=True)
    ovr_show = ovr_df.copy()
    ovr_show["Ranking FIFA"] = ovr_show["team"].map(FIFA_RANKING)
    ovr_show["Seleção"] = ovr_show["team"].map(lambda t: f"{FLAGS.get(t,'')} {t}")
    ovr_show = ovr_show.sort_values("OVR Médio", ascending=False)[["Seleção","OVR Médio","Ranking FIFA"]]
    st.dataframe(ovr_show, use_container_width=True, hide_index=True)
