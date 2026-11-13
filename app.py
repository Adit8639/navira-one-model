import time

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Navira One · Repair Console", layout="wide",
                   initial_sidebar_state="collapsed")

TEAL = "#1C9AA3"
BLUE = "#5E8FC4"
NAVY = "#0F2B46"
PALE = "#E9F5F6"
GOLD = "#C9A227"
RED = "#D64545"
AMBER = "#E3A008"
GREEN = "#2E9E5B"
GREY = "#C9CFD6"
INK = "#0F2B46"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
header[data-testid="stHeader"], #MainMenu, footer {display:none !important;}
.stApp {background:#F3F6F9;}
.block-container {padding-top:1.1rem; padding-bottom:2rem; max-width:1400px;}
.stApp, .stApp p, .stApp li, .stApp label {font-family:'Inter',sans-serif; color:#0F2B46;}
h1,h2,h3,h4 {font-family:'Montserrat',sans-serif !important; color:#0F2B46 !important;}

.topbar {background:linear-gradient(100deg,#0F2B46 0%,#14476A 55%,#1C9AA3 100%); border-radius:18px;
  padding:18px 26px; display:flex; align-items:center; justify-content:space-between; margin-bottom:14px;
  box-shadow:0 8px 24px rgba(15,43,70,.18);}
.brand {font-family:'Montserrat'; font-weight:800; font-size:1.7rem; color:#fff; letter-spacing:1px;}
.brand span {color:#C9A227;}
.brand small {display:block; font-weight:500; font-size:.82rem; letter-spacing:.4px; color:#CFE6EA; margin-top:2px;}
.live {font-family:'Montserrat'; font-weight:700; font-size:.78rem; color:#fff; background:rgba(255,255,255,.14);
  padding:7px 14px; border-radius:30px; letter-spacing:1px;}
.live b {color:#7CF0A9;}

[data-testid="stTab"] {height:44px; border-radius:10px; padding:0 22px !important; margin-right:6px; background:#fff;
  box-shadow:0 2px 8px rgba(15,43,70,.06);}
[data-testid="stTab"] p {font-family:'Montserrat' !important; font-weight:700; font-size:.95rem; color:#5B6B7C !important;}
[data-testid="stTab"][aria-selected="true"] {background:#0F2B46 !important;}
[data-testid="stTab"][aria-selected="true"] p {color:#fff !important;}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {display:none !important;}
[class*="st-key-card"] {background:#fff; border:none !important; padding:16px 18px; border-radius:16px;
  box-shadow:0 3px 14px rgba(15,43,70,.07);}

.kpi {background:#fff; border-radius:16px; padding:14px 18px; box-shadow:0 3px 14px rgba(15,43,70,.07);
  border-top:4px solid #1C9AA3; height:100%;}
.kpi .l {font-size:.78rem; font-weight:600; color:#5B6B7C; text-transform:uppercase; letter-spacing:.6px;}
.kpi .v {font-family:'Montserrat'; font-weight:800; font-size:1.9rem; color:#0F2B46; line-height:1.15;}
.kpi .s {font-size:.82rem; color:#5B6B7C;}

.who {background:#fff; border-radius:16px; padding:12px 14px; border:2px solid transparent;
  box-shadow:0 3px 14px rgba(15,43,70,.07); display:flex; gap:12px; align-items:center; min-height:84px;}
.who.on {border-color:#1C9AA3; background:#F4FBFB;}
.av {width:46px; height:46px; border-radius:50%; display:flex; align-items:center; justify-content:center;
  font-family:'Montserrat'; font-weight:800; color:#fff; font-size:1rem; flex-shrink:0;}
.who .n {font-family:'Montserrat'; font-weight:700; font-size:.98rem;}
.who .t {font-size:.8rem; color:#5B6B7C; line-height:1.3;}

.lane {background:#fff; border-radius:18px; padding:18px 20px 14px; box-shadow:0 3px 14px rgba(15,43,70,.07); height:100%;}
.lane h4 {margin:0 0 2px 0; font-size:1.05rem;}
.pill {display:inline-block; font-family:'Montserrat'; font-weight:700; font-size:.72rem; letter-spacing:.8px;
  padding:4px 10px; border-radius:20px; color:#fff;}
.node {display:flex; gap:12px; position:relative; padding-bottom:12px;}
.node:not(:last-child)::after {content:""; position:absolute; left:13px; top:28px; bottom:0; width:2px; background:#DCE3EA;}
.dot {width:28px; height:28px; border-radius:50%; flex-shrink:0; display:flex; align-items:center; justify-content:center;
  color:#fff; font-weight:800; font-size:.8rem; z-index:1;}
.node .a {font-weight:700; font-size:.92rem;}
.node .b {font-size:.82rem; color:#5B6B7C;}
.res {border-radius:14px; padding:12px 14px; margin-top:4px;}
.res .big {font-family:'Montserrat'; font-weight:800; font-size:1.35rem;}
.mini {display:flex; gap:10px; margin-top:10px;}
.mini div {flex:1; background:#F3F6F9; border-radius:12px; padding:8px 10px;}
.mini .k {font-size:.72rem; color:#5B6B7C; text-transform:uppercase; letter-spacing:.5px; font-weight:600;}
.mini .x {font-family:'Montserrat'; font-weight:800; font-size:1.1rem;}

.phone {width:250px; margin:0 auto; background:#111; border-radius:34px; padding:12px; box-shadow:0 10px 30px rgba(0,0,0,.25);}
.screen {background:#EEF2F6; border-radius:24px; padding:14px 10px 18px; min-height:330px;}
.notch {width:80px; height:6px; background:#111; border-radius:6px; margin:-6px auto 12px;}
.from {font-size:.7rem; color:#5B6B7C; text-align:center; margin:6px 0 4px; font-weight:600;}
.bub {background:#fff; border-radius:16px 16px 16px 4px; padding:10px 12px; font-size:.82rem; line-height:1.4;
  color:#0F2B46; box-shadow:0 1px 3px rgba(0,0,0,.06); margin-bottom:8px;}
.bub.bad {border-left:4px solid #D64545;}
.bub.good {border-left:4px solid #1C9AA3;}

.legend {display:flex; gap:16px; flex-wrap:wrap; font-size:.82rem; color:#0F2B46; margin:2px 0 4px;}
.legend span i {display:inline-block; width:12px; height:12px; border-radius:3px; margin-right:6px; vertical-align:-1px;}

div.stButton > button {border-radius:12px; font-family:'Montserrat'; font-weight:700; border:1.5px solid #D5DEE7;}
div.stButton > button[kind="primary"] {background:#0F2B46; border-color:#0F2B46;}
div.stButton > button[kind="primary"] p {color:#fff !important;}
[data-testid="stSlider"] label p {font-weight:600; font-size:.88rem;}
</style>
""", unsafe_allow_html=True)


def kpi(col, label, value, sub="", color=TEAL):
    col.markdown(f"<div class='kpi' style='border-top-color:{color}'><div class='l'>{label}</div>"
                 f"<div class='v'>{value}</div><div class='s'>{sub}</div></div>", unsafe_allow_html=True)


def lakh(n):
    return f"{n / 1e5:.2f} lakh" if n >= 1e5 else f"{n:,.0f}"


def clean(fig, h):
    fig.update_layout(height=h, margin=dict(l=8, r=8, t=10, b=8), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter", color=INK, size=13), showlegend=False)
    return fig


st.markdown("""<div class='topbar'><div class='brand'>NAVIRA <span>ONE</span><small>Repair console · Team ARTHA</small></div>
<div class='live'><b>●</b> LIVE MODEL</div></div>""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Citizen desk", "District control room", "Reserve test"])

# =====================================================================================
# 1. CITIZEN DESK: the same person through the old and the repaired Navira One
# =====================================================================================
PEOPLE = {
    "Rekha": dict(full="Rekha Devi", age=61, ini="RD", col="#8E5BB5", scheme="Widow pension",
                  amt=2000, issue="Spelt 'Rekha Kumari' in the land list", kind="gap"),
    "Imran": dict(full="Imran Shaikh", age=34, ini="IS", col="#5E8FC4", scheme="Ration + job match",
                  amt=1500, issue="Daily-wage worker, no fixed address", kind="gap"),
    "Shanti": dict(full="Shanti Bai", age=58, ini="SB", col="#C2185B", scheme="Insulin refill",
                   amt=0, issue="Diabetic, collects insulin every month", kind="health"),
    "Vikram": dict(full="Vikram Rao", age=47, ini="VR", col="#E07B39", scheme="Housing support",
                   amt=0, issue="Family income above the limit", kind="ineligible"),
}

if "who" not in st.session_state:
    st.session_state.who = "Rekha"


def pick(n):
    st.session_state.who = n


def old_path(p, id_down, link_down):
    k = p["kind"]
    if k == "health":
        steps = [("Arrives at clinic", "Regular patient, prescription on file", "ok")]
        if id_down or link_down:
            steps += [("ID / record check", "System offline at the counter", "bad"),
                      ("Sent home", "Told to come back when the link works", "bad")]
            return steps, dict(head="Sent away without insulin", c=RED, days=4, lost="4 doses",
                               reason="None", who="No one"), ("bad", "CLINIC SCREEN", "Verification failed. Please try again later. Error 503.")
        steps += [("ID / record check", "Passes", "ok"), ("Insulin given", "", "ok")]
        return steps, dict(head="Insulin given", c=GREEN, days=0, lost="—", reason="—", who="System"), \
            ("good", "CLINIC SCREEN", "Verified. Dispense 30 days.")
    steps = [("Application in", p["scheme"], "ok")]
    if id_down:
        steps += [("ID check", "Vendor ID module down", "bad"),
                  ("Stuck", "Nothing moves until the module is back", "bad")]
        return steps, dict(head="Stuck in the queue", c=AMBER, days=21, lost=f"₹{p['amt'] * 0.7:,.0f}" if p["amt"] else "—",
                           reason="None", who="No one"), ("bad", "NAVIRA ONE", "Service temporarily unavailable. Try later.")
    steps += [("ID check", "Passes", "ok"), ("Model scores the case", "Record does not fit the pattern", "bad"),
              ("Refused automatically", "No reason, no person", "bad")]
    if k == "ineligible":
        res = dict(head="Refused, no reason given", c=RED, days=0, lost="—", reason="None", who="The model")
    else:
        res = dict(head="Refused in error", c=RED, days=210, lost=f"₹{p['amt'] * 7:,.0f}", reason="None", who="The model")
    return steps, res, ("bad", "NAVIRA ONE", f"Application {p['scheme'].upper()[:3]}-20418 rejected. Code E-417. Appeal online.")


def new_path(p, id_down, link_down):
    k = p["kind"]
    idstep = ("ID check", "Code sent to phone on record (ID module switched off)" if id_down else "Passes", "fix" if id_down else "ok")
    if k == "health":
        steps = [("Arrives at clinic", "Regular patient, prescription on file", "ok")]
        if link_down:
            steps += [("Link down", "Counter uses stored patient list", "fix"),
                      ("Insulin given", "30 days, logged, checked later", "ok")]
            msg = "Clinic 14 · Shanti Bai · insulin 30 days given from stored list (offline). Will sync later."
        else:
            steps += [idstep, ("Insulin given", "30 days", "ok")]
            msg = "Clinic 14 · Shanti Bai · insulin 30 days given."
        return steps, dict(head="Insulin given today", c=GREEN, days=0, lost="—", reason="—", who="Clinic staff"), ("good", "CLINIC SCREEN", msg)
    steps = [("Application in", p["scheme"], "ok"), idstep]
    if k == "ineligible":
        steps += [("Model flags it", "Cannot refuse on its own", "fix"),
                  ("Officer A. Mehta reviews", "Income ₹2.6 lakh vs ₹2 lakh limit", "ok"),
                  ("Notice sent", "Reason + 15 days to reply", "ok")]
        return steps, dict(head="Refused, with a reason", c=BLUE, days=0, lost="—", reason="Written", who="A. Mehta, Ward 7"), \
            ("good", "NAVIRA ONE", "Notice from A. Mehta, Ward 7 office: your family income (₹2.6 lakh, tax record 2025) is above the ₹2 lakh limit. Wrong? Reply within 15 days or visit Desk 112.")
    gap = "Name differs in two lists" if p["full"].startswith("Rekha") else "No address or wage proof"
    fix = "Desk 112 links both lists" if p["full"].startswith("Rekha") else "Desk adds address + work history"
    steps += [("Model flags a gap", gap, "fix"),
              ("Payment kept on", "A data gap is never a no", "ok"),
              (fix, "Officer signs it off, day 10", "ok")]
    msg = ("Your widow pension continues. Your name is spelt two ways in our lists. Bring any one ID to Desk 112 (Ward office) when you can."
           if p["full"].startswith("Rekha") else
           "Your ration continues. Visit any Navira desk once to add your address and past work; matching jobs will show after that.")
    return steps, dict(head="Paid throughout", c=GREEN, days=0, lost="₹0", reason="—", who="Officer, after desk visit"), ("good", "NAVIRA ONE", msg)


def lane(title, tag, tagc, steps, res):
    colors = {"ok": TEAL, "bad": RED, "fix": GOLD}
    marks = {"ok": "✓", "bad": "✕", "fix": "↻"}
    html = f"<div class='lane'><span class='pill' style='background:{tagc}'>{tag}</span><h4 style='margin-top:8px'>{title}</h4><div style='margin-top:12px'>"
    for a, b, s in steps:
        html += (f"<div class='node'><div class='dot' style='background:{colors[s]}'>{marks[s]}</div>"
                 f"<div><div class='a'>{a}</div><div class='b'>{b}</div></div></div>")
    html += (f"</div><div class='res' style='background:{res['c']}18; border:1.5px solid {res['c']}'>"
             f"<div class='big' style='color:{res['c']}'>{res['head']}</div></div>"
             f"<div class='mini'><div><div class='k'>Days without help</div><div class='x'>{res['days']}</div></div>"
             f"<div><div class='k'>Lost</div><div class='x'>{res['lost']}</div></div>"
             f"<div><div class='k'>Decided by</div><div class='x' style='font-size:.9rem'>{res['who']}</div></div></div></div>")
    return html


def phone(kind, sender, text):
    return (f"<div class='phone'><div class='screen'><div class='notch'></div><div class='from'>{sender}</div>"
            f"<div class='bub {kind}'>{text}</div></div></div>")


with tab1:
    cols = st.columns(4)
    for c, (k, p) in zip(cols, PEOPLE.items()):
        on = "on" if st.session_state.who == k else ""
        c.markdown(f"<div class='who {on}'><div class='av' style='background:{p['col']}'>{p['ini']}</div>"
                   f"<div><div class='n'>{p['full']}, {p['age']}</div><div class='t'><b>{p['scheme']}</b><br>{p['issue']}</div></div></div>",
                   unsafe_allow_html=True)
        c.button("Select" if not on else "Selected", key="b" + k, on_click=pick, args=(k,), width="stretch",
                 type="primary" if on else "secondary")
    p = PEOPLE[st.session_state.who]
    s1, s2, _ = st.columns([1, 1, 2])
    id_down = s1.toggle("ID module down", value=False)
    link_down = s2.toggle("Clinic link down", value=p["kind"] == "health")
    o_steps, o_res, o_msg = old_path(p, id_down, link_down)
    n_steps, n_res, n_msg = new_path(p, id_down, link_down)
    a, b, c = st.columns([1.15, 1.15, 0.95], gap="medium")
    a.markdown(lane("Navira One today", "BEFORE", RED, o_steps, o_res), unsafe_allow_html=True)
    b.markdown(lane("Navira One repaired", "AFTER", TEAL, n_steps, n_res), unsafe_allow_html=True)
    with c:
        view = st.segmented_control("What they see",
                                    ["Before", "After"], default="After", key="msgview" + st.session_state.who)
        m = o_msg if view == "Before" else n_msg
        st.markdown(phone(*m), unsafe_allow_html=True)

# =====================================================================================
# 2. DISTRICT CONTROL ROOM: 24 months after the switch
# =====================================================================================
NAMES = ["Ardan", "Belor", "Caspen", "Dhalia", "Elvar", "Faruk", "Ganthi", "Halden", "Iskar", "Jorvi",
         "Kesar", "Lunel", "Maren", "Nadir", "Orvel", "Pashan", "Qerin", "Rasul", "Selva", "Tarun",
         "Udal", "Varen", "Wesna", "Xaro", "Yaval", "Zarin", "Amrel", "Bhoran", "Coval", "Daresh"]
ROWS = [4, 5, 6, 6, 5, 4]
HX, HY = [], []
STARTS = [1, 0, 0, 0, 0, 1]
for r, n in enumerate(ROWS):
    for j in range(n):
        HX.append(j + STARTS[r] + (0.5 if r % 2 else 0))
        HY.append(-r * 0.87)
HX, HY = np.array(HX) - np.mean(HX), np.array(HY)
FLAGGED = 43000 * 0.333  # eligible people among cases the old model refused each month


@st.cache_data
def simulate(start_err, extra_desks, seed=4):
    rng = np.random.default_rng(seed)
    e0 = np.clip(rng.normal(start_err, 2.2, 30), 1.0, 14) / 100
    floor = np.clip(rng.normal(1.4, 0.6, 30), 0.4, 3.0) / 100
    pop = rng.dirichlet(np.ones(30) * 6)
    err = e0.copy()
    checks = np.zeros((25, 30))
    status = np.full((25, 30), "wait", dtype=object)
    flags = np.zeros((25, 30), bool)
    rate = np.full((25, 30), np.nan)
    wrong = np.zeros(25)
    under = np.zeros(30)
    for m in range(1, 25):
        speed = np.where(status[m - 1] == "red", 0.30 + extra_desks / 100, 0.17)
        err = floor + (err - floor) * (1 - speed)
        checks[m] = rng.binomial(100, err)
        wrong[m] = FLAGGED * float((err * pop).sum())
        if m >= 3:
            rate[m] = checks[m - 2:m + 1].sum(axis=0) / 3
            status[m] = np.where(rate[m] < 2, "green", np.where(rate[m] <= 5, "amber", "red"))
            under = np.where(rate[m] < 2, under + 1, 0)
            flags[m] = flags[m - 1] | (under >= 3)
            flags[m] &= rate[m] < 2
    return dict(rate=rate, status=status, flags=flags, wrong=wrong, pop=pop)


def hexmap(sim, m):
    st_ = sim["status"][m]
    cmap = {"wait": GREY, "green": GREEN, "amber": AMBER, "red": RED}
    col = [cmap[s] for s in st_]
    lw = [5 if f else 0 for f in sim["flags"][m]]
    txt = [("" if np.isnan(r) else f"<b>{r:.1f}</b>") for r in sim["rate"][m]]
    fig = go.Figure(go.Scatter(
        x=HX, y=HY, mode="markers+text", text=txt, textfont=dict(color="white", size=13, family="Montserrat"),
        marker=dict(symbol="hexagon", size=74, color=col, line=dict(color=GOLD, width=lw)),
        customdata=np.array(NAMES), hovertemplate="%{customdata}<br>%{text}%<extra></extra>"))
    fig.add_trace(go.Scatter(x=HX, y=HY - 0.3, mode="text", text=NAMES, hoverinfo="skip",
                             textfont=dict(color="rgba(255,255,255,.85)", size=9)))
    clean(fig, 470)
    fig.update_xaxes(visible=False, range=[-3.4, 3.4])
    fig.update_yaxes(visible=False, range=[-4.9, 0.55], scaleanchor="x")
    return fig


def trend(sim, m):
    x = np.arange(1, 25)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=[FLAGGED] * 24, line=dict(color=RED, width=2, dash="dot"), name="old"))
    fig.add_trace(go.Scatter(x=x[:m], y=sim["wrong"][1:m + 1], line=dict(color=TEAL, width=4),
                             fill="tozeroy", fillcolor="rgba(28,154,163,.12)"))
    fig.add_trace(go.Scatter(x=[m], y=[sim["wrong"][m]], mode="markers", marker=dict(size=12, color=NAVY)))
    fig.add_annotation(x=m, y=sim["wrong"][m], text=f"<b>{sim['wrong'][m]:,.0f}</b>", showarrow=False, yshift=16,
                       font=dict(color=NAVY, size=13))
    fig.add_annotation(x=24, y=FLAGGED, text="old model", showarrow=False, yshift=12, xanchor="right",
                       font=dict(color=RED, size=12))
    clean(fig, 190)
    fig.update_xaxes(range=[0.5, 24.5], dtick=3, title=None, gridcolor="#EEF1F4", ticks="", tickprefix="M")
    fig.update_yaxes(range=[0, FLAGGED * 1.15], gridcolor="#EEF1F4", tickformat=",")
    return fig


def room(sim, m, slots):
    st_ = sim["status"][m]
    g, a_, r = (st_ == "green").sum(), (st_ == "amber").sum(), (st_ == "red").sum()
    paid = 2.2e5 * min(1, (m / 6)) ** 1.3
    desks = int(min(4000, 4000 * m / 6))
    kpi(slots[0], "Month", f"M{m}", "after the switch", NAVY)
    kpi(slots[1], "Look-back paid", lakh(paid), "of 2.2 lakh, by M6", TEAL)
    kpi(slots[2], "Desks open", f"{desks:,}", "of 4,000", BLUE)
    kpi(slots[3], "Wrong refusals this month", f"{sim['wrong'][m]:,.0f}", f"old model: {FLAGGED:,.0f}", GREEN)
    kpi(slots[4], "Model flags back", f"{int(sim['flags'][m].sum())}", "districts, gold outline", GOLD)
    slots[5].plotly_chart(hexmap(sim, m), width="stretch", config={"displayModeBar": False}, key=f"hx{m}{time.time()}")
    slots[6].plotly_chart(trend(sim, m), width="stretch", config={"displayModeBar": False}, key=f"tr{m}{time.time()}")
    x = np.arange(3, m + 1)
    mix = go.Figure()
    for key_, colr_, nm_ in [("red", RED, "above 5%"), ("amber", AMBER, "2 to 5%"), ("green", GREEN, "under 2%")]:
        mix.add_trace(go.Scatter(x=x, y=[(sim["status"][i] == key_).sum() for i in x], stackgroup="one", mode="none",
                                 fillcolor=colr_, name=nm_, hovertemplate="M%{x}: %{y} districts<extra>" + nm_ + "</extra>"))
    clean(mix, 150)
    mix.update_xaxes(range=[2.5, 24.5], dtick=3, tickprefix="M", gridcolor="#EEF1F4")
    mix.update_yaxes(range=[0, 30], dtick=10, gridcolor="#EEF1F4")
    slots[8].plotly_chart(mix, width="stretch", config={"displayModeBar": False}, key=f"mx{m}{time.time()}")
    if m < 3:
        slots[7].markdown("<div class='kpi' style='border-top-color:#C9CFD6'><div class='l'>District rates</div>"
                          "<div class='v' style='font-size:1.2rem'>Collecting checks</div>"
                          "<div class='s'>first rates out after 300 checks</div></div>", unsafe_allow_html=True)
    else:
        slots[7].markdown(
            f"<div class='kpi' style='border-top-color:{NAVY}'><div class='l'>Districts this month</div>"
            f"<div style='display:flex;gap:18px;margin-top:4px'>"
            f"<div><div class='v' style='color:{GREEN}'>{g}</div><div class='s'>under 2%</div></div>"
            f"<div><div class='v' style='color:{AMBER}'>{a_}</div><div class='s'>2 to 5%</div></div>"
            f"<div><div class='v' style='color:{RED}'>{r}</div><div class='s'>above 5%</div></div></div></div>",
            unsafe_allow_html=True)


with tab2:
    c0, c1, c2, c3 = st.columns([1.2, 1.2, 1, 0.8])
    start_err = c0.slider("Officer error at the start (%)", 2.0, 10.0, 6.0, 0.5)
    extra = c1.slider("Extra desks to a red district", 0, 40, 20, 5)
    month = c2.slider("Month", 1, 24, 12)
    c3.write("")
    play = c3.button("▶  Play 24 months", type="primary", width="stretch")
    sim = simulate(start_err, extra)
    k = st.columns(5)
    left, right = st.columns([1.35, 1], gap="medium")
    with left:
        with st.container(border=True, key="card1"):
            st.markdown(f"<div class='legend'><span><i style='background:{GREEN}'></i>Under 2%: flags may return</span>"
                        f"<span><i style='background:{AMBER}'></i>2 to 5%: officer decides</span>"
                        f"<span><i style='background:{RED}'></i>Above 5%: meet before refusing, desks sent</span>"
                        f"<span><i style='background:#fff;border:3px solid {GOLD}'></i>Flags back</span></div>",
                        unsafe_allow_html=True)
            map_slot = st.empty()
    with right:
        with st.container(border=True, key="card2"):
            st.markdown("**Wrong refusals a month**")
            trend_slot = st.empty()
        mix_slot = st.empty()
        with st.container(border=True, key="card99"):
            st.markdown("**Districts by band, month by month**")
            area_slot = st.empty()
    slots = [k[0].empty(), k[1].empty(), k[2].empty(), k[3].empty(), k[4].empty(), map_slot, trend_slot, mix_slot, area_slot]
    if play:
        for mm in range(1, 25):
            room(sim, mm, slots)
            time.sleep(0.45)
    else:
        room(sim, month, slots)

# =====================================================================================
# 3. RESERVE TEST
# =====================================================================================
BASE = dict(benefit=2000, people=2.2, months=7, breach=5.0, desks=4000)
WORST = dict(benefit=3000, people=3.0, months=10, breach=10.0, desks=5000)
RESERVE = 850


def need(v):
    ppl = v["people"] * 1e5
    return (ppl * v["benefit"] * v["months"] * 1.1 + ppl * 5000 + v["breach"] * 1e5 * 2000 + v["desks"] * 9e5) / 1e7


def setv(d):
    for kk, vv in d.items():
        st.session_state["r_" + kk] = vv


for kk, vv in BASE.items():
    st.session_state.setdefault("r_" + kk, vv)

with tab3:
    l, r = st.columns([1, 1.5], gap="large")
    with l:
        with st.container(border=True, key="card3"):
            b1, b2 = st.columns(2)
            b1.button("Our estimate", on_click=setv, args=(BASE,), width="stretch")
            b2.button("Everything goes wrong", on_click=setv, args=(WORST,), width="stretch", type="primary")
            v = dict(
                benefit=st.slider("Average benefit (₹ a month)", 1500, 3000, step=100, key="r_benefit"),
                people=st.slider("People wrongly refused (lakh)", 1.8, 3.0, step=0.1, key="r_people"),
                months=st.slider("Months they went unpaid", 5, 10, key="r_months"),
                breach=st.slider("People hit by the breach (lakh)", 3.0, 10.0, step=0.5, key="r_breach"),
                desks=st.slider("Desks needed", 3500, 5000, step=100, key="r_desks"),
            )
        single = []
        for kk in BASE:
            single.append(need(dict(BASE, **{kk: WORST[kk]})) - need(BASE))
        rng = np.random.default_rng(7)
        draws = {kk: rng.triangular(min(BASE[kk], lo), BASE[kk], WORST[kk], 10000)
                 for kk, lo in dict(benefit=1500, people=1.8, months=5, breach=3.0, desks=3500).items()}
        fut = need(draws) - need(BASE)
        c_a, c_b = st.columns(2)
        kpi(c_a, "Worst single risk", f"+₹{max(single):,.0f} Cr", "any one alone fits", TEAL)
        kpi(c_b, "10,000 random futures", f"{(fut <= RESERVE).mean() * 100:.0f}%", "covered by the reserve", NAVY)
    extra_need = need(v) - need(BASE)
    used = max(0.0, extra_need)
    short = max(0.0, used - RESERVE)
    with r:
        with st.container(border=True, key="card4"):
            colr = TEAL if used < 600 else (AMBER if used <= RESERVE else RED)
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=used, number=dict(prefix="₹", suffix=" Cr", font=dict(size=46, family="Montserrat", color=NAVY)),
                gauge=dict(axis=dict(range=[0, 1000], tickvals=[0, 250, 500, 850, 1000], ticktext=["0", "250", "500", "850", "1,000"]),
                           bar=dict(color=colr, thickness=0.32), bgcolor="#EEF2F6", borderwidth=0,
                           steps=[dict(range=[850, 1000], color="#F9DADA")],
                           threshold=dict(line=dict(color=NAVY, width=4), thickness=0.9, value=RESERVE))))
            clean(fig, 300)
            fig.update_layout(margin=dict(l=40, r=40, t=30, b=10))
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            if short > 0:
                msg, mc = f"₹{short:,.0f} Cr over the ₹850 Cr reserve. Taken from year-2 reform ({short / 790 * 100:.0f}% of it).", RED
            else:
                msg, mc = f"Covered. ₹{RESERVE - used:,.0f} Cr of the ₹850 Cr reserve left.", TEAL
            st.markdown(f"<div style='text-align:center;font-family:Montserrat;font-weight:700;font-size:1.05rem;color:{mc};margin-top:-8px'>{msg}</div>",
                        unsafe_allow_html=True)
        parts = {
            "Back pay": (v["people"] * 1e5 * v["benefit"] * v["months"] * 1.1 - 2.2e5 * 2000 * 7 * 1.1) / 1e7,
            "Delay payment": (v["people"] - 2.2) * 1e5 * 5000 / 1e7,
            "Breach care": (v["breach"] - 5) * 1e5 * 2000 / 1e7,
            "Desks": (v["desks"] - 4000) * 9e5 / 1e7,
        }
        with st.container(border=True, key="card5"):
            st.markdown("**Where the extra money goes (₹ Cr)**")
            names = list(parts.keys())
            vals = [parts[n] for n in names]
            fig = go.Figure(go.Bar(y=names, x=vals, orientation="h", marker_color=[TEAL if x <= 0 else BLUE for x in vals],
                                   text=[f"{x:+,.0f}" for x in vals], textposition="outside", cliponaxis=False))
            clean(fig, 190)
            fig.update_yaxes(autorange="reversed")
            fig.update_xaxes(gridcolor="#EEF1F4", zerolinecolor=NAVY, range=[min(-120, min(vals) * 1.3), max(150, max(vals) * 1.25)])
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
