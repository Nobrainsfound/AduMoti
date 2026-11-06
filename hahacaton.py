import time
import streamlit as st
# 1) Сделать надписи на кнопках больше 
# 2) Красивый дизайн 
# 3) Сделать чтобы линии клеток не пересекали текст  
# 4) Сделать чтобы темы были 6 , 7 может 8 класса 
# 5) Сделать нормальные игры
# 6) Сделать чтобы нельзя было прейти к следубщей теме до изучения предидущей 
# 7) Исправить ошибки в некторых играх

# Настройка оформления страницы сайта
st.set_page_config(
    page_title="AducationMotivation",
    page_icon="🦉",
    layout="centered"
)

# ─── Игровое состояние: XP, серия побед, пройденные темы ──────────────
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "completed" not in st.session_state:
    st.session_state.completed = set()
if "theory_step" not in st.session_state:
    st.session_state.theory_step = 0

# Оформление в стиле Duolingo: зелёные объёмные кнопки, белые карточки
st.markdown("""
<style>
/* ═══════════════════════════════════════════════════════════════════
   DUOLINGO-СТИЛЬ
   Зелёный #58CC02 · объёмные кнопки · белые карточки · Nunito
   ═══════════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Cousine:wght@400;700&display=swap');

:root {
    --duo-green: #58cc02;
    --duo-green-dark: #58a700;
    --duo-blue: #1cb0f6;
    --duo-blue-dark: #1899d6;
    --duo-red: #ff4b4b;
    --duo-red-dark: #ea2b2b;
    --duo-yellow: #ffc800;
    --duo-yellow-dark: #e6a800;
    --duo-purple: #ce82ff;
    --duo-purple-dark: #a568cc;
    --duo-orange: #ff9600;
    --duo-orange-dark: #e08600;
    --duo-teal: #00cd9c;
    --duo-teal-dark: #00a37d;
    --duo-ink: #3c3c3c;
    --duo-muted: #777777;
    --duo-line: #e5e5e5;
    --duo-bg: #ffffff;
}

/* ─── ФОН: чистый белый лист, как в Duolingo ──────────────────────── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--duo-bg) !important;
    background-image:
        radial-gradient(900px 520px at 88% -12%, rgba(88, 204, 2, 0.12), transparent 60%),
        radial-gradient(760px 460px at -12% 108%, rgba(28, 176, 246, 0.10), transparent 55%) !important;
    background-attachment: fixed !important;
}

[data-testid="stMainBlockContainer"],
.block-container {
    max-width: 1080px !important;
    padding-top: 1.4rem !important;
    padding-bottom: 3rem !important;
}

header[data-testid="stHeader"],
#MainMenu,
footer,
[data-testid="stDecoration"],
[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stVerticalBlock"] { gap: 0.6rem !important; }
[data-testid="stHorizontalBlock"] { gap: 1rem !important; align-items: stretch !important; }

/* ─── ТИПОГРАФИКА ─────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], .stApp, p, li, span, div {
    font-family: 'Nunito', 'Segoe UI', Tahoma, sans-serif !important;
}

.stApp, .markdown-text, p, li, span { color: var(--duo-ink); }

h1, h2, h3 {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 900 !important;
    color: var(--duo-ink) !important;
    letter-spacing: -0.015em !important;
    background: none !important;
    padding: 0 !important;
    text-shadow: none !important;
}

h2, h3 {
    font-size: 1.55rem !important;
    line-height: 1.25 !important;
    margin: 0.2rem 0 0.9rem !important;
}

h1 {
    color: var(--duo-green) !important;
    font-size: clamp(2rem, 5vh, 2.8rem) !important;
}

h1::after, h2::after, h3::after { display: none !important; }

/* ─── ВЕРХНЯЯ ПАНЕЛЬ ──────────────────────────────────────────────── */
.duo-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
    padding: 0.2rem 0 1.1rem;
    margin-bottom: 1.2rem;
    border-bottom: 2px solid var(--duo-line);
}

.duo-logo {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    font-size: clamp(1.5rem, 3.2vh, 2rem);
    font-weight: 900;
    color: var(--duo-green) !important;
    letter-spacing: -0.02em;
}

.duo-owl {
    display: grid;
    place-items: center;
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    background: var(--duo-green);
    color: #fff;
    font-size: 1.55rem;
    line-height: 1;
    box-shadow: 0 4px 0 var(--duo-green-dark);
}

.duo-stats { display: flex; gap: 0.55rem; flex-wrap: wrap; }

.duo-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.42rem 0.9rem;
    border-radius: 999px;
    background: #f7f7f7;
    border: 2px solid var(--duo-line);
    font-weight: 800;
    color: var(--duo-ink) !important;
    font-size: 0.92rem;
    white-space: nowrap;
}

.duo-chip-green {
    background: #e8ffd8;
    border-color: #b8ef8a;
    color: #3f8f05 !important;
}

.duo-chip-gold {
    background: #fff6d6;
    border-color: #ffd966;
    color: #9a7100 !important;
}

/* ─── ПРИВЕТСТВЕННЫЙ БАННЕР ──────────────────────────────────────── */
.duo-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    background: linear-gradient(135deg, #58cc02 0%, #7ae020 100%);
    border-radius: 18px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 5px 0 var(--duo-green-dark);
    color: #fff;
}

.duo-banner-title {
    font-size: 1.25rem;
    font-weight: 900;
    color: #fff !important;
    line-height: 1.25;
}

.duo-banner-text {
    margin-top: 0.2rem;
    font-size: 0.95rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.92) !important;
}

.duo-banner-emoji {
    font-size: 2.4rem;
    line-height: 1;
    filter: drop-shadow(0 2px 0 rgba(0, 0, 0, 0.12));
    animation: duoBob 3s ease-in-out infinite;
}

@keyframes duoBob {
    0%, 100% { transform: translateY(0) rotate(-4deg); }
    50% { transform: translateY(-8px) rotate(4deg); }
}

/* ─── ПРОГРЕСС УРОКА ─────────────────────────────────────────────── */
.duo-progress {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 0.1rem 0 1.2rem;
}

.duo-progress-track {
    flex: 1;
    height: 16px;
    border-radius: 999px;
    background: #e5e5e5;
    overflow: hidden;
}

.duo-progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(180deg, #7ae020 0%, #58cc02 100%);
    box-shadow: inset 0 -3px 0 rgba(0, 0, 0, 0.12);
    transition: width 0.3s ease;
}

.duo-progress-label {
    font-weight: 900;
    color: var(--duo-green-dark) !important;
    font-size: 0.9rem;
    white-space: nowrap;
}

/* ─── БАЗОВЫЕ КНОПКИ ─────────────────────────────────────────────── */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border-radius: 16px !important;
    border: 0 !important;
    min-height: 3.3rem !important;
    padding: 0.75rem 1.3rem !important;
    white-space: normal !important;
    line-height: 1.2 !important;
    transition: transform 0.07s ease, box-shadow 0.07s ease, filter 0.07s ease !important;
    box-shadow: 0 4px 0 rgba(0, 0, 0, 0.18) !important;
}

/* Основная кнопка — зелёная, как «Продолжить» в Duolingo */
.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"],
.stFormSubmitButton > button {
    background: var(--duo-green) !important;
    color: #fff !important;
    box-shadow: 0 4px 0 var(--duo-green-dark) !important;
}

/* Вторичная — белая с серой рамкой */
.stButton > button[kind="secondary"],
button[data-testid="stBaseButton-secondary"] {
    background: #fff !important;
    color: var(--duo-muted) !important;
    border: 2px solid var(--duo-line) !important;
    box-shadow: 0 4px 0 var(--duo-line) !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    filter: brightness(1.04) !important;
    transform: none !important;
}

.stButton > button[kind="primary"]:active,
button[data-testid="stBaseButton-primary"]:active,
.stFormSubmitButton > button:active {
    transform: translateY(4px) !important;
    box-shadow: 0 0 0 var(--duo-green-dark) !important;
}

.stButton > button[kind="secondary"]:active,
button[data-testid="stBaseButton-secondary"]:active {
    transform: translateY(4px) !important;
    box-shadow: 0 0 0 var(--duo-line) !important;
}

.stButton > button:focus-visible {
    outline: 3px solid #84d8ff !important;
    outline-offset: 2px !important;
}

.stButton > button:disabled {
    background: #e5e5e5 !important;
    color: #afafaf !important;
    border: 0 !important;
    box-shadow: 0 4px 0 #d1d1d1 !important;
    transform: none !important;
    opacity: 1 !important;
    cursor: not-allowed !important;
}

/* ─── ПЛИТКИ ПРЕДМЕТОВ ───────────────────────────────────────────── */
[class*="st-key-subject_"] .stButton > button,
[class*="st-key-subject_"] > button {
    background: var(--duo, #58cc02) !important;
    color: var(--duo-text, #fff) !important;
    border: 0 !important;
    border-radius: 22px !important;
    text-transform: none !important;
    letter-spacing: 0.005em !important;
    font-size: clamp(1.25rem, 2.4vh, 1.65rem) !important;
    font-weight: 900 !important;
    line-height: 1.15 !important;
    min-height: 8.6rem !important;
    padding: 0.9rem 0.6rem !important;
    box-shadow: 0 6px 0 var(--duo-dark, #58a700) !important;
    text-shadow: 0 1px 0 rgba(0, 0, 0, 0.12);
}

[class*="st-key-subject_"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 0 var(--duo-dark, #58a700) !important;
}

[class*="st-key-subject_"] button:active {
    transform: translateY(4px) !important;
    box-shadow: 0 2px 0 var(--duo-dark, #58a700) !important;
}

[class*="st-key-subject_informatics"] button { --duo: #1cb0f6; --duo-dark: #1899d6; }
[class*="st-key-subject_history"] button     { --duo: #ff9600; --duo-dark: #e08600; }
[class*="st-key-subject_geography"] button   { --duo: #58cc02; --duo-dark: #58a700; }
[class*="st-key-subject_biology"] button     { --duo: #00cd9c; --duo-dark: #00a37d; }
[class*="st-key-subject_physics"] button     { --duo: #ce82ff; --duo-dark: #a568cc; }
[class*="st-key-subject_chemistry"] button   { --duo: #ff4b4b; --duo-dark: #ea2b2b; }
[class*="st-key-subject_math"] button        { --duo: #ffc800; --duo-dark: #e6a800; --duo-text: #5a4300; text-shadow: none; }

/* ─── КНОПКИ «ВЫБРАТЬ» И «ИЗУЧИТЬ» ──────────────────────────────── */
[class*="st-key-prof_"] .stButton > button,
[class*="st-key-prof_"] > button,
[class*="st-key-topic_"] .stButton > button,
[class*="st-key-topic_"] > button {
    background: var(--duo-green) !important;
    color: #fff !important;
    border: 0 !important;
    border-radius: 16px !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.08em !important;
    min-height: 3rem !important;
    padding: 0.55rem 0.8rem !important;
    box-shadow: 0 4px 0 var(--duo-green-dark) !important;
}

[class*="st-key-prof_"] .stButton > button:hover,
[class*="st-key-prof_"] > button:hover,
[class*="st-key-topic_"] .stButton > button:hover,
[class*="st-key-topic_"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 0 var(--duo-green-dark) !important;
}

[class*="st-key-prof_"] .stButton > button:active,
[class*="st-key-prof_"] > button:active,
[class*="st-key-topic_"] .stButton > button:active,
[class*="st-key-topic_"] > button:active {
    transform: translateY(3px) !important;
    box-shadow: 0 1px 0 var(--duo-green-dark) !important;
}

/* ─── КАРТОЧКИ ───────────────────────────────────────────────────── */
.duo-card {
    position: relative;
    height: 100%;
    background: #fff;
    border: 2px solid var(--duo-line);
    border-bottom-width: 4px;
    border-radius: 18px;
    padding: 1rem 1.05rem 1.05rem;
    min-height: 9rem;
    color: var(--duo-ink);
    font-size: 0.98rem;
    font-weight: 600;
    line-height: 1.45;
    box-shadow: 0 2px 0 rgba(0, 0, 0, 0.03);
    transition: transform 0.12s ease, border-color 0.12s ease;
}

.duo-card:hover {
    transform: translateY(-2px);
    border-color: #d4d4d4;
}

.duo-card .card-title {
    display: block;
    font-weight: 900;
    font-size: 1.16rem;
    line-height: 1.25;
    color: var(--duo-ink) !important;
    margin-bottom: 0.4rem;
}

.duo-card .card-mission {
    color: var(--duo-muted) !important;
    font-weight: 700;
    font-size: 0.95rem;
}

.duo-card .card-book {
    display: block;
    margin-top: 0.7rem;
    padding-top: 0.6rem;
    border-top: 2px dashed #ededed;
    font-size: 0.8rem;
    font-weight: 700;
    color: #9a9a9a !important;
}

.duo-node {
    display: inline-grid;
    place-items: center;
    width: 2.5rem;
    height: 2.5rem;
    margin-bottom: 0.65rem;
    border-radius: 50%;
    background: var(--duo, var(--duo-green));
    color: #fff !important;
    font-size: 1.05rem;
    font-weight: 900;
    line-height: 1;
    box-shadow: 0 3px 0 var(--duo-dark, var(--duo-green-dark));
}

.duo-node-emoji {
    background: #f4f9ff;
    color: #1cb0f6 !important;
    box-shadow: 0 3px 0 #d7ecfb;
    font-size: 1.3rem;
}

/* ─── КОНСПЕКТ ───────────────────────────────────────────────────── */
.theory-box {
    position: relative;
    background: #fff;
    border: 2px solid var(--duo-line);
    border-radius: 18px;
    padding: 1.55rem 1.35rem 1.15rem;
    margin: 0.9rem 0 1.2rem;
    box-shadow: 0 3px 0 var(--duo-line);
}

.theory-box::before {
    content: "КОНСПЕКТ";
    position: absolute;
    top: -0.85rem;
    left: 1.2rem;
    padding: 0.18rem 0.8rem;
    border-radius: 999px;
    background: var(--duo-green);
    color: #fff;
    font-family: 'Nunito', sans-serif;
    font-size: 0.72rem;
    font-weight: 900;
    letter-spacing: 0.1em;
    box-shadow: 0 2px 0 var(--duo-green-dark);
}

.theory-box p,
.theory-box li {
    font-size: 1.02rem !important;
    line-height: 1.6 !important;
    color: #4b4b4b !important;
    font-weight: 600 !important;
    margin-bottom: 0.55rem !important;
}

.theory-box b,
.theory-box strong {
    color: #2f7d00 !important;
}

.theory-src {
    margin-top: 0.7rem;
    padding-top: 0.6rem;
    border-top: 2px dashed #ededed;
    font-style: normal;
    font-size: 0.88rem;
    font-weight: 700;
    color: #9a9a9a !important;
}

/* ─── ПОДПИСИ ПАНЕЛЕЙ ────────────────────────────────────────────── */
.panel-title {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 0.8rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--duo-muted) !important;
    padding-bottom: 0.5rem;
    margin-bottom: 0.75rem;
    border-bottom: 2px solid var(--duo-line);
}

/* ─── МОНИТОР СИМУЛЯЦИИ ──────────────────────────────────────────── */
[data-testid="stCode"] {
    background: #131f24 !important;
    border: 2px solid #131f24 !important;
    border-radius: 16px !important;
    box-shadow: 0 5px 0 #0b1317 !important;
}

[data-testid="stCode"] pre,
[data-testid="stCode"] pre * {
    color: #b8ff72 !important;
    font-family: 'Cousine', 'Consolas', monospace !important;
    font-size: 1rem !important;
    text-shadow: 0 0 8px rgba(184, 255, 114, 0.35);
}

[data-testid="stCodeActions"],
[data-testid="stCodeActions"] svg {
    color: #9fb3bd !important;
}

/* ─── ПОЛЯ ВВОДА ─────────────────────────────────────────────────── */
[data-testid="stNumberInput"] input {
    background: #fff !important;
    border: 2px solid var(--duo-line) !important;
    border-radius: 12px !important;
    color: var(--duo-ink) !important;
    font-weight: 800 !important;
    font-size: 1.08rem !important;
    padding: 0.5rem 0.7rem !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: var(--duo-blue) !important;
    box-shadow: 0 0 0 2px rgba(28, 176, 246, 0.2) !important;
}

[data-testid="stNumberInput"] label {
    font-weight: 800 !important;
    color: var(--duo-ink) !important;
    font-size: 0.95rem !important;
}

[data-testid="stNumberInput"] button {
    background: #f7f7f7 !important;
    border: 0 !important;
    color: var(--duo-muted) !important;
    box-shadow: none !important;
    min-height: 0 !important;
}

[data-testid="stNumberInput"] button:hover {
    background: #ededed !important;
    color: var(--duo-ink) !important;
}

/* ─── СООБЩЕНИЯ ──────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 16px !important;
    border: 2px solid var(--duo-line) !important;
    padding: 0.85rem 1rem !important;
    font-weight: 800 !important;
    box-shadow: 0 3px 0 rgba(0, 0, 0, 0.05) !important;
}

.stSuccess [data-testid="stAlert"],
div.stSuccess {
    background: #efffe0 !important;
    border-color: #a8e06a !important;
}

.stError [data-testid="stAlert"],
div.stError {
    background: #fff0f0 !important;
    border-color: #ffb3b3 !important;
}

.stSuccess [data-testid="stAlertBody"],
.stSuccess p {
    color: #2f7d00 !important;
}

.stError [data-testid="stAlertBody"],
.stError p {
    color: #c22a2a !important;
}

/* ─── ПОДПИСИ ────────────────────────────────────────────────────── */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: var(--duo-muted) !important;
    font-style: normal !important;
    font-weight: 700 !important;
}

/* ─── XP-ПОЛОСА ПОД ШАПКОЙ ───────────────────────────────────────── */
.duo-xpbar-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: -0.6rem 0 1.2rem;
}

.duo-xpbar {
    flex: 1;
    height: 14px;
    border-radius: 999px;
    background: #eef0f2;
    overflow: hidden;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.08);
}

.duo-xpbar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #58cc02, #ffc800);
    transition: width 0.5s cubic-bezier(0.2, 0.9, 0.3, 1.2);
}

.duo-xpbar-label {
    font-size: 0.82rem;
    font-weight: 800;
    color: var(--duo-muted) !important;
    white-space: nowrap;
}

/* ─── БЕЙДЖИ ПРОГРЕССА НА ПРЕДМЕТАХ ─────────────────────────────── */
[data-testid="stColumn"] {
    position: relative;
}

.duo-tile-progress {
    position: absolute;
    top: -10px;
    right: 4px;
    z-index: 5;
    min-width: 2.6rem;
    height: 2.6rem;
    padding: 0 0.45rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    background: var(--duo-yellow);
    color: #5a4300 !important;
    font-size: 0.75rem;
    font-weight: 900;
    transform: rotate(8deg);
    box-shadow: 0 3px 0 var(--duo-yellow-dark);
    pointer-events: none;
}

.duo-tile-progress.is-done {
    background: var(--duo-green);
    color: #fff !important;
    box-shadow: 0 3px 0 var(--duo-green-dark);
    font-size: 1.05rem;
}

/* ─── ПРОЙДЕННЫЕ КАРТОЧКИ ───────────────────────────────────────── */
.duo-card.done {
    border-color: #b8ef8a;
    background: #fbfff5;
}

.done-badge {
    position: absolute;
    top: -11px;
    right: 10px;
    z-index: 5;
    padding: 0.22rem 0.6rem;
    border-radius: 999px;
    background: var(--duo-yellow);
    color: #5a4300 !important;
    font-size: 0.68rem;
    font-weight: 900;
    transform: rotate(6deg);
    box-shadow: 0 2px 0 var(--duo-yellow-dark);
}

/* ─── ТЕОРИЯ ПО ШАГАМ ───────────────────────────────────────────── */
.duo-theory-emoji {
    font-size: 3.2rem;
    line-height: 1;
    text-align: center;
    margin: 0.2rem 0 0.6rem;
    filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.08));
    animation: duoBob 3.4s ease-in-out infinite;
}

.duo-theory-step-label {
    text-align: center;
    font-size: 0.78rem;
    font-weight: 900;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--duo-green-dark) !important;
    margin-bottom: 0.8rem;
}

.duo-theory-step p {
    font-size: 1.12rem !important;
    line-height: 1.6 !important;
    text-align: center;
    max-width: 620px;
    margin: 0 auto 0.8rem !important;
}

.duo-theory-step .theory-src {
    text-align: center;
}

.duo-dots {
    display: flex;
    gap: 9px;
    justify-content: center;
    margin: 0.2rem 0 1rem;
}

.duo-dots i {
    width: 11px;
    height: 11px;
    border-radius: 50%;
    background: var(--duo-line);
    transition: 0.3s;
}

.duo-dots i.on {
    background: var(--duo-green);
    transform: scale(1.3);
}

/* ─── ЭКРАН ПОБЕДЫ ──────────────────────────────────────────────── */
.duo-win {
    text-align: center;
    background: linear-gradient(150deg, #f4ffe9, #ffffff);
    border: 2px solid #b8ef8a;
    border-bottom-width: 4px;
    border-radius: 18px;
    padding: 1.2rem;
    margin: 0.8rem 0;
    box-shadow: 0 4px 0 #d7f5bb;
}

.duo-stars {
    font-size: 2.2rem;
    letter-spacing: 0.3rem;
}

.duo-win-title {
    font-size: 1.4rem;
    font-weight: 900;
    color: #2f7d00 !important;
    margin: 0.3rem 0;
}

.duo-win-text {
    font-weight: 800;
    color: var(--duo-muted) !important;
}

.duo-game-stats {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 0.7rem;
}

/* ─── КОНФЕТТИ ──────────────────────────────────────────────────── */
.duo-confetti {
    position: relative;
    height: 0;
    overflow: visible;
    pointer-events: none;
    z-index: 20;
}

.duo-confetti span {
    position: absolute;
    top: -10px;
    width: 9px;
    height: 14px;
    border-radius: 2px;
    opacity: 0;
    animation: duoConfetti 1.8s ease-in forwards;
}

@keyframes duoConfetti {
    0% { opacity: 1; transform: translateY(0) rotate(0); }
    100% { opacity: 0; transform: translateY(220px) rotate(540deg); }
}

/* ─── ПРОКРУТКА ──────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb {
    background: var(--duo-green);
    border-radius: 8px;
    border: 2px solid #fff;
}
::-webkit-scrollbar-track { background: #f0f0f0; }

/* ─── МОБИЛЬНАЯ ВЕРСИЯ ───────────────────────────────────────────── */
@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"],
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Колонки на телефоне идут друг под другом */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
    }

    [data-testid="stHorizontalBlock"] > div {
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }

    .duo-topbar { justify-content: center; }
    .duo-logo { font-size: 1.4rem; }
    .duo-banner { padding: 0.9rem 1rem; }
    .duo-banner-title { font-size: 1.1rem; }

    [class*="st-key-subject_"] .stButton > button,
    [class*="st-key-subject_"] > button {
        min-height: 6rem !important;
        font-size: 1.1rem !important;
    }
}
</style>
    """, unsafe_allow_html=True)

