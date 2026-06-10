
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
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    Image = ImageDraw = ImageFont = None

st.set_page_config(
    page_title="Dashboard Copa 2026, bySamuelJakeCascavel",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS / DARK DASHBOARD
# =========================
def inject_css():
    """PATCH FIFA CLEAN: tema claro oficial, vermelho FIFA, contraste alto e chaveamento limpo."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    :root {
        --fifa-bg: #f4f4f4;
        --fifa-card: #ffffff;
        --fifa-soft: #f7f7f7;
        --fifa-line: #dedede;
        --fifa-text: #151515;
        --fifa-muted: #666666;
        --fifa-red: #e10600;
        --fifa-red-dark: #b90400;
        --fifa-blue: #0b1f3a;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', Arial, Helvetica, sans-serif !important;
        color: var(--fifa-text) !important;
    }

    .stApp {
        background:
            linear-gradient(90deg, rgba(225,6,0,.035) 0 1px, transparent 1px 100%),
            linear-gradient(180deg, rgba(0,0,0,.025) 0 1px, transparent 1px 100%),
            var(--fifa-bg) !important;
        background-size: 44px 44px, 44px 44px, auto !important;
        color: var(--fifa-text) !important;
    }

    .block-container {
        max-width: 98vw !important;
        padding-top: 1.1rem !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
        padding-bottom: 3rem !important;
    }

    h1, h2, h3 {
        font-family: 'Inter', Arial, sans-serif !important;
        color: var(--fifa-text) !important;
        font-weight: 900 !important;
        letter-spacing: -.045em !important;
        text-transform: none !important;
    }

    .muted, .details-copy, .stCaptionContainer, [data-testid="stCaptionContainer"] {
        color: var(--fifa-muted) !important;
    }
    .gold, .neon { color: var(--fifa-red) !important; font-weight: 900; }

    .card, .clean-card, .round-card, .match-card, .group-shell, .thirds-trigger-card {
        background: var(--fifa-card) !important;
        border: 1px solid var(--fifa-line) !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 26px rgba(0,0,0,.055) !important;
        color: var(--fifa-text) !important;
    }

    .stButton > button {
        background: var(--fifa-red) !important;
        color: #ffffff !important;
        border: 1px solid var(--fifa-red) !important;
        border-radius: 999px !important;
        font-family: 'Inter', Arial, sans-serif !important;
        font-weight: 800 !important;
        text-transform: none !important;
        letter-spacing: -.02em !important;
        box-shadow: none !important;
        min-height: 2.25rem !important;
    }
    .stButton > button:hover {
        background: var(--fifa-red-dark) !important;
        color: #ffffff !important;
        border-color: var(--fifa-red-dark) !important;
        transform: translateY(-1px);
    }

    /* Botões secundários, popovers e expanders */
    div[data-testid="stPopover"] > button,
    button[data-testid="stBaseButton-secondary"],
    button[kind="secondary"],
    .streamlit-expanderHeader {
        background: #ffffff !important;
        color: var(--fifa-text) !important;
        border: 1px solid var(--fifa-line) !important;
        border-radius: 999px !important;
        font-weight: 800 !important;
        box-shadow: none !important;
    }
    div[data-testid="stPopover"] > button:hover,
    button[data-testid="stBaseButton-secondary"]:hover {
        border-color: var(--fifa-red) !important;
        color: var(--fifa-red) !important;
        background: #fff7f7 !important;
    }

    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid var(--fifa-line) !important;
        border-radius: 14px !important;
        padding: 13px 14px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,.05) !important;
        color: var(--fifa-text) !important;
    }
    div[data-testid="stMetricValue"] {
        color: var(--fifa-red) !important;
        font-family: 'Inter', Arial, sans-serif !important;
        font-weight: 900 !important;
    }
    div[data-testid="stMetricLabel"] { color: var(--fifa-muted) !important; }

    input, textarea {
        background: #ffffff !important;
        border: 1px solid #cfcfcf !important;
        color: var(--fifa-text) !important;
        border-radius: 8px !important;
        font-family: 'Inter', Arial, sans-serif !important;
        font-weight: 700 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: var(--fifa-text) !important;
        border-color: #cfcfcf !important;
        border-radius: 8px !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--fifa-line) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        background: #ffffff !important;
        color: var(--fifa-text) !important;
    }
    div[data-testid="stDataFrame"] * {
        color: var(--fifa-text) !important;
    }

    [data-baseweb="tab-list"] { gap: 10px; border-bottom: 1px solid var(--fifa-line); }
    [data-baseweb="tab"] {
        background: transparent !important;
        border: 0 !important;
        color: var(--fifa-muted) !important;
        font-family: 'Inter', Arial, sans-serif !important;
        font-weight: 800 !important;
        text-transform: none !important;
        border-radius: 0 !important;
    }
    [aria-selected="true"] {
        color: var(--fifa-red) !important;
        border-bottom: 3px solid var(--fifa-red) !important;
    }

    .shirt-badge {
        display: inline-flex;
        width: 25px;
        height: 25px;
        min-width: 25px;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: #ffffff;
        border: 1px solid #d7d7d7;
        margin-right: 6px;
        font-size: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,.10);
    }

    .group-shell {
        padding: 10px !important;
        margin-bottom: 12px !important;
    }
    .group-mini-title, .fifa-bracket-title, .thirds-title {
        font-family: 'Inter', Arial, sans-serif !important;
        font-size: .76rem !important;
        font-weight: 900 !important;
        color: var(--fifa-red) !important;
        letter-spacing: .02em !important;
        text-transform: uppercase !important;
        margin-bottom: 6px !important;
    }

    .match-card-vintage {
        background: #ffffff;
        border: 1px solid var(--fifa-line);
        border-radius: 12px;
        padding: 7px 9px;
        margin: 7px 0 10px 0;
        box-shadow: 0 4px 13px rgba(0,0,0,.04);
    }
    .match-scoreline {
        display: grid !important;
        grid-template-columns: minmax(0, 1fr) 62px minmax(0, 1fr) !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 7px !important;
        width: 100% !important;
        font-family: 'Inter', Arial, sans-serif !important;
        font-weight: 800 !important;
    }
    .match-team-left, .match-team-right {
        display: flex !important;
        align-items: center !important;
        min-width: 0 !important;
        font-size: .72rem !important;
        line-height: 1.05 !important;
        color: var(--fifa-text) !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    .match-team-left { justify-content: flex-start !important; }
    .match-team-right { justify-content: flex-end !important; text-align: right !important; }
    .match-team-left span:last-child, .match-team-right span:last-child, .ko-team-name span:last-child {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        color: var(--fifa-text) !important;
    }
    .scoreboard-number, .ko-score-pill {
        display: inline-flex !important;
        justify-content: center !important;
        align-items: center !important;
        min-width: 24px !important;
        padding: 2px 5px !important;
        background: #f2f2f2 !important;
        color: var(--fifa-text) !important;
        border: 1px solid #d8d8d8 !important;
        border-radius: 5px !important;
        font-family: 'Inter', Arial, sans-serif !important;
        font-weight: 900 !important;
        font-size: .82rem !important;
    }
    .score-separator { color: #9a9a9a !important; font-size: .75rem !important; margin: 0 2px; }

    /* Chaveamento estilo oficial: claro, simétrico e com conectores finos */
    .ko-card-compact {
        position: relative;
        background: #ffffff !important;
        border: 1px solid #dcdcdc !important;
        border-left: 3px solid var(--fifa-red) !important;
        border-radius: 10px !important;
        padding: 7px !important;
        margin-bottom: 11px !important;
        box-shadow: 0 6px 16px rgba(0,0,0,.045) !important;
    }
    .ko-card-compact::after {
        content: "";
        position: absolute;
        right: -10px;
        top: 50%;
        width: 10px;
        height: 1px;
        background: #c9c9c9;
    }
    .ko-card-header {
        color: #8b8b8b !important;
        font-family: 'Inter', Arial, sans-serif !important;
        font-size: .60rem !important;
        text-transform: uppercase !important;
        letter-spacing: .06em !important;
        margin-bottom: 6px !important;
        font-weight: 800 !important;
    }
    .ko-team-row {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 5px !important;
        min-width: 0 !important;
        font-size: .66rem !important;
        line-height: 1.05 !important;
        color: var(--fifa-text) !important;
        border-bottom: 1px solid #eeeeee !important;
        padding: 4px 0 !important;
    }
    .ko-team-row:last-child { border-bottom: none !important; }
    .ko-team-name {
        display: flex !important;
        align-items: center !important;
        min-width: 0 !important;
        max-width: 116px !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        color: var(--fifa-text) !important;
    }
    .ko-winner-row { color: var(--fifa-red) !important; font-weight: 900 !important; }
    .ko-placeholder {
        background: #ffffff !important;
        border: 1px dashed #d3d3d3 !important;
        border-radius: 10px !important;
        padding: 12px 8px !important;
        margin-bottom: 10px !important;
        color: #999999 !important;
        font-family: 'Inter', Arial, sans-serif !important;
        font-size: .68rem !important;
        text-align: center;
    }

    .details-copy { color: #3a3a3a !important; font-size: .78rem; line-height: 1.45; }
    .thirds-trigger-card {
        background: #ffffff !important;
        border: 1px solid var(--fifa-line) !important;
        border-radius: 14px !important;
        padding: 10px 12px;
        margin: 8px 0 14px 0;
    }
    .tactic-pitch {
        background:
            linear-gradient(90deg, rgba(255,255,255,.18) 1px, transparent 1px),
            linear-gradient(180deg, rgba(255,255,255,.18) 1px, transparent 1px),
            linear-gradient(135deg, #1c8f4a, #0f6a38) !important;
        background-size: 42px 42px, 42px 42px, auto !important;
        border: 1px solid #0f6a38 !important;
        border-radius: 14px !important;
        padding: 18px;
        margin: 10px 0;
    }
    .player-chip, .reserve-box {
        background: #ffffff !important;
        border: 1px solid #dcdcdc !important;
        border-radius: 10px !important;
        color: var(--fifa-text) !important;
    }
    .player-chip strong { color: var(--fifa-red) !important; }

    /* Correção global de contraste no tema claro */
    .stApp, .stApp *, p, span, label, div, small {
        color: inherit;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown span, label {
        color: var(--fifa-text) !important;
    }
    .stAlert, .stAlert * { color: var(--fifa-text) !important; }

    @media (max-width: 1200px) {
        .match-team-left, .match-team-right, .ko-team-row { font-size: .61rem !important; }
        .ko-team-name { max-width: 92px !important; }
    }


    /* ===== PATCH PONTUAL: escudos reais e tabela oficial limpa ===== */
    .shirt-badge img {
        width: 20px !important;
        height: 20px !important;
        object-fit: contain !important;
        display: block !important;
    }
    .official-title {
        margin: 0 0 .85rem 0;
        font-weight: 900;
        color: var(--fifa-text);
        letter-spacing: -.04em;
    }
    div[data-testid="stImage"] img {
        border-radius: 50%;
    }


    /* ===== PATCH FINAL: assinatura + placar único sem duplicação ===== */
    .creator-signature {
        margin-top: -0.65rem;
        margin-bottom: 1rem;
        color: #666666 !important;
        font-size: .82rem;
        font-weight: 700;
        letter-spacing: -.01em;
    }

    .creator-signature strong {
        color: #e10600 !important;
        font-weight: 900;
    }

    .match-single-team-left,
    .match-single-team-right {
        display: flex !important;
        align-items: center !important;
        min-width: 0 !important;
        font-size: .74rem !important;
        font-weight: 800 !important;
        color: var(--fifa-text) !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        min-height: 34px !important;
    }

    .match-single-team-left {
        justify-content: flex-start !important;
    }

    .match-single-team-right {
        justify-content: flex-end !important;
        text-align: right !important;
    }

    .match-x {
        text-align: center !important;
        font-weight: 900 !important;
        color: #9a9a9a !important;
        padding-top: .35rem !important;
    }

    div[data-testid="stNumberInput"] input {
        text-align: center !important;
        font-weight: 900 !important;
        padding-left: 2px !important;
        padding-right: 2px !important;
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

# =========================
# PATCH ESCUDOS REAIS
# Escudos compactos embutidos em base64 para funcionar no Streamlit Cloud sem pasta externa.
# =========================
TEAM_LOGOS = {
    "México": "data:image/png;base64,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",
    "África do Sul": "data:image/png;base64,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",
    "Coreia do Sul": "data:image/png;base64,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",
    "República Tcheca": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXH////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////u7u78/PvpKx7///+WFy7JyckAJnr//v7Ly8vnKh79/Pz39/j89PWnGyru7e2YGC+ZHTSzHSjQJSPcKCDCISW7ICfMJCOgGSzjKR/7+/vOzc37+PikGivqMCO3Hyj09fXn5+fQ0NDj4+OwHSnr6uroKh7a2trfKCDw8PDU1NSzWWnd3d3Sxsju3eCdGCzNkpzZJyHy4eThKB/YqLHz8fK+ISe/dYLRmaPWJiH57e7t19vrOy/TJiL4urWoP1LqNSnCe4fIoKf9+fm4ZnXtVUvQy8zGIyWjMUXlyMu1X2+aGC3q0dXrRjvkwsf16+3IhJDEkpsQM4LivsXWeXvVMi+eKD69x93KipW/g43X19fxpKDpLB++b3zxeXDOtLirRliqt9PUoqqjNEjdsLjwb2bZrrXpzdLqQTXQwcTuW1Hd19f619XzkIrNrrLz5efsT0TdzM7Xtrfw1NWdJTvAa3auTV6rGyrFgIvd0tPY09PyqqbloJzVZmjokI3k1tfiNCzrY1rtysnhPTXobmb65uXzl5HcY2HgusDQvL5cdKrr5OXu8fa1wNnI0OK7QEr4y8mtSl3jRz7cjo/0sKzo6Ojw6+vXw8TUzM3AipPmrKzmW1OuKDXelpXDOkDot7bZQT7yhX7hdnbHdnxsgrN/krzR2Ofm6vIJLX/Z3utNZ6Leqqvg39/lMCXVkpjoenPqf3nwu7etNETCUFbLR0v2wsC1SFWiHi/DJyvXvsHLgYbjgX7PJybh4eHds7qLnMP02tqjsc8YOoeYp8o4Vpje4+7eS0bj2NnZqai7ND2uutXOU1ewUF9CXpwmRo6QocX1npktTJEgQYvdurqnITGyZHPwAAAALnRSTlMAF/bvAdK7/d4GhjPlC6fotGhCkp+uJU92vw6M6h44zdhJcRGWfsdVW8PKwe37xVgvowAAAAlwSFlzAAALEwAACxMBAJqcGAAACVxJREFU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",
    "Canadá": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXH////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////y8vL////FKBwtKibNRTrwxsJXVVH////FKR3j4+LNRjvJNiuenJvHLyP++/sxLirGKx/fhoDuv7v9+Pj99/b9/f3KOi9hX1w5NjKIhoTgi4QvLCj7+/vRU0nUYVjGLSHoq6bvw8DU1NPGLCDprqn//f367ezPS0HZcWmAfntCPzv56ej+/Pzyzcr23NrIMSbPTkT34+LmoZvXa2PTWlHQUEfqsazuwb3y0c778vHYbmXadm/RVUs0MS02My9FQj9mZGH5+fnlnpn019XdgXn55+bknJbhjYfad3Djl5Lz0tDUXlXilI7cfHXrtbHz09Hz8/L23tzIMyhVUk/tvLnyz8zYb2fSV05MSkZta2ibmpjv7+9eXFmgnpzq6up3dXLh4eCurazz1NLsubXTXVPuwb788/PMQDbtu7fPTELbenLVZVzJNSnik43npqLeg3z89fT9+fnprKjl5OTkmpToqKP66+r67u2qqafwyMTOSD745ePrtrK6ubjHxsWWlJKamJZAPTrl5eUuKyfQ0M7S0dBaWFWTkY/c29pyb23npaDst7P12df2393rs6/34N7xysfKPDHRVEr78O/Zc2v89PONjIrcfnfY2Nf19fV8enjx8fHmo57Ozcz77+7o6OdPTEm9vLu0s7LhkYqysK+3tbRSUEyjoqC1tLJZV1SDgn/XamFJRkPg39/X1tVHRUFRT0s+PDjt7eyMiojAv72382rMAAAATHRSTlMAY+/zC+EI9/kDEBPAVYFB/S77Algn7HY25pMGFk8OzYzW0cSrSiqPH6VnvdphsKFvtNy3AUYbGDLIXbVTnYcj6T2ofEjHRIZpnIjMItFP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",
    "Bósnia e Herzegovina": "data:image/png;base64,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",
    "Catar": "data:image/png;base64,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",
    "Suíça": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAABlBMVEX////aKRyFm6A8AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAhklEQVR4AWJgpBCMGsA4GgbDPgwYkADIt9gxnryApB+fKuzmgkRHDWAcjYURGwbIqR8fGxRCMIySmfBpQpaDaQbRowagVW3IAYWPDQo8GB4NRGoHIipAjgdUGWQeSiwgS4wWqiAwGoij6QAEKE4HxAE8uXHUAGLBaCAChlaxEBtwyOooDkQAMFgM0WkMsGgAAAAASUVORK5CYII=",
    "Brasil": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXEZMnUYrkcZrkYhO3MhPHQZM3UYMnQAR04ZMnQTsEsYM3QYrUcYrkYZM3X82wImsU4Zr0YAs0wYrkccMnUjL3YAQGoYM3UbNHQqRXEZrUcYrUYYrkYYrkcZrkanrDwXMnQZM3UWNHY3U20ZMnUYM3QYrkcYrkcZrkYYrkYXrkYYMnU5SmSssTsYMnQYMnQeOXQYM3Y+WWoVMHwzTm0YMnQkPnIZrkYYrkYYrkYYrUYYrkcYrUYZMnUYM3QYM3Vid1xVbWKGk0wyTW+wuT2hqT90hVWstDyPm0UarUYZrkYYrkYYrkYZrkcYM3UYMnS1vTlMZWYYMnS1wT8YM3T83AIYM3SrvUYZM3QZM3UYMnQZM3QkPXAwSm4ZMnQYMnQYMnQYMnRlbE7/3ABnbE0cqlUZr0YYrkYYqkgYrEcZrUcYrkQYrUYZrUb83AJeZlKflTFRamMZM3WAjk8YMnT/5QCooC9zdUiblDNXa12HhzwYMHOgpz/KtBxtgVf73AOasT0nPW3Mux383AJxdEjGsx1pbkyPk0E4T2kMh9H///8ZM3X93AIZrkeIs2dco4wQlKNPsFj9/v9OsFlmd6NmtOLo9fMMh9Bbr+Atl9efz+30+v3y+Pzh8PqgulCxudBer+FNp90qlteuwEVfsOEajMVzq3hMYJOu1/Df4uw4TocnrW/z9u7PzjxpwqqBwejk8vrE1I99v+f09/DNzCeauVUWi8kSicxuqn0qkrdFsktXoZGNtWIVoXWKu0eLvEby9vTL0eB1hawzSoVCWI6Snr5Kpt0lk9ZGnJ/v9/w3l6x5rnIylbBoqIIbj9SEsmpMnprZzh0fjsGDsWt8uUcymti73vJ8i7EwR4PK5fUoQX6yu9EeN3iGlLZsfKdcbp6+xthhc6FitXNAqLh5tKaMytbr9fur0M2Ty6bX6/fW6/clj7zs9vdZo48ZrUtmr2fl1BVWsVZislQqql6iwjwWlp83q19jsuGJuVKapcLX3OdMYZTR1uNRZZfU2eWcp8O281RwAAAA0nRSTlMA54f+3+D++gHoDfUZ+UXoBjMDPREHBNzq24FIcFFN9V85LNre75XB6GhCj8f32n7kHtoL2c/eYu7gH1aMojNT4t/s2vn15/jwMMrSznlcvPveZ/6a+ob90sXkdtjbl7Jz4r8dvglQpxVdbimmrcx/uN3g7KYK1nHG1BEq9MblQ/nG49yb1r/b0P////////////////////////////////////////////////////////////////////////////////////////////////7AuSNTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF3ElEQVR4AWIgADQJyBMCXBZchJRgBQJgUSFZa6ZeKes0ITAPIgZmEiR4siBKhDV6e3sthSEcGR4ITQypqQ5VZcXcywvTp24OFSRE8TAxeTPbMMmB1Mnx5jJrgRlMNszeTEwww0BCuLEWyOFqYC9LCTNo+YJUCjEx9/ZaSIOYRGDz3l6oH0DBB8IMDAzqvb3E+oEh3UuNFz32uHjVvHIIWi4LViEkJcAgBw16sACIEJZmEJDiALGgqsBMNILDMgNNhKG0yhhdiMcSXQQKPAWte30FBcGBBxLiUMzPC+1J6mY3jeMTAwmAcKqgoFSvrKAniI2OwYHPC01CDBwK4t06PT09Sd0goKIAcT0DgyZvb2+vBvbosOLt7YV5XSmyuxtsQLuJGTfIiMhqqIXSvb0WOJJDdq8PMyQYGRS4u7vZleV7enqufJt8xUOZvbub2w9iQiazD7MVhIlOymRxyNmABMXiuru7Y+SXne3p6Znc29v7dYcra3d3tzY4JNSkObJw5HFQ1IOwiH93d3fgvKWd/VADJnRemufI1t3tL8LAAFcFsgk7tlPp7uYuPt3ZiWRAZ+cOJ+7ubnE77FqQgag+e3e3gfyJTjQDOk/IG3R3s+uDvYGsARWI2ut1d3c7B+wE6UdxQWfn6wDn7u7uCHtYhKLqBAERPm2J7u5udoet28H60Qzo3L7Vgb27u7sojA8UFiAdqFgbFN3d3bG6uyHaUcMALLZbVxKiSBtVKwSIlXR3dyu7Xl4KVgsiELEA4oHw0vM1yt3d3bbYvSEq3t3tcQakDoSPLVz4ZO3atY9Wr179eOHCYyAhED7j0d2tJwqxEoPk6+6W7AOpAuElk7oQYNJUkBAI95l1d/Nh6IQB0242d5AqMEYyAaG/052t2xSmHJOO7u52g8QgyIipMDcg6d9Z192dgKkRBpS6u41AcXAcpL+zcxbUD7MgXJDoW6PubiWYckzauLtbcllnZ+fLmWAtS6AGfAfzZr7q7Ow8LdndjVFGIQHVbrPLnZ2dszeATZgBNWAByIBFc+d0dnaeN+tWRVKPweTsZgFFw+yuuVc7OzuRDbg6twtkQB9rNyOGLiTA2c3yY+/evW+6umZfW7HiJtQFN1esuDa7q+vA4sWLL5ZVFCCpx2BydrPs6+3tndbV1XXg6L0pB+9OmXLo38EpU6Zc7+rqWtMDBvwYupAAkgH37jycsnL5kbuH/87vnnLoJ+kGrLrf1dW1/MjRVdfnd/+//YtIA2pbmz5s2bLlQFdX142HIANWHTo8ZX734VXzu7q6pu3atetLR0wjkosxmPxgX/Zs7urq+n3j9oOVy+//mXJrfvdKcGhO6+3t3U8gFpAMOHjkTveD5d3dt46SaQAmIMYF8IQ0adM5lIR0btOkrjnTp08nIiGBUyIk/yGnxM4lk4hMiSAD5kDKDxQDOqee7OzsJNIFM0C5p7NzEzQcNkG4IFEiDYCARc+gBpwE502wICkGLJoL1d/VBcndIBMIGZDYbbAHpK6zE1k/kgl7DLoTMZIfEojolpgHNWD9rFlP161b92Ljxo3PZ81aDxWdp4qvTGVgiO9mc4Eq7ezsnNDb2zuxp6enHyHk0t0dj2QhBlO/u9sJUTNhGnDJqbtbH0MXElDs7lbeAbcP04Blzt3deNsIHCrd7LrbYCZgGLBNl61bD3u9CANB3d2SW3EaME+yuzsIphQ7LarX3V3YNx1iBJoLpu8JxFOxwoAie3e30eJTYBNQDTgVbNTdza4IU4iTVmDv7pZwC78wHSUap18Id5Po7maHNhZx6gYBPtXu7m4JR/ez2+Eu2LbMxRHU+lHFXbEjA0NbNlBTycT1/TtIQgqWNwE1jthsDZGV4WMrhYDax2zODZ/BKbESZCB3CJ5aGROIJIh3d3dzO3z62NPTo9PdrRKNvWWGqRMOOCBNxosgA6LgrX24NDEMwMTC2Lq723p6QsvxtQjwmqQY1Z3Sw1+PVw1+SUOVlOZk/EoIyBq2ENIPAE/ucEYm117tAAAAAElFTkSuQmCC",
    "Marrocos": "data:image/png;base64,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",
    "Haiti": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXH67sD///vn2qP////Fv5zQx5Xaz53////////89Nb78cbu5bb/++377bTy4Zz89NLMxp/JwI/EvZH567D37LvLkW7///v47Lv///zYvoH89NXt4K756q/MfWvRonLlyYft4a315aX//fH///n///8INqH1FhUGLYUFLIPrCgruDQzpBwcGL4voswvxERD0FBMFK4AHMZMGLocGLYb9997vDw/ksBIHL5AGLokLOKAGLormBgX32mgHMpb///xfd6743HHosxGbq9CYnI0GL40ZQZvuX1/oV0366KL888/xzFX43nj++eMRPJ355JD+++732WL211z766xccpb//fgdQpMkR5A+XJn88MPXEg/89NfltBstUZ3++uj78cpKZZh/iY2foo7+/fR2hJT77LIIM5mUkHn44H/Kw5v44IYINJsyT4b3UU14elpJXHVTapJRP3g6VIDBvZtCWXyBf1TNx6L2HRr77rmOhkxre5Dm6OxUY3FqcWKvrpcOM4odPopjdpFtY1WikkArS4tPPXPvSEhfamnfTEicqMPFpi3Y2duwro/47MDXHQ/zMxNwdV4zUZWFjpCzmzdIY6PJzNTwxkAqTpv09fhTQn/z6sTzgkfqrCJpfKnoUj326bZnepaLkIbcSw0ERTQfMnoUOpLqFxdZaXrWrjDvnDbzKiios887SWTI0OVka2TySBeMeUOagjoNI4jySDZdXGCQn755i7P655qQi2iWeS/eWg29BQVsVkPHsla6v8mpnln0ODKvtcLc0qP1lZXuXCOoeVfg05gEO1eoqJGFlr8uL2rZt03aryB6kMXxz2Xz01E9S11fdqmOlZDwyUl8aETODAxUQ4OlZl3wjEL0XUb5xMT+8PD1cEXroi9FNl58ckw5Snd6f3OqpXnQix/u7/HRQjnDcyTugnxlcnbIOR/bPQ6bTEV5iax7cJaYn58tRn/tpCzqmgz12Gl3azft1GvPoXyFlLedPDmXOzXNliHLUC2iXDrBuITp5tjgIxL24pofIb7PAAAAdHRSTlMAkyPZE/f15QMNX4S5VpXDa+36+aOf+zGjNft0yqf+9eTJtEso////////////////////////////////////////////////////////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",
    "Escócia": "data:image/png;base64,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",
    "Estados Unidos": "data:image/png;base64,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",
    "Paraguai": "data:image/png;base64,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",
    "Austrália": "data:image/png;base64,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",
    "Turquia": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAC5VBMVEVMaXHjChbjChfjCRfiChfjChbjCRb/AADiChfjChbiChbaACTiChbiChfjCRfjCRblDBnmCBjjChffDBjiCxbjChbgDBjiChbiChbUACrjChfiChfjChbhCRbiChbjChbiCBjjCxbiChbhCxbfDw/kChXiCBjdERHjCRbjCRfiChfjCRbhDx7lDBnjChbiCRfmDBjjCRfjChXlChniCRbkDRrjChfiCRbjCRflCBnfBxfjCRXiCRbiChbjChfjCRbjCRjjChbiChfjChbjChfiChfjCRfiChfjCRfjCRXiCRbjCRfiCRbiCRjiChfjChbiCRfiBxXkCBriCRfnCxfaEhLjCRbiCRfjChfiChbiChbjChfjCxfkCRfjChfiChfhBxbkBhTiDhziChbiChbjCRbjCxfiCRbkCBXjChfiCxffAB/jChfkCBbhCxfjChfiCRbjChf////jCxjyj5X0o6jkER3tYWrjDRr72tzrTljoOUT++PnkEBz3vcDubXX3ur396uv3uLz/+/vlFyTkFiLvdn32rbL2r7PykJX+9PX//f3+9/j98PDtZG35zM/qR1DjDhv61tj3trrmIS3kFiPxhYvnLzrnKzb+8/TqS1XykZf5y87qRE774OLua3P+9fb97u/kDxz0nqP73N798vL++vruZm74wcTuZ2/vcHfweoHxiI761Nb3tbnqSFLnLTj2rrP4wMPmJjHlHyvzl53xhIvlGCXnMDvmICzoOEP4vsHkFCDuaHDvc3rzmJ7mKDP85+j2rLHxh43kFSHyipD7293qRU7609XlGSb3u77xhoz85ufnMTz62NrtYGnwfYTrTVfzlJrzk5nwf4boMj3pO0XoMz7wfoXyjJL97/DkEh70oabzlZvrVF31pKnuaXHwe4LweYH98fHoN0L+9vfyjpT73+H73uDweH/++fr5zdDjDBn6z9Lvb3fsVl/5ys3nLDf4wsXvdXznKTTsWGH5xskc16QKAAAAcXRSTlMA3vqA/fftAZn4fwep+/CdFB/cKS16Kn18Bnhip09kZT8uqkUQMD4PnO/8ZxEoqJoV8S8yoBOm65seIFNQfo04VMGOwNvZjNqLUr43vTWt+aEkHaIWDp+jr6vhrkBNsPMiJhKy4O5B7DrdLAh5OSt3UY3jMaAAAAAJcEhZcwAACxMAAAsTAQCanBgAAARFSURBVHgBYsAJuEUcRO04eHg47EStRbhxKsMO2HO5HDkLkQCnM5c9O3a1WIAVcyaSXjjThUsQi2JMEMjBC9eDxmBREsZUjwZCTFjQdKFwWfgN0DSgAnbtVBT1WDhs8njCQl0Jiw4MoTgdVFsRwDgFQzFWAUYjhB5kEGOIVTkWwXhlZH0wYIMS8Vi0IQlxysJ0IUAaCfoLC/0x3GBMtPshDuFTRdgNAiqMEHHiyagkkD4YZo8mXidMZTJyetCGiSLRtWVIHGxMOZj1DAwC6agKDuzbWLmsqOjp847VH1FlkHlsiFRtgixeWLWpuwgBPnx9gyKLxNGAOUEYOf/sWIHQDGG9rUbShMxkEYOaEI4kuncBRFdRUdHj9mefl7/rXFHT/BBJATIzDGKAFVL+PwrXPvliLVRt64MlpRVQNirFBClhmBGia2D6T0xACBYWll24VIzMh7NtQU5gF4Lz+2D62/fAxSCMs+UQGo10AaWFDLjghi6oAVsx7ZvSAleGzPBmYEDyQQNUfwN2HxcWFmIYLM7AwOAIM3ECVP+Z7TARDLp+KpqQFwNDNjwbT4YaMB9NERK3pBSJA2KycjOIgGgQ3tkMMaByIoiHHZcUoQemGIMDTOlKiP6ibTABLHRJ0czphYWF16ethkkWMIjCmKVQA3bBBLDQJUVFc+bOnldU2QqTlGJwgjH7IQb0wvjY6BKImhpE7nBjsIApbIRIToLxMehFVYsXQtS0IeQ4GGRgnB6IZB2Mj0rfvnf/FkRBUVETUnIwwzBgN6pGGK9s1l2oE4uKGlAMoNgLGIGIZDzMejiNLRBzYLKwaESEMEwGQWNGYz6DNUx6OTSMpsEEsNAlRUtnFBYWXrt5AyZpw5AFY26BJuVjJCVlYQZueGZaB3VCPcxITBozM0kyMDjD1B2HGnDwJEwEg8bIzj4MDAxccGVNUBNOEV+gSDAwMNjDDZgxE2rCfsyoxFGk+YJKVVe4CeVQA4o6jsDFIIyr5yE0GukOKlSRCsXC0zAT1q5HVlp25TKmm0AKQD5gYBBEqlgOw0woaqqCVSwt85fcwR4qTJYgHzAwBIAMg+I+WNFeVLS0o7Nt5arOT6+WPYJKolP8EP0MusiV6/Q6uCOgjNdP0DVC+VqJUAMY+KEiEGpWHXL1/u09du8XFhbqw/QzmJpDtMLIzasOnaspKlrwov3lF5gYJs0mADeAQR5TupBgE0caoZ+BwQ+LCQSEIpH1M5DezBNSRzGAwYiPgIVo0pqKqPoZGBRY0ZTg5bKqoetnYJCFFwx4tYIlWWMx9TMwKBDtC00s9oOAKpENZiEM/8NAKA/YgQSICJxdHgYGdjk2AroLzVHSD8xqBBDQQM5ZGKZp6Zsi1OJgAZbAwYShDyrAFKyLQxOqsKWtO1QHCuUqHoSqDh/PW9wLJWGx+kiAy098etDlJPM8pTw49PQ4PKQ8xSTRZeF8ACLzigjydDIiAAAAAElFTkSuQmCC",
    "Alemanha": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAC91BMVEVMaXG/f3+okm+okm5/f3+pk2+ql3H//wCqqlWpkm+ymWaokm+ZmWauk2upk2+okm+okm+pk2+qmXeok26qlG+qk26qjXGmkG6pk2+qlGqok2+pk2+okm+pkm+ok26pkm+okm+qkm6ok2+okm+qjXGtjnCnlG6tlnOqj2+lmXKokW2ok26qk2+okm6pk2+pkm6okm6okm6pk2+fn1+qk2+okm+2kW2pkm6pkm+ok26okm+okm+oknCpk2+okm6pk2+ok2+pkm6qlGqskmyok2+qk26pkm+ok26mlW6qf3+qkm6pk26okm6pkm6pkm+okG6ok26qkW6ok26ok26okm6jkW2qlHGpk26qkW2qkmypkm+qk26pk2+slnCllmmnlXKok2+pkm6okm6vj2+qlG2pkm6okm+nlW+ok26qk3Gpk26qk26okm+pkm6nkW2qkW2okm+okm6okm6pk26qkXCpkm6okm6pk2+qkG6pkm+nk2+ok26qk26nkm+okm+okXCok2+ok2+ok26nkW2okmyok2+ok3Cqkm+okm6pk26nkW2qk2+qkm+pk3CqknCnkm+ok2+pkm6ok26ii3Opkm6olW6pk26mk2uqk2+qlG2pk2+qkm6qkW2ok2+pk26pk26mkW2qk2+okm+qlG+mlG+pk26pk26skG6wiXWok2+ok26slGqokXCpkm6pkW+okW2nlG2ok2+pkm+pk2+pkm+okm6qknCmlHCokm+ok2+qknGok26qlG6olG+pkm+okm6pkm+pkm6pkm6okm6okm+pkm+okm6pk26okm+pk2+qkm+pk26okm6ok2+ok2+ok26pk22okm+okm+ok3Cok26ok26pkm6tkW2olG6pkm+ok2+ok26ok26pk2+pk26ok22okm6okm+mk3Cpkm6ok2+pk26ok26ok2+ok2+pk26nk3Kokm6oknCnk26okm+ok26pkm+nj2+ok2+ok26pkm+pk2+pkm6okm+okm6RkW2pkm+pk26pk2+TgfK8AAAA/HRSTlMABPzdAqobAQP6CpkFE5WLkIkPUzBvCRfODI6MfJKavKJsVf4SGUMWJxQ4+Tnp04aUhIAIfuAHj57mpbdE0I131esYKOFRyoouBni7c+K1LFgzq6Z2DiSD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",
    "Curaçao": "data:image/png;base64,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",
    "Costa do Marfim": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXFCtaBGt6LE6OEwrpb/iBpKuKQwrpYxrpc2sJn/ih8xrpcyrpf9///1+/qI0MSm3NExrpc1r5kzr5hmw7H/hBST1Mj/jyn/ky95yrthwK9Tu6j8/f3/nUT/+vb/hBM4sZv/iRxWvKrg8/BOuaY0sJk/s56P08fk9PH/lTXx+ff/gxL/+fSd2M7/jib//////Pk8spz/5cz/////mz/////T7ul2ybr/mDnW7+v/hBIwrpbz+vk6spxdv63L6+QxrZf/8eX/jCOGz8H///3/oEit39X/hxn/hRT/t3T//fz/6dT/xZD/////////hhf/hBP/hBQ3sJrq9/WY18uN0sVQuqb/hRRrxbT3+/qh2s/7/fxwxrf///+24tr///86sZu449v/unv/hRb/rmP/pFH/0qf/////gxOx4Nj/o06Azb99zL3/rGBzyLj4/PtYvav/s2z///////+p3dP////+hBP////r9/XB5uD/38P////n9vL/9/Du+Pf/////7+D/p1X/wor/////4cZuxbVBs57P7Ofc8e3/9eyk29GDzcDI6eP/////////////8+n///////////////+95t7/8OP/ypr/////////////////////////////1bD/69n/9u3///9GtqH/////////7NzQ7ef/p1f/jSX/////2LX/////sWj/zJ7/x5P/27n/////7t7/////+PL///9hwa////9GtaH///9Quqfe8+6onFb////a8ez/v4T///////////////9pxbT/////7+L/////kSv/////////1Kz5/PzO6+WX18trxbVcvqw/r5ZWvamQomlOuaX/nD////9dtp1JsJT/////////////n0d/pnX/4sj/yZf6p1f/////////z6T/////ki7/5tDy+fiNo21Zqoa0pWb/jyVVq4viiidlqH//vYLl9fKw4Nf///9txbX////ulz1wuZ3SjzP/jiekupF7sYmhz7r//v3///8xrpf/hBNMjgcwAAAA/XRSTlMAzsvR+tvI/fTe1e3q/vXAxvHh58DtwszIv8HF/cL2/dnYw+LH49HB5cbw9fTEzvf61Nrzw/zZv8Xc+Pfz1sLV+OnRwP7ByN7pwP3dxAUd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",
    "Equador": "data:image/png;base64,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",
    "Países Baixos": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXHybCD1ayLybCDzayD3bRz/cTjzayHzbCH/KADzayDyayHwbCHyayDzayHybB7ybB/yayDybCDzayDyayDybCHybCDzbCL1bB/ybCH0bCD0bCDzbCDzax/zbCD/aCLyayDyayDyayDybCDzbCHzayDybB/yayDzayDvbx/yayDyayHzbCHzayDzayDzbCH////zbyXy8vL//v3w8PH+/v74+Pnz8/PzbSL8/P35+fr7+/zv7/DzcCj9/f339/j19PXv7u/t7e7s7O339vfzbiP6+vv29vbr6+z08/T0eDL0dS719fXw6eXzcir0cyv0eTTybiXx8PDx7uzwfT3w6uf+9O7r3dfxdjHv7u7s4NrwejfrzLzy7+70ezfquJz/+fb0cyz82cbv5uLpwKr3nGju5eDvhErxn3Lsybf1hUb0djD0dC3s2Mzu2c7p0MP6vZr83s3rvqbtlmbu7Ozr49/tzr34roX5sIj3l2HxgUPwh0797OLycSnm5OTwmmrq6uru6efs5+b+9/PtkV/70bns2tDspX7u3dT1gkPv6uno6Onwj1nug0b6waD++PXt6uro2ND08/L+9fD//fzt0cHqup/u4tzxlGDwtpbui1X+8uzvw6zt6+zsm2///PrtxrDn0sj2j1bqtZf+7+f4qX34q4Ht5+Tsro3pvKP2k1zu4Njwr4z4o3T1fjz1iUz0fDn3n273mmb1gD/xdC7p08fx0b//+/j71L3ulWHwgEHxcCfospT95dnxkl35t5Htq4boqIX949T2i0/swqvowq7weTXq5eX4p3rtnnL96t/rl2rqx7T7x6v5s437zrXytJLtwajyrIbrvKTtkmHxcy7xhUn08O76w6Ts0sXsspTqsJDsz7/v3tXzonTo39rsonnvvJ/v4tzsj1rvdjL3nmz2jFH03dHyyrTv7+/yqoP7zLL29fXv49381b/rqIL1597tsJDuvKHsonjzp3zpq4j5uZX81cD39fX02cvzuZvt1snwwqrsfkHxspDw29Fouzm9AAAAL3RSTlMA5Rq23goEx8gBnP4ivNcpT/qO82b2fywy/EZdr2/sB6ejO+hUQhTRdRCTkYjNwQbp0LEAAAAJcEhZcwAACxMAAAsTAQCanBgAAAgqSURBVHgBYsAF2JRkFdmVhfWFlTkUNJTkcSnDAdgEFOX09fX1beM613mDGMIy0qw41GIBPELK+vp+mwqSJhuAQH/hjdREfX1hLgksarEACQVJfduNOxImvzuXuihr8/pVG/sK58/fsclQX59XCot6NMCvyK0fVxC2pGC9BcjpUOyXej5hyTI/fX0OVTT1aECNS1J/Q1/CjlXIuiGG+C89NbvCX1+fmR9NDxJgE5HT33Aj4WwnRAs6aVF5KKzCVl+QSw1JDzIQ4NOvPdd/HqbdolY/I2OmftWrS3CTLDbW1Dy10JeTZUPWBwUSvPr6qTWHFsFU18+s0v/y/IW+xfMM/WvbqqDChstmFz7T12eR5oRqgwMhbv2spP5lrlCF+vr3PszQ35exRl9/jYX+r58z4OI5BfPPBujrK8B1QgG7Rd+U1g1wZSH6fnPuRYC5Fvr6F17UBsLcoK+flTS5XJ8Dqg8O2A0NKsHqIcQFP31IRES3bM28oq+vH4cICX39VGOsBsCc73p5H8QUff2IaXVOjt11R8D89l1gSl9f3x+fAQdufUyZOweiNCbSxcaozslk7kx9/ZONEx8Vx/uBJfAZcDXN0WCugVsISOFN00hfRxMTI4/IPH39eSs8zc0ePgGJ43KBob6+fnWHr5GBlYEByNFPnEycrKx9nF2c3B1q9fWjTWwiu+r1A/X19ROxewFkwMfpdqbWpnYGMfo7b+v7WOWWdns6m0XaGL3S159o6mBq4nImH78B+umxbqYGBgYX9ZNvXl2xML9srqenkaORxzb9y3al13ZaObtv09fXz8Htgl4HczuQAbf0Y9yC2ibm+zo1mDibmDu3bHExX54SGGwSCYpdHAbY6uvru77vuetramBQpq9voW/oYpfXZGLj7OPkdOmMkVmPfrzLJId2fX19b+wuABkACmRXIwMDsx59ff2ilPwoF3sPJzePl3+Sre7URs/Z+ca8jLABgRdNDQxcDiye2mVl6eNg5eli0u1z4bh15NbAW7E+xBiwONjGwMDScYKRgZWHvYmLiZlNQ2hIo0mw/lsfEzOXDNwuqAW5H4Q/udhYOzo62ng4OTu7m/k4Oxlt0+8ymvo3xcq0KRmkIBt7GMAN0A9pc3KycfSw8bEycjNyNnK8E63/1qgoMMbAN3weIQOeLCi7dexzqIlRt5GZtYm9jaOLs6dlhP7tGJOY3N8Geae34DEAlFGKlxuYGljHJge7GBiYOhkZ2Ti6mHta9ugfzTUq6Wi3m/QYlJL1cXgBZMDBrWbWoMrEwMDK08Tc0srRyMjq+oLcq71WNs5p+kWxkSvxuMBfX18/08DS0tTAwNTIw9LFx9nI2sPOwcYyQ783/7KbyST9K9Ug7fr6XtgDEWRAeIm1pbW174Qm66lvo6x8LCONTKzCT+rrr7a09jEvmlRP0IBp0y1dDMINe2Pqt+gfSzNyMzCwtLTep69vmOlgYGcSdewk2AQ8LtA/HtMYtVtff1bKyiv6gZnunp4GBgY/qvTbJ1kbWRmVvll9AGQCDgMSQXLzXNu+6oekmdg4msydvjJ9up2JqYFbrN/W+ge+ZiYmUSAlOMMAbABYRbijSaSRnYGBgZlvg6mJkYFlXrT+FV8TE6NpYGlcgZgDkdXXd71tYmdjCYlNI3OQJyyv6U9cU2RlcgaiJAB7LMAN0F/gZOJkYOAZvtzO3t3IB2TSAv0Wff0oow4iDVh8+r6dgUGTq/4eDwMnkH6DNpDOXHMwpa+PwwXgxpB++9Tk5F36tsEGBp6TFuvPqnMBGWBi1xGiX21kA85KBAwIDzUwaHybOcnAYNJB/cCbdSD9wXdcDNyDrOxSQO7QJ2DAk1AzM3trOwPToNKFhquduw0MDKJc9SNWm7qY+EL168dhD0SIF2YYmbkYmFmaTrTV139o8rLBwMDgYG+8vn6yQaMVAQOywfK5+W4GLtYGXSDOchMTDysDgwmx4Rej4+2ql4PEQBiHC7xAcvpP0s1MJ7i5P9bX14/38LQx8bE2sDTySXmSmaZfDFYAquuxeIFZvz8LIj8ndk/uwhYQu2W1p7mZBygUo/TTw6NBQhB8OEyfGd6ygAIt/UNrIbLVD/TTd4OZa1zqJsXvaTIwMFipnw4WgRJLC/W1ofrgQEC/fC+o1oIqAVHRR4sXrtDXv2tg4HYaxIdji71L9QXgOqGAjdF79gm4EijDdtbuLXl2BgbmiAIbJFM+O5ERs6Enor8pYT1IGoFnuBi4xIKCoBQhpq+vv2h+pb4I1F4kipNZ/1sYNBwh6mt93cysrC1NDUpmQQQg5OHm/fq8GM1EBgYGJhb9vrBVEEVg8uJxFwMzazMDd3B7Byykr69f2Vygz8IE0oCBmVgsKrYvQ4RksauRmamZqYERTK++vr7Fufnl+ow8GHohgIdPv3L29zi4+l0u993dnB3j4QL665Jmr9Lnw6WfgYFVRj+gtX8/rKEQUqrvezx+EqjtBDajtqJ/R5w+sybEOqwkp6ygfmpNTSpYPYiIOepaBGprgFz/dMmpTfqiGtjCDwmIs+vbVjQnwSMU1nzVf1Y4udxQnx1PdwMKOFVY9L1uzH+9GeQAOM5qnd/npc+I2crHBljFRPU7z28vQBTzXmentHbqi4oR3fNj4pLUP1y4ZCPEARYnJu9dpM/NhT3ycQB+GX2LtbPfgToQ65IS9hvqM4vjUIkTqPLpe7VO3qi/tjlpnT6jCk51gOGWkBcT1D/Rf6p/qYWgDtGeRzVOXF1/8+vN+ixKqMIk8OSFuPW5hci0HmKPlLoUhIGTBAAK8/+AjHyT+wAAAABJRU5ErkJggg==",
    "Japão": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXH59/EZFQgYFQcVEwr///8aFggkIhr///8XFAv39Or39Ov39e349u739ewPDQSlizOwlDeUk47////Hs3OvlDgnJBzs7Ov9/f0PDQSwlDgYFg37+/v////////////7+/v///8fHhU8MxIWFQv28uhUU0wPDQV7eXX////////09PNPQhmvkzifnZqQkIsRDwZIPBa+p104Ni/p6eijiTNANhPd3dvNzMrj4t7///////////+urqr9/f1/fnq5oE4QDQXZy56fhzLf393z8OL49vA5ODH08eWioZ2KiYQ/PTZQT0lHRT3////////////////////d0Kg3LxD///////////////9VSBrx7NzRwIq2nEf////////u6dWukjaFg4CbgjDY2Nc2NC3DrmkbGRAuLSViYVzQ0M+9vbr////////8/PzGxsP////UxJP////Dw8Cnp6MkIAs9PDT///////87ODIlIAtEQToUEgl+aShcTh2ukjjj2bogGwqPeS3///97aCcaFQjh17RnZmBvbmjw69r29fWbmpb59vAPDQT////jABawlDhvbmgvLCSvrqv///7Pz81/fnnZDyK/vrwVEwoSEAd4d3IYFg3qRFTqQFCiPUQfHRU2MSniAhg9MiwrKCBKOjXtWWfVEyRkY14lIhqIRUi4uLXGxcMoJh7LHi7++Pjwcn7x8fBMS0Tygo3cCh5ramSwNT/d3dz29vX8/PweGxMiHxePjoqYQkdnREGBgHufnpuLioYbGBB9R0dQPDipOUFtRkNVQj73s7lGRD3rSVnnJDdxcGr9/f3r6+pCNS/kBRusq6ilPkV0c23MzMpSUEqXl5PEJTTU09Lf397mGCxbWlSVlJCHhoGfP0To5+ZhQkDKyshVU03zj5neBxuxsK37297SFyimpaK9Kzj0naZ6V1XsUWC0Mjy1Mj34wMWysa7oLT/719rxnKSlYmXxfomtrKnJQU2ITE61ZWvUvL5fXljBwL6+vru1UlrWUV3Z2dj1MvD4AAAAjHRSTlMA7/Hx3v3vzbvd6ers7ev+0vjFCMDzzO7o+PDY/QIT3ed20dPb6MDzwYEM9cr1x8bqzcT97M7O49roN5ikze7Cyu7EzOTj7sPlycT87cFA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",
    "Suécia": "data:image/png;base64,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",
    "Tunísia": "data:image/png;base64,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",
    "Bélgica": "data:image/png;base64,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",
    "Egito": "data:image/png;base64,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",
    "Irã": "data:image/png;base64,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",
    "Nova Zelândia": "data:image/png;base64,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",
    "Espanha": "data:image/png;base64,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",
    "Cabo Verde": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXG3fxykYAC2fRm4giK2fRm3fxy4gyS5giG5gyO1fBi2fhm3gR64giK1fRi0eg61fRjXuYK2fhqZZgC3fhu2fBi1fRjav42zhBLBkj7MpV+1ehO2fRq0exaydxC1dQ2veAzDlUO3gR/cwZPSsHK3gB7PqWexcw2udwq8hyq1fRm2fBm/fwC0eBLIoFa6hSiydxG1fRuwcxCzeQ+/jjjTsnjFmky0fRi1fhu0ehbm1rW1exS9iS+0dRS7iC22fRm5hCa2fhq+ijHjzqq+jTe2fhrZu4j///8cLmPdBSv++Pl1gKB3gqG+w9ImN2p2gaE4SHdAT3xZZo3w8fX//v4qO23i5Os3R3Z4gqKVnbYdL2QwQXKzucseMGQgMmfS1eDl5+3Cx9WQmbOss8ZwfJ15hKMoOWxkcJX++/z+/fwzQ3P8+fXfx5xQXYb5+fvy8/ZCUX5NW4U9THpXZIsvP3Bnc5eTm7VfbJHV2OKEjqv48+nKz9uKlK/a3eb9/PppdZibo7o1RXRIVoHY2+Sgp75RX4i1u8z7+PPt4Mg6Snj59e0gMWW3vc7N0N3n6e7w5M/++frpYXn//f2Djaqkq8GWn7f3+Pn17uBbaI50fZ+eprwjNWhteZvhH0Ly6NevtcjBxtWmrcKGkKzs3cV9h6VTYYmOl7H7/P369u/u4crRrW327+Ps7vOMlbCrsMTIzNnq2buIka1dapDmSWWZobnm0bC6wNDjM1JhbpO8wtHiJUaBi6jnT2reDDHgGTtKWYPiKkrYi5/oZX3Lo1vo6u/zpbL9+/jf4ekyQnK0kamPjKidj6m/xNP069vc3+f8+vYpOmzr27/liJuCjKnefZTpV3HpeY5+fp7kO1nmconpXXblPVrCkqdVYouqkqqvjaXlQF1gbJJ6eJnwlKTizKXMpV+JiKTdxJbQmKzx59T38ebOqWfEl0fCk0DisL3Q1N/ofZHfETXgjqKSkKv2y9TEma5qdJfNlqnlQl+6mK7Mn7LVlajfEzfOpLbjL0/bepAsdXDuAAAAR3RSTlMA7QPl9Ovy9fPz6NDx7dw04v3LCvXytvsb9feL1JVDaFD19f369vclL/Su+RCa9vR4wz6E9fj22cF//nL2Wfah7/D0/fO//bD12YQAAAAJcEhZcwAACxMAAAsTAQCanBgAAAalSURBVHgBYkABTPzy0lpCfFxcrIyMjDy8nA68vGxsbGy8joysrMwCMq668nI6KBqQObLcrDzsLnqCORumu2MDx6b3bxWUktTncOQSkkXWCAPaiydh04dF7NhFbZgmZJodi1JcQuzIGmEAasCa5sTkWUmT/Rvc8+ecCA2N9QsNDQhyd1/e1pK8rTosD2IkbgMWFHl4eHjERQcWRrp7e/hHgkDNogZ393QPP5BMVFbhbnd3d6wGsLi7uwenzYhZXxsMsabIIwzCcHd3X+OR7j6tr+LMlJo5KfgMSPRogetxb0QyIMGjOGEaQgqnC3w9AosDQ+dAVKIa4OHh4VcIkcDjBV+PEztSl1VD1GUhuSDMo3Dnui1bIBJ4DNjpMQumxt19qceURBB4H3/OPcwD5HW4HE4vbEMOg4pGULiDcABRBnC6u7tv85gCt8XdPa8iHgJq3fPXxiBJYI9GkAFr1ucjq8PJxuoFkAFwHcfc3TO73N1XZ7q7g7JWl7u7ex1cEkcggg3ocndf8aTK/eXr8+7PV4WErMpxP/+mw3312xXuK1dluq/sd3dvB5mD0wV1hze41z1d4f5qg7t7VZW7e3u7u3t7tnv22RD3sxfd3XNy3I8d7sCVEsEuWF0FssC9LwyanME8OBES4u7+EqQCpwsgILM1LjC8KTkExJvWO7/hso9P/Ryf3UnJ64+AhPC6AAyCkz08mhoqg861pQRGt9b7p28qbQ1MAyUIjxObyirwGdCcnhue5uFR6eHhEbuzecaSpJrUplCPktKgErB2CFGOJxZ8IUoqozw8PFKDZ+WCaA8Pj+LdsyESIDJqGQ4DQOUBzAAPD79ZleASBKTFIy2wNWh/AJjpUbAAlxeQDFjmkTUlHKLeI3TO/f+HHmzf9W/PtZOdHrllD9sIGzB7UdrMbrD+7m93Ds319Nw798aDA56ee98ltXp4EGHAxpIdYO2zr1854Lnv1sH7/qVB+4P+3jwNzp6EDTiREg4OvNwr+z5O/D4zGmRY7Iya9DgQgxgXbOwG6Z997/bcS58hIRewMbIAotsDjwGgpAyOhRqQWr9ffw5dh9hZ4hviDxKCYpxegBmQBVb9c99BcBUB0hWYEAGioBhUsuDMC74ehVN9QIl2xu3foVANHh4e6akItgdeA2rLlnrEgXQenBjg4XE3tbwIFBweJ2Ztqve5vKwenLTweaG5NL0mclGLh0fJnnseHgHTJuzafGldrodHQXFA0eW10HA8gyshcboHV1eAQj03yKPwxw4Pj8nuEw58OlUQviR2ZnjZ5AswX4BqDZxh0AtWFZnWdPWuh8cy9+MpoHi4UF89FZIwwbKg7MwCq9KRaR53d/dmsBK/LX43Z3p4FDRA8uCMBHfkWADVuDzIGmEAZMARsAEe0VO/3oGwPDw8TmW4oxiwxt3dnRGmCZkGGTANqi005ksTlHl6uxeqAaBKmhVZIwywgoozcESBtH7rhTAfbfdENaA7xN29ixmmCZnmynZ3dwfFAki/h0djJIjunOiJZkCnu7v7VkNkjTDAvdjd3b0YpAuCy0DUSU90A4Lc3d1VjGGakGldQXcUzy7z8PAIn4hhQKq7u7ukEbJGGFBQdHd3XweyFoJTSzw8nu2FGOADEQKR893d3VmYYJqQaSZQoZgQC1IExt7lHh4vPNEN6MYZiwwMrKB6ExEI3rM8oj5gGLDU3d29QwbZYgTQUnZ3d08G2w4ivMOiTlzFMGChu7u7lAFCEzLQ0Hd3d18Oj0hv9xmBm9ENyAIlIyVcLXbmee7u7vNBtoOwt/sZTAOS3d3d+82RrUUG8pKgxFgO0u3h4eHt7l56C+oCcCnn4eFRDqqxTRSQNaEAZlDjIbgTYoK3u3vFNagB0GgMB7UaFgug6EEB/KqghlACpDT1dnfPeAw1AOKC8OOgppISP4oeVCANSkzufftBbvB2d/e6ATUA7ILAPpAPzbD2VuBASA2kKM8bEgZeIP2gzARyQRDI/e6CONIAHPCZgkxwnxIHCkQkA2Irl4MklJmxpmIkwGQOdoN7dZa3u/sEuAtOgMpid3dxLmEktTiYYjaggsE9uAfJgB6w892l+IjQz8BgqQpKUCAHZ8BcAOK4t9uJ4bATHciJioN1uE/a5enpOXcChGMlYo2uECdf2IId1EJ2d884uucoRH+dHpc6TvVYgK2oCko3NEdEGosqfEKAMdmL5ECcDso+mtwS+BRjl5PgZncGG7HSSQBf6sWuGyyqzs0iPmmrpoAcmEcWISEmKqSBXycAwi1SS8vdIDoAAAAASUVORK5CYII=",
    "Arábia Saudita": "data:image/png;base64,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",
    "Uruguai": "data:image/png;base64,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",
    "França": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXEiMU4jL0sWU4wWVYwcQXAeQ14AOWwXU4szQVgWU4wWU4sWU4wXVY0gME0gL00fMEwhLUkgME0gL0wiME0gMEwgME0WU4oWU4wVUowZVIgXVIwgL0whME0gME0eM00gL0whMEsgL0whL00iMU4iL1ImNFEhME0gL0whME0jMU4WVI0YVI0oN1MhL00kM08oNlIhME4gL0wlNFEhME0hME0oNlIgL0wWVIsTVIwXVIsWVIwWVYwXU4sXU4sYU44WU4whMEwgL0whL0wfMEwfMEwkMk8iME4gL0shMU0mNFAgL0wgMEwkM08lNFEVUooWVIsWVIwXVIsWVIwXUosXU4sWU4wXU4sXU4wWVIwjMU4gL0whMEwhME0jMU0pOFMxQVo4RmAhME3K1Nf///+wur/+/v/6+/wjMk/5+vr8/Pz5+vvn7O0iMU2xu8DR2ty+yM33+PmxvMH09fb4+fn9/f3x8/TL1djq7e8XVIwyQVv3+PgrOVVTYHa4w8jQ2Nrh5ujAys7f5efp7O4mNVFQXXTJ09b9/v7N1tny9fW3wcXk6Opqdoje4+Xl6etIVW309vc3RV/L0dZmc4WEj52lsLiqtLt1gZFlcYR5hJTd5OajrLa7xMm4wsb19/jI0tWzvcLEztG0vsMpOVTm6uzEz9N+iplNW3EvPlmBjZuYo61FU2uVn6uKlaJwfI1VYneuuL6st72cpbDa4eMtPFejrbc8S2M6SWK8xsooNlLU3N/i6OnX3uG1v8Xu8fKapa/o6uydqLDO09lJV25ib4K0vcSPm6a5v8jc4uTW3N58iZeTnqqIkp/O19rt8fKNmKTCzNDY4OKzusM+TWXGzNLBx86LlqNDUWlPXHNLWW/R1dri5eh3g5Opsrvf4+dfbH/Z3OG2v8TS2t1teIvL1NbW3eCVoayps7rGz9OHk6FyfY7s7/C9w8vd4OTV2t7JztRZZXrb3+NBT2fv8vOnrrqxuMHu7/Gutr+Yoa2xu7+8xsu0u8PS1txdan7FzdFodYaifh+tAAAAYnRSTlMA+hXwZgsIAjcEh6v6FUJFKRv7yOKclTD2Rx27T/7UGC4eNHiwDurdbiJZJVXiuPnVwX337fPvhF8ZdsJw/UA06lRgoD9I8NhlqbqSOs6iO9dkr+BNoeGYTLLSjImKJHqVucQtrt8AAAAJcEhZcwAACxMAAAsTAQCanBgAAAZKSURBVHgBYsAJInjhUoFwFimMSBuYajZmcRiTaJo3nJvHgZuLk4GBgYPbujIgyIJorVBgH1ZZKQ3xhIVEZSUXO1SceIrbttIKopqd2baSdD+wW3OEhEIM8Oe2tIKHB0SICJKNk4GBFaIORIEwhDdEyLhYDVAEku1aTpGkJOEYPvL0s4uZuYkktWYkJQkpkWWCY9KW7blb5iy7tjxJXZUcEwyTtl890HixfOnhqiRRMgxgZ6yZ/bW4Ir0sOXlKrpAg6SZwuiftnPm5sz09OTn5SBLp4cipl5SUVPMrK6Wp+dSRDBPS0x9/0uGp0xoXXmh+mHMpSYifdB8oJa3uSk6+8CR7QfeEFaZw/ZoaYqJGWsRECqdx0unk5N2lSxYsKb6ZxAYxgckvNwkEGFUEIAL4SK+klSvftac/WrRkQm0SE1ilgHrS4f2pedOOrU7KSCBYrignZcxuz369a1HfhH5ZsAsERZLW5qWm5qWmpk69nJRIII+wCyedKksp2XxiUd+8bW4gB7AJJx1L3Xhk4vXV0zek5rUmxYMEcWP+pJvJpVmZ+Q0Pu0uq1EHqzJNe/Tw441B7Svv7m6tSi6r08Scu56T9+eklKY+WPOydt1iYgYFBkXFi0ey7KVmTjt5qL2ldk7o/yRxkLE4slzF/V0l6yuYlc+sLq+QYGBg8kw7mXen8PmXm+pbJmd+qNuStUMMbCiJVyfklpSnNS+Y0Fn8yZWfwyV1e1FtW1p6SkvKxdWbKj2Wp65I0cVrPwMAgtyU5ubQkJb2hYEH1jCRvJoOk5/Ulad1vfhe2p2R+eFBdm3oNfwbRSypILstuT8k5mVr/cWJSUtLkjvYTcxbkFW3oy0q5PSVlct75JBmQTbhwdNKz5Kb29PTO9MYFfQem1678eHtu3rRVz1NT9xeWptxJWZN6LMkRl2YQUEpan9xbmt6e3Vl9ck5+SVZm+u33W9ecn7E2ddqmkpSXWZc2EHABg1zG1FnpKWUp89pLzp1ta1rS/Lr3UHNKyvSNRX9T0u9WHNq4Fn8YMPAnXX6anjOhr3pee2H7vhP1ycnJe9cdLv66JnV9SvWDe3+mTUlSADkVN1ZJeplSvq9+Vsq8rOySeenpZUueJh/5em9l6v323nklk6ZOliVQyiglfUg527E7uak9uySz5POe930pe47NTJueOiPr3dr2NwdrRHBbDgbspisKdyWXNefX727uPdGxN3VHypKj/SkrU3tKDnzKfH0/yRCsDA/hnDSlO3lWevrnnLmpJ/OTdyxKOTe/Zt+P1HXzilekL09KSlLGoxkEFE0zzrSVF7aXlLaldhU21ScXTkhed/Vt6vTP7S0VtUmiWvIgVfiwi1vS8v1L01PaO+tS/6WlpGS2n131vTN/U3NK1Zf10FIKn34GBkHDpKSk2X0T2lMye5uKUzJTujd+u7Fxw9GU5bW1hCIRAthlvJJqk5MXrp/4Izn57Is1hVPTJ81InXrvQc3iJFeIEkIkp2/Sy+TkVbktB5OTk/t3rrjTeXv/tJkza5OSNAhphQJBs4wpycmTk3ZuTU5eBqqtbkxenZSUJEtMyQ4BPqAaoicpaUtqckFLrp9aUlISo7Ay3sIEDZgnPZuakZSUNLEu+X6SFoOqpiLesgwDyJtl/NoGqo+S+ufPTtLDkCckoKSbtA7kd5ARp9q2Z0AqKUK6oEDRSVQ3KenxfFCRBjKgpW56khgR1SIUKKjkJiW1XO+Zv/BVT8+y47P/Tz/9r2hxUpKvB3Fh4MSYtO3M1fKO5OSOEyc275n/ZPOeR+XJBddaM5IMiPEHu/7iTen7ejsW7pjbtWhBXl5qakFbcvKFhcmzDq1PEoM6Eh/FrtZy/Ubr41v5XV1z54Jq5NS5BTsKulLzCnYdT/LEpxMG+HVBrYmqKzlLKpqTFzxs/Nc458XuvvLGPXtrhIhtc6myGclmbNu+8/KkWd2Tth5vvtXf/+XKmYxcLZglRNAyUfrGakmLe/pB2QCUHpOSTIjMh0jAQz8p18BI1F1dw8VbTBl/uwA7YBUgWHxh1zgoAC8LizYDA4MUC4sUAwOMR4rLAOPg4QJ1FSWZuUDmQHmkGSBtx8DAICkhbQ/q/fKAeSQZIKEDcrukg44lyAAIjyQDmMGqJYPBFAeEB2ajEwC1iF+SxXJZiQAAAABJRU5ErkJggg==",
    "Senegal": "data:image/png;base64,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",
    "Iraque": "data:image/png;base64,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",
    "Noruega": "data:image/png;base64,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",
    "Argentina": "data:image/png;base64,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",
    "Argélia": "data:image/png;base64,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",
    "Áustria": "data:image/png;base64,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",
    "Jordânia": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXH////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////BCi////8BAgINgEhEREQsLS3FGj3yzdVYWFhZWVlhrId/vJ55eXn//////v7CDTH6+voREhINDg4FBgbBCzAQgUojjFkiIyOEhYUWFxcCAwMGBwfm5uZlZWUyMzMeHx8YGRl1dXXh4eFycnKur6/DETXbcofee4/qq7idzLXEFDf++fr34ebj4+MICQng4OAnKChra2v4+Pj8/PyUlZWen5/a2tqtrq65uroEBQXghZfkk6PWW3TFFzr33uP9+Pn77vDKLk701dvijJ3wxc77/fzg7+ddqoTj8Okgilbz0dhqsY5wtJOay7NAm2+Jwab9/v3y8vJhYWGCg4NNTU3R0dE7PDyio6NnZ2c2Nzc/QECcnZ2RkpIZGhocHR1dXV3FxcX++vvSSmbvwcrCDzP89PbGHT/1193ttcD78PLIJkb88/Xjj6DcdovzztXrr7vJKUnaa4Lssr766+7YZXzYYnr009nHI0T4/Prd7eVJoHVWVlb0+fbfgJTP5tvk8euWl5fDEzbn8+0xk2PghJegzrgYhlEOgEnY6+Ffq4Zts5Hd3d0diFTe3t7Nzc3KysqwsbFjY2O8vb1aWlqNjo4tLi4LDAzo6OgkJSW2t7dwcHBISEirrKy+v7/rrrrQRGDoprPxydHQRWHnn62Nw6nVWHG628s9mW3ll6dZqIGn0bypqqpYp4H45OhSUlKr07+v1cOZmpoZhlG22cjNO1nPQV1RpHz45emw1sPu9vLTU21HR0fr6+s4lmgzlGXV1dUnjVv22t99u50uLy9lrot5uZorLCwVFhbBwcHCwsJoaGh/f3/AMqjxAAAANHRSTlMADxY3JW686/kENgbWo9/orK+OKYlF+3yRRteYEQ3JzL+C2uVJTAizuoTYd53uoApmntTgC9L4HAAAAAlwSFlzAAALEwAACxMBAJqcGAAABXlJREFUeAFigAJ2RxIBO1QjDFDBAB8LEoCPI6YLbMzAwNXVzMw92M3MzD/YO8TMzGyi92+QePAkMzN3V38zN1cQz8wGtwGJjrknDzq6tJt1Ozo6TnFNdXR0zDlllunoOMHsqOMxs0NphAwIc3Q/69gf5vQrwtHnmGNbuOOFs47n/FoPng4wC3R0PE6UAYlOSRmONhGOPn8cJ4c7hp937E9xvJDjODHQ0TEgjAgX+Cc6JU1wtI1wTHO8mAQ2IPO449/Djh2BjlmOjoQMOHO6JTfHMWO/4/cIx8npWe7hjvezHUNPgBLJ/0DHf50EDUhznGIWFODodMIswrG327HnHCgo3Y45BvU5Hgl0DOxyIuSC3r5TZmZJJ0PMzHy9/U95+7qfCfL2Mwv2znX3nuTm7WYWHIwzFkItSQChWNIBiQAzJZIIMA046ura7lhnRRDUOTYfOFCPxQu2ZmYOjtYmBIG1o725ud2oASMrDLZuRU8YJKaD6GjKDLAqmTsLzQSiXWA1w8TEJN/RMd/ExGSGFcIUog2YNrUsJq/Y0bE4L6Zs6jQyDDCZjcjgsz0IGsCPmRujEAZEIfSbQL3AD6tVocDYcbKZWShKdi6cCTNhZiGKAT/NzX848kE1woCRY4+ZWarjVySVC51gBjjlIQmXOTaYmzc4GsF0QoGCY6iZmY1jCVylxwKYdhB93RkuUeS419z8myMbVCMM6DlOMDPrcnSCKXS+BNKHwIthEh7Fjk3m5o2OOjCdUCDueMTMzNfRcTXMplkFV0pg+ufPWToPJr7a0bHW3Py5ozhUIwyoOh40MzMLc7wJU2hiYuJcBDGhCGY7SK7Ascrc3LzGUQWmEwqYHJ1czczug9MdSB0YL4IYgFLS3nF8bG5e6+jIBNUIB0qOHWZmbY51YJ1QYrrj/JUFJY7ToVwwtcqx3tz8riMPXCMMSDhuMTObmO60BKwMQsy5WmpiMq9iGYQHJpc4tXiZm8c6CsH0wYGkY5ifmVmOYzlYHYS4DPa88zUID0wucLxlbu652VEUrhEGOPkd+8zM1jsuxyhBwBqhRORyx2pz83WOypwwfQgg5JhpZuZ+0HEFVC1WaoVjlae5+T1HEYQ+OGBxSgsBpeaHyAkfzZStCaB07LXGiQWuDQkIOvqYmflnoYQCmgHljms9zc1vOAogaUMAZsdWXzOzR47xpWja4NzSeMcH5uZeGxyZEbqQgaBjhpmZ2QXHVXFwLSiMrYscn5iD4hC7AxgYWMRcgszMQgIcFyMVQAgjPGIct3mZm9+u5MAaAiCg6djpb2bWleaIUZaDjIl2rFxnbu65yVERpBYr5jZybDcDxYQTchkG0mxiYrLUCRQD5s2OWmpYNYMBF0fLezMzs6eOTguh2uBUlJNjrLm5+asWDi6wUhwEq+OHFDMzv0xHx41wrWDGRkfHnZ7m5p/eOrLi0AoFvI77Q8zM/PodHZchVSaFMRD9XlWOvFCFuChODcdOXzMzvwxHx4SXYLtNTExeFDk6Nu42N/fa46jAjUsnDMjIO36eZGZmFpjmGL8DnLG27oh3XLPP3Nz8yx5HOUaYOtw0o5xjQJCZmVnQQUfH1ys9TN4lODpubjI3N/9Y4ygvg1sfAjCyObauNzMz8812dHSsqHB0dHxTa25uvneDo4YsQhU+Fqe0o2O3m5mZWUcyqFDcVm1ubv4s1tHREEshgAOwcjhm9ZqZmbltcXRs3GVubt601pGDQPyhAmY+RxcfNzOzFEfH7ebmu5orHfnwph9MoC/h6BjQkwsyYHd1jaMjL5HeBwzJJEkpR8fDbY6O9ZscHaUwy1AklbiYnAbQDrWuNsHUg8MMGREOR0cxaYxKCIdybMLC6hrC2MQRYgDdxt9LptP80QAAAABJRU5ErkJggg==",
    "Portugal": "data:image/png;base64,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",
    "Colômbia": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXH////+//8VbLz//v70MD798/PzLz77ur/0OUf/+fnzLz70MUAgc7/1QU/3+vz/+/v95ecRarv////1Ul+ixeTy9/v0N0b//////Pz+9PX////3bXf////////////////0MUD////////14QD5lp37xMlmn9P////98fLzM0GPuN/////4fof////////0MUD5o6n8yc796+z////3ZG/0NUMOaLr5kZn1Tlv1PUvzLz4qecNNkMxHjMr8z9P////0MD8vfcMAX7YldsD7wcaeweP94+Wav+L1RFIbcL6uzejK3u/////97e735ij0+Pv4g4z///9rotX24gD0NkRDicn5oaf///9vpdbV5PP4eIKBsNs7hMf809b97vD7t7yoyOb3Z3P////6+/31W2f82t32XGn/9/f4h4/0NEP2S1j83N4FYrjG2+/6qbD////////////k7vf////u9Pn////24gEmd8H////14wb////1SVaTvOEAXrb//fm00Oq61Ov4+v1jntP////25RX////zMkF4qtgLZbn////////////96uv2cHv////460r1+Pv4iZH0O0r3YW3////7/P37r7Xm7/j5naP78or94OPh7PbR4/LA1+1dmtHY5/PP4fE3gsb785p0qNf///80gMUYbrz///z7tbr35R/////9+c3////46lD0Okn//////fH78IL9+9v1V2P57Fj81tn2dH4DYbdal9BTk87c6fRRks3p8fhJjMuKtt5Qkcz79aX89rb//////fb57m79++L898L24wr14gD7rbP///////r7sLf////57WH46Df24w39+tP46UP7vsP///97rNj////7vMGsy+i+1uz7vcL93+FZmNDZ5/TY5/Pw9fooeME4gcYBX7bo8fgccL4RarsldsHe6vX9/On24gP898P89az//fL2X2v////3bnj89rD9++T////897wneMHH3O/z9/vs8/rq8vn4jJX4gYr0MD/////24gAAX7as/YMwAAAA/HRSTlMAAfvP/vXy/c3W+PjsyM74++bR/sTL9NpS/fQFwCIQw+/u7NP+xNLAFfDlxMzApFXpx9Tr8cDe08LG0vvFv8DXjvLD+8bRyuTGy8rP2t/s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",
    "Uzbequistão": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXEYNCIXMiAWMiAWMyAWMyAWMiAVMiEVMyAbOBsWMiAjKSkWMyAWMiEXMiAWMiATMh0XMyAAOhYWMCAaNSQWMx8XMyEWMiAVMh8WMiAWMyAXMiEWMiAYMiEdOCciPCsiPCsXMyEWMiAXMyEXMiAbNiUYNSAZMiEWMiAmQC8YNSIXMyAWMiEoQzIXMyH///8mQC/Z3dpOZFZneW7v8e+CkYh0hXoxSjo+VUYYMyGZpZ3+/v5tf3SMmpGfqqOwubP5+fg0TT06UUKEk4l4iX58jIIYNCKrta9kd2zR1tNZbWDx8fDJ0Mz8/fyzvLb19vX6+/vBycSHlYyToJfoSk/pRktFXE1CWUoZNSP71NVVaVz09fRJX1EiPSssRTVxgnehraUdOSfc4N7rS1HP1dHU2dbs7ezGzciQnZU3Tz9hdGe0vbj84uMnQTHn6uhCPC9SZ1pxTEMrOCjSUlX62druWF35ur0pQzLL0c2+xsFbb2LW2tjg5OEcOCXx8/LKVVaNnJL6xcf3oqX3qqy4WlnfSk5jdmrsU1n95+fkTVH5wsS1vriUoZju7+6cqKD7z9DkSU1MYVP0jJCBkIY2Tj8fOilqfHCnsqsGBwfxZmuTUUzydXnXVlhdcWT98PDsT1TkRUq6w72sWFaKmI+xVlT4t7klNSXi5ePcUFT//Pz96+vq6+r4sLI3OSvKW13jVFnl6OaoqanW29hnRz5GXU7+9PQfNCPN0s/Ey8bzfoLWS076ysv+9/j+9vagrKQcMyKFVU6BT0fvXGBqTUO5wbxEQjWkr6i7vLxzdXTb29vExMS+W1qgWVbzfIFORTkyNyn2naHzgoalT0z2mp31lJjmRElIPjL0iIzybnP5vb+aV1PuX2T0hYmtXFliUEU9PS5WRjr83t+6VFT69fTEU1O4wbsyQTI/QECbm5s5OjofICAkJSXa3tv1kZR3UUnwa3CMT0ldQTaKSkSsaGXyen6Ki4uFhoZPT09rbGxlZmZYW1oyMzNeZmHnUlglPCv51daudOT/AAAALnRSTlMA8VXM4Xi0JC8JqwbUTLtoGdsCD+lHmYhQcD3PgDPu9v7lvpqO+RQek/n4pF/57btnkAAAAAlwSFlzAAALEwAACxMBAJqcGAAAB9pJREFUeAFiwAvYxRX5mLjxKsEDOJn44ian9IUranDgUYUTyIoxRvkFlEwqW2noXM7ML4xTIVYgzC9t7rx8b3Np8cFHodcfOvjNVeUSFcKqFAsQ4uVSnevnG3mnc8l9PT29/YXF7c1bNwQ7CrIKYFGNAdhlWCyC07Y2txcXWupBwflLC2Y3+vqYKRAMUU4mPgMzH+vdszvPFEE1QyjLzfXzm+Z5J4QxiuEJUVkxRqME/1WX56+7B9GGQi6b1TpzKThEJdUw3M3AwCDAKmjuXLOy8caEW8tQNCJxzrWETMpx8JurxcWLFqLcvFyqHgt9H05KXvcASQMmc9vBXaXNezYET1EUZwdZC8EcGowWwb17lt5ecWA/ph50kfwloTsjwSEqAdHOwMBsXK0fuTO05b6eXrhTjIfRRKOCcKPwGAuPMCPzTEfHtkwjc6+JHkYx5o7hsZl6enqWhcXtTfO8XXlgBrC5lyQXHwZHmpVpQYK7vX189WKrjKDpMYZm6fFmVvv67Gw9rNztFzdYZbpAHLR2UWiXH9wA5Z7+dRBxvWl2pq5BwYttXINcXMzMqha7mnlVOdr0ZFk5Ggdl2GZYxU93gqq8uwZhgIxrzhyoMPHU3TX2zDAv8E/b0wnVaaqvr2+op2eir69vrGegDwPZenrhIHYQVJment6ipdOVYAZIFOiHQGVwGNCtpzcZZMAOqDI9Pb2Wm3ZsMAOkLPTnQ2VwG1AJMiAgFqpOT+90Y7A2zAD2cv1D0KSPaUBKYGBgoK1erT/IAH0vuAH1kZNVYAZwRjjcOAeRwTTACCJRoK+vH6CvbwXh6enpFefYsMIMYGB5c/0dRAanARn6+mmB+vqbIMr09PRat1bxww1QWth0BiKD04AUff0jGfr61nEQdXp6V/XDROEGKFt1nYZIYBoQ7e3t7ayX66uvHzRXX19/GkSdnmWyfi4iO7G6wFISpgGgsLPVa9PX14+K09fXnw41oGimiRuivGfyWglNSbgMSNDXtzbQ26Cvn+cGMWHzxRQWuA8YODL1k8F5SQ/TgCRPT08zvRp9/Td6etn6+voWEANmXbCHJ0QGBm6t6Jn5YAlMA8DR6Kivr+9QU1Onr6/vClan96jRWRzhAgZmn7cHwBI4DDADhQQELwSr01sxL4oJyQDlvrIWsISLvr7+6ojYAH19/SpIZgK7wA+iGUT614IUWoZYlyMigYGB36YDkqG9QGp8DEGkE8KAiF6QABSDTcx/v5wRuVyVDdcPBYeiQTRUmb6hG8KALfr6+ukgi+309fUbQIwPl+35kHzAwM1oMvMaSEJvmi/EBO8YPYQBzvr6+j0gaRt9ff0KEKP+v40ksgEMbN1Nt0ASenpb3Jc7OCTZOeohGbBDX18/CyTtpK+v75urp7c/xDcOOQgYGCRdSopBKojEH89uF0RxAAOHk3UoUp0QW+FUWVDp5X5sslV8zI6qdBtXdzs7Z3Dwga1YUrYYXhhAgBCL4c5CsByYsPFxybZ1t/J7us9lsquPs7tFg332sR3w0sRywV4LKYhGOBBfvLserBdMmCeaOyU6xZrHTbUonzJ1imNinHm5ebkBWE5Pz+3AlxQW5EgEAQ6nlaHboAqQqHKLKVORuCBmos2m9f1mMiBNKFh6x5VZIHkkXJ5RAyrIAj2gORAkZR5sol9SaiKP2VjRyVq1AJyWQMrA2LhOv2KxjZnVcv0Kc7CAnl6Yu69+3uInZbZiKJaDAadI0tmDUHVgytX6zUQ98ygjhQgz/zxQsqj12K6v72lTu7bdWxM1EUAAa3xOK1gnhIjyTTFw2gjywjGDsOjq2jjnDfoBfjF6enpPuoKwOICBgVNk+WxETEYYRpsXbH/14mTaqZ8nyo31Kxz004LBPskv7ZVXh9iJRrLadITAI8JLv0EhLXrG9+PHX89I8wnU1/c0SwQ7zXJXvytaIoIBTsEdFxaBFenp6fXpW7jonzyhr68f/XK1fkA1rCjT+3QxVQRrI4uBgUHUwmE+pGTT06sMcLPXfwHOmXne+q5RkMykp3c+ZF4YclGECrh6+luhOSLFW2/hxldgA47/0HeZqG8Gdpvlrq4GeKWMqhkEBORSrywBK9SrtJ765/WMkyATvs3Y6NWm3wYWvzTJUw4zDSGAhFP0ocNglT36Rxz0T23019df/fzricR9+qCUoFd4u3cKvG2G0IYENOI7ko/q6blF+ejrJ1XrB/x+/rJaXz++vA5col0LWRWFmQlQAKf0vsjOZ2aG+r7e+jaxlfqeM07p+wa52et76Onprb1aYsqGngvRgbrikbL1j+usMi2iHYzd2rp/pSaER9jp2+vp6RVN6LfjIdzxkJVPXbP+mZ6enpeDtf0WNz29xKxU/ZRYPb2i1i53FuxJEBXw6qauWQFq8YQZ6uuneRr66/smTNXTWzvh5lMRbHkIE/BqppRNOKqnpxfhkf3GoTfFClSf5k/Y3S2Hp6uAAkQ1A/uTIbEJjlI9Pb3NoZH7RIjVz8AgJZfQUXoXqRya1d5hK0ic+yGAncfl8aQVIG+AnLCsfra3BzO+BIgJhNksNjXO/xwB0v9gQvOGMG1OTEX4RXTk+7beWX9Pb1lLaY59LqJJiF8XYMiyHNITDSMPrQtp8jZjQa9FkNXhZgtJMjpHL12Vbc5FOPnhMIWdzXyfFwsvDlmihEV5xAmEHgCLheggTUH43gAAAABJRU5ErkJggg==",
    "RD Congo": "data:image/png;base64,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",
    "Inglaterra": "data:image/png;base64,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",
    "Croácia": "data:image/png;base64,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",
    "Gana": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVMaXEAAAAAAAAAAAHWASMAAAH///8AFAgAAAEAPQDdACUClTYAAAH95AEDljYIlzXWASN3uh4AAAFJqyYAAAAAAAH+/fzcIB7WAiP///8AAAABlDYAAAAAAAADAwMNDQ2UlJQAAAAAAAEAAAHWBCLWASPUACQAAADWASQAAAD///8AAADkUBj82gIAAADWASMAAAAMmDQAAAGfn59MRADf398AAAEAAAHWASMAAADiRRknoS7BwcH8/Pr14wP71gMAAAAAAADY2NhbsiT09PT1twhycnIAAAEAAAEypCsZnTCampoAAAAEljXt7e38/PvWASPWACMBlTb74AF9fX2Dg4PWASPeISAAlDbVACMmJib39/cEBAIBAQAenjAAAABitCKjyBT64wIAAAAAAAEAAAAAAADWACSIiIjV1QjTACgBlTf60ATd2wjXACPK1QwEBASFvxrZEyDbGR8TmzLWACNcXFz97EXWACMAAADnYxUAAADuiw8AAAAsJwLZDyDrdhKbxhb+/v2Owhn09PDXBiLl5eXeLRx7uh70rQmsyxLn3AUAOx1TryR9vRyWxBbgNxrj3RD45AI6Ojp4eHh4bAEaFwADAgH1swhrYAH55Ak7piplZWXXACXC0Q7Pz8/98G7WACNXV1Xl3Qj/5QAbGxvVASTVASP55RYBlTe70A/4wgbn0AHG1AzQ1gz97VLp3gX96jn5ywVqtyH//N7VACOwsLDXACTkzwhHR0eOjo7z4QNRUVEAlTf4yQUBlTbo6OhBqinrexLsfRHVASTRvgFycnItLS3ocBPVACTwmQ3//OTvlA3/9qrv4AT76C51cDz+72P/+c//+Mbx4x4AlDYAljb/5AABlDb95AH95AEAljy0tLS4uLiexRQAljb/4AD/5AD/5QAAkDciIiKaigHEsAFdVAHItQ/xnwy3t7fezANGRkb98HRRUVH98YjWASTYxQLo1SbwlgtHRS7ayzGPhCH98YEIBwH/+cukpKT////+5QEAAADWASQBlTeyFQ1eAAAA+3RSTlMAMSuh+7n9B8IBA+6s/ufd7cK1wDio6Mfo+RD6HAT7876Bi7HixRkkunb2cL/1FvFL2I+/wMmTmfVkwMbB4vfwC0XFv9ncxYi8w8zAXeHR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",
    "Panamá": "data:image/png;base64,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"
}

def team_logo_src(team: str) -> str:
    return TEAM_LOGOS.get(team, "")


def team_badge_html(team: str) -> str:
    """PATCH ESCUDOS: badge circular usando escudo real; fallback para bandeira."""
    logo = team_logo_src(team)
    if logo:
        return f"<span class='shirt-badge'><img src='{logo}' alt='{team}' /></span>"
    return f"<span class='shirt-badge'>{FLAGS.get(team, '🏳️')}</span>"


def team_label_html(team: str) -> str:
    """PATCH VINTAGE: rótulo HTML seguro para cards compactos."""
    return f"{team_badge_html(team)}<span>{team}</span>"


def event_summary_text(match_id: str) -> str:
    """Resumo humano dos autores de gols e assistências já salvos no session_state."""
    events = st.session_state.events.get(match_id, [])
    if not events:
        return "Sem gols registrados."

    lines = []
    for ev in events:
        team = ev.get("team", "")
        scorer = ev.get("scorer", "") or "Autor indefinido"
        assist = ev.get("assist", "")
        if assist:
            lines.append(f"{FLAGS.get(team, '')} {team}: {scorer} — assistência: {assist}")
        else:
            lines.append(f"{FLAGS.get(team, '')} {team}: {scorer}")
    return "<br>".join(lines)


def ensure_events_for_score(match_id: str, home: str, away: str, hg: int, ag: int):
    """PATCH BUGFIX: garante que todo placar confirmado tenha os eventos correspondentes."""
    expected = int(hg) + int(ag)
    current = st.session_state.events.get(match_id, [])
    if expected == 0:
        st.session_state.events[match_id] = []
        return
    if len(current) != expected:
        make_auto_events(match_id, home, away, int(hg), int(ag))

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
    # PATCH CRAQUES: buffs hardcoded para pontos fora da curva da simulação.
    neymar_mask = (df["team"].eq("Brasil") & df["player_name"].str.contains("neymar", case=False, na=False))
    messi_mask = (df["team"].eq("Argentina") & df["player_name"].str.contains("messi", case=False, na=False))
    cr7_mask = (df["team"].eq("Portugal") & df["player_name"].str.contains("cristiano|ronaldo", case=False, na=False, regex=True))
    df.loc[neymar_mask, "ovr"] = 96
    df.loc[messi_mask, "ovr"] = 96
    df.loc[cr7_mask, "ovr"] = 96
    df["display"] = df["player_name"] + " · " + df["pos"] + " · OVR " + df["ovr"].astype(str)
    return df

def stable_rand_int(seed: str, low: int, high: int) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    value = int(digest[:8], 16)
    return low + (value % (high - low + 1))

def generate_player_ovr(team: str, pos: str, name: str, club: str) -> int:
    # PATCH CRAQUES: Neymar, Messi e Cristiano Ronaldo recebem OVR fixo de craque geracional.
    name_l = str(name).lower()
    if team == "Brasil" and "neymar" in name_l:
        return 96
    if team == "Argentina" and "messi" in name_l:
        return 96
    if team == "Portugal" and ("cristiano" in name_l or "ronaldo" in name_l):
        return 96
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

def team_star_factor(team: str) -> float:
    """
    Mede o peso dos craques do time.
    PATCH: se houver escalação manual, usa os 5 melhores TITULARES.
    """
    try:
        if "lineups" in st.session_state and team in st.session_state.lineups:
            return lineup_star_factor(team)
        df = players_df[players_df["team"] == team].sort_values("ovr", ascending=False)
        if df.empty:
            return OVR_LOOKUP.get(team, 70)
        return float(df.head(5)["ovr"].mean())
    except Exception:
        return OVR_LOOKUP.get(team, 70)


def top_deciders(team: str, n: int = 2) -> str:
    """Retorna os principais jogadores capazes de decidir."""
    try:
        if "lineups" in st.session_state and team in st.session_state.lineups:
            return top_deciders_from_lineup(team, n)
        df = players_df[players_df["team"] == team].sort_values("ovr", ascending=False).head(n)
        if df.empty:
            return "sem destaque definido"
        return ", ".join([f"{r['player_name']} ({int(r['ovr'])})" for _, r in df.iterrows()])
    except Exception:
        return "sem destaque definido"


def team_power(team: str, ovr_lookup: dict) -> float:
    """
    PATCH REALISMO OVR:
    A força agora é dominada pelo OVR dos titulares/elenco e pelo peso dos craques.
    Ranking ainda entra, mas não deixa seleção fraca virar favorita só por acaso.
    """
    rank = FIFA_RANKING.get(team, 48)

    try:
        ovr = float(lineup_ovr(team)) if "lineups" in st.session_state and team in st.session_state.lineups else float(ovr_lookup.get(team, 70))
    except Exception:
        ovr = float(ovr_lookup.get(team, 70))

    star = float(team_star_factor(team))

    # Normalizações mais agressivas: 70 vira mediano; 80+ vira elite.
    ovr_score = float(np.clip((ovr - 62) / 26, 0, 1))
    star_score = float(np.clip((star - 64) / 26, 0, 1))
    rank_score = float(np.clip((49 - rank) / 48, 0, 1))

    # OVR manda no jogo. Craques decidem. Ranking desempata.
    return float(0.76 * ovr_score + 0.17 * star_score + 0.07 * rank_score)

def match_probabilities(home: str, away: str, knockout: bool = False) -> dict:
    """
    PATCH REALISMO OVR:
    Probabilidades calculadas por rating contínuo:
    - OVR médio/titulares com peso alto;
    - top 5 craques com peso relevante;
    - ranking FIFA como ajuste fino.
    Diferenças grandes de OVR geram favoritismo esmagador e reduzem zebras irreais.
    """
    try:
        home_ovr = float(lineup_ovr(home)) if "lineups" in st.session_state and home in st.session_state.lineups else float(OVR_LOOKUP.get(home, 70))
        away_ovr = float(lineup_ovr(away)) if "lineups" in st.session_state and away in st.session_state.lineups else float(OVR_LOOKUP.get(away, 70))
    except Exception:
        home_ovr = float(OVR_LOOKUP.get(home, 70))
        away_ovr = float(OVR_LOOKUP.get(away, 70))

    home_star = float(team_star_factor(home))
    away_star = float(team_star_factor(away))

    home_rank = FIFA_RANKING.get(home, 48)
    away_rank = FIFA_RANKING.get(away, 48)

    # Rating em escala "pontos de força".
    # Cada ponto de OVR pesa muito mais que ranking.
    home_rating = 1.00 * home_ovr + 0.22 * home_star + 0.055 * (49 - home_rank)
    away_rating = 1.00 * away_ovr + 0.22 * away_star + 0.055 * (49 - away_rank)

    diff = float(home_rating - away_rating)

    # Logistic mais inclinada: OVR maior vira favoritismo real.
    if knockout:
        p_home = 1 / (1 + np.exp(-diff / 3.15))
        p_home = float(np.clip(p_home, 0.025, 0.975))
        return {"home": p_home, "away": float(1 - p_home)}

    # Empate só fica alto quando o jogo é realmente parelho.
    draw = 0.285 * np.exp(-abs(diff) / 7.2) + 0.045
    draw = float(np.clip(draw, 0.045, 0.30))

    p_home_no_draw = 1 / (1 + np.exp(-diff / 3.35))
    p_home_no_draw = float(np.clip(p_home_no_draw, 0.02, 0.98))

    remaining = 1 - draw
    p_home = remaining * p_home_no_draw
    p_away = remaining * (1 - p_home_no_draw)

    return {"home": float(p_home), "draw": float(draw), "away": float(p_away)}

def decimal_odd(prob: float, margin: float = 0.94) -> float:
    """Converte probabilidade em odd decimal."""
    prob = max(float(prob), 0.01)
    return round(max(1.01, 1 / (prob * margin)), 2)


def odds_text(home: str, away: str) -> str:
    """PATCH BANDEIRAS: odds com bandeiras e nomes, sem siglas truncadas."""
    p90 = match_probabilities(home, away, knockout=False)
    pko = match_probabilities(home, away, knockout=True)
    return (
        f"90min: {FLAGS.get(home,'')} {home} {decimal_odd(p90['home'])} · "
        f"Empate {decimal_odd(p90['draw'])} · "
        f"{FLAGS.get(away,'')} {away} {decimal_odd(p90['away'])}<br>"
        f"Avança: {FLAGS.get(home,'')} {home} {decimal_odd(pko['home'])} · "
        f"{FLAGS.get(away,'')} {away} {decimal_odd(pko['away'])}"
    )


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
    if "historical_sims" not in st.session_state:
        st.session_state.historical_sims = load_history() if "load_history" in globals() else {"total": 0, "wins": {t: 0 for t in ALL_TEAMS}}
    if "knockout_rounds" not in st.session_state:
        st.session_state.knockout_rounds = {}
    if "team_stage" not in st.session_state:
        st.session_state.team_stage = {t: "Fase de Grupos" for t in ALL_TEAMS}
    if "champion" not in st.session_state:
        st.session_state.champion = None
    # PATCH: estado da gestão tática sem remover lógica existente
    if "lineups" not in st.session_state:
        st.session_state.lineups = {}
    if "formations" not in st.session_state:
        st.session_state.formations = {}
    if "tactic_team" not in st.session_state:
        st.session_state.tactic_team = ALL_TEAMS[0]


# =========================
# PATCH HISTÓRICO DE SIMULAÇÕES
# Persistência leve em JSON local; no Streamlit Cloud funciona enquanto o container estiver ativo.
# Também mantém fallback em session_state.
# =========================
HISTORY_FILE = Path("historico_simulacoes.json")

def default_history() -> dict:
    return {"total": 0, "wins": {t: 0 for t in ALL_TEAMS}}

def load_history() -> dict:
    try:
        if HISTORY_FILE.exists():
            data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            if "total" in data and "wins" in data:
                for t in ALL_TEAMS:
                    data["wins"].setdefault(t, 0)
                return data
    except Exception:
        pass
    return default_history()

def save_history(data: dict):
    try:
        HISTORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

def ensure_history_state():
    if "historical_sims" not in st.session_state:
        st.session_state.historical_sims = load_history()

def record_historical_champion(team: str):
    ensure_history_state()
    if not team:
        return
    hist = st.session_state.historical_sims
    hist["total"] = int(hist.get("total", 0)) + 1
    hist.setdefault("wins", {})
    hist["wins"][team] = int(hist["wins"].get(team, 0)) + 1
    st.session_state.historical_sims = hist
    save_history(hist)

def reset_historical_simulations():
    st.session_state.historical_sims = default_history()
    save_history(st.session_state.historical_sims)

def historical_winrate_df() -> pd.DataFrame:
    ensure_history_state()
    hist = st.session_state.historical_sims
    total = max(int(hist.get("total", 0)), 0)
    rows = []
    for t in ALL_TEAMS:
        wins = int(hist.get("wins", {}).get(t, 0))
        rows.append({
            "Escudo": team_logo_src(t),
            "Seleção": f"{FLAGS.get(t,'')} {t}",
            "Títulos": wins,
            "Win Rate": round((wins / total * 100) if total else 0, 2),
            "Ranking FIFA": FIFA_RANKING[t],
            "OVR": round(float(OVR_LOOKUP.get(t, 0)), 1) if "OVR_LOOKUP" in globals() else 0,
        })
    return pd.DataFrame(rows).sort_values(["Títulos", "Win Rate", "OVR"], ascending=[False, False, False]).reset_index(drop=True)

init_state()
ensure_history_state()
players_df = load_players()
ovr_df = team_ovr_table(players_df)
OVR_LOOKUP = dict(zip(ovr_df["team"], ovr_df["OVR Médio"]))


# =========================
# PATCH: GESTÃO TÁTICA / TITULARES E RESERVAS
# =========================
FORMATION_LINES = {
    "4-3-3": [("Atacantes", 3, ["FW"]), ("Meias", 3, ["MF"]), ("Defensores", 4, ["DF"]), ("Goleiro", 1, ["GK"])],
    "4-4-2": [("Atacantes", 2, ["FW"]), ("Meias", 4, ["MF"]), ("Defensores", 4, ["DF"]), ("Goleiro", 1, ["GK"])],
    "3-5-2": [("Atacantes", 2, ["FW"]), ("Meias", 5, ["MF"]), ("Defensores", 3, ["DF"]), ("Goleiro", 1, ["GK"])],
}


def squad_display_list(team: str) -> list:
    """Lista dos 26 convocados em formato usado nos selectboxes."""
    df = players_df[players_df["team"] == team].sort_values(["pos", "ovr"], ascending=[True, False])
    return df["display"].tolist()


def player_row_from_display(team: str, display: str):
    """Recupera a linha do jogador a partir do texto do selectbox."""
    if not display:
        return None
    name = display.split(" · ")[0]
    df = players_df[(players_df["team"] == team) & (players_df["player_name"] == name)]
    if df.empty:
        return None
    return df.iloc[0]


def default_lineup(team: str, formation: str = "4-3-3") -> list:
    """Gera uma escalação inicial equilibrada por posição e OVR."""
    df = players_df[players_df["team"] == team].copy().sort_values("ovr", ascending=False)
    chosen = []
    used = set()

    # A formação é renderizada de ataque para defesa, mas aqui escolhemos por necessidade posicional.
    needs = []
    for _, amount, positions in FORMATION_LINES.get(formation, FORMATION_LINES["4-3-3"]):
        for _ in range(amount):
            needs.append(positions[0])

    # Garante goleiro e linhas por posição.
    for pos in ["GK", "DF", "MF", "FW"]:
        amount = needs.count(pos)
        candidates = df[df["pos"] == pos].sort_values("ovr", ascending=False)
        for _, row in candidates.head(amount).iterrows():
            disp = row["display"]
            if disp not in used:
                chosen.append(disp)
                used.add(disp)

    # Fechada com melhores disponíveis caso alguma posição não tenha quantidade suficiente.
    for _, row in df.iterrows():
        if len(chosen) >= 11:
            break
        disp = row["display"]
        if disp not in used:
            chosen.append(disp)
            used.add(disp)

    return chosen[:11]


def ensure_lineup(team: str):
    """Inicializa escalação da seleção se ainda não existir."""
    formation = st.session_state.formations.get(team, "4-3-3")
    if team not in st.session_state.lineups or len(st.session_state.lineups.get(team, [])) != 11:
        st.session_state.lineups[team] = default_lineup(team, formation)
    return st.session_state.lineups[team]


def lineup_ovr(team: str) -> float:
    """OVR médio dos titulares. Se não houver escalação, usa o OVR médio do elenco."""
    try:
        lineup = ensure_lineup(team)
        vals = []
        for disp in lineup:
            row = player_row_from_display(team, disp)
            if row is not None:
                vals.append(float(row["ovr"]))
        if vals:
            return float(np.mean(vals))
    except Exception:
        pass
    return float(OVR_LOOKUP.get(team, 70))


def lineup_star_factor(team: str) -> float:
    """Média dos 5 melhores titulares, usada como fator de craque decisivo."""
    try:
        lineup = ensure_lineup(team)
        vals = []
        for disp in lineup:
            row = player_row_from_display(team, disp)
            if row is not None:
                vals.append(float(row["ovr"]))
        if vals:
            return float(np.mean(sorted(vals, reverse=True)[:5]))
    except Exception:
        pass
    return float(OVR_LOOKUP.get(team, 70))


def top_deciders_from_lineup(team: str, n: int = 2) -> str:
    """Mostra craques titulares, sem apagar o cálculo original dos elencos."""
    try:
        lineup = ensure_lineup(team)
        rows = []
        for disp in lineup:
            row = player_row_from_display(team, disp)
            if row is not None:
                rows.append(row)
        rows = sorted(rows, key=lambda r: float(r["ovr"]), reverse=True)[:n]
        if rows:
            return ", ".join([f"{r['player_name']} ({int(r['ovr'])})" for r in rows])
    except Exception:
        pass
    try:
        df = players_df[players_df["team"] == team].sort_values("ovr", ascending=False).head(n)
        if not df.empty:
            return ", ".join([f"{r['player_name']} ({int(r['ovr'])})" for _, r in df.iterrows()])
    except Exception:
        pass
    return "sem destaque definido"


def available_options_for_slot(team: str, current_value: str, selected_values: list) -> list:
    """Evita duplicar jogadores nos 11 slots, mantendo o valor atual disponível."""
    options = squad_display_list(team)
    selected = set([v for v in selected_values if v != current_value])
    filtered = [o for o in options if o not in selected]
    if current_value and current_value not in filtered:
        filtered.insert(0, current_value)
    return filtered


def render_player_chip(team: str, display: str):
    row = player_row_from_display(team, display)
    if row is None:
        st.markdown("<div class='player-chip'>A definir</div>", unsafe_allow_html=True)
        return
    st.markdown(
        f"""
        <div class="player-chip">
            <strong>{row['player_name']}</strong><br>
            <span class="muted">{row['pos']} · OVR {int(row['ovr'])}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_tactical_board(team: str):
    """Campo tático visual com titulares e reservas usando os 26 convocados."""
    st.markdown(f"### 🧩 Gestão de Escalação — {FLAGS.get(team,'')} {team}")
    ctop1, ctop2, ctop3 = st.columns([1.2, 1.2, 2.4])
    with ctop1:
        formation = st.selectbox(
            "Formação",
            list(FORMATION_LINES.keys()),
            index=list(FORMATION_LINES.keys()).index(st.session_state.formations.get(team, "4-3-3")),
            key=f"formation_{team}"
        )
    st.session_state.formations[team] = formation

    with ctop2:
        if st.button("Restaurar melhores 11", key=f"reset_lineup_{team}", use_container_width=True):
            st.session_state.lineups[team] = default_lineup(team, formation)
            st.rerun()

    lineup = ensure_lineup(team)

    with ctop3:
        st.markdown(
            f"""
            <div class="clean-card">
                <span class="mini-stat-title">Força dos titulares</span><br>
                <span class="mini-stat-value">OVR {lineup_ovr(team):.1f}</span>
                <div class="mini-stat-sub">Craques: {top_deciders_from_lineup(team, 2)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div class='tactic-pitch'>", unsafe_allow_html=True)
    slot_index = 0
    new_lineup = list(lineup)

    for line_title, amount, _positions in FORMATION_LINES[formation]:
        st.markdown(f"<div class='tactic-line-title'>{line_title}</div>", unsafe_allow_html=True)
        cols = st.columns(amount)
        for i in range(amount):
            with cols[i]:
                current = new_lineup[slot_index] if slot_index < len(new_lineup) else squad_display_list(team)[0]
                options = available_options_for_slot(team, current, new_lineup)
                idx = options.index(current) if current in options else 0
                selected = st.selectbox(
                    f"Slot {slot_index + 1}",
                    options,
                    index=idx,
                    key=f"lineup_{team}_{slot_index}",
                    label_visibility="collapsed"
                )
                new_lineup[slot_index] = selected
                render_player_chip(team, selected)
                slot_index += 1

    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.lineups[team] = new_lineup[:11]
    duplicated = [p for p in set(new_lineup) if new_lineup.count(p) > 1]
    if duplicated:
        st.warning("Há jogadores duplicados na escalação. Troque um dos repetidos para preservar o realismo.")

    reserves = [p for p in squad_display_list(team) if p not in st.session_state.lineups[team]]
    with st.expander(f"Reservas ({len(reserves)})", expanded=False):
        res_rows = []
        for disp in reserves:
            row = player_row_from_display(team, disp)
            if row is not None:
                res_rows.append({"Pos": row["pos"], "Jogador": row["player_name"], "Clube": row["club"], "OVR": int(row["ovr"])})
        if res_rows:
            st.dataframe(pd.DataFrame(res_rows).sort_values(["OVR"], ascending=False), use_container_width=True, hide_index=True)


def set_tactic_team(team: str):
    st.session_state.tactic_team = team
    ensure_lineup(team)

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


def group_form_for_team(team: str, group: str) -> str:
    """PATCH FORMA: mini esteira com os três jogos do grupo: 🟢 vitória, 🟡 empate, 🔴 derrota."""
    marks = []
    matches = [m for m in st.session_state.group_matches if m.get("group") == group and team in [m["home"], m["away"]]]
    for m in matches:
        r = st.session_state.results.get(m["id"], {})
        if not r.get("played"):
            continue
        hg, ag = int(r.get("home_goals", 0)), int(r.get("away_goals", 0))
        if hg == ag:
            marks.append("🟡")
        else:
            won = (m["home"] == team and hg > ag) or (m["away"] == team and ag > hg)
            marks.append("🟢" if won else "🔴")
    return "".join(marks) if marks else "—"

def prepare_standings_display(df: pd.DataFrame) -> pd.DataFrame:
    """PATCH TABELA: escudo real + ordem oficial de colunas."""
    show = df.copy()
    show["Escudo"] = show["Time"].map(team_logo_src)
    show["PTS"] = show["Pts"]
    cols = ["Pos", "Escudo", "Seleção", "PTS", "J", "V", "E", "D", "GP", "GC", "SG", "Forma", "FP", "Ranking", "OVR"]
    return show[[c for c in cols if c in show.columns]]

def render_standings_dataframe(df: pd.DataFrame, hide_extra: bool = True):
    """PATCH ESCUDOS: renderiza a classificação com ImageColumn quando possível."""
    show = prepare_standings_display(df)
    if hide_extra:
        show = show[[c for c in ["Pos", "Escudo", "Seleção", "PTS", "J", "V", "E", "D", "GP", "GC", "SG", "Forma"] if c in show.columns]]
    st.dataframe(
        show,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Escudo": st.column_config.ImageColumn("", width="small"),
            "Seleção": st.column_config.TextColumn("Seleção", width="medium"),
            "Forma": st.column_config.TextColumn("Últimos Jogos", width="small"),
            "PTS": st.column_config.NumberColumn("PTS", width="small"),
        }
    )

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
        df["Forma"] = df["Time"].map(lambda t: group_form_for_team(t, group))
        # PATCH TABELA: ordem oficial pedida: PTS, J, V, E, D, GP, GC, SG + mini esteira.
        tables[group] = df[["Pos", "Seleção", "Time", "Pts", "J", "V", "E", "D", "GP", "GC", "SG", "Forma", "FP", "Ranking", "OVR"]]
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
    """
    PATCH REALISMO OVR:
    Primeiro sorteia o resultado respeitando probabilidades fortes por OVR.
    Depois gera um placar coerente com esse resultado.
    Isso reduz zebras absurdas sem eliminar o drama do futebol.
    """
    probs = match_probabilities(home, away, knockout=False)
    outcome = random.choices(
        ["home", "draw", "away"],
        weights=[probs["home"], probs["draw"], probs["away"]],
        k=1
    )[0]

    try:
        home_ovr = float(lineup_ovr(home)) if "lineups" in st.session_state and home in st.session_state.lineups else float(OVR_LOOKUP.get(home, 70))
        away_ovr = float(lineup_ovr(away)) if "lineups" in st.session_state and away in st.session_state.lineups else float(OVR_LOOKUP.get(away, 70))
    except Exception:
        home_ovr = float(OVR_LOOKUP.get(home, 70))
        away_ovr = float(OVR_LOOKUP.get(away, 70))

    home_star = float(team_star_factor(home))
    away_star = float(team_star_factor(away))
    diff = (home_ovr - away_ovr) + 0.22 * (home_star - away_star)

    # Volume ofensivo com limites para não virar placar de handebol.
    home_xg = 1.05 + max(diff, -10) * 0.075 + (home_ovr - 70) * 0.035
    away_xg = 1.05 + max(-diff, -10) * 0.075 + (away_ovr - 70) * 0.035

    home_xg = float(np.clip(home_xg, 0.22, 3.35))
    away_xg = float(np.clip(away_xg, 0.22, 3.35))

    if outcome == "draw":
        # Empates mais comuns: 0x0, 1x1, 2x2; 3x3 é raro.
        g = int(np.random.choice([0, 1, 2, 3], p=[0.20, 0.52, 0.23, 0.05]))
        return g, g

    if outcome == "home":
        ag = int(np.random.poisson(max(0.22, away_xg * 0.72)))
        margin_base = 1 + int(np.random.poisson(max(0.15, (home_xg - away_xg) * 0.45 + 0.25)))
        # Favorito muito superior pode abrir margem.
        if diff > 7 and random.random() < min(0.55, diff / 22):
            margin_base += 1
        hg = ag + max(1, margin_base)
        return min(int(hg), 7), min(int(ag), 6)

    # away vence
    hg = int(np.random.poisson(max(0.22, home_xg * 0.72)))
    margin_base = 1 + int(np.random.poisson(max(0.15, (away_xg - home_xg) * 0.45 + 0.25)))
    if diff < -7 and random.random() < min(0.55, abs(diff) / 22):
        margin_base += 1
    ag = hg + max(1, margin_base)
    return min(int(hg), 6), min(int(ag), 7)

def store_simulated_match(m):
    """
    PATCH BUGFIX: simula partida de grupo e sincroniza placar + autores/assistências.
    Resolve o caso em que a tabela atualizava, mas os detalhes do jogo ficavam vazios.
    """
    mid = m["id"]
    home, away = m["home"], m["away"]
    hg, ag = simulate_score(home, away)

    st.session_state.results[mid] = {
        "home_goals": int(hg),
        "away_goals": int(ag),
        "played": True
    }

    # Sincroniza os widgets visuais.
    st.session_state[f"{mid}_hg"] = int(hg)
    st.session_state[f"{mid}_ag"] = int(ag)
    st.session_state[f"{mid}_played"] = True

    # Gols/assistências e cartões também entram no estado imediatamente.
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
    PATCH BUGFIX: sorteia autores e assistentes e salva em todos os lugares que a UI usa.
    Atacantes e meias têm maior peso; assistências podem ficar vazias.
    """
    events = []

    for team, goals in [(home, int(hg)), (away, int(ag))]:
        df = players_df[players_df["team"] == team].copy()
        if df.empty or goals <= 0:
            continue

        pos_weights = {"FW": 5.2, "MF": 3.2, "DF": 1.1, "GK": 0.03}
        weights = df["pos"].map(pos_weights).fillna(1.0).to_numpy(dtype=float)

        # Craques participam um pouco mais, mas sem virar videogame quebrado.
        if "ovr" in df.columns:
            ovr_boost = np.clip((df["ovr"].to_numpy(dtype=float) - 65) / 25, 0, 1.4)
            weights = weights * (1 + ovr_boost)

        weights = weights / weights.sum()
        names = df["display"].tolist()

        for goal_n in range(goals):
            scorer_display = str(np.random.choice(names, p=weights))

            assist_options = ["Sem assistência"] + names
            assist_weights = np.array([0.20] + list(weights * 0.80), dtype=float)
            assist_weights = assist_weights / assist_weights.sum()
            assist_display = str(np.random.choice(assist_options, p=assist_weights))

            if assist_display == scorer_display:
                assist_display = "Sem assistência"

            scorer_pure = pure_player_name(scorer_display)
            assist_pure = pure_player_name(assist_display)
            events.append({"team": team, "scorer": scorer_pure, "assist": assist_pure})

            # Keys dos selectboxes. Assim, ao abrir Detalhes, já aparece preenchido.
            st.session_state[f"{match_id}_{team}_g{goal_n}_scorer"] = scorer_display
            st.session_state[f"{match_id}_{team}_g{goal_n}_assist"] = assist_display

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
    """
    PATCH FINAL — PLACAR ÚNICO NA FASE DE GRUPOS:
    remove o placar HTML duplicado e mantém apenas os inputs centrais.
    Súmula, eventos, tática e simulação continuam iguais.
    """
    mid = m["id"]
    home, away = m["home"], m["away"]
    current = st.session_state.results.get(
        mid,
        {"home_goals": 0, "away_goals": 0, "played": False}
    )

    st.session_state.setdefault(f"{mid}_hg", int(current.get("home_goals", 0)))
    st.session_state.setdefault(f"{mid}_ag", int(current.get("away_goals", 0)))
    st.session_state.setdefault(f"{mid}_played", bool(current.get("played", False)))

    # Linha principal do confronto: escudo/nome + placar único + escudo/nome.
    c_team_h, c_hg, c_x, c_ag, c_team_a, c_details = st.columns([1.35, .34, .08, .34, 1.35, .30])

    with c_team_h:
        st.markdown(
            f"<div class='match-single-team-left'>{team_label_html(home)}</div>",
            unsafe_allow_html=True
        )

    with c_hg:
        hg = st.number_input(
            f"Gols {home}",
            min_value=0,
            max_value=15,
            key=f"{mid}_hg",
            label_visibility="collapsed"
        )

    with c_x:
        st.markdown("<div class='match-x'>x</div>", unsafe_allow_html=True)

    with c_ag:
        ag = st.number_input(
            f"Gols {away}",
            min_value=0,
            max_value=15,
            key=f"{mid}_ag",
            label_visibility="collapsed"
        )

    with c_team_a:
        st.markdown(
            f"<div class='match-single-team-right'>{team_label_html(away)}</div>",
            unsafe_allow_html=True
        )

    with c_details:
        played = st.checkbox("OK", key=f"{mid}_played")

    st.session_state.results[mid] = {
        "home_goals": int(hg),
        "away_goals": int(ag),
        "played": bool(played)
    }

    if played and mid not in st.session_state.discipline:
        st.session_state.discipline[mid] = {
            home: {"yellow": 0, "second_yellow_red": 0, "direct_red": 0, "yellow_direct_red": 0, "fp": 0},
            away: {"yellow": 0, "second_yellow_red": 0, "direct_red": 0, "yellow_direct_red": 0, "fp": 0}
        }

    if played:
        ensure_events_for_score(mid, home, away, int(hg), int(ag))

    dcol1, dcol2 = st.columns([.72, .28])
    with dcol1:
        if st.button("🎲 Jogar", key=f"sim_one_{mid}", use_container_width=True):
            store_simulated_match(m)
            st.rerun()

    with dcol2:
        if hasattr(st, "popover"):
            detail_ctx = st.popover("⚙️", use_container_width=True)
        else:
            detail_ctx = st.expander("ℹ️ Súmula", expanded=False)

        with detail_ctx:
            st.markdown("**Ficha da partida**")
            st.markdown(
                f"<div class='details-copy'>Ranking: {home} #{FIFA_RANKING[home]} · OVR titulares {lineup_ovr(home):.1f}<br>"
                f"Ranking: {away} #{FIFA_RANKING[away]} · OVR titulares {lineup_ovr(away):.1f}</div>",
                unsafe_allow_html=True
            )

            if st.button(f"🧩 Tática {home[:10]}", key=f"tactic_{mid}_{home}", use_container_width=True):
                set_tactic_team(home)
                st.toast(f"Prancheta aberta para {home}. Vá na aba 🧩 Tática.")

            if st.button(f"🧩 Tática {away[:10]}", key=f"tactic_{mid}_{away}", use_container_width=True):
                set_tactic_team(away)
                st.toast(f"Prancheta aberta para {away}. Vá na aba 🧩 Tática.")

            st.markdown("---")
            st.markdown("**Gols e assistências**")

            if played:
                st.markdown(
                    f"<div class='details-copy'>{event_summary_text(mid)}</div>",
                    unsafe_allow_html=True
                )
                render_goal_selectors(mid, home, away, int(hg), int(ag))
            else:
                st.caption("Confirme o jogo para registrar os eventos.")

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
    """PATCH BUGFIX: monta os 16-avos com 32 classificados, limpando chave antiga sem apagar grupos."""
    direct, best_thirds, thirds_df = qualified_teams()
    teams = list(dict.fromkeys(direct + best_thirds))

    tables, overall = compute_group_tables()
    group_perf = []
    for g, df in tables.items():
        for _, r in df.iterrows():
            if r["Time"] in teams:
                group_perf.append(r)

    seed_df = pd.DataFrame(group_perf).sort_values(
        ["Pts", "SG", "GP", "FP", "Ranking"],
        ascending=[False, False, False, True, True]
    ).reset_index(drop=True)
    seeds = seed_df["Time"].tolist()

    if len(seeds) < 32:
        st.error("Ainda não há 32 classificados. Confira se todos os grupos foram fechados.")
        return
    seeds = seeds[:32]

    # Limpa apenas dados antigos do mata-mata, preservando fase de grupos e estatísticas já registradas.
    old_ko_ids = []
    for matches in st.session_state.knockout_rounds.values():
        old_ko_ids.extend([m["id"] for m in matches])
    for mid in old_ko_ids:
        st.session_state.results.pop(mid, None)
        st.session_state.events.pop(mid, None)
        st.session_state.discipline.pop(mid, None)

    pair_indices = [(0,31),(15,16),(7,24),(8,23),(3,28),(12,19),(4,27),(11,20),
                    (1,30),(14,17),(6,25),(9,22),(2,29),(13,18),(5,26),(10,21)]
    matches = []
    for i, (a, b) in enumerate(pair_indices):
        matches.append({"id": f"KO_32_{i}", "phase": "16-avos", "home": seeds[a], "away": seeds[b]})

    st.session_state.knockout_rounds = {"16-avos": matches}
    st.session_state.champion = None

    for t in ALL_TEAMS:
        if t not in teams:
            st.session_state.team_stage[t] = "Fase de Grupos"
    for t in teams:
        st.session_state.team_stage[t] = "16-avos"


def get_match_winner(mid, home, away, hg, ag):
    if hg > ag:
        return home
    if ag > hg:
        return away
    return st.session_state.results.get(mid, {}).get("winner", home)


def simulate_knockout_match(m):
    """PATCH BUGFIX: simula mata-mata e sincroniza placar, vencedor, eventos e cartões."""
    mid, home, away = m["id"], m["home"], m["away"]
    hg, ag = simulate_score(home, away)

    if hg == ag:
        probs = match_probabilities(home, away, knockout=True)
        winner = random.choices([home, away], weights=[probs["home"], probs["away"]], k=1)[0]
    else:
        winner = home if hg > ag else away

    st.session_state.results[mid] = {"home_goals": int(hg), "away_goals": int(ag), "played": True, "winner": winner}
    st.session_state[f"{mid}_ko_hg"] = int(hg)
    st.session_state[f"{mid}_ko_ag"] = int(ag)
    st.session_state[f"{mid}_ko_played"] = True
    st.session_state[f"{mid}_winner"] = winner

    make_auto_events(mid, home, away, int(hg), int(ag))
    simulate_cards_for_match(mid, home, away)
    return winner


def auto_advance_completed_rounds():
    """Avança automaticamente fases já encerradas, sem recriar fases existentes."""
    changed = False
    for phase in ROUND_ORDER:
        if phase not in st.session_state.knockout_rounds:
            continue
        if not current_round_complete(phase):
            continue
        if phase == "Final":
            if not st.session_state.champion:
                advance_round("Final")
                changed = True
            continue
        next_phase = NEXT_ROUND[phase]
        if next_phase not in st.session_state.knockout_rounds:
            advance_round(phase)
            changed = True
    return changed


def simulate_remaining_knockout():
    """Simula todo o mata-mata restante até sair campeão."""
    if not st.session_state.knockout_rounds:
        generate_round_of_32()
    guard = 0
    while not st.session_state.champion and guard < 10:
        guard += 1
        phase_to_play = None
        for phase in ROUND_ORDER:
            if phase in st.session_state.knockout_rounds and not current_round_complete(phase):
                phase_to_play = phase
                break
        if phase_to_play is None:
            changed = auto_advance_completed_rounds()
            if not changed:
                break
            continue
        simulate_round(phase_to_play)
        auto_advance_completed_rounds()


def render_placeholder_card(label: str = "A definir"):
    st.markdown(f"""<div class="ko-placeholder">{label}</div>""", unsafe_allow_html=True)


def render_knockout_match_compact(m):
    """
    PATCH FINAL — PLACAR ÚNICO NO MATA-MATA:
    remove o placar HTML duplicado e mantém apenas os inputs centrais.
    Súmula, odds, eventos, tática e avanço de fase continuam iguais.
    """
    mid, phase, home, away = m["id"], m["phase"], m["home"], m["away"]
    current = st.session_state.results.get(
        mid,
        {"home_goals": 0, "away_goals": 0, "played": False, "winner": home}
    )

    st.session_state.setdefault(f"{mid}_ko_hg", int(current.get("home_goals", 0)))
    st.session_state.setdefault(f"{mid}_ko_ag", int(current.get("away_goals", 0)))
    st.session_state.setdefault(f"{mid}_ko_played", bool(current.get("played", False)))

    if st.session_state.get(f"{mid}_winner") not in [home, away]:
        st.session_state[f"{mid}_winner"] = current.get("winner", home)

    played_now = bool(st.session_state.results.get(mid, {}).get("played", False))
    winner_now = st.session_state.results.get(mid, {}).get("winner", "")
    h_cls = "ko-winner-row" if winner_now == home and played_now else ""
    a_cls = "ko-winner-row" if winner_now == away and played_now else ""

    st.markdown(f"<div class='ko-card-header'>{phase}</div>", unsafe_allow_html=True)

    # Linha principal do confronto: escudo/nome + placar único + escudo/nome.
    c_home, c_hg, c_x, c_ag, c_away = st.columns([1.15, .34, .08, .34, 1.15])

    with c_home:
        st.markdown(
            f"<div class='match-single-team-left {h_cls}'>{team_label_html(home)}</div>",
            unsafe_allow_html=True
        )

    with c_hg:
        hg = st.number_input(
            f"{home[:10]}",
            min_value=0,
            max_value=15,
            key=f"{mid}_ko_hg",
            label_visibility="collapsed"
        )

    with c_x:
        st.markdown("<div class='match-x'>x</div>", unsafe_allow_html=True)

    with c_ag:
        ag = st.number_input(
            f"{away[:10]}",
            min_value=0,
            max_value=15,
            key=f"{mid}_ko_ag",
            label_visibility="collapsed"
        )

    with c_away:
        st.markdown(
            f"<div class='match-single-team-right {a_cls}'>{team_label_html(away)}</div>",
            unsafe_allow_html=True
        )

    b1, b2, b3 = st.columns([.44, .34, .22])

    with b1:
        if st.button("🎲 Jogar", key=f"sim_ko_one_{mid}", use_container_width=True):
            simulate_knockout_match(m)
            auto_advance_completed_rounds()
            st.rerun()

    with b2:
        played = st.checkbox("OK", key=f"{mid}_ko_played")

    if int(hg) > int(ag):
        winner = home
    elif int(ag) > int(hg):
        winner = away
    else:
        winner = st.session_state.get(f"{mid}_winner", home)

    st.session_state.results[mid] = {
        "home_goals": int(hg),
        "away_goals": int(ag),
        "played": bool(played),
        "winner": winner
    }

    if played:
        ensure_events_for_score(mid, home, away, int(hg), int(ag))

    with b3:
        if hasattr(st, "popover"):
            detail_ctx = st.popover("ℹ️", use_container_width=True)
        else:
            detail_ctx = st.expander("ℹ️ Súmula", expanded=False)

    with detail_ctx:
        d1, d2 = st.columns(2)

        with d1:
            if st.button("🧩 Tática", key=f"tactic_ko_{mid}", use_container_width=True):
                set_tactic_team(home)
                st.toast(f"Prancheta aberta para {home}. Vá na aba 🧩 Tática.")

        with d2:
            if int(hg) == int(ag):
                winner = st.selectbox("Quem passa se empatar?", [home, away], key=f"{mid}_winner")
                st.session_state.results[mid]["winner"] = winner

        p90 = match_probabilities(home, away, knockout=False)
        pko = match_probabilities(home, away, knockout=True)

        st.markdown(
            f"""
            <div class='details-copy'>
                <strong>Odds 90min</strong><br>
                {FLAGS.get(home,'')} {home}: {decimal_odd(p90['home'])} · Empate: {decimal_odd(p90['draw'])} · {FLAGS.get(away,'')} {away}: {decimal_odd(p90['away'])}<br><br>
                <strong>Chance de avançar</strong><br>
                {FLAGS.get(home,'')} {home}: {decimal_odd(pko['home'])} · {FLAGS.get(away,'')} {away}: {decimal_odd(pko['away'])}<br><br>
                <strong>OVR em campo</strong><br>
                {home}: {lineup_ovr(home):.1f} · {away}: {lineup_ovr(away):.1f}<br><br>
                <strong>Camisa pesada</strong><br>
                {home}: {top_deciders(home, 2)}<br>
                {away}: {top_deciders(away, 2)}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.markdown("**Gols e assistências**")

        if played:
            st.markdown(
                f"<div class='details-copy'>{event_summary_text(mid)}</div>",
                unsafe_allow_html=True
            )
            render_goal_selectors(mid, home, away, int(hg), int(ag))
        else:
            st.caption("Feche o jogo para registrar os eventos.")


def render_phase_column(title: str, matches: list, empty_slots: int = 0):
    st.markdown(f"<div class='fifa-bracket-title'>{title}</div>", unsafe_allow_html=True)
    if not matches:
        for _ in range(empty_slots):
            render_placeholder_card()
        return
    for m in matches:
        render_knockout_match_compact(m)


def split_matches_for_side(phase: str, side: str) -> list:
    matches = st.session_state.knockout_rounds.get(phase, [])
    if not matches:
        return []
    half = len(matches) // 2
    if phase == "Final":
        return matches
    return matches[:half] if side == "left" else matches[half:]



def _safe_font(size=24, bold=False):
    """PATCH EXPORT PNG: tenta carregar fonte limpa para desenho do chaveamento."""
    if ImageFont is None:
        return None
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            pass
    return ImageFont.load_default()


def _match_export_label(m):
    mid = m["id"]
    res = st.session_state.results.get(mid, {})
    hg = res.get("home_goals", "") if res.get("played") else ""
    ag = res.get("away_goals", "") if res.get("played") else ""
    return str(hg), str(ag)


def build_bracket_png() -> bytes:
    """PATCH EXPORT PNG: desenha o chaveamento completo em PNG, estável no Streamlit."""
    if Image is None or ImageDraw is None:
        return b""

    W, H = 1900, 1120
    img = Image.new("RGB", (W, H), "#F4F4F4")
    draw = ImageDraw.Draw(img)
    title_font = _safe_font(42, True)
    sub_font = _safe_font(22, False)
    round_font = _safe_font(18, True)
    team_font = _safe_font(16, True)
    score_font = _safe_font(18, True)
    small_font = _safe_font(13, False)

    red = "#E10600"
    text = "#151515"
    muted = "#666666"
    line = "#C9C9C9"
    card = "#FFFFFF"

    draw.rectangle([0, 0, W, H], fill="#F4F4F4")
    draw.rectangle([0, 0, W, 92], fill="#FFFFFF")
    draw.rectangle([0, 88, W, 92], fill=red)
    draw.text((58, 24), "Simulador Copa 2026", fill=text, font=title_font)
    champ = st.session_state.champion or "Campeão a definir"
    draw.text((58, 72), f"Chaveamento completo · {champ}", fill=muted, font=sub_font)

    phases = ["16-avos", "Oitavas", "Quartas", "Semifinal", "Final"]
    xs = {"16-avos": 70, "Oitavas": 430, "Quartas": 790, "Semifinal": 1150, "Final": 1510}
    y_start = 130
    card_w, card_h = 265, 54
    max_rows = {"16-avos": 16, "Oitavas": 8, "Quartas": 4, "Semifinal": 2, "Final": 1}

    positions = {}
    for ph in phases:
        matches = st.session_state.knockout_rounds.get(ph, [])
        nmax = max_rows[ph]
        gap = (H - y_start - 80 - card_h) / max(1, nmax - 1)
        x = xs[ph]
        draw.text((x, y_start - 32), ph.upper(), fill=red, font=round_font)
        for i, m in enumerate(matches):
            # Mantém espaçamento da fase cheia para ficar simétrico.
            y = y_start + i * gap * (nmax / max(1, len(matches))) if len(matches) and ph != "16-avos" else y_start + i * gap
            if ph == "Final":
                y = 520
            positions[m["id"]] = (x, y)
            draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=12, fill=card, outline="#DCDCDC", width=1)
            draw.rectangle([x, y, x + 5, y + card_h], fill=red)
            hg, ag = _match_export_label(m)
            home, away = m["home"], m["away"]
            res = st.session_state.results.get(m["id"], {})
            winner = res.get("winner", "") if res.get("played") else ""
            hfill = red if winner == home else text
            afill = red if winner == away else text
            draw.text((x + 14, y + 8), home[:22], fill=hfill, font=team_font)
            draw.text((x + card_w - 38, y + 8), str(hg), fill=text, font=score_font)
            draw.text((x + 14, y + 30), away[:22], fill=afill, font=team_font)
            draw.text((x + card_w - 38, y + 30), str(ag), fill=text, font=score_font)

    # Linhas horizontais entre fases por ordem de avanço.
    for ph in phases[:-1]:
        cur = st.session_state.knockout_rounds.get(ph, [])
        nxt = st.session_state.knockout_rounds.get(NEXT_ROUND.get(ph, ""), [])
        for j, nm in enumerate(nxt):
            if 2*j < len(cur) and cur[2*j]["id"] in positions and nm["id"] in positions:
                x1, y1 = positions[cur[2*j]["id"]]
                x2, y2 = positions[nm["id"]]
                y1c = y1 + card_h / 2
                y2c = y2 + card_h / 2
                midx = x1 + card_w + 24
                draw.line([x1 + card_w, y1c, midx, y1c], fill=line, width=2)
                if 2*j+1 < len(cur) and cur[2*j+1]["id"] in positions:
                    xb, yb = positions[cur[2*j+1]["id"]]
                    ybc = yb + card_h / 2
                    draw.line([xb + card_w, ybc, midx, ybc], fill=line, width=2)
                    draw.line([midx, y1c, midx, ybc], fill=line, width=2)
                    draw.line([midx, y2c, x2, y2c], fill=line, width=2)
                else:
                    draw.line([midx, y1c, x2, y2c], fill=line, width=2)

    draw.text((58, H - 45), "Gerado no Simulador da Copa 2026", fill=muted, font=small_font)
    out = BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()

def render_fifa_bracket():
    """Novo chaveamento em uma tela: lado esquerdo -> centro/final <- lado direito."""
    phases = st.session_state.knockout_rounds
    left, center, right = st.columns([4.8, 1.7, 4.8], gap="small")

    with left:
        l1, l2, l3, l4 = st.columns([1.4, 1.2, 1.0, .9], gap="small")
        with l1:
            render_phase_column("16-avos", split_matches_for_side("16-avos", "left"), empty_slots=8)
        with l2:
            render_phase_column("Oitavas", split_matches_for_side("Oitavas", "left"), empty_slots=4)
        with l3:
            render_phase_column("Quartas", split_matches_for_side("Quartas", "left"), empty_slots=2)
        with l4:
            render_phase_column("Semi", split_matches_for_side("Semifinal", "left"), empty_slots=1)

    with center:
        st.markdown("<div class='fifa-bracket-title'>Grande Final</div>", unsafe_allow_html=True)
        final_matches = phases.get("Final", [])
        if final_matches:
            render_knockout_match_compact(final_matches[0])
        else:
            render_placeholder_card("Final a definir")
        if st.session_state.champion:
            st.success(f"🏆 {FLAGS.get(st.session_state.champion,'')} {st.session_state.champion}")

    with right:
        r1, r2, r3, r4 = st.columns([.9, 1.0, 1.2, 1.4], gap="small")
        with r1:
            render_phase_column("Semi", split_matches_for_side("Semifinal", "right"), empty_slots=1)
        with r2:
            render_phase_column("Quartas", split_matches_for_side("Quartas", "right"), empty_slots=2)
        with r3:
            render_phase_column("Oitavas", split_matches_for_side("Oitavas", "right"), empty_slots=4)
        with r4:
            render_phase_column("16-avos", split_matches_for_side("16-avos", "right"), empty_slots=8)


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
    """PATCH BUGFIX: avança fases sem quebrar quando a rodada ainda não está perfeita."""
    matches = st.session_state.knockout_rounds.get(phase, [])
    if not matches:
        return

    winners = []
    for m in matches:
        r = st.session_state.results.get(m["id"])
        if not r or not r.get("played", False):
            return
        winner = get_match_winner(m["id"], m["home"], m["away"], int(r["home_goals"]), int(r["away_goals"]))
        if winner not in [m["home"], m["away"]]:
            winner = m["home"]
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

    if len(winners) % 2 != 0:
        st.warning("Rodada incompleta para montar a próxima fase.")
        return

    next_phase = NEXT_ROUND[phase]
    next_matches = []
    for i in range(0, len(winners), 2):
        next_matches.append({"id": f"KO_{next_phase}_{i//2}", "phase": next_phase, "home": winners[i], "away": winners[i+1]})

    st.session_state.knockout_rounds[next_phase] = next_matches
    for w in winners:
        st.session_state.team_stage[w] = next_phase


def simulate_round(phase):
    """Simula todos os jogos de uma fase do mata-mata com sincronização visual completa."""
    for m in st.session_state.knockout_rounds.get(phase, []):
        simulate_knockout_match(m)
    auto_advance_completed_rounds()

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
# PATCH ASSINATURA FINAL: mantém o topo limpo e adiciona a autoria discreta.
st.title("Dashboard Simulador Copa 2026")
st.markdown(
    "<div class='creator-signature'>by <strong>Samuel França Jakecascavel</strong></div>",
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Seleções", "48")
m2.metric("Jogadores", f"{len(players_df):,}".replace(",", "."))
m3.metric("OVR médio geral", f"{players_df['ovr'].mean():.1f}")
m4.metric("Jogos da fase de grupos", "72")

tab_groups, tab_knockout, tab_stats, tab_simulations, tab_history, tab_final, tab_tactics, tab_squads = st.tabs(
    ["⚽ Fase de Grupos", "🏆 Mata-Mata", "📊 Estatísticas", "🧠 Cenários", "📈 Probabilidades Históricas", "🌍 Classificação Final", "🧩 Tática", "👥 Elencos/OVR"]
)

# =========================
# ABA: FASE DE GRUPOS
# =========================
with tab_groups:
    st.subheader("Fase de Grupos")

    c1, c2, c3 = st.columns([1.05, 1.05, 3.2])
    with c1:
        if st.button("🎲 Jogar pendentes", use_container_width=True):
            for m in st.session_state.group_matches:
                if not st.session_state.results.get(m["id"], {}).get("played", False):
                    store_simulated_match(m)
            st.rerun()
    with c2:
        if st.button("🧹 Resetar torneio", use_container_width=True):
            for key in ["results", "events", "knockout_rounds", "team_stage", "champion", "discipline", "fair_play"]:
                if key in st.session_state:
                    del st.session_state[key]
            init_state()
            st.rerun()
    with c3:
        st.markdown(
            "<div class='clean-card'><span class='muted'>Marque o placar no estilo súmula: simples por fora, completo nos detalhes.</span></div>",
            unsafe_allow_html=True
        )

    tables, overall_stats = compute_group_tables()
    direct, best_thirds, thirds_df = qualified_teams()
    show_thirds = thirds_df[["Grupo", "Seleção", "Time", "Pts", "J", "V", "E", "D", "GP", "GC", "SG", "Forma", "FP", "Ranking", "OVR"]].copy()

    st.markdown("<div class='thirds-trigger-card'><div class='thirds-title'>Terceiros na briga</div><div class='muted'>Oito melhores continuam. O resto tá eliminado.</div></div>", unsafe_allow_html=True)

    # Pop-up/Popover dos melhores terceiros: ocupa zero espaço enquanto fechado.
    if hasattr(st, "popover"):
        with st.popover("🏁 Ver ranking de terceiros", use_container_width=True):
            st.caption("Critérios: pontos, saldo, gols marcados, fair play e ranking.")
            thirds_show = prepare_standings_display(show_thirds)
            thirds_show.insert(0, "Grupo", show_thirds["Grupo"].values)
            st.dataframe(
                thirds_show[["Grupo", "Escudo", "Seleção", "PTS", "J", "V", "E", "D", "GP", "GC", "SG", "Forma"]],
                use_container_width=True,
                hide_index=True,
                column_config={"Escudo": st.column_config.ImageColumn("", width="small"), "Forma": st.column_config.TextColumn("Últimos Jogos", width="small")}
            )
            q = direct + best_thirds
            st.markdown("**Classificados provisórios**")
            st.write(", ".join([f"{FLAGS.get(t,'')} {t}" for t in q]))
    else:
        with st.expander("🏁 Ver ranking de terceiros", expanded=False):
            st.caption("Critérios: pontos, saldo, gols marcados, fair play e ranking.")
            thirds_show = prepare_standings_display(show_thirds)
            thirds_show.insert(0, "Grupo", show_thirds["Grupo"].values)
            st.dataframe(
                thirds_show[["Grupo", "Escudo", "Seleção", "PTS", "J", "V", "E", "D", "GP", "GC", "SG", "Forma"]],
                use_container_width=True,
                hide_index=True,
                column_config={"Escudo": st.column_config.ImageColumn("", width="small"), "Forma": st.column_config.TextColumn("Últimos Jogos", width="small")}
            )
            q = direct + best_thirds
            st.markdown("**Classificados provisórios**")
            st.write(", ".join([f"{FLAGS.get(t,'')} {t}" for t in q]))

    # Grade 3x4: mais grupos visíveis ao mesmo tempo.
    group_items = list(GROUPS.items())
    grid_cols = st.columns(3)

    for idx, (group, teams) in enumerate(group_items):
        with grid_cols[idx % 3]:
            st.markdown(
                f"<div class='group-shell'><div class='group-mini-title'>Grupo {group}</div><span class='muted'>" +
                " · ".join([f"{FLAGS.get(t,'')} {t}" for t in teams]) +
                "</span></div>",
                unsafe_allow_html=True
            )

            matches = [m for m in st.session_state.group_matches if m["group"] == group]
            with st.expander("Jogos e tabela", expanded=(group in ["A", "B", "C"])):
                if st.button(f"🎲 Jogar Grupo {group}", key=f"sim_group_{group}", use_container_width=True):
                    for gm in matches:
                        if not st.session_state.results.get(gm["id"], {}).get("played", False):
                            store_simulated_match(gm)
                    st.rerun()

                render_standings_dataframe(tables[group], hide_extra=True)

                for m in matches:
                    render_match_input(m)

# =========================
# ABA: MATA-MATA
# =========================
with tab_knockout:
    st.subheader("Chave eliminatória")

    if not all_played_group_matches():
        st.warning("Feche os 72 jogos da fase de grupos para liberar a chave.")
    else:
        top_actions = st.columns([1.4, 1.4, 1.8, 3.4])

        with top_actions[0]:
            if not st.session_state.knockout_rounds:
                if st.button("Montar chave", use_container_width=True):
                    generate_round_of_32()
                    st.rerun()
            else:
                st.success("Chave gerada")

        with top_actions[1]:
            if st.session_state.knockout_rounds:
                if st.button("🎲 Jogar próxima fase", use_container_width=True):
                    for phase in ROUND_ORDER:
                        if phase in st.session_state.knockout_rounds and not current_round_complete(phase):
                            simulate_round(phase)
                            break
                    auto_advance_completed_rounds()
                    st.rerun()

        with top_actions[2]:
            if st.session_state.knockout_rounds:
                if st.button("🚀 Jogar mata-mata restante", use_container_width=True):
                    simulate_remaining_knockout()
                    st.rerun()

        with top_actions[3]:
            st.markdown(
                "<span class='muted'>Chave limpa no estilo oficial. A súmula fica no ícone de informação de cada jogo.</span>",
                unsafe_allow_html=True
            )

    if st.session_state.knockout_rounds:
        changed = auto_advance_completed_rounds()
        if changed:
            st.rerun()

        render_fifa_bracket()

        # PATCH EXPORT PNG: download do chaveamento em imagem oficial.
        png_bytes = build_bracket_png()
        if png_bytes:
            st.download_button(
                "⬇️ Baixar chaveamento em PNG",
                data=png_bytes,
                file_name="chaveamento_copa_2026.png",
                mime="image/png",
                use_container_width=True,
            )
        else:
            st.caption("Exportação em PNG indisponível: Pillow não está instalado no ambiente.")

        st.markdown("---")
        st.markdown("### Atalhos por fase")

        visible_phases = [p for p in ROUND_ORDER if p in st.session_state.knockout_rounds]
        phase_cols = st.columns(len(visible_phases))
        for idx, phase in enumerate(visible_phases):
            with phase_cols[idx]:
                if st.button(f"Simular {phase}", key=f"sim_phase_{phase}", use_container_width=True):
                    simulate_round(phase)
                    st.rerun()
                if current_round_complete(phase):
                    st.success("Fechada")
                else:
                    st.info("Em aberto")

    if st.session_state.champion:
        st.success(f"🏆 Campeão: {FLAGS.get(st.session_state.champion,'')} {st.session_state.champion}")

# =========================
# ABA: ESTATÍSTICAS
# =========================
with tab_stats:
    st.subheader("Estatísticas")
    goals_df, assists_df = event_tables()
    cards_df = discipline_table()

    total_goals = int(goals_df["Gols"].sum()) if not goals_df.empty else 0
    top_scorer = "—" if goals_df.empty else f"{goals_df.iloc[0]['Jogador']} ({goals_df.iloc[0]['Gols']})"
    top_assist = "—" if assists_df.empty else f"{assists_df.iloc[0]['Jogador']} ({assists_df.iloc[0]['Assistências']})"
    best_ovr_team = ovr_df.sort_values("OVR Médio", ascending=False).iloc[0]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Gols registrados", total_goals)
    k2.metric("Artilheiro", top_scorer)
    k3.metric("Garçom", top_assist)
    k4.metric("Maior OVR", f"{FLAGS.get(best_ovr_team['team'],'')} {best_ovr_team['team']} · {best_ovr_team['OVR Médio']:.1f}")

    st.markdown("<div class='clean-card'><span class='muted'>Relatórios detalhados ficam recolhidos para manter o painel limpo. Abra apenas o que quiser analisar.</span></div>", unsafe_allow_html=True)

    with st.expander("🥅 Artilharia detalhada", expanded=not goals_df.empty):
        if goals_df.empty:
            st.info("Nenhum gol registrado ainda.")
        else:
            st.dataframe(goals_df, use_container_width=True, hide_index=True)

    with st.expander("🎯 Assistências detalhadas", expanded=False):
        if assists_df.empty:
            st.info("Nenhuma assistência registrada ainda.")
        else:
            st.dataframe(assists_df, use_container_width=True, hide_index=True)

    with st.expander("🟨 Cartões e Fair Play", expanded=False):
        st.caption("Fair Play negativo: amarelo=-1, vermelho 2A=-3, vermelho direto=-4, amarelo+VD=-5.")
        if cards_df.empty:
            st.info("Nenhum cartão registrado ainda. Jogos simulados geram cartões automaticamente; jogos manuais começam com fair play 0.")
        else:
            st.dataframe(cards_df, use_container_width=True, hide_index=True)

    with st.expander("📈 OVR por seleção", expanded=False):
        ovr_show = ovr_df.copy()
        ovr_show["Seleção"] = ovr_show["team"].map(lambda t: f"{FLAGS.get(t,'')} {t}")
        ovr_show = ovr_show.sort_values("OVR Médio", ascending=False)[["Seleção", "OVR Médio"]]
        st.dataframe(ovr_show, use_container_width=True, hide_index=True)

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
    st.subheader("Cenários computacionais de campeão")
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
                    record_historical_champion(champ)
            st.rerun()
    with s3:
        if st.button("🧹 Zerar histórico de simulações"):
            st.session_state.sim_wins = {t: 0 for t in ALL_TEAMS}
            st.session_state.sim_runs = 0
            reset_historical_simulations()
            st.rerun()

    sim_df = pd.DataFrame([{"Seleção": f"{FLAGS.get(t,'')} {t}", "Títulos simulados": v, "Probabilidade": (v / st.session_state.sim_runs * 100 if st.session_state.sim_runs else 0), "Ranking FIFA": FIFA_RANKING[t], "OVR": OVR_LOOKUP.get(t, 70)} for t, v in st.session_state.sim_wins.items()])
    sim_df = sim_df.sort_values(["Títulos simulados", "Probabilidade", "OVR"], ascending=[False, False, False]).reset_index(drop=True)
    sim_df["Probabilidade"] = sim_df["Probabilidade"].round(2).astype(str) + "%"
    top_sim = sim_df.iloc[0]["Seleção"] if not sim_df.empty else "—"
    sm1, sm2 = st.columns(2)
    sm1.metric("Torneios simulados", st.session_state.sim_runs)
    sm2.metric("Mais campeão nas simulações", top_sim)
    with st.expander("🏆 Ranking completo das simulações", expanded=True):
        st.dataframe(sim_df, use_container_width=True, hide_index=True)


# =========================
# ABA: PROBABILIDADES HISTÓRICAS
# =========================
with tab_history:
    st.subheader("Probabilidades Históricas")
    ensure_history_state()
    hist_total = int(st.session_state.historical_sims.get("total", 0))
    hist_df = historical_winrate_df()
    h1, h2, h3 = st.columns(3)
    h1.metric("Total de simulações", hist_total)
    leader = hist_df.iloc[0] if not hist_df.empty else None
    h2.metric("Maior win rate", f"{leader['Seleção']} · {leader['Win Rate']}%" if leader is not None and hist_total else "—")
    h3.metric("Campeão mais recorrente", f"{leader['Títulos']} títulos" if leader is not None and hist_total else "—")

    c_hist1, c_hist2 = st.columns([1, 3])
    with c_hist1:
        if st.button("🧹 Zerar histórico", use_container_width=True):
            reset_historical_simulations()
            st.rerun()
    with c_hist2:
        st.caption("O ranking abaixo usa todas as simulações completas feitas na aba Cenários. Quanto mais simulações, mais estável fica a leitura.")

    hist_view = hist_df.copy()
    hist_view["Win Rate"] = hist_view["Win Rate"].map(lambda x: f"{x:.2f}%")
    st.dataframe(
        hist_view,
        use_container_width=True,
        hide_index=True,
        column_config={"Escudo": st.column_config.ImageColumn("", width="small")}
    )

# =========================
# ABA: CLASSIFICAÇÃO FINAL
# =========================
with tab_final:
    st.subheader("Classificação Final Geral — 1º ao 48º")
    final_df = final_ranking_table()

    champion_row = final_df.iloc[0] if not final_df.empty else None
    total_games_df = tournament_team_stats()
    played_total = int(total_games_df["J"].sum() / 2) if not total_games_df.empty else 0

    f1, f2, f3 = st.columns(3)
    f1.metric("Líder atual", champion_row["Seleção"] if champion_row is not None else "—")
    f2.metric("Jogos disputados", played_total)
    f3.metric("Critério", "Fase + desempenho")

    st.caption("Ordenação: fase alcançada, pontos, vitórias, saldo, gols pró e ranking FIFA.")
    with st.expander("🌍 Ver tabela completa 1º ao 48º", expanded=True):
        st.dataframe(final_df, use_container_width=True, hide_index=True)

# =========================
# ABA: GESTÃO TÁTICA
# =========================
with tab_tactics:
    st.subheader("Prancheta Tática")
    st.markdown("<div class='clean-card'><span class='muted'>Monte titulares e reservas. A simulação passa a considerar o OVR médio dos 11 titulares e os craques escalados, sem apagar o banco de dados original.</span></div>", unsafe_allow_html=True)
    select_col, info_col = st.columns([1.2, 2.8])
    with select_col:
        tactic_team = st.selectbox(
            "Seleção",
            ALL_TEAMS,
            index=ALL_TEAMS.index(st.session_state.get("tactic_team", ALL_TEAMS[0])),
            format_func=lambda t: f"{FLAGS.get(t,'')} {t}",
            key="tactic_team_selector"
        )
        st.session_state.tactic_team = tactic_team
        ensure_lineup(tactic_team)
    with info_col:
        st.markdown(
            f"""
            <div class="clean-card">
                <div class="mini-stat-title">Resumo tático</div>
                <div class="mini-stat-value">{FLAGS.get(tactic_team,'')} {tactic_team}</div>
                <div class="mini-stat-sub">Ranking FIFA #{FIFA_RANKING[tactic_team]} · OVR elenco {OVR_LOOKUP.get(tactic_team, 0):.1f} · OVR titulares {lineup_ovr(tactic_team):.1f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    render_tactical_board(tactic_team)

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
