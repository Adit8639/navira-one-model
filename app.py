"""
Navira One Repair Model - Team ARTHA, GIM Bizrupt final
A working model of our plan to repair Navira One.
Every number here matches the deck and its backup slides (A1, A2).
Run locally:  streamlit run app.py
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Navira One Repair Model", layout="wide",
                   initial_sidebar_state="expanded")

# ------------------------------------------------------------------ colours
TEAL = "#0F6E6E"
NAVY = "#14213D"
RED = "#B3261E"
AMBER = "#B26A00"
GREEN = "#1E7B34"
GOLD = "#C9A227"
GREY = "#8A8F98"
LIGHT = "#E6E8E3"

# ------------------------------------------------------------------ paper theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Open+Sans:wght@400;600;700&display=swap');
.stApp { background-color: #FFFFFF; color: #000000; }
.stApp p, .stApp li, .stApp label, .stMarkdown, .stCaption, td, th {
    font-family: 'Open Sans', sans-serif; color: #000000; }
h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif !important; color: #000000 !important; }
h1 { font-weight: 800 !important; letter-spacing: -0.5px; font-size: 2.1rem !important; }
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] *, [data-testid="stMetricDelta"] *,
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * {
    white-space: normal !important; overflow: visible !important; text-overflow: clip !important; }
.stButton button p { white-space: nowrap; }
.stButton button[kind="primary"] p { color: #FFFFFF !important; font-weight: 700; }
[data-testid="stSidebar"] { background-color: #F4F5F2; border-right: 1px solid #D5D8D0; }
[data-testid="stMetricValue"] { font-family: 'Montserrat', sans-serif; font-weight: 800;
    color: #000000; font-size: 1.75rem; line-height: 1.15; }
[data-testid="stMetricLabel"] p { font-weight: 700; color: #000000; font-size: 0.95rem; }
[data-testid="stMetricDelta"] { font-weight: 600; }
div[data-testid="stVerticalBlockBorderWrapper"] { border-color: #BFC4BA !important; }
.kicker { font-family: 'Montserrat', sans-serif; font-weight: 700; color: #0F6E6E;
    letter-spacing: 1.5px; font-size: 0.8rem; text-transform: uppercase; margin-bottom: -6px; }
.gold { height: 3px; width: 70px; background: #C9A227; margin: 2px 0 10px 0; }
.note { font-size: 0.9rem; color: #333333; }
.tag { display: inline-block; padding: 2px 9px; border-radius: 3px; font-weight: 700;
    font-size: 0.8rem; color: #FFFFFF; }
.tile { border: 1.5px solid; border-radius: 6px; padding: 7px 9px; margin-bottom: 8px;
    min-height: 112px; background: #FFFFFF; }
.tile .nm { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 0.85rem; color: #000; }
.tile .rt { font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 1.35rem; }
.tile .st { font-size: 0.74rem; font-weight: 600; }
.step { border-left: 4px solid; padding: 6px 12px; margin-bottom: 10px; background: #FFFFFF; }
.step .when { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 0.8rem; }
.big { font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 2.6rem; line-height: 1.1; }
.stmt td, .stmt th { padding: 4px 10px; border-bottom: 1px solid #DDD; font-size: 0.92rem; }
.stmt { border-collapse: collapse; width: 100%; }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------ helpers
def people(n):
    """Indian style: lakh above 1 lakh, else thousands with commas."""
    if n >= 1e5:
        return f"{n / 1e5:.1f} lakh"
    return f"{n:,.0f}"


def cr(x, dec=0):
    return f"₹{x:,.{dec}f} Cr"


def header(kicker, title, sub=None):
    st.markdown(f"<div class='kicker'>{kicker}</div>", unsafe_allow_html=True)
    st.markdown(f"# {title}")
    st.markdown("<div class='gold'></div>", unsafe_allow_html=True)
    if sub:
        st.markdown(f"<div class='note'>{sub}</div>", unsafe_allow_html=True)


def base_layout(fig, h=360, legend=True):
    fig.update_layout(template="plotly_white", height=h, margin=dict(l=10, r=10, t=30, b=10),
                      font=dict(family="Open Sans, sans-serif", color="#000000", size=13),
                      paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", showlegend=legend,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0))
    fig.update_xaxes(showline=True, linecolor="#000000", gridcolor="#EEEEEE")
    fig.update_yaxes(showline=True, linecolor="#000000", gridcolor="#EEEEEE")
    return fig


def show(fig):
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# ------------------------------------------------------------------ model inputs (deck base case)
POP = 4.8e7                # Navira population
RURAL = 1.68e7             # 35% rural or peri-urban
BENEFIT = 2000             # average benefit, Rs a month
PEOPLE = 220000             # wrongly refused (top of case range)
MONTHS = 7                 # months unpaid on average
INTEREST = 1.1             # back pay with 10% interest
DELAY_PAY = 5000           # payment for the delay, per person
BREACH = 500000               # people in the breach
CARE = 2000                # breach care per person
DESKS = 4000               # offline desks
DESK_COST = 9e5            # per desk over 24 months
RESERVE = 850              # Rs Cr held until month 6
Y2_REFORM = 790            # Rs Cr of reform spend in year 2
CRORE = 1e7

SCALE = {"people": 1e5, "breach": 1e5}  # these two sliders work in lakh
STRESS = {  # name: (label, base, low, high)
    "benefit": ("Benefit a month (₹)", BENEFIT, 1500, 3000),
    "people": ("People wrongly refused", PEOPLE, 180000, 300000),
    "months": ("Months unpaid", MONTHS, 5, 10),
    "breach": ("People in the breach", BREACH, 300000, 1000000),
    "desks": ("Desks needed", DESKS, 3500, 5000),
}


def relief_need(benefit, ppl, months, breach, desks):
    """Rs Cr needed for the five lines the stress test moves."""
    back = ppl * benefit * months * INTEREST / CRORE
    delay = ppl * DELAY_PAY / CRORE
    care = breach * CARE / CRORE
    desk = desks * DESK_COST / CRORE
    return {"Back pay": back, "Delay payments": delay, "Breach care": care, "Desks": desk}


def total_need(v):
    return sum(relief_need(v["benefit"], v["people"], v["months"], v["breach"], v["desks"]).values())


BASE_VALS = {k: STRESS[k][1] for k in STRESS}
BASE_NEED = total_need(BASE_VALS)

# ------------------------------------------------------------------ navigation
PAGES = ["Overview", "1 · Refusal switch", "2 · Stress test", "3 · District board",
         "4 · Money", "5 · Rekha's case"]
if "page" not in st.session_state:
    st.session_state.page = PAGES[0]


def go_to(p):
    st.session_state.page = p


with st.sidebar:
    st.markdown("<div class='kicker'>Team ARTHA · GIM Bizrupt</div>", unsafe_allow_html=True)
    st.markdown("### Navira One Repair Model")
    st.radio("Screens", PAGES, key="page", label_visibility="collapsed")
    st.divider()
    st.markdown("**Live demo**")
    st.button("▶ Demo 1: Refusal switch", on_click=go_to, args=(PAGES[1],), width="stretch")
    st.button("▶ Demo 2: Stress test", on_click=go_to, args=(PAGES[2],), width="stretch")
    st.caption("Screens 3 to 5 are kept for questions.")
    st.divider()
    st.caption("All inputs are the deck's base case. Every number is a simple product "
               "of stated inputs, so any judge can change one and see the effect.")

page = st.session_state.page


# ================================================================== OVERVIEW
def overview():
    header("Repairing Navira One · working model",
           "The repair plan, with every number open to change",
           "Navira One wrongly refused about 2 lakh people, leaked records through a vendor ID module "
           "and broke clinic checks during outages. This model runs the four parts of our ₹4,200 Cr "
           "plan with the same inputs as our deck.")
    st.write("")
    c = st.columns(4)
    with c[0]:
        with st.container(border=True):
            st.metric("Wrong refusals a month", f"{43000 / 3:,.0f} → {43000 / 3 * 0.05:,.0f}",
                      delta="-95% once only an officer can refuse", delta_color="inverse")
    with c[1]:
        with st.container(border=True):
            st.metric("Relief need in the base case", cr(BASE_NEED),
                      delta=f"reserve of {cr(RESERVE)} on top", delta_color="off", delta_arrow="off")
    with c[2]:
        with st.container(border=True):
            st.metric("Worst case, all five inputs", f"+{cr(total_need({k: STRESS[k][3] for k in STRESS}) - BASE_NEED)}",
                      delta=f"₹{total_need({k: STRESS[k][3] for k in STRESS}) - BASE_NEED - RESERVE:.0f} Cr past the reserve; any one input alone fits", delta_color="inverse")
    with c[3]:
        with st.container(border=True):
            st.metric("Running cost left for budgets", "₹140 Cr a year",
                      delta="from ₹350 Cr; about ₹29 per citizen", delta_color="off", delta_arrow="off")

    st.write("")
    a, b = st.columns([1.05, 1])
    with a:
        with st.container(border=True):
            st.markdown("#### What each screen answers")
            rows = [
                ("1 · Refusal switch", "Does taking refusals away from the model cut the harm, and what does it cost in officer time?"),
                ("2 · Stress test", "If our numbers are wrong, does the ₹850 Cr reserve still cover it?"),
                ("3 · District board", "How do we know a district is failing, and what happens next?"),
                ("4 · Money", "Where the ₹4,200 Cr goes, and who pays to run Navira One after month 24"),
                ("5 · Rekha's case", "What one wrongly refused citizen sees before and after the repair"),
            ]
            for name, q in rows:
                cc = st.columns([1.15, 2])
                cc[0].button(name, on_click=go_to, args=(name,), key="ov" + name, width="stretch")
                cc[1].markdown(f"<div style='padding-top:6px'>{q}</div>", unsafe_allow_html=True)
    with b:
        with st.container(border=True):
            st.markdown("#### The plan in four lines")
            st.markdown(
                "- **The model may approve, but only a named officer can refuse.** A data gap is never a no; "
                "people get a notice and 15 days to reply.\n"
                "- **Everyone wrongly refused in the last 14 months is found and paid**, with 10% interest and ₹5,000, "
                "by month 6, with no claim form.\n"
                "- **The vendor ID module goes off in month 1**, with three ways to prove identity and 4,000 offline desks.\n"
                "- **Each district's wrong-refusal rate is checked in the field and published**, and the rate decides "
                "what happens there.")
            fig = go.Figure(go.Bar(
                x=[680, 1510, 1160, 850], y=["Relief", "Stabilise", "Reform", "Reserve"], orientation="h",
                marker_color=[RED, TEAL, NAVY, GOLD], text=["₹680 Cr", "₹1,510 Cr", "₹1,160 Cr", "₹850 Cr held to M6"],
                textposition="auto", textfont=dict(color="white", size=13)))
            base_layout(fig, 210, legend=False)
            fig.update_yaxes(autorange="reversed")
            fig.update_xaxes(title="₹ Cr, total ₹4,200 Cr over 24 months")
            show(fig)


# ================================================================== 1 REFUSAL SWITCH
def refusal_switch():
    header("Screen 1 · Effectiveness", "What changes when only a named officer can refuse",
           "Flip the switch. The same cases reach the system each month; what changes is who is allowed to say no.")
    st.write("")
    left, right = st.columns([1, 2.1])
    with left:
        with st.container(border=True):
            repaired = st.toggle("**Only a named officer can refuse**", value=False, key="repaired")
            if repaired:
                st.markdown(f"<span class='tag' style='background:{TEAL}'>REPAIRED</span> "
                            "Model flags, officer decides, notice and 15 days to reply", unsafe_allow_html=True)
            else:
                st.markdown(f"<span class='tag' style='background:{RED}'>OLD SETUP</span> "
                            "The model refuses on its own, with no reason given", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("**Inputs** (deck base case)")
            flags = st.slider("Cases the model would refuse, a month", 30000, 60000, 43000, 1000,
                              help="6 lakh automated refusals in 14 months ÷ 14 ≈ 43,000 (backup A2)")
            elig = st.slider("Share of them who were actually eligible (%)", 20.0, 50.0, 33.3, 0.1,
                             format="%.1f", help="One in three, which gives 2.0 lakh wrong refusals over 14 months")
            miss = st.slider("Officer still gets it wrong (%)", 1.0, 15.0, 5.0, 0.5,
                             help="Share of eligible people an officer still refuses. "
                                  "Measured each month by the field re-checks.")
            unpaid_new = st.slider("Months unpaid until fixed, repaired", 0.5, 3.0, 1.0, 0.5,
                                   help="Notice, 15-day reply and field re-checks catch errors fast")
            minutes = st.slider("Officer minutes per case", 10, 40, 20, 5)

    eligible = flags * elig / 100
    wrong_old = eligible
    wrong_new = eligible * miss / 100
    months = np.arange(1, 25)
    cum_old = wrong_old * months
    cum_new = wrong_new * months
    owed_old = wrong_old * 24 * BENEFIT * MONTHS * INTEREST / CRORE
    owed_new = wrong_new * 24 * BENEFIT * unpaid_new * INTEREST / CRORE
    officers = flags * minutes / 60 / 160
    wrong_m = wrong_new if repaired else wrong_old
    owed = owed_new if repaired else owed_old

    with right:
        m = st.columns(3)
        with m[0]:
            with st.container(border=True):
                st.metric("Wrongly refused a month", people(wrong_m),
                          delta=(f"-{(1 - wrong_new / wrong_old) * 100:.0f}% vs old setup" if repaired else "one in three refusals"),
                          delta_color="inverse" if repaired else "off", delta_arrow="auto" if repaired else "off")
        with m[1]:
            with st.container(border=True):
                st.metric("Over 24 months", people(wrong_m * 24),
                          delta=(f"{people(wrong_old * 24 - wrong_new * 24)} people spared" if repaired else "people refused in error"),
                          delta_color="normal" if repaired else "off", delta_arrow="auto" if repaired else "off")
        with m[2]:
            with st.container(border=True):
                st.metric("Back pay owed later", cr(owed, 1 if owed < 10 else 0),
                          delta=(f"unpaid {unpaid_new:g} month, not {MONTHS}" if repaired else f"unpaid {MONTHS} months on average"),
                          delta_color="off", delta_arrow="off")
        with st.container(border=True):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=cum_old, name="Old setup: model refuses",
                                     line=dict(color=RED, width=4 if not repaired else 2, dash="solid" if not repaired else "dot")))
            fig.add_trace(go.Scatter(x=months, y=cum_new, name="Repaired: officer refuses",
                                     line=dict(color=TEAL, width=4 if repaired else 2, dash="solid" if repaired else "dot"),
                                     fill="tozeroy" if repaired else None, fillcolor="rgba(15,110,110,0.08)"))
            fig.add_annotation(x=24, y=cum_old[-1], text=f"<b>{people(cum_old[-1])}</b>", showarrow=False,
                               xanchor="right", yanchor="bottom", font=dict(color=RED, size=14))
            fig.add_annotation(x=24, y=cum_new[-1], text=f"<b>{people(cum_new[-1])}</b>", showarrow=False,
                               xanchor="right", yanchor="bottom", font=dict(color=TEAL, size=14))
            base_layout(fig, 400)
            fig.update_xaxes(title="Month", dtick=3)
            top = int(np.ceil(cum_old[-1] / 1e5)) + 1
            fig.update_yaxes(title="People wrongly refused, total", tickvals=[i * 1e5 for i in range(top)],
                             ticktext=["0"] + [f"{i} lakh" for i in range(1, top)])
            show(fig)

    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("**The cost we accept**")
            st.markdown(f"<div class='big'>{officers:,.0f}</div>", unsafe_allow_html=True)
            st.markdown(f"full-time officers nationally: {flags:,.0f} cases × {minutes} minutes ÷ 160 hours a month. "
                        "Refusals get slower; we say so on day one.")
    with c2:
        with st.container(border=True):
            st.markdown("**Why the error falls**")
            st.markdown("- A data gap (two spellings, a missing paper) keeps the payment going while a desk fixes it\n"
                        "- No stop without a written reason and 15 days to reply\n"
                        "- If the office cannot show the record, the person is paid")
    with c3:
        with st.container(border=True):
            st.markdown("**How we keep it honest**")
            st.markdown("- 100 random field re-checks per district a month measure the officer error\n"
                        "- The model's own flag error is tracked apart; 15% of vendor pay depends on it\n"
                        "- Model flags return only in districts under 2% for three months (screen 3)")
    st.button("Next: Stress test →", on_click=go_to, args=(PAGES[2],), type="primary")


# ================================================================== 2 STRESS TEST
def set_stress(which):
    for k in STRESS:
        st.session_state["s_" + k] = STRESS[k][1 if which == "base" else 3] / SCALE.get(k, 1)


def stress_test():
    header("Screen 2 · Viability", "If our numbers are wrong, does the reserve still hold?",
           "Five inputs carry the most doubt. Move any of them; the ₹850 Cr reserve held until month 6 has to absorb the change.")
    for k in STRESS:
        if "s_" + k not in st.session_state:
            st.session_state["s_" + k] = STRESS[k][1] / SCALE.get(k, 1)
    st.write("")
    left, right = st.columns([1, 2.1])
    with left:
        with st.container(border=True):
            b = st.columns(2)
            b[0].button("Base case", on_click=set_stress, args=("base",), width="stretch")
            b[1].button("All at worst", on_click=set_stress, args=("worst",), width="stretch", type="primary")
            v = {}
            v["benefit"] = st.slider("Benefit a month (₹)", 1500, 3000, step=100, key="s_benefit")
            v["people"] = 1e5 * st.slider("People wrongly refused (lakh)", 1.8, 3.0, step=0.05, key="s_people",
                                    help="Case range is 1.8 to 2.2 lakh; we test up to 3.0 lakh")
            v["months"] = st.slider("Months unpaid on average", 5, 10, step=1, key="s_months")
            v["breach"] = 1e5 * st.slider("People in the breach (lakh)", 3.0, 10.0, step=0.25, key="s_breach",
                                    help="The case says 'several hundred thousand'")
            v["desks"] = st.slider("Desks needed", 3500, 5000, step=100, key="s_desks")
            st.caption("Our base case: ₹2,000 · 2.2 lakh · 7 months · 5 lakh · 4,000 desks")

    need = total_need(v)
    extra = need - BASE_NEED
    short = max(0.0, extra - RESERVE)
    with right:
        m = st.columns(3)
        with m[0]:
            with st.container(border=True):
                st.metric("Extra money needed", f"{'+' if extra >= 0 else '-'}{cr(abs(extra))}",
                          delta="over the base case", delta_color="off", delta_arrow="off")
        with m[1]:
            with st.container(border=True):
                left_ = RESERVE - extra
                st.metric("Reserve left", cr(left_) if left_ >= 0 else f"-{cr(-left_)}",
                          delta=f"{min(100, max(0, extra) / RESERVE * 100):.0f}% of the reserve used",
                          delta_color="off" if short == 0 else "inverse")
        with m[2]:
            with st.container(border=True):
                if short == 0:
                    st.metric("Verdict", "Covered", delta="no cut to other work", delta_color="normal")
                else:
                    st.metric("Verdict", f"₹{short:,.0f} Cr short",
                              delta=f"slow year-2 reform by {short / Y2_REFORM * 100:.0f}%", delta_color="inverse")
        # reserve bar
        with st.container(border=True):
            fig = go.Figure()
            used = max(0, min(extra, RESERVE))
            fig.add_trace(go.Bar(x=[used], y=["Reserve"], orientation="h", marker_color=TEAL if short == 0 else RED,
                                 name="Used", text=[f"used {cr(used)}"], textposition="inside",
                                 textfont=dict(color="white")))
            fig.add_trace(go.Bar(x=[RESERVE - used], y=["Reserve"], orientation="h", marker_color=LIGHT, name="Left",
                                 text=[cr(RESERVE - used) + " left" if RESERVE - used > 60 else ""], textposition="inside"))
            if short > 0:
                fig.add_trace(go.Bar(x=[short], y=["Reserve"], orientation="h", marker_color="#E8A39E",
                                     name="Taken from year-2 reform", text=[f"+{cr(short)}"], textposition="outside"))
            fig.add_vline(x=RESERVE, line=dict(color="#000", width=2, dash="dash"))
            fig.add_annotation(x=RESERVE, y=1.0, yref="paper", text="<b>₹850 Cr reserve</b>", showarrow=False,
                               yanchor="bottom", font=dict(size=12))
            base_layout(fig, 130, legend=False)
            fig.update_layout(barmode="stack", margin=dict(l=10, r=10, t=30, b=10))
            fig.update_xaxes(range=[0, max(1000, RESERVE + short + 80)], title=None)
            fig.update_yaxes(showticklabels=False)
            show(fig)

        t1, t2 = st.columns(2)
        # tornado
        with t1:
            with st.container(border=True):
                st.markdown("**Each input alone, low to high** (₹ Cr)")
                rows = []
                for k, (lab, base, lo, hi) in STRESS.items():
                    lo_v = dict(BASE_VALS, **{k: lo})
                    hi_v = dict(BASE_VALS, **{k: hi})
                    rows.append((lab, total_need(lo_v) - BASE_NEED, total_need(hi_v) - BASE_NEED))
                rows.sort(key=lambda r: r[2] - r[1])
                fig = go.Figure()
                fig.add_trace(go.Bar(y=[r[0] for r in rows], x=[r[1] for r in rows], orientation="h",
                                     marker_color=TEAL, name="Low", text=[f"{r[1]:.0f}" for r in rows],
                                     textposition="outside"))
                fig.add_trace(go.Bar(y=[r[0] for r in rows], x=[r[2] for r in rows], orientation="h",
                                     marker_color=RED, name="High", text=[f"+{r[2]:.0f}" for r in rows],
                                     textposition="outside"))
                base_layout(fig, 280)
                fig.update_layout(barmode="overlay")
                fig.update_xaxes(range=[-170, 270], zeroline=True, zerolinecolor="#000")
                fig.update_traces(cliponaxis=False, textfont=dict(size=12))
                fig.update_yaxes(tickfont=dict(size=12, color="#000"))
                show(fig)
                st.caption("Any one input at its worst stays well inside the reserve.")
        # waterfall of current scenario
        with t2:
            with st.container(border=True):
                st.markdown("**Your scenario, step by step** (₹ Cr)")
                steps, labels = [], []
                for k, (lab, base, lo, hi) in STRESS.items():
                    alone = total_need(dict(BASE_VALS, **{k: v[k]})) - BASE_NEED
                    steps.append(alone)
                    labels.append({"benefit": "Benefit", "people": "People", "months": "Months",
                                   "breach": "Breach", "desks": "Desks"}[k])
                together = extra - sum(steps)
                steps.append(together)
                labels.append("Together")
                fig = go.Figure(go.Waterfall(
                    x=labels + ["Total"], y=steps + [extra], measure=["relative"] * len(steps) + ["total"],
                    text=[f"{s_:+.0f}" for s_ in steps] + [f"{extra:+.0f}"], textposition="outside",
                    increasing=dict(marker_color=RED), decreasing=dict(marker_color=TEAL),
                    totals=dict(marker_color=NAVY), connector=dict(line=dict(color="#999"))))
                fig.add_hline(y=RESERVE, line=dict(color=GOLD, width=2, dash="dash"),
                              annotation_text="reserve 850", annotation_position="top left")
                base_layout(fig, 280, legend=False)
                fig.update_yaxes(range=[min(0, min(np.cumsum(steps + [0]))) - 60, max(RESERVE, extra) + 120])
                show(fig)
                st.caption("Benefit, people and months multiply, so bad news on all three costs more than the sum of each.")

    with st.expander("10,000 random futures: how often does the reserve cover it?"):
        rng = np.random.default_rng(7)
        n = 10000
        draws = {k: rng.triangular(lo, base, hi, n) for k, (lab, base, lo, hi) in STRESS.items()}
        sim = (draws["people"] * draws["benefit"] * draws["months"] * INTEREST + draws["people"] * DELAY_PAY
               + draws["breach"] * CARE + draws["desks"] * DESK_COST) / CRORE - BASE_NEED
        cover = (sim <= RESERVE).mean() * 100
        cc = st.columns([1, 2])
        with cc[0]:
            st.metric("Futures the reserve covers", f"{cover:.1f}%")
            st.metric("Bad 1-in-20 future needs", cr(np.percentile(sim, 95)))
            st.caption("Each input is drawn at random between its low and high value, most often near our base case. "
                       "This is a check on the reserve size, not a forecast.")
        with cc[1]:
            fig = go.Figure(go.Histogram(x=sim, nbinsx=60, marker_color=TEAL))
            fig.add_vline(x=RESERVE, line=dict(color=RED, width=2, dash="dash"),
                          annotation_text="reserve ₹850 Cr", annotation_position="top")
            base_layout(fig, 250, legend=False)
            fig.update_xaxes(title="Extra need over base case, ₹ Cr")
            fig.update_yaxes(title="Futures")
            show(fig)

    with st.expander("How each line is worked out"):
        parts = relief_need(v["benefit"], v["people"], v["months"], v["breach"], v["desks"])
        base_parts = relief_need(*[BASE_VALS[k] for k in ["benefit", "people", "months", "breach", "desks"]])
        df = pd.DataFrame({
            "Line": list(parts.keys()),
            "Formula": [f"{people(v['people'])} × ₹{v['benefit']:,} × {v['months']} months × 1.1",
                        f"{people(v['people'])} × ₹5,000",
                        f"{people(v['breach'])} × ₹2,000",
                        f"{v['desks']:,} × ₹9 lakh"],
            "Base, ₹ Cr": [round(x) for x in base_parts.values()],
            "Now, ₹ Cr": [round(x) for x in parts.values()],
        })
        st.dataframe(df, hide_index=True, width="stretch")
        st.caption("If the reserve is not enough, the gap comes out of year-2 reform (₹790 Cr), "
                   "in the order written at month 6: look-back count, breach size, desks, then reform.")


# ================================================================== 3 DISTRICT BOARD
REGIONS = ["North", "South", "East", "West", "Central", "Coast"]


def district_board():
    header("Screen 3 · Control", "Each district's wrong-refusal rate decides what happens there",
           "The statistics office re-checks 100 random decisions per district each month. "
           "A district is judged on its last three months, that is 300 checks.")
    if "month_seed" not in st.session_state:
        st.session_state.month_seed = 1
    st.write("")
    left, right = st.columns([1, 2.6])
    with left:
        with st.container(border=True):
            avg = st.slider("Average officer error (%)", 0.5, 8.0, 3.0, 0.5,
                            help="True share of eligible people still refused, across Navira")
            spread = st.slider("How much districts differ (points)", 0.0, 4.0, 1.5, 0.5)
            res_desks = st.slider("Reserve desks sent to each red district", 0, 60, 25, 5)
            if st.button("Run another month ▶", width="stretch", type="primary"):
                st.session_state.month_seed += 1
            st.caption(f"Simulated month: M{3 + st.session_state.month_seed}")
        with st.container(border=True):
            st.markdown(f"<span class='tag' style='background:{GREEN}'>UNDER 2%</span> "
                        "Model flags may return to help officers; spare desk staff move out", unsafe_allow_html=True)
            st.write("")
            st.markdown(f"<span class='tag' style='background:{AMBER}'>2% TO 5%</span> "
                        "Normal path: an officer decides, and the rate is published", unsafe_allow_html=True)
            st.write("")
            st.markdown(f"<span class='tag' style='background:{RED}'>ABOVE 5%</span> "
                        "No refusal until someone has met the person; reserve desks sent; incident board asks why",
                        unsafe_allow_html=True)
            st.caption("2% and 5% are starting lines, to be reset after six months of data.")

    rng = np.random.default_rng(100 + st.session_state.month_seed)
    shape = np.random.default_rng(11)
    true = np.clip(avg / 100 + shape.normal(0, spread / 100, 30) + rng.normal(0, 0.003, 30), 0.002, 0.25)
    pop = shape.dirichlet(np.ones(30) * 6) * POP
    checks = rng.binomial(100, np.repeat(true[:, None], 3, axis=1))
    rate = checks.sum(axis=1) / 300 * 100
    status = np.where(rate < 2, "green", np.where(rate <= 5, "amber", "red"))
    df = pd.DataFrame({
        "District": [f"D{i + 1:02d} · {REGIONS[i % 6]}" for i in range(30)],
        "People": pop, "Wrong in 300 checks": checks.sum(axis=1), "Rate %": rate, "Status": status,
        "Last 3 months": [" / ".join(str(x) for x in r) for r in checks],
    })
    n_g, n_a, n_r = (status == "green").sum(), (status == "amber").sum(), (status == "red").sum()

    with right:
        m = st.columns(4)
        for col, lab, val, sub in [
            (m[0], "Under 2%", n_g, "flags may return"),
            (m[1], "2% to 5%", n_a, "normal path"),
            (m[2], "Above 5%", n_r, "seen before stopped"),
            (m[3], "Reserve desks sent", n_r * res_desks, f"≈ {cr(n_r * res_desks * DESK_COST / CRORE)} over two years"),
        ]:
            with col:
                with st.container(border=True):
                    st.metric(lab, f"{val:,}", delta=sub, delta_color="off", delta_arrow="off")
        with st.container(border=True):
            colors = {"green": GREEN, "amber": AMBER, "red": RED}
            words = {"green": "Flags may return", "amber": "Officer decides", "red": "Meet before refusing"}
            for r0 in range(0, 30, 6):
                cols = st.columns(6)
                for j in range(6):
                    i = r0 + j
                    c = colors[status[i]]
                    cols[j].markdown(
                        f"<div class='tile' style='border-color:{c}'>"
                        f"<div class='nm'>D{i + 1:02d} <span style='font-weight:400;color:#555'>{REGIONS[i % 6]}</span></div>"
                        f"<div class='rt' style='color:{c}'>{rate[i]:.1f}%</div>"
                        f"<div class='st' style='color:{c}'>{words[status[i]]}</div>"
                        f"<div class='st' style='color:#555'>{df['Last 3 months'][i]} wrong of 100</div></div>",
                        unsafe_allow_html=True)
    total_desks = DESKS + n_r * res_desks
    st.markdown(
        f"<div class='note'>Desks in use: {DESKS:,} + {n_r * res_desks:,} reserve = <b>{total_desks:,}</b>"
        f"{' (inside the 5,000 the stress test allows)' if total_desks <= 5000 else ' (<b>above</b> the 5,000 the stress test allows)'}. "
        "District names are placeholders; the case gives 48 million people, and we assume about 30 districts.</div>",
        unsafe_allow_html=True)
    with st.expander("Table, for questions"):
        show_df = df.copy()
        show_df["People"] = show_df["People"].map(people)
        show_df["Rate %"] = show_df["Rate %"].round(1)
        st.dataframe(show_df.sort_values("Rate %", ascending=False), hide_index=True, width="stretch")
        st.caption("Field re-checks: 30 districts × 100 = 3,000 a month; 3,000 × 24 × ₹1,500 a visit ≈ ₹11 Cr, "
                   "from the ₹180 Cr oversight line.")


# ================================================================== 4 MONEY
def money():
    header("Screen 4 · Profitability", "Where ₹4,200 Cr goes, and who pays to run it after month 24",
           "Navira One earns no fees from essential services, so we treat value as money saved and harm avoided.")
    st.write("")
    a, b = st.columns([1.25, 1])
    with a:
        with st.container(border=True):
            st.markdown("**The ₹4,200 Cr, by part** (₹ Cr)")
            labels = ["Plan", "Relief", "Stabilise", "Reform", "Reserve to M6",
                      "Back pay", "Delay pay", "Breach care",
                      "ID, security", "Desks", "Records", "Clinics",
                      "State code", "Oversight", "Team"]
            parents = ["", "Plan", "Plan", "Plan", "Plan",
                       "Relief", "Relief", "Relief",
                       "Stabilise", "Stabilise", "Stabilise", "Stabilise",
                       "Reform", "Reform", "Reform"]
            values = [4200, 680, 1510, 1160, 850, 340, 110, 230, 600, 360, 320, 230, 500, 420, 240]
            cmap = {"Plan": "#333333", "Relief": RED, "Stabilise": TEAL, "Reform": NAVY, "Reserve to M6": GOLD}
            col = [cmap.get(l, cmap.get(p, GREY)) for l, p in zip(labels, parents)]
            fig = go.Figure(go.Treemap(labels=labels, parents=parents, values=values, branchvalues="total",
                                       marker=dict(colors=col, line=dict(color="white", width=2)),
                                       texttemplate="<b>%{label}</b><br>%{value:,}", hovertemplate="%{label}: ₹%{value:,} Cr<extra></extra>", root_color="white",
                                       textfont=dict(color="white", size=13)))
            base_layout(fig, 380, legend=False)
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), uniformtext=dict(minsize=10, mode="hide"))
            show(fig)
    with b:
        with st.container(border=True):
            st.markdown("**Spend by year** (₹ Cr)")
            fig = go.Figure()
            for nm, y1, y2, c in [("Relief", 630, 50, RED), ("Stabilise", 1000, 510, TEAL), ("Reform", 370, 790, NAVY)]:
                fig.add_trace(go.Bar(x=["Year 1", "Year 2"], y=[y1, y2], name=nm, marker_color=c,
                                     text=[y1, y2], textposition="inside", textfont=dict(color="white")))
            fig.add_trace(go.Bar(x=["Reserve"], y=[850], name="Reserve", marker_color=GOLD, text=[850],
                                 textposition="inside"))
            base_layout(fig, 380)
            fig.update_layout(barmode="stack", legend=dict(traceorder="normal"))
            fig.add_annotation(x="Year 1", y=2000, text="<b>2,000</b>: visible by M12", showarrow=False, yshift=12)
            fig.add_annotation(x="Year 2", y=1350, text="<b>1,350</b>", showarrow=False, yshift=12)
            show(fig)

    st.markdown("### Running cost after month 24")
    l, r = st.columns([1, 2.1])
    with l:
        with st.container(border=True):
            st.markdown("Base running cost **₹350 Cr a year**: desks 170, digital team 120, oversight 60.")
            dup = st.slider("Flagged records that are duplicates (%)", 0.0, 3.0, 1.0, 0.25,
                            help="30 lakh records flagged; each duplicate stopped saves ₹24,000 a year")
            rent = st.slider("Vendor licence rent saved (% of ₹450 Cr a year)", 0, 30, 20, 5)
            users = st.slider("Paid desk uses a day, per desk", 0, 40, 20, 5)
            fee = st.slider("Fee per optional service (₹)", 0, 40, 20, 5,
                            help="Essential services stay free; bill payments and printing carry the fee")
    d = 30e5 * dup / 100 * 24000 / CRORE
    v_ = 450 * rent / 100
    f = DESKS * users * fee * 300 / CRORE
    left_ = 350 - d - v_ - f
    with r:
        with st.container(border=True):
            fig = go.Figure(go.Waterfall(
                x=["Running<br>cost", "Duplicates<br>stopped", "Vendor rent<br>ended", "Desk<br>fees", "Left for<br>budgets"],
                y=[350, -d, -v_, -f, left_], measure=["absolute", "relative", "relative", "relative", "total"],
                text=["350", f"-{d:.0f}", f"-{v_:.0f}", f"-{f:.0f}", f"{left_:.0f}"], textposition="outside",
                decreasing=dict(marker_color=TEAL), totals=dict(marker_color=NAVY),
                increasing=dict(marker_color=RED), connector=dict(line=dict(color="#999"))))
            base_layout(fig, 270, legend=False)
            fig.update_yaxes(range=[0, 400], title="₹ Cr a year")
            show(fig)
            mm = st.columns(3)
            mm[0].metric("Left for budgets", cr(left_), delta=f"{(350 - left_) / 350 * 100:.0f}% met by savings",
                         delta_color="off", delta_arrow="off")
            mm[1].metric("Per citizen a year", f"₹{left_ * CRORE / POP:,.0f}", delta="of ₹73 before savings",
                         delta_color="off", delta_arrow="off")
            mm[2].metric("Duplicates alone", cr(d), delta=f"{30e5 * dup / 100:,.0f} records", delta_color="off", delta_arrow="off")

    st.markdown("### Value per person")
    vals = [("₹875", "per citizen, once", "₹4,200 Cr ÷ 4.8 crore people"),
            ("₹20,400", "to each wrongly refused person", "₹2,000 × 7 × 1.1 + ₹5,000"),
            ("₹180", "per rural resident for a desk within reach for two years", "₹9 lakh ÷ 5,000 people"),
            ("₹73", "per citizen a year to run, before savings", "₹350 Cr ÷ 4.8 crore")]
    cols = st.columns(4)
    for c, (big, what, how) in zip(cols, vals):
        with c:
            with st.container(border=True):
                st.markdown(f"<div class='big'>{big}</div>", unsafe_allow_html=True)
                st.markdown(f"**{what}**")
                st.caption(how)
    st.caption("We did not count selling ID checks as income: UIDAI charges ₹20 per e-KYC, but a state that just leaked "
               "records should not sell lookups on them. A UK Cabinet Office review (2012) found a digital transaction "
               "can cost about a fiftieth of a face-to-face one, so digital stays the default and desks serve those who need them.")


# ================================================================== 5 REKHA
def rekha():
    header("Screen 5 · The product a citizen sees", "Rekha's widow pension, before and after the repair",
           "Her name is spelt differently in two government lists. Under the old setup that gap became a refusal.")
    st.write("")
    when = st.select_slider("Move through her case", ["Day 0", "Day 3", "Day 10", "Day 15", "Month 3 on"],
                            value="Month 3 on")
    idx = ["Day 0", "Day 3", "Day 10", "Day 15", "Month 3 on"].index(when)
    before = [("Day 0", "Refused automatically, no reason given"),
              ("Day 3", "Travels to the district office; told to appeal online"),
              ("Day 10", "Nothing happens; she waits for an answer"),
              ("Day 15", "Appeal pending, no reply and no payment"),
              ("Month 3 on", "Still unpaid; borrowing to buy medicines")]
    after = [("Day 0", "Model flags the name gap; the pension keeps paying"),
             ("Day 3", "SMS: bring one document to the nearest desk"),
             ("Day 10", "Desk links both lists; an officer signs it off"),
             ("Day 15", "Record statement shows the fix and who saw it"),
             ("Month 3 on", "One record, one name; payment never stopped")]
    a, b, c = st.columns([1, 1, 1.05])
    for col, title, steps, colr, paid in [(a, "Before", before, RED, False), (b, "After", after, TEAL, True)]:
        with col:
            with st.container(border=True):
                st.markdown(f"<span class='tag' style='background:{colr}'>{title.upper()}</span>", unsafe_allow_html=True)
                st.write("")
                for i, (w, t) in enumerate(steps):
                    on = i <= idx
                    st.markdown(f"<div class='step' style='border-color:{colr if on else LIGHT};"
                                f"opacity:{1 if on else 0.3}'><div class='when' style='color:{colr}'>{w}</div>{t}</div>",
                                unsafe_allow_html=True)
                months_out = [0, 0, 0, 0.5, 3][idx]
                lost = 0 if paid else BENEFIT * months_out
                st.metric("Pension lost so far", f"₹{lost:,.0f}",
                          delta="paid throughout" if paid else ("and rising each month" if lost else "payment stopping"),
                          delta_color="normal" if paid else "inverse")
    with c:
        with st.container(border=True):
            st.markdown("**Record statement, on request**")
            st.markdown("<div class='note'>Navira One: your record</div>", unsafe_allow_html=True)
            show_fix = idx >= 2
            st.markdown(f"""