# ─── Шапка с живым XP-прогрессом (идея из PROFIPARK) ─────────────────
def render_header():
    xp = st.session_state.xp
    streak = st.session_state.streak
    level = xp // 500 + 1
    in_level = xp % 500
    percent = int(in_level / 500 * 100)
    st.markdown(f"""
<div class="duo-topbar">
    <div class="duo-logo"><span class="duo-owl">🦉</span> AducationMotivation</div>
    <div class="duo-stats">
        <span class="duo-chip duo-chip-gold">🔥 серия {streak}</span>
        <span class="duo-chip duo-chip-green">💎 {xp} XP</span>
    </div>
</div>
<div class="duo-xpbar-row">
    <div class="duo-xpbar"><div class="duo-xpbar-fill" style="width:{percent}%"></div></div>
    <span class="duo-xpbar-label">Уровень {level} · {in_level}/500 XP</span>
</div>
""", unsafe_allow_html=True)


render_header()

# ==============================================================================
# КОНСТРУКТОРЫ ДАННЫХ
# Предмет → профессии → 2 темы (по учебникам РБ) → теория + закрепляющая игра
# fields: (подпись поля, min, max, стартилное значение)
# ok:     проверка (a, b) → bool ; report: (a, b) → строка расчёта для монитора
# ==============================================================================
def topic(name, book, theory, mission, scene, fields, ok, hint, win, fail, report=None, won=None, lost=None):
    """Одна учебная тема: теория из пособия + игра, которая её закрепляет."""
    return {
        "name": name,
        "book": book,
        "theory": theory,
        "game": {
            "mission": mission, "scene": scene, "fields": fields,
            "ok": ok, "hint": hint, "win": win, "fail": fail,
            "report": report, "won": won, "lost": lost,
        },
    }


def profession(icon, title, blurb, topics):
    return {"icon": icon, "title": title, "blurb": blurb, "topics": topics}


def subject(icon, title, professions):
    return {"icon": icon, "title": title, "professions": professions}


DATA = {
    # ═════════════════════════ ИНФОРМАТИКА ═════════════════════════
    "informatics": subject("💻", "Информатика", [
        profession("🕹", "Геймдизайнер", "Собирает анимацию и настраивает плавность игры.", [
            topic("Алгоритм с повторением: игровой цикл",
                  "Інфарматыка, 8 клас (выд. «Адукацыя і выхаванне»), раздзел «Алгарытмы: цыкл»",
                  ["У цыкла ёсць параметр, умова спынення і цела. Кожны кадр экрана — адзін крок цыкла.",
                   "Длительность анимации = число кадров / FPS; ниже 24 FPS глаз видит «дёргание».",
                   "Кейс: прыжок героя тормозит и длится дольше секунды — собери его из нужного числа кадров."],
                  "Миссия: сделай анимацию прыжка плавной и быстрой",
                  "[ДВИЖОК] анимация jump.ninja\n FPS = 12 | кадров = 3\n ⚠ рывки, тайминг 0.25 с → не вписывается",
                  [("FPS (кадров в секунду)", 0, 120, 12), ("Кадров в анимации", 0, 60, 3)],
                  lambda a, b: a >= 24 and b * 1000.0 / max(a, 1) <= 500,
                  "ставь FPS не ниже 24 и сокращай анимацию до 0.5 с (например 15 кадров при 30 FPS)",
                  "🏆 Анимация плавная и успевает в тайминг уровня!",
                  "💥 Анимация дёргается или не влезает в тайминг.",
                  lambda a, b: f"длительность = {b}/{a} = {b / float(max(a, 1)):.2f} с при {a} FPS"),
            topic("Двоичное кодирование: палитра спрайта",
                  "Інфарматыка, 7 клас (выд. «Адукацыя і выхаванне»), раздзел «Кадаванне інфармацыі»",
                  ["Каждый бит удваивает число оттенков: n бит дают 2^n цветов.",
                   "Вес изображения = число пикселей × бит на пиксель / 8 (в байтах).",
                   "Кейс: спрайт героя должен иметь не меньше 256 оттенков и весить до 1 КБ."],
                  "Миссия: кодируй спрайт: 256+ оттенков и файл до 1 КБ",
                  "[ФАЙЛ] sprite.png | 1 бит на пиксель\n оттенков = 2 → ⚠ градиент «ступенями»\n [ЛИМИТ] вес ≤ 1024 байта",
                  [("Бит на пиксель", 1, 16, 1), ("Пикселей в спрайте", 100, 4096, 100)],
                  lambda a, b: 2 ** a >= 256 and b * a <= 8192,
                  "256 оттенков — это 8 бит; при 8 битах спрайт до 1024 пикселей влезет в 1 КБ",
                  "🏆 Палитра богатая, файл лёгкий — спрайт ушёл в сборку!",
                  "💥 Оттенков мало или файл не проходит по весу.",
                  lambda a, b: f"оттенков = 2^{a} = {2 ** a}, вес = {b * a // 8} байт"),
        ]),
        profession("🌐", "Веб-разработчик", "Делает сайт быстрым: вес страницы и кэш.", [
            topic("Измерение информации: вес страницы",
                  "Інфарматыка, 6 клас (выд. «Адукацыя і выхаванне»), раздзел «Вымярэнне інфармацыі»",
                  ["Информацию измеряют в битах и байтах: 1 КБ = 1024 байта; страница — это сумма её файлов.",
                   "Время загрузки ≈ вес × 3 мс/КБ, а кэш позволяет не скачивать часть файлов повторно.",
                   "Кейс: интернет-магазин теряет покупателей — уложи загрузку в 1 секунду."],
                  "Миссия: уложи загрузку страницы в 1 секунду",
                  "[БРАУЗЕР] GET /shop\n вес = 900 КБ | кэш = 0 %\n [ЖДЁМ...] ██████████░░ 3.0 с",
                  [("Вес страницы, КБ", 0, 2000, 900), ("Кэш (повторных визитов), %", 0, 100, 0)],
                  lambda a, b: a >= 100 and a * (1 - b / 100.0) * 3 <= 1000,
                  "уменьши вес до ~300 КБ или подними кэш выше 60 %",
                  "🏆 Страница открывается мгновенно — покупатель оформляет заказ!",
                  "💥 Покупатель закрывает вкладку раньше загрузки.",
                  lambda a, b: f"загрузка ≈ {int(a * (1 - b / 100.0) * 3)} мс (скачиваем {int(a * (1 - b / 100.0))} из {a} КБ)"),
            topic("Ветвящийся алгоритм: условие для меню",
                  "Інфарматыка, 8 клас (выд. «Адукацыя і выхаванне»), раздзел «Разгалужаныя алгарытмы»",
                  ["Ветвление выбирает одну из двух ветвей по условию: если вес ≤ порога — лёгкая версия сайта.",
                   "Порог выбирают не больше норматива 1000 КБ, иначе условие теряет смысл.",
                   "Кейс: настрой вес страницы и порог так, чтобы сработала «лёгкая» ветка."],
                  "Миссия: настрой условие так, чтобы сработала лёгкая ветка",
                  "[КОД] if (вес <= порог): лёгкая версия\n else: полная версия\n вес = 1500 КБ | порог = 100 КБ → полная ветка ⚠",
                  [("Вес страницы, КБ", 0, 2000, 1500), ("Порог в условии, КБ", 0, 2000, 100)],
                  lambda a, b: a <= b <= 1000,
                  "порог должен быть не меньше веса и не больше норматива 1000 КБ (например вес 800, порог 1000)",
                  "🏆 Условие истинно: посетитель получает быструю лёгкую версию!",
                  "💥 Срабатывает тяжёлая ветка, страница грузится долго.",
                  lambda a, b: f"условие «вес <= {b}»: " + ("истинно → лёгкая ветка" if a <= b else "ложно → полная ветка")),
        ]),
        profession("🔐", "Аналитик по кибербезопасности", "Проверяет, сколько займёт взлом пароля.", [
            topic("Защита информации: длина пароля",
                  "Інфарматыка, 11 клас (выд. «Адукацыя і выхаванне»), раздзел «Ахова інфармацыі»",
                  ["Программы-переборщики перебирают миллионы вариантов в секунду, а не «угадывают» пароль.",
                   "Число вариантов растёт экспоненциально: каждый символ умножает их на размер алфавита.",
                   "Кейс: компания требует новый пароль для корпоративной почты."],
                  "Миссия: настрой пароль, который не успеют подобрать",
                  "[БРЮТФОРС] скорость 10^10 вариантов/с\n длина = 6 | классов = 1\n [ЦЕЛЬ] admin",
                  [("Длина пароля, символов", 0, 64, 6), ("Классов символов (1-4)", 1, 4, 1)],
                  lambda a, b: a >= 12 and b >= 3,
                  "нужно минимум 12 символов и 3 разных класса (буквы, цифры, знаки)",
                  "🏆 На такой пароль ушли бы тысячелетия — данные под защитой!",
                  "💥 Пароль вскрыт за секунды.",
                  lambda a, b: f"вариантов ≈ 10^{int(a * b * 0.6)} → перебор ~{10 ** max(0, min(9, a * b // 4))} с"),
            topic("Шифрование: шифр Цезаря",
                  "Інфарматыка, 10 клас (выд. «Адукацыя і выхаванне»), раздзел «Шыфраванне»",
                  ["Шифр подстановки сдвигает символ по кругу алфавита: новый номер = (номер + сдвиг) mod размер алфавита.",
                   "В алфавите 33 буквы, поэтому после 33 сдвиг символ возвращается на своё место.",
                   "Кейс: передай партнёру букву «С» (№20), выбрав верный сдвиг."],
                  "Миссия: зашифруй букву так, чтобы вышла буква №20",
                  "[ШИФР ЦЕЗАРЯ] алфавит = 33\n буква №5, сдвиг 0 → №5 ⚠ ждём №20\n [ПРИЁМ] (н + с) mod 33",
                  [("Номер исходной буквы", 1, 33, 5), ("Сдвиг шифра", 0, 33, 0)],
                  lambda a, b: ((a - 1 + b) % 33) + 1 == 20 and b > 0,
                  "сдвиг = (20 − номер буквы) по модулю 33: для буквы №5 это сдвиг 15",
                  "🏆 Шифровка собрана: письмо читает только адресат!",
                  "💥 Получилась не та буква — сообщение не читается.",
                  lambda a, b: f"буква №{a} + сдвиг {b} = №{((a - 1 + b) % 33) + 1} (ожидался №20)"),
        ]),
    ]),

    # ═════════════════════════ ИСТОРИЯ ═════════════════════════
    "history": subject("🏛", "История", [
        profession("⛏", "Археолог", "Ищет находку в нужном слое земли.", [
            topic("Древнейшее население: стратиграфия",
                  "Гісторыя Беларусі, 5 клас (выд. «Народная асвета»), раздзел «Стужка часу. Першабытнае грамадства»",
                  ["Земля — как страница истории: верхний слой молодой, нижние древнее.",
                   "Чем глубже слой, тем старше находка: слои считают сверху вниз.",
                   "Кейс: копатель перепутал слои — найди эпоху бронзы (3-й слой, 100-180 см)."],
                  "Миссия: подними артефакт эпохи бронзы",
                  "[РАЗРЕЗ] 1 | 2 | 3 | 4 | 5 | 6\n глубина: 0 → 300 см\n [ЗАДАЧА] слой эпохи бронзы",
                  [("Слой (1 — верхний)", 1, 6, 1), ("Глубина находки, см", 0, 300, 20)],
                  lambda a, b: a == 3 and 100 <= b <= 180,
                  "эпоха бронзы — это 3-й слой, глубина 100-180 см",
                  "🏆 Бронзовый кинжал в руках — находка попадёт в музей!",
                  "💥 Пустой грунт или не та эпоха.",
                  lambda a, b: f"слой {a}, глубина {b} см → эпоха: {['нынешняя', 'средневековье', 'бронза', 'неолит', 'палеолит', 'ледниковая'][a - 1]}"),
            topic("Археологические памятники: подсчёт находок",
                  "Гісторыя Беларусі, 5 клас (выд. «Народная асвета»), раздзел «Гарадзішчы і курганы»",
                  ["Городище и курган раскапывают площадями: находки считают на 10 м² раскопа.",
                   "Всего находок ≈ площадь × плотность / 10 — так планируют срок экспедиции.",
                   "Кейс: сезон ограничен, собери партию от 8 до 20 находок."],
                  "Миссия: спланируй раскоп на 8-20 находок",
                  "[ЭКСПЕДИЦИЯ] раскоп 4 м² | 2 находки на 10 м²\n итого ≈ 0.8 → ⚠ сезон пустой\n [ПЛАН] 8-20 находок",
                  [("Площадь раскопа, м²", 1, 100, 4), ("Находок на 10 м²", 1, 50, 2)],
                  lambda a, b: 8 <= a * b / 10.0 <= 20,
                  "например 40 м² и 3 находки на 10 м² даст ровно 12",
                  "🏆 Коллекция собрана: материал на год работы!",
                  "💥 Находок слишком мало или раскоп раздут.",
                  lambda a, b: f"всего ≈ {a * b / 10.0:.1f} находок с {a} м²"),
        ]),
        profession("🖌", "Реставратор", "Держит музейный климат, чтобы документы не рассыпались.", [
            topic("Культура ВКЛ: рукописная книга",
                  "Гісторыя Беларусі, 6 клас (выд. «Народная асвета»), раздзел «Культура Вялікага Княства Літоўскага»",
                  ["Бумага, пергамент и краска живут в своих условиях: жара сушит, сырость рождает плесень.",
                   "Для рукописей держат 16-20 °C и влажность 45-55 %.",
                   "Кейс: в хранилище сломалась вентиляция — настрой приборы, пока летопись не поплыла."],
                  "Миссия: выстави климат для летописи XIII века",
                  "[ХРАНИЛИЩЕ] датчик A: 30 °C | датчик B: 90 %\n ⚠ на пергаменте появилась плесень\n [ПАНЕЛЬ] температура | влажность",
                  [("Температура, °C", 0, 40, 30), ("Влажность, %", 0, 100, 90)],
                  lambda a, b: 16 <= a <= 20 and 45 <= b <= 55,
                  "норма 16-20 °C и 45-55 % влажности",
                  "🏆 Чернила не выцветут, бумага не поплывёт.",
                  "💥 Экспонат продолжает разрушаться.",
                  lambda a, b: f"{a} °C / {b} % → " + ("паспортные условия" if (16 <= a <= 20 and 45 <= b <= 55) else "режим хранения нарушен")),
            topic("Памятники архитектуры: датировка",
                  "Гісторыя Беларусі, 6 клас (выд. «Народная асвета»), раздзел «Сажэнне і дойлідства»",
                  ["Софийский собор в Полоцке заложен в 1030-х — 1060-х годах, это XI век.",
                   "Номер века на единицу больше числа сотен в году: 1044 → 10 + 1 = XI.",
                   "Кейс: подпись к экспозиции перепутала века — восстанови дату."],
                  "Миссия: дай правильную дату Софийского собора",
                  "[МУЗЕЙ] «Софийскі сабор, XII стагоддзе»\n ✗ научный совет недоволен\n [ЗАДАЧА] год | век",
                  [("Год постройки", 1000, 2000, 1000), ("Век", 1, 20, 12)],
                  lambda a, b: 1030 <= a <= 1070 and b == 11,
                  "собор строился в 1030-1060-х годах, век = 10 + 1 = XI",
                  "🏆 Экспозиция исправлена: XI век, Полоцк!",
                  "💥 Датировка не сходится с летописью.",
                  lambda a, b: f"год {a} → век {int(a / 100) + 1}, ты указал {b}"),
        ]),
        profession("🎬", "Исторический консультант", "Следит, чтобы в фильме не перепутали века.", [
            topic("Стужка часу: как из года получить век",
                  "Гісторыя Беларусі, 6 клас (выд. «Народная асвета»), раздзел «Стужка часу»",
                  ["Век — это сотня лет, нумерация начинается с 1 года.",
                   "Век = целая часть от (год / 100) + 1: для 1380 → 13 + 1 = XIV век.",
                   "Кейс: режиссёр ставит Куликовскую битву и хочет написать «XV век»."],
                  "Миссия: поставь верную дату и век битвы",
                  "[ТИТР] «Куликовская битва, XV век»\n ✗ дата спорная\n [ПУЛЬТ] год | век",
                  [("Год события", 1300, 1450, 1400), ("Век", 1, 20, 15)],
                  lambda a, b: 1375 <= a <= 1385 and b == 14,
                  "битва 1380 года, век = 13 + 1 = 14",
                  "🏆 Титр исправлен: 1380 год, XIV век!",
                  "💥 Зрители пишут про путаницу веков.",
                  lambda a, b: f"год {a} → век {int(a / 100) + 1}, ты указал {b}"),
            topic("Хронология войн XV-XVI веков",
                  "Гісторыя Беларусі, 7 клас (выд. «Народная асвета»), раздзел «Войны Вялікага Княства Літоўскага»",
                  ["События на Руси и в ВКЛ датируют парой чисел: начало и конец.",
                   "Длительность = конец − начало; Ливонская война 1558-1583 заняла 25 лет.",
                   "Кейс: в сценарии война «растянулась» на век — поправь хронологию."],
                  "Миссия: задай сроки войны XVI века длительностью 20-30 лет",
                  "[СЦЕНАРИЙ] война 1500–1500 → 0 лет ⚠\n [ЦЕЛЬ] XVI век, 20-30 лет",
                  [("Год начала", 1500, 1600, 1500), ("Год окончания", 1500, 1700, 1500)],
                  lambda a, b: 1500 <= a <= 1599 and 20 <= b - a <= 30,
                  "Ливонская война: 1558-1583 годы",
                  "🏆 Хронология точная: война укладывается в 25 лет!",
                  "💥 Сценарий не сходится с учебником.",
                  lambda a, b: f"{a}–{b}: {b - a} лет"),
        ]),
    ]),

    # ═════════════════════════ ГЕОГРАФИЯ ═════════════════════════
    "geography": subject("🗺", "География", [
        profession("🧭", "Картограф", "Ставит объекты на карту по координатам.", [
            topic("Градусная сетка: широта и долгота",
                  "Геаграфія, 6 клас (выд. «Народная асвета»), раздзел «Глобус. Градусная сетка»",
                  ["Любая точка Земли — это два числа: широта (север-юг) и долгота (запад-восток).",
                   "Широта меняется от 0° на экваторе до 90° на полюсе, долгота — до 180°.",
                   "Кейс: экспедиция прислала точку, но навигатор сбит — найди город (Москва ≈ 56° с.ш., 38° в.д.)."],
                  "Миссия: поставь метку точно на город",
                  "[КАРТА]        N\n   W ───┤   •   │   ?   ├── E\n        └───────┼───────┘\n          метка не на месте",
                  [("Широта (Москва ≈ 56)", -90, 90, 0), ("Долгота (Москва ≈ 38)", -180, 180, 0)],
                  lambda a, b: abs(a - 56) <= 3 and abs(b - 38) <= 4,
                  "цель около 56° с.ш. и 38° в.д.",
                  "🏆 Метка встала ровно на город: легенда готова!",
                  "💥 Метка уехала в океан.",
                  lambda a, b: f"точка ({a}; {b}) → сдвиг до цели ≈ {int(abs(a - 56) * 111 + abs(b - 38) * 60)} км"),
            topic("Масштаб карты",
                  "Геаграфія, 6 клас (выд. «Народная асвета»), раздзел «Маштаб карты»",
                  ["Масштаб говорит, сколько км «спрятано» в одном сантиметре карты.",
                   "Реальное расстояние = расстояние в см × км в 1 см.",
                   "Кейс: измерь маршрут так, чтобы в реальности вышло 50-150 км."],
                  "Миссия: переведи расстояние с карты в реальность",
                  "[ЛИНЕЙКА] на карте 1 см | масштаб 1 см = 1 км\n в реальности 1 км → ⚠ слишком мало\n [ПЛАН] 50-150 км",
                  [("Расстояние на карте, см", 1, 30, 1), ("Сколько км в 1 см", 1, 50, 1)],
                  lambda a, b: 50 <= a * b <= 150,
                  "например 5 см при масштабе 1 см = 20 км даст ровно 100 км",
                  "🏆 Маршрут посчитан: 100 км, туристы в пути!",
                  "💥 Расстояние не сходится с планом.",
                  lambda a, b: f"{a} см × {b} км = {a * b} км в реальности"),
        ]),
        profession("✈️", "Штурман-логист", "Считает время перелёта и запас топлива.", [
            topic("Скорость, время и расстояние",
                  "Геаграфія, 6 клас (выд. «Народная асвета»), раздзел «Скорасць і час»",
                  ["Время = расстояние / скорость, а ветер скорость прибавляет или отнимает.",
                   "7000 км при 850 км/ч — это больше 8 часов, экипажу нужен резерв топлива.",
                   "Кейс: рейс через континент, топливо дорогое — выбери эшелон с попутным ветром."],
                  "Миссия: уложи перелёт в 8 часов и не сжечь всё топливо",
                  "[ПОЛЁТ] 7000 км | V = 850 км/ч\n ветер 0 км/ч | резерв 0 %\n ⚠ стыковка под вопросом",
                  [("Попутный ветер, км/ч", 0, 150, 0), ("Резерв топлива, %", 0, 100, 0)],
                  lambda a, b: 7000.0 / (850 + a) <= 8 and b >= 15,
                  "попутный ветер от ~25 км/ч и резерв минимум 15 %",
                  "🏆 Прибытие по расписанию и с запасом топлива!",
                  "💥 Рейс не укладывается в окно аэропорта.",
                  lambda a, b: f"время = 7000/(850+{a}) = {7000.0 / (850 + a):.1f} ч, резерв {b} %"),
            topic("Часовые пояса",
                  "Геаграфія, 6 клас (выд. «Народная асвета»), раздзел «Часавыя поясы»",
                  ["Земля разделена на 24 пояса, каждый шире на 15° долготы.",
                   "Время в городе = время в данном поясе + номер пояса (с переходом через полночь).",
                   "Кейс: в Лондоне 12:00 — назначь видеосвязь с Минском (2-й пояс)."],
                  "Миссия: переведи лондонский полдень в минский час",
                  "[ЧАСЫ] Лондон 12:00 | пояс 0\n Минск 12:00 → ⚠ созвон сорван\n [ЦЕЛЬ] 14:00 в Минске",
                  [("Час в Лондоне", 0, 23, 12), ("Номер пояса Минска", 0, 23, 0)],
                  lambda a, b: b == 2 and (a + b) % 24 == 14,
                  "Минск во 2-м поясе: 12 + 2 = 14 часов",
                  "🏆 Созвон назначен на 14:00 — разница поясов учтена!",
                  "💥 Собеседник ждёт звонка в другое время.",
                  lambda a, b: f"в Минске {(a + b) % 24}:00 (нужно 14:00)"),
        ]),
        profession("🌪", "Метеоролог аэродрома", "Решает, можно ли садиться в непогоду.", [
            topic("Погода и атмосферные явления",
                  "Геаграфія, 7 клас (выд. «Народная асвета»), раздзел «Атмасфера і надвор’е»",
                  ["У каждого аэродрома есть «минимумы» — худшие условия для посадки.",
                   "Видимость не ниже 800 м, боковой ветер не выше 30 км/ч.",
                   "Кейс: шторм, борт на подходе, топливо тает — реши честно."],
                  "Миссия: разреши посадку или отправь на второй круг",
                  "[ПОГОДА] видимость 100 м | ветер 55 км/ч\n [БОРТ 204] 12 мин топлива\n ДИСПЕТЧЕР: жду решения",
                  [("Видимость, м", 0, 2000, 100), ("Боковой ветер, км/ч", 0, 60, 55)],
                  lambda a, b: a >= 800 and b <= 30,
                  "нужно одновременно: видимость от 800 м и ветер до 30 км/ч",
                  "🏆 Посадка разрешена: минимумы соблюдены!",
                  "💥 Погода ниже минимумов — второй круг.",
                  lambda a, b: f"видимость {a} м (норма ≥ 800), ветер {b} км/ч (норма ≤ 30)"),
            topic("Закономерности температуры по высоте",
                  "Геаграфія, 7 клас (выд. «Народная асвета»), раздзел «Тэмпература паветра»",
                  ["В тропосфере температура падает примерно на 6 °C на каждый километр подъёма.",
                   "t на высоте = t у земли − 6 × высота / 1000.",
                   "Кейс: найди высоту, где воздух 0…+5 °C — границу снежного покрова."],
                  "Миссия: найди высоту снеговой границы",
                  "[ГОРА] высота 0 м | +30 °C у подножия\n ⚠ на вершине всё ещё тепло\n [ЦЕЛЬ] 0…+5 °C",
                  [("Высота, м", 0, 5000, 0), ("Температура у земли, °C", -20, 40, 30)],
                  lambda a, b: 0 <= b - 6.0 * a / 1000 <= 5,
                  "при +30 °C у земли нужна высота около 4200-5000 м",
                  "🏆 Снеговая граница найдена: ледник на месте!",
                  "💥 Расчёт высоты неверный.",
                  lambda a, b: f"на {a} м температура ≈ {b - 6.0 * a / 1000:.1f} °C"),
        ]),
    ]),

    # ═════════════════════════ БИОЛОГИЯ ═════════════════════════
    "biology": subject("🌿", "Биология", [
        profession("🧬", "Генетик", "Предсказывает, сколько детёнышей унаследуют признак.", [
            topic("Законы Менделя: расщепление 3:1",
                  "Біялогія, 10-11 клас (выд. «Адукацыя і выхаванне»), раздзел «Законы Менделя»",
                  ["Скрещивая двух носителей скрытого признака (Aa × Aa), получают расщепление 3:1.",
                   "В F2 из 16 возможных исходов 12 — доминантный признак и 4 — скрытый.",
                   "Кейс: в зоопарке спорят, сколько серых крольчат ждать от пары переносчиков."],
                  "Миссия: собери правильное менделевское расщепление",
                  "[СКРЕЩИВАНИЕ] Aa × Aa\n всего потомков: 8 | серых: 4\n [ОЖИДАНИЕ] 3 : 1",
                  [("Всего потомков F2", 0, 16, 8), ("Из них серых", 0, 16, 4)],
                  lambda a, b: a == 16 and b == 12,
                  "возьми 16 потомков и 12 серых — тогда будет ровно 3:1",
                  "🏆 12 к 4 — чистое расщепление, план разведения принят!",
                  "💥 Соотношение не сходится.",
                  lambda a, b: (f"доля серых = {b}/{a} = {100.0 * b / a:.0f} % (нужно 75 %)" if a else "нет потомков")),
            topic("Генотип и число гамет",
                  "Біялогія, 9 клас (выд. «Адукацыя і выхаванне»), раздзел «Размнажэнне і спадчыннасць»",
                  ["Число типов гамет = 2^n, где n — число гетерозиготных пар генов.",
                   "У одной пары (Aa) — 2 типа гамет, у трёх пар (AaBbCc) — уже 8.",
                   "Кейс: посчитай разнообразие гамет для плана скрещивания."],
                  "Миссия: укажи верное число типов гамет",
                  "[ГЕНОТИП] AaBbCc | 1 пара гетерозигот\n типов гамет: 1 → ⚠ мало\n [ФОРМУЛА] 2^n",
                  [("Пар гетерозиготных генов (n)", 1, 5, 1), ("Указываемое число гамет", 1, 32, 1)],
                  lambda a, b: a >= 2 and b == 2 ** a,
                  "число гамет = 2 в степени n: при n = 3 это 8 типов",
                  "🏆 Разнообразие посчитано верно: таблица скрещивания сложится!",
                  "💥 Число гамет не соответствует генотипу.",
                  lambda a, b: f"2^{a} = {2 ** a} типов гамет, ты указал {b}"),
        ]),
        profession("🌱", "Агроном-ботаник", "Настраивает свет и полив теплицы.", [
            topic("Фотосинтез: свет, вода, углекислый газ",
                  "Біялогія, 7 клас (выд. «Народная асвета»), раздзел «Фотасінтэз»",
                  ["Растение строит органические вещества из света, воды и CO₂ — это фотосинтез.",
                   "Культурам нужно 12-16 часов света и примерно 200-400 мл воды в сутки.",
                   "Кейс: рассада тянется и желтеет — подбери режим."],
                  "Миссия: выстави режим света и полива",
                  "[ТЕПЛИЦА] свет 4 ч | полив 900 мл\n 🌱 листья желтеют\n [ПАНЕЛЬ] досветка | влага",
                  [("Свет, часов в сутки", 0, 24, 4), ("Полив, мл в сутки", 0, 1000, 900)],
                  lambda a, b: 12 <= a <= 16 and 200 <= b <= 400,
                  "ищи середину: 12-16 часов света и 200-400 мл воды",
                  "🏆 Рассада зазеленела: урожай спасён!",
                  "💥 Растения продолжают гибнуть.",
                  lambda a, b: f"свет {a} ч (норма 12-16), вода {b} мл (норма 200-400)"),
            topic("Условия прорастания семян",
                  "Біялогія, 7 клас (выд. «Народная асвета»), раздзел «Насенне. Умовы прарошчвання»",
                  ["Семенам нужны тепло, вода и воздух; без двух факторов проросток не появится.",
                   "Оптимум для большинства культур: 18-25 °C и влажность 60-80 %.",
                   "Кейс: партия семян не взошла — найди причину и выставь условия."],
                  "Миссия: заставь семена прорасти",
                  "[ПРОРАЩИВАНИЕ] 0 °C | влажность 0 %\n всхожесть 0 % → ⚠ партия стоит\n [ЦЕЛЬ] 18-25 °C, 60-80 %",
                  [("Температура, °C", 0, 40, 0), ("Влажность субстрата, %", 0, 100, 0)],
                  lambda a, b: 18 <= a <= 25 and 60 <= b <= 80,
                  "тёплое и влажное: 18-25 °C и 60-80 % влажности",
                  "🏆 Появились дружные всходы — партия в строю!",
                  "💥 Семена остаются спящими.",
                  lambda a, b: f"{a} °C / {b} % → " + ("семена прорастают" if (18 <= a <= 25 and 60 <= b <= 80) else "прорастания нет")),
        ]),
        profession("🩺", "Врач-эпидемиолог", "Останавливает вспышку инфекции.", [
            topic("Инфекционные болезни и путь заражения",
                  "Біялогія, 9 клас (выд. «Народная асвета»), раздзел «Інфекцыйныя хваробы»",
                  ["R — сколько людей заражает один больной; R больше 1 — эпидемия растёт.",
                   "R ≈ контакты в день × доля незащищённых / 5: 10 контактов при 80 % охвата дают R ≈ 0,4.",
                   "Кейс: в городе вспышка — снизь R ниже единицы."],
                  "Миссия: снизь коэффициент распространения ниже 1",
                  "[ШТАБ] охват 20 % | 30 контактов/день\n R ≈ 4.8 → больницы заполняются\n [ЦЕЛЬ] R < 1",
                  [("Охват вакцинацией, %", 0, 100, 20), ("Контактов в день", 0, 40, 30)],
                  lambda a, b: b * (1 - a / 100.0) / 5.0 < 1,
                  "R считается как контакты × (1 − охват/100) / 5: подними охват и урежь контакты",
                  "🏆 Цепочка заражения рвётся, вспышка погашена!",
                  "💥 Число больных удваивается каждую неделю.",
                  lambda a, b: f"R ≈ {b * (1 - a / 100.0) / 5.0:.2f} (нужно меньше 1)"),
            topic("Иммунитет и коллективный барьер",
                  "Біялогія, 8 клас (выд. «Народная асвета»), раздзел «Імунітэт»",
                  ["Прививки формируют иммунитет, а когда привита большинство — болезнь не находит хозяев.",
                   "Порог коллективного иммунитета = (1 − 1/R0) × 100 %; при R0 = 4 это 75 %.",
                   "Кейс: посчитай, сколько людей нужно привить при данном R0."],
                  "Миссия: подними охват прививок выше порога",
                  "[ПОЛИКЛИНИКА] R0 = 4 | привито 20 %\n ⚠ порог 75 % не достигнут\n [ПЛАН] охват ≥ порога",
                  [("R0 (сколько заражает больной)", 1, 10, 4), ("Охват прививками, %", 0, 100, 20)],
                  lambda a, b: a >= 3 and b >= 100.0 * (1 - 1.0 / a),
                  "при R0 = 4 нужно привить не меньше 75 % населения",
                  "🏆 Порог пройден: эпидемии негде разогнаться!",
                  "💥 Охвата не хватает, болезнь находит хозяев.",
                  lambda a, b: f"нужен охват ≥ {100.0 * (1 - 1.0 / a):.0f} %, выставлен {b} %"),
        ]),
    ]),

    # ═════════════════════════ ФИЗИКА ═════════════════════════
    "physics": subject("⚛", "Физика", [
        profession("🚀", "Ракетостроитель", "Выводит ракету на орбиту расчётом тяги.", [
            topic("Второй закон Ньютона: a = F / m",
                  "Фізіка, 9 клас (выд. «Адукацыя і выхаванне», Л.А. Исаченкова і інш.), раздзел «Другі закон Ньютана»",
                  ["Ускорение ракеты — это тяга двигателя, делённая на её массу: a = F/m.",
                   "Для старта нужно ускорение не меньше 25 м/с², но двигатель тяжелее 4000 кН ракета не поднимет.",
                   "Кейс: лёгкая ракета с слабым мотором не отрывается — найди пару «тяга — масса»."],
                  "Миссия: подбери тягу и массу для старта",
                  "[СТАРТ] F = 500 кН | m = 400 т\n a = 1.3 м/с² → ⚠ не отрывается\n [БЮДЖЕТ] тяга ≤ 4000 кН",
                  [("Тяга двигателя, кН", 0, 6000, 500), ("Масса ракеты, т", 10, 500, 400)],
                  lambda a, b: a / float(b) >= 25 and a <= 4000,
                  "уменьши массу и подними тягу, но не больше 4000 кН (например 2000 кН и 60 т)",
                  "🏆 Ракета отрывается от стартового стола!",
                  "💥 Старт не состоялся.",
                  lambda a, b: f"a = F/m = {a / float(b):.1f} м/с² (нужно ≥ 25)"),
            topic("Сила тяжести и вес тела: P = m·g",
                  "Фізіка, 7 клас (выд. «Адукацыя і выхаванне»), раздзел «Сіла цяжару. Вага цела»",
                  ["Вес тела — сила, с которой тело давит на опору: P = m × g.",
                   "На Земле g ≈ 10 Н/кг, поэтому масса 80 кг даёт вес около 800 Н.",
                   "Кейс: подбери массу и планету, чтобы вес попал в 800-1000 Н."],
                  "Миссия: выстави вес аппарата в 800-1000 Н",
                  "[ВЕСЫ] m = 150 кг | g = 10 Н/кг\n P = 1500 Н → шасси на пределе\n [ЦЕЛЬ] 800-1000 Н",
                  [("Масса аппарата, кг", 1, 200, 150), ("Ускорение свободного падения, Н/кг", 1, 26, 10)],
                  lambda a, b: 800 <= a * b <= 1000,
                  "например 80 кг при g = 10 Н/кг (Земля) — ровно 800 Н",
                  "🏆 Вес в допуске: шасси выдержат посадку!",
                  "💥 Аппарат слишком тяжёлый или лёгкий.",
                  lambda a, b: f"P = m·g = {a} × {b} = {a * b} Н"),
        ]),
        profession("🏗", "Инженер-строитель", "Рассчитывает балку перекрытия.", [
            topic("Момент силы и равновесие",
                  "Фізіка, 9 клас (выд. «Адукацыя і выхаванне»), раздзел «Момант сілы. Раўнавага»",
                  ["Момент изгиба балки растёт с нагрузкой и длиной пролёта: M ≈ нагрузка × пролёт / 8.",
                   "Для нашей стали предел 500 кН·м, а пролёт меньше 5 м неудобен для монтажа.",
                   "Кейс: прораб ставит тонкую балку на длинный пролёт — проверь расчёт."],
                  "Миссия: выбери нагрузку и пролёт без разрушения",
                  "[ПЕРЕКРЫТИЕ] нагрузка 900 кН | пролёт 19 м\n M = 2137 кН·м → ⚠ прогиб виден\n [ПРЕДЕЛ] M ≤ 500 кН·м",
                  [("Нагрузка, кН", 0, 1000, 900), ("Пролёт балки, м", 1, 20, 19)],
                  lambda a, b: a >= 200 and a * b / 8.0 <= 500 and b >= 5,
                  "сократи нагрузку или пролёт так, чтобы M было до 500 (например 300 кН и 10 м)",
                  "🏆 Прогиб в допусках: перекрытие принято комиссией!",
                  "💥 Балка не проходит проверку прочности.",
                  lambda a, b: f"M = {a}×{b}/8 = {a * b / 8.0:.0f} кН·м (предел 500)"),
            topic("Давление твёрдых тел",
                  "Фізіка, 8 клас (выд. «Адукацыя і выхаванне»), раздзел «Ціск цвёрдых цел»",
                  ["Давление — сила, делённая на площадь опоры: p = F / S.",
                   "1 кН на 1 м² — это 1 кПа; грунт здания держит 50-150 кПа.",
                   "Кейс: подбери силу и площадь фундамента, чтобы давление было в норме."],
                  "Миссия: выстави давление фундамента 50-150 кПа",
                  "[ФУНДАМЕНТ] F = 200 кН | S = 1 м²\n p = 200 кПа → ⚠ грунт просядет\n [НОРМА] 50-150 кПа",
                  [("Сила давления, кН", 1, 200, 200), ("Площадь опоры, м²", 1, 50, 1)],
                  lambda a, b: 50 <= a / float(b) <= 150,
                  "100 кН на 1 м² — ровно 100 кПа; или расширь площадь опоры",
                  "🏆 Давление в норме: здание простоит век!",
                  "💥 Фундамент продавливает грунт.",
                  lambda a, b: f"p = F/S = {a / float(b):.0f} кПа (норма 50-150)"),
        ]),
        profession("⚡", "Энергетик", "Собирает цепь, чтобы ток не сжёг прибор.", [
            topic("Закон Ома для участка цепи",
                  "Фізіка, 9 клас (выд. «Адукацыя і выхаванне»), раздзел «Закон Ома»",
                  ["Ток в цепи — это напряжение, делённое на сопротивление: I = U / R.",
                   "Прибор живёт при токе 0.5-2 А: меньше — не работает, больше — перегорает.",
                   "Кейс: в щитке 240 В, а резистор забыли поставить — собери цепь."],
                  "Миссия: выстави ток в безопасном диапазоне",
                  "[ЦЕПЬ] U = 240 В | R = 1 Ом\n I = 240 А → 🔥 предохранитель сгорел\n [ПАСПОРТ] 0.5 ≤ I ≤ 2 А",
                  [("Напряжение, В", 0, 240, 240), ("Сопротивление, Ом", 1, 100, 1)],
                  lambda a, b: 0.5 <= a / float(b) <= 2,
                  "нужно, чтобы напряжение делённое на сопротивление дало 0.5-2 А (например 100 В и 50 Ом)",
                  "🏆 Ток штатный: лампа горит ровно, приборы целы!",
                  "💥 Цепь сгорает или не запускается.",
                  lambda a, b: f"I = U/R = {a / float(b):.2f} А (допустимо 0.5-2 А)"),
            topic("Мощность электрического тока",
                  "Фізіка, 9 клас (выд. «Адукацыя і выхаванне»), раздзел «Магутнасць электрычнага току»",
                  ["Мощность — произведение напряжения на силу тока: P = U × I.",
                   "Бытовой прибор нормально работает при 200-500 Вт, больше — выбивает пробки.",
                   "Кейс: подбери режим прибора, чтобы уложиться в 200-500 Вт."],
                  "Миссия: выстави мощность прибора 200-500 Вт",
                  "[ЩИТОК] 220 В × 5 А = 1100 Вт\n ⚠ автомат выбит\n [ПАСПОРТ] 200-500 Вт",
                  [("Напряжение, В", 1, 240, 220), ("Сила тока, А", 1, 10, 5)],
                  lambda a, b: 200 <= a * b <= 500,
                  "220 В при 1 А — это 220 Вт, при 2 А уже 440 Вт",
                  "🏆 Мощность в паспорте: прибор работает часами!",
                  "💥 Пробки выбивает, прибор встаёт.",
                  lambda a, b: f"P = U·I = {a * b} Вт (норма 200-500)"),
        ]),
    ]),

    # ═════════════════════════ ХИМИЯ ═════════════════════════
    "chemistry": subject("🧪", "Химия", [
        profession("💊", "Фармацевт-технолог", "Варит раствор нужной концентрации.", [
            topic("Массовая доля вещества в растворе",
                  "Хімія, 9 клас (выд. «Народная асвета», І.Л. Шымановіч), раздзел «Масавая доля рэчыва»",
                  ["Раствор — вещество, растворённое в воде; важна доля: сколько граммов на весь раствор.",
                   "ω = масса соли / (масса соли + объём воды); для лечебного раствора нужно 8-12 %.",
                   "Кейс: аптека получила заказ — не пересоли, попади в процент."],
                  "Миссия: выстави концентрацию раствора 8-12 %",
                  "[РЕАКТОР] соль 250 г | вода 1000 мл\n ω = 20 % → ⚠ слишком концентрированно\n [ЗАДАНИЕ] 8-12 %",
                  [("Масса соли, г", 0, 500, 250), ("Объём воды, мл", 0, 1000, 1000)],
                  lambda a, b: (a + b) > 0 and 0.08 <= a / float(a + b) <= 0.12,
                  "уменьши соль или добавь воды: 100 г соли и 900 мл воды — ровно 10 %",
                  "🏆 Партия прошла контроль: раствор ровно 10 %!",
                  "💥 Концентрация не соответствует рецептуре.",
                  lambda a, b: (f"ω = {a}/({a}+{b}) = {100.0 * a / (a + b):.1f} %" if (a + b) else "ω = н/д (пусто)")),
            topic("Количество вещества и молярная масса",
                  "Хімія, 8 клас (выд. «Народная асвета», І.Л. Шымановіч), раздзел «Колькасць рэчыва. Моль»",
                  ["Моль — порция частиц, а молярная масса показывает, сколько граммов в одном моле.",
                   "Количество вещества ν = m / M: 36 г воды при M = 18 г/моль — это 2 моль.",
                   "Кейс: отмерь реактив так, чтобы вышло 2-5 моль."],
                  "Миссия: отмерь 2-5 моль реактива",
                  "[ВЕСЫ] вода 100 г | M = 18 г/моль\n ν = 5.6 моль → ⚠ избыток\n [ЦЕЛЬ] 2-5 моль",
                  [("Масса вещества, г", 1, 500, 100), ("Молярная масса, г/моль", 1, 200, 18)],
                  lambda a, b: 2 <= a / float(b) <= 5,
                  "36 г воды при M = 18 г/моль — это ровно 2 моль",
                  "🏆 Навеска верна: синтез пойдёт по уравнению!",
                  "💥 Реактив отмерян неверно, расчёт сорван.",
                  lambda a, b: f"ν = m/M = {a / float(b):.2f} моль (нужно 2-5)"),
        ]),
        profession("🔥", "Технолог-синтезатор", "Добывает аммиак для удобрений.", [
            topic("Обратимые реакции и условия синтеза",
                  "Хімія, 11 клас (выд. «Адукацыя і выхаванне»), раздзел «Зваротныя рэакцыі»",
                  ["Аммиак делают из азота и водорода, но реакция идёт только в жёстких условиях.",
                   "Оптимум: 400-500 °C и 150-350 атмосфер; горячее — газы распадаются обратно.",
                   "Кейс: завод удобрений встал — запусти колонну синтеза в правильном режиме."],
                  "Миссия: выведи синтез аммиака на оптимум",
                  "[КОЛОННА] 700 °C | 1 атм\n выход NH₃ = 2 % → ⚠ реакция стоит\n [ЦЕЛЬ] 400-500 °C, 150-350 атм",
                  [("Температура, °C", 0, 800, 700), ("Давление, атм", 0, 500, 1)],
                  lambda a, b: 400 <= a <= 500 and 150 <= b <= 350,
                  "температура 400-500 °C и давление 150-350 атмосфер",
                  "🏆 Колонна вышла на мощность: аммиак пошёл в цех!",
                  "💥 Реакция не идёт, колонна простаивает.",
                  lambda a, b: f"{a} °C / {b} атм → " + ("выход NH₃ высокий" if (400 <= a <= 500 and 150 <= b <= 350) else "выход NH₃ недостаточный")),
            topic("Скорость химических реакций",
                  "Хімія, 10 клас (выд. «Адукацыя і выхаванне»), раздзел «Хуткасць хімічных рэакцый»",
                  ["Скорость реакции растёт с температурой и концентрацией реагирующих веществ.",
                   "Правило Вант-Гоффа: каждые +10 °C ускоряют реакцию в 2-4 раза.",
                   "Кейс: разогони реакцию до 8-32 условных единиц скорости."],
                  "Миссия: разогони реакцию до 8-32 у.е. скорости",
                  "[ЦЕХ] 20 °C | концентрация 5 у.е.\n v ≈ 0.5 → ⚠ реактор почти стоит\n [ПЛАН] 8-32 у.е.",
                  [("Температура, °C", 20, 80, 20), ("Концентрация, у.е.", 1, 100, 5)],
                  lambda a, b: 8 <= (2 ** ((a - 20) / 10.0)) * b / 10.0 <= 32,
                  "правило Вант-Гоффа: +10 °C → ×2; при 50 °C и концентрации 20 скорость = 16 у.е.",
                  "🏆 Реакция идёт с плановой скоростью: план выполнен!",
                  "💥 Реактор стоит или разгоняется слишком бурно.",
                  lambda a, b: f"v ≈ 2^{(a - 20) // 10} × {b}/10 = {(2 ** ((a - 20) / 10.0)) * b / 10.0:.1f} у.е."),
        ]),
        profession("🧫", "Судебный химик", "Нейтрализует опасную пробу с места происшествия.", [
            topic("Реакция нейтрализации",
                  "Хімія, 9 клас (выд. «Народная асвета», І.Л. Шымановіч), раздзел «Рэакцыя нейтралізацыі»",
                  ["Кислота и щёлочь гасят друг друга: на выходе — вода и соль.",
                   "Объёмы должны совпасть (±5 мл), иначе проба останется едкой; больше 150 мл брать опасно.",
                   "Кейс: в лаборатории разлили кислоту — сделай пробу безопасной для вывоза."],
                  "Миссия: приведи пробу к нейтральной реакции",
                  "[ПРОБА №7] кислота 200 мл | щёлочь 0 мл\n pH = 1 → ⚠ едкая, к вывозу не годится\n [ЦЕЛЬ] pH ≈ 7",
                  [("Кислота, мл", 0, 200, 200), ("Щёлочь, мл", 0, 200, 0)],
                  lambda a, b: abs(a - b) <= 5 and 20 <= max(a, b) <= 150,
                  "объёмы кислоты и щёлочи должны совпадать (±5 мл) и быть в пределах 20-150 мл",
                  "🏆 Проба нейтрализована: улика доедет до экспертизы!",
                  "💥 Реакция ещё едкая или объём опасен.",
                  lambda a, b: f"избыток {abs(a - b)} мл, объём пробы {max(a, b)} мл"),
            topic("Индикаторы и среда раствора",
                  "Хімія, 8 клас (выд. «Народная асвета», І.Л. Шымановіч), раздзел «Індыкатары»",
                  ["Индикатор меняет цвет в кислой или щелочной среде: лакмус краснеет в кислоте.",
                   "Чтобы смена цвета было видно, берут 2-5 капель индикатора на 10-30 мл пробы.",
                   "Кейс: покажи пробирку для фотофиксации — подбери капли и объём."],
                  "Миссия: сделай смену цвета видимой",
                  "[ПРОБИРКА] 50 мл пробы | 0 капель лакмуса\n цвет не изменился → ⚠ нет фото\n [ЦЕЛЬ] 2-5 капель на 10-30 мл",
                  [("Капель индикатора", 0, 20, 0), ("Объём пробы, мл", 0, 100, 50)],
                  lambda a, b: 2 <= a <= 5 and 10 <= b <= 30,
                  "2-5 капель индикатора на 10-30 мл раствора",
                  "🏆 Окраска проявилась: протокол с фото готов!",
                  "💥 Пробирка не показывает ничего.",
                  lambda a, b: f"{a} капель на {b} мл пробы"),
        ]),
    ]),

    # ═════════════════════════ МАТЕМАТИКА ═════════════════════════
    "math": subject("📐", "Математика", [
        profession("🎮", "Геймдизайнер", "Создаёт физику прыжков и траектории в 3D-мирах.", [
            topic("Каардынатная плоскость: оси X и Y",
                  "Матэматыка, 6 клас (выд. «Народная асвета»), раздзел «Каардынатная плоскасць»",
                  ["Чтобы заспавнить персонажа, компьютеру нужны точные координаты: горизонталь — ось X, вертикаль — ось Y.",
                   "Весь мир игры состоит из невидимой сетки координат: прыжок — изменение Y, бег — изменение X.",
                   "Кейс: сломался код прыжка ниндзя — он не перелетает яму с лавой. Почини его!"],
                  "Миссия: настрой прыжок персонажа",
                  "[Y]\n 5 |       \n 4 |       \n 3 |       \n 2 |       \n 1 |       \n 0 |  🥷  [ ЛАВА ]  👑\n   -------------------\n      2    4  5  6   8   [X]",
                  [("Пик прыжка по оси X (центр ямы)", 0, 10, 0), ("Высота прыжка по оси Y", 0, 10, 0)],
                  lambda a, b: b >= 3 and 4 <= a <= 6,
                  "сделай высоту Y не меньше 3, а пик X поставь в 5 — центр ямы",
                  "🏆 Баг исправлен! Ниндзя перелетел лаву и забрал корону!",
                  "💥 Ошибка! Ниндзя упал в лаву.",
                  won="[Y]\n 4 |          🥷 \n 3 |         /  \\n 2 |        /    \\n 1 |       /      \\n 0 |      [ ЛАВА ]  🥷👑\n   -------------------\n      2    4  5  6   8   [X]",
                  lost="[Y]\n 4 |       \n 3 |       \n 2 |       \n 1 |         💥 \n 0 |    [ 🥷 ЛАВА ]  👑\n   -------------------\n      2    4  {a}  6   8   [X]"),
            topic("Масштаб и подобие: размер спрайта",
                  "Матэматыка, 8 клас (выд. «Народная асвета»), раздзел «Падобныя трохвугольнікі. Маштаб»",
                  ["Увеличение изображения — умножение всех размеров на один коэффициент (масштаб).",
                   "Итоговый размер = исходный × масштаб; для HD-игры нужен спрайт 64-256 px.",
                   "Кейс: исходный спрайт 8 px — подбери масштаб, не раздув файл."],
                  "Миссия: разгони спрайт до 64-256 пикселей",
                  "[ГРАФИКА] исходник 8 px | масштаб 1\n на экране 8 px → ⚠ крошечный спрайт\n [ЦЕЛЬ] 64-256 px",
                  [("Масштаб (увеличение)", 1, 20, 1), ("Исходный размер, px", 8, 512, 8)],
                  lambda a, b: 64 <= a * b <= 256,
                  "например 32 px при масштабе 4 даст 128 px",
                  "🏆 Спрайт чёткий и в нужном размере!",
                  "💥 Спрайт слишком мелкий или залит на весь экран.",
                  lambda a, b: f"{b} px × {a} = {a * b} px на экране"),
        ]),
        profession("📊", "Финансовый аналитик", "Просчитывает доходы технокомпаний и стартапов.", [
            topic("Працэнты: прибыль и рентабельность",
                  "Матэматыка, 6 клас (выд. «Народная асвета»), раздзел «Адсоткі»",
                  ["Прибыль — разница между доходом и расходом: прибыль = доход − расход.",
                   "Рентабельность = прибыль / расход × 100 %; инвестор смотрит и на абсолют, и на процент.",
                   "Кейс: стартап просит вложения — покажи модель с прибылью от 1500 тыс. ₽."],
                  "Миссия: собери финансовую модель стартапа",
                  "[ОТЧЁТ] доход 3000 | расход 2800\n прибыль = 200 тыс. ₽ → ⚠ инвестор откажет\n [ЦЕЛЬ] ≥ 1500 и доход ≥ 1.5 × расход",
                  [("Доход в месяц, тыс. ₽", 0, 10000, 3000), ("Расход в месяц, тыс. ₽", 0, 10000, 2800)],
                  lambda a, b: (a - b) >= 1500 and a >= 1.5 * b,
                  "подними доход и урежь расход: например 6000 и 3000 тыс. ₽",
                  "🏆 Модель сходится: стартап получает раунд инвестиций!",
                  "💥 Инвестор закрыл презентацию.",
                  lambda a, b: f"прибыль = {a - b} тыс. ₽, покрытие расхода = " + (f"{a / float(b):.2f}×" if b else "н/д")),
            topic("Лінейнае ўраўненне: точка безубыточности",
                  "Алгебра, 7 клас (выд. «Адукацыя і выхаванне»), раздзел «Лінейнае ўраўненне з адной зменнай»",
                  ["Прибыль с партии — это (цена − себестоимость) × число изделий.",
                   "Чтобы окупить цех, нужна наценка 20-60 ₽ на изделие при плане 1000 штук.",
                   "Кейс: реши уравнение наценки и подбери цену с себестоимостью."],
                  "Миссия: задай наценку 20-60 ₽ на изделие",
                  "[ПЛАН] цена 200 ₽ | себестоимость 200 ₽\n наценка 0 ₽ → ⚠ работа в убыток\n [ЦЕЛЬ] наценка 20-60 ₽",
                  [("Цена за штуку, ₽", 10, 200, 200), ("Себестоимость за штуку, ₽", 10, 200, 200)],
                  lambda a, b: 20 <= a - b <= 60,
                  "например цена 90 ₽ при себестоимости 50 ₽ — наценка 40 ₽",
                  "🏆 План окупается: партия идёт в плюс!",
                  "💥 Наценка нулевая или грабительская.",
                  lambda a, b: f"прибыль с 1000 шт. = {(a - b) * 1000} ₽"),
        ]),
        profession("🏛", "Архитектор-проектировщик", "Рисует удобные лестницы и пропорции зданий.", [
            topic("Прапорцыі: формула удобной лестницы",
                  "Матэматыка, 7 клас (выд. «Народная асвета»), раздзел «Прапорцыя»",
                  ["Ступень — это высота h и глубина d, из них складывается шаг человека.",
                   "Удобная лестница: 2h + d = 60-66 см при высоте ступени 15-18 см.",
                   "Кейс: прораб построил крутую лестницу, по ней не поднять мебель."],
                  "Миссия: спроектируй удобную лестницу",
                  "[ЧЕРТЕЖ] h = 28 см | d = 20 см\n 2h + d = 76 → ⚠ идти тяжело\n [НОРМА] 60 ≤ 2h + d ≤ 66",
                  [("Высота ступени, см", 5, 30, 28), ("Глубина ступени, см", 20, 50, 20)],
                  lambda a, b: 15 <= a <= 18 and 60 <= 2 * a + b <= 66,
                  "поставь h в диапазон 15-18 и подбери d так, чтобы 2h + d было 60-66 см",
                  "🏆 Шаг ложится ровно, мебель пройдёт!",
                  "💥 Лестницей невозможно пользоваться.",
                  lambda a, b: f"2h + d = {2 * a + b} см (норма 60-66), высота h = {a} см"),
            topic("Тэарэма Піфагора: уклон марша",
                  "Геаметрыя, 8 клас (выд. «Народная асвета»), раздзел «Тэарэма Піфагора»",
                  ["Марш лестницы — гипотенуза прямоугольного треугольника: c = √(a² + b²).",
                   "Нормы: длина марша до 450 см, уклон (высота / проекция) не круче 0.8.",
                   "Кейс: посчитай марш так, чтобы он влез в лестничную клетку."],
                  "Миссия: построй марш по теореме Пифагора",
                  "[ГЕОМЕТРИЯ] высота 300 см | проекция 100 см\n уклон 3.0 → ⚠ это стремянка\n [НОРМА] c ≤ 450 см, уклон ≤ 0.8",
                  [("Высота марша, см", 200, 350, 300), ("Горизонтальная проекция, см", 100, 600, 100)],
                  lambda a, b: (a ** 2 + b ** 2) ** 0.5 <= 450 and a / float(b) <= 0.8,
                  "например высота 240 см и проекция 360 см: марш ≈ 433 см, уклон 0.67",
                  "🏆 Марш в нормах: подниматься безопасно!",
                  "💥 Лестница не влезает в клетку или слишком крутая.",
                  lambda a, b: f"марш = √({a}²+{b}²) = {(a ** 2 + b ** 2) ** 0.5:.0f} см, уклон {a / float(b):.2f}"),
        ]),
    ]),
}