<table class='stmt'>
<tr><th align='left'>Used in your last decision</th><th align='left'>Source</th></tr>
<tr><td>Name</td><td>{'two lists, linked 10 Mar' if show_fix else '<span style="color:#B3261E">two spellings, not linked</span>'}</td></tr>
<tr><td>Age</td><td>birth certificate</td></tr>
<tr><td>Income</td><td>self-declared</td></tr>
</table>""", unsafe_allow_html=True)
            st.write("")
            log = [("08 Mar", "Welfare office, decision"), ("10 Mar", "Desk 112, correction"),
                   ("14 Mar", "Clinic, medicines")][: max(1, min(3, idx))]
            rows = "".join(f"<tr><td>{d_}</td><td>{w_}</td></tr>" for d_, w_ in log)
            st.markdown(f"<table class='stmt'><tr><th align='left'>Who opened it, last 90 days</th><th></th></tr>{rows}</table>",
                        unsafe_allow_html=True)
            st.caption("Estonia has shown citizens every query on their data since 2017.")
        with st.container(border=True):
            st.markdown("**If she was refused in the last 14 months**")
            mo = st.slider("Months she went unpaid", 1, 14, 7)
            owed = BENEFIT * mo * INTEREST + DELAY_PAY
            st.metric("Look-back pays her", f"₹{owed:,.0f}", delta=f"₹2,000 × {mo} × 1.1 + ₹5,000, no claim form",
                      delta_color="off", delta_arrow="off")
    st.markdown("<div class='note'><b>Other routes the repair adds.</b> Desks in existing offices (about one per 5,000 rural people) "
                "handle corrections and replies. If a clinic's link fails, regular medicine is dispensed for up to 30 days "
                "from its stored patient list. Identity can be shown by a code to the phone on record, a QR card that needs "
                "no network, or in person.</div>", unsafe_allow_html=True)


# ------------------------------------------------------------------ router
{PAGES[0]: overview, PAGES[1]: refusal_switch, PAGES[2]: stress_test,
 PAGES[3]: district_board, PAGES[4]: money, PAGES[5]: rekha}[page]()