# Порядок предметов на первом экране
ORDER = ["informatics", "history", "geography", "biology", "physics", "chemistry", "math"]

# ─── Память для переключения экранов сайта ───
if 'screen' not in st.session_state:
    st.session_state.screen = "subjects"

if 'subject' not in st.session_state:
    st.session_state.subject = None

if 'profession' not in st.session_state:
    st.session_state.profession = 0

if 'lesson' not in st.session_state:
    st.session_state.lesson = 0


def set_screen(screen_name):
    st.session_state.screen = screen_name


def current_subject():
    return DATA[st.session_state.subject]


def current_profession():
    return current_subject()["professions"][st.session_state.profession]


def current_lesson():
    return current_profession()["topics"][st.session_state.lesson]


def theory_html(lines, source=None):
    """Конспект темы: белая карточка в стиле Duolingo + ссылка на пособие."""
    html = "<div class='theory-box'>" + "".join(f"<p>{line}</p>" for line in lines)
    if source:
        html += f"<div class='theory-src'>📖 {source}</div>"
    return html + "</div>"


def progress_html(step, total=4):
    """Полоса прогресса урока, как в Duolingo."""
    percent = int(round(100 * step / total))
    return (
        "<div class='duo-progress'>"
        f"<div class='duo-progress-track'><div class='duo-progress-fill' style='width:{percent}%'></div></div>"
        f"<div class='duo-progress-label'>{step} / {total}</div>"
        "</div>"
    )


# ─── Прогресс: какие темы уже пройдены ──────────────────────────────
def topic_key(subject_key=None, profession_index=None, lesson_index=None):
    subject_key = st.session_state.subject if subject_key is None else subject_key
    profession_index = st.session_state.profession if profession_index is None else profession_index
    lesson_index = st.session_state.lesson if lesson_index is None else lesson_index
    return f"{subject_key}|{profession_index}|{lesson_index}"


def topic_done(subject_key=None, profession_index=None, lesson_index=None):
    return topic_key(subject_key, profession_index, lesson_index) in st.session_state.completed


def mark_topic_done(subject_key=None, profession_index=None, lesson_index=None):
    st.session_state.completed.add(topic_key(subject_key, profession_index, lesson_index))


def subject_stats(key):
    """Сколько тем предмета пройдено из всех."""
    item = DATA[key]
    total = sum(len(prof["topics"]) for prof in item["professions"])
    done = sum(
        1
        for pi, prof in enumerate(item["professions"])
        for li in range(len(prof["topics"]))
        if topic_done(key, pi, li)
    )
    return done, total


def profession_stats(index):
    prof = current_subject()["professions"][index]
    total = len(prof["topics"])
    done = sum(1 for li in range(total) if topic_done(st.session_state.subject, index, li))
    return done, total


# ─── Теория по шагам ────────────────────────────────────────────────
def theory_next():
    total = len(current_lesson()["theory"])
    st.session_state.theory_step = min(total - 1, st.session_state.theory_step + 1)


def theory_prev():
    st.session_state.theory_step = max(0, st.session_state.theory_step - 1)


def confetti_html():
    """Лёгкое CSS-конфетти в духе PROFIPARK."""
    colors = ["#58cc02", "#ffc800", "#1cb0f6", "#ce82ff", "#ff4b4b", "#00cd9c"]
    pieces = []
    for i in range(28):
        left = (i * 3.7) % 100
        delay = (i % 14) * 0.07
        color = colors[i % len(colors)]
        pieces.append(
            f"<span style='left:{left:.1f}%;background:{color};animation-delay:{delay:.2f}s'></span>"
        )
    return "<div class='duo-confetti'>" + "".join(pieces) + "</div>"



def default_board(game, values, won):
    """Экран монитора, если у темы нет своей ASCII-сцены результата."""
    lines = [
        "[ВВОД] " + game["fields"][0][0] + " = " + str(values[0]),
        "[ВВОД] " + game["fields"][1][0] + " = " + str(values[1]),
    ]
    if game.get("report"):
        lines.append("[РАСЧЁТ] " + game["report"](values[0], values[1]))
    lines += ["", "РЕЗУЛЬТАТ: OK ✅" if won else "РЕЗУЛЬТАТ: ОШИБКА 💥"]
    return "\n".join(lines)


def board_text(game, values, won):
    """Своя сцена результата (won/lost) либо универсальный отчёт."""
    template = game.get("won" if won else "lost")
    if template is None:
        return default_board(game, values, won)
    return template.format(a=values[0], b=values[1])


# ─── Переходы между экранами ───────────────────────────────────────────────
# Колбэки on_click выполняются ДО перерисовки страницы, поэтому одно нажатие
# кнопки сразу открывает следующий экран — второй клик не нужен.
def open_subject(key):
    st.session_state.subject = key
    st.session_state.profession = 0
    st.session_state.lesson = 0
    set_screen("professions")


def open_profession(index):
    st.session_state.profession = index
    st.session_state.lesson = 0
    set_screen("topics")


def open_topic(index):
    st.session_state.lesson = index
    st.session_state.theory_step = 0
    set_screen("theory")



# ==============================================================================
# ЭКРАН 1: ВЫБОР ПРЕДМЕТА (весь на одном экране, без прокрутки)
# ==============================================================================
if st.session_state.screen == "subjects":
    st.markdown("""
<div class="duo-banner">
    <div>
        <div class="duo-banner-title">Привет! Готов учиться? 🦉</div>
        <div class="duo-banner-text">Выбери предмет — и иди к новым знаниям шаг за шагом.</div>
    </div>
    <div class="duo-banner-emoji">💚</div>
</div>
""", unsafe_allow_html=True)
    st.subheader("Выбери школьный предмет для практики:")

    for start, size in ((0, 4), (4, 3)):
        cols = st.columns(size, gap="small")
        for col, key in zip(cols, ORDER[start:start + size]):
            item = DATA[key]
            with col:
                st.button(f"{item['icon']} {item['title']}", key=f"subject_{key}", use_container_width=True,
                          on_click=open_subject, args=(key,))
                done, total = subject_stats(key)
                if done:
                    done_cls = " is-done" if done == total else ""
                    done_label = "✓" if done == total else f"{int(done / total * 100)}%"
                    st.markdown(
                        f"<div class='duo-tile-progress{done_cls}'>{done_label}</div>",
                        unsafe_allow_html=True,
                    )


# ==============================================================================
# ЭКРАН 2: ВЫБОР ПРОФЕССИИ
# ==============================================================================
elif st.session_state.screen == "professions":
    item = current_subject()
    st.markdown(progress_html(1), unsafe_allow_html=True)
    st.subheader(f"Где нужна {item['title'].lower()}? Выбери профессию мечты:")
    subj_done, subj_total = subject_stats(st.session_state.subject)
    st.caption(f"📚 Пройдено тем по предмету: {subj_done} из {subj_total}")

    cols = st.columns(len(item["professions"]), gap="medium")
    for index, (col, prof) in enumerate(zip(cols, item["professions"])):
        with col:
            prof_done, prof_total = profession_stats(index)
            prof_label = "✓ все темы" if prof_done == prof_total else f"{prof_done}/{prof_total} тем"
            st.markdown(
                f"<div class='duo-card'><div class='duo-node duo-node-emoji'>{prof['icon']}</div>"
                f"<span class='card-title'>{prof['title']}</span>"
                f"{prof['blurb']}"
                f"<span class='card-book'>📚 {prof_label}</span></div>",
                unsafe_allow_html=True,
            )
            st.button("Выбрать", key=f"prof_{st.session_state.subject}_{index}", use_container_width=True,
                      on_click=open_profession, args=(index,))


    st.button("⬅ Назад к предметам", on_click=set_screen, args=("subjects",))


# ==============================================================================
# ЭКРАН 3: ВЫБОР ТЕМЫ (2 темы по учебному пособию)
# ==============================================================================
elif st.session_state.screen == "topics":
    prof = current_profession()
    st.markdown(progress_html(2), unsafe_allow_html=True)
    st.subheader(f"{prof['icon']} {prof['title']}: какие темы нужно изучить?")

    cols = st.columns(len(prof["topics"]), gap="medium")
    for index, (col, lesson) in enumerate(zip(cols, prof["topics"])):
        node_style = "--duo:#1cb0f6;--duo-dark:#1899d6" if index % 2 == 0 else "--duo:#ce82ff;--duo-dark:#a568cc"
        done = topic_done(st.session_state.subject, st.session_state.profession, index)
        done_cls = " done" if done else ""
        done_badge = "<span class='done-badge'>✓ пройдено</span>" if done else ""
        with col:
            st.markdown(
                f"<div class='duo-card{done_cls}'>{done_badge}<div class='duo-node' style='{node_style}'>{index + 1}</div>"
                f"<span class='card-title'>{lesson['name']}</span>"
                f"<div class='card-mission'>{lesson['game']['mission']}</div>"
                f"<span class='card-book'>📖 {lesson['book']}</span></div>",
                unsafe_allow_html=True,
            )
            st.button("Повторить" if done else "Изучить",
                      key=f"topic_{st.session_state.subject}_{st.session_state.profession}_{index}",
                      use_container_width=True, on_click=open_topic, args=(index,))


    st.button("⬅ Назад к профессиям", on_click=set_screen, args=("professions",))


# ==============================================================================
# ЭКРАН 4: ТЕОРИЯ ТЕМЫ (из учебного пособия)
# ==============================================================================
elif st.session_state.screen == "theory":
    lesson = current_lesson()
    lines = lesson["theory"]
    total = len(lines)
    step = max(0, min(st.session_state.theory_step, total - 1))
    st.markdown(progress_html(3), unsafe_allow_html=True)
    st.subheader(f"📖 {lesson['name']}")

    dots = "".join(f"<i class=\"{'on' if i <= step else ''}\"></i>" for i in range(total))
    st.markdown(f"<div class='duo-dots'>{dots}</div>", unsafe_allow_html=True)

    emoji = ["💡", "📌", "🧩", "🎯"][step % 4]
    st.markdown(
        f"<div class='theory-box duo-theory-step'>"
        f"<div class='duo-theory-emoji'>{emoji}</div>"
        f"<div class='duo-theory-step-label'>Шаг {step + 1} из {total}</div>"
        f"<p>{lines[step]}</p>"
        f"<div class='theory-src'>📖 {lesson['book']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    col_prev, col_next = st.columns(2, gap="medium")
    with col_prev:
        if step > 0:
            st.button("← Назад", on_click=theory_prev, use_container_width=True)
        else:
            st.button("⬅ К темам", on_click=set_screen, args=("topics",), use_container_width=True)
    with col_next:
        if step < total - 1:
            st.button("Дальше →", type="primary", on_click=theory_next, use_container_width=True)
        else:
            st.button("🎮 К игре", type="primary", on_click=set_screen, args=("game",), use_container_width=True)


# ==============================================================================
# ЭКРАН 5: ИГРА, ЗАКРЕПЛЯЮЩАЯ ТЕМУ
# ==============================================================================
elif st.session_state.screen == "game":
    lesson = current_lesson()
    game = lesson["game"]
    st.markdown(progress_html(4), unsafe_allow_html=True)
    st.subheader(game["mission"])
    st.markdown(
        f"<div class='duo-game-stats'>"
        f"<span class='duo-chip duo-chip-gold'>🔥 серия: {st.session_state.streak}</span>"
        f"<span class='duo-chip'>🎯 За победу: +30 XP</span>"
        f"<span class='duo-chip duo-chip-green'>💎 Всего: {st.session_state.xp} XP</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown("<div class='panel-title'>🎮 Панель кода (ввод данных)</div>", unsafe_allow_html=True)
        values = []
        for index, (label, lo, hi, default) in enumerate(game["fields"]):
            values.append(st.number_input(
                label, min_value=lo, max_value=hi, value=default,
                key=f"inp_{st.session_state.subject}_{st.session_state.profession}_{st.session_state.lesson}_{index}",
            ))
        run_code = st.button("▶ Запустить симуляцию кода", type="primary", use_container_width=True)

    with col2:
        st.markdown("<div class='panel-title'>📺 Монитор симуляции</div>", unsafe_allow_html=True)
        plot_placeholder = st.empty()
        plot_placeholder.code(game.get("scene", "Ожидание запуска симуляции..."))

        if run_code:
            with st.spinner("Компиляция и симуляция..."):
                time.sleep(0.6)
            won = bool(game["ok"](values[0], values[1]))
            plot_placeholder.code(board_text(game, values, won))
            if won:
                first_time = not topic_done()
                mark_topic_done()
                xp_gain = 30 if first_time else 5
                st.session_state.xp += xp_gain
                st.session_state.streak += 1
                st.markdown(confetti_html(), unsafe_allow_html=True)
                st.markdown(
                    f"<div class='duo-win'>"
                    f"<div class='duo-stars'>⭐⭐⭐</div>"
                    f"<div class='duo-win-title'>Тема пройдена!</div>"
                    f"<div class='duo-win-text'>+{xp_gain} XP · серия {st.session_state.streak} 🔥</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                st.success(game["win"])
            else:
                st.session_state.streak = 0
                st.error(f"{game['fail']} Подсказка: {game['hint']}.")

    st.button("⬅ К темам профессии", on_click=set_screen, args=("topics",))


