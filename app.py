import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="SupeRR Selector | Round 1", page_icon="🏏", layout="wide")
DATA = Path(__file__).parent 

@st.cache_data
def load_data():
    bat = pd.read_csv(DATA / "batters.csv")
    bowl = pd.read_csv(DATA / "bowlers.csv")
    return bat, bowl

bat, bowl = load_data()

st.title("🏏 SupeRR Selector — Season 2, Round 1")
st.caption("Pressure performance • team-carrying ability • strong opposition • consistency")
st.markdown("**Analytical shortlist:** 2022–2026 IPL and men's T20I evidence, with all nationalities represented in the selected pool.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Batters shortlisted", len(bat))
c2.metric("Bowlers shortlisted", len(bowl))
c3.metric("Evaluation dimensions", "4")
c4.metric("Data window", "2022–2026")

bat_tab, bowl_tab, method_tab = st.tabs(["🏏 Batters", "🎯 Bowlers", "📊 Methodology"])

with bat_tab:
    st.subheader("Top 10 batters")
    st.caption("Ranked using the strong-opposition batter analysis table. Rates are calculated from the supplied analytical dataset.")
    display = bat[["rank", "striker_name", "matches", "seasons", "runs", "pressure_sr", "strong_pressure_sr", "strong_avg", "strong_carry_rate", "strong_top_scorer_rate", "overall_score_role"]].copy()
    display.columns = ["Rank", "Batter", "Matches", "Seasons", "Runs", "Pressure SR", "Strong-opposition pressure SR", "Strong-opposition avg", "Strong-opposition carry rate", "Top-scorer rate", "Composite score"]
    st.dataframe(display.style.format({"Pressure SR":"{:.1f}", "Strong-opposition pressure SR":"{:.1f}", "Strong-opposition avg":"{:.1f}", "Strong-opposition carry rate":"{:.1%}", "Top-scorer rate":"{:.1%}", "Composite score":"{:.1f}"}), use_container_width=True, hide_index=True)
    selected = st.selectbox("Explore a batter", bat["striker_name"].tolist(), key="batter")
    p = bat.loc[bat.striker_name == selected].iloc[0]
    a,b,c,d = st.columns(4)
    a.metric("Composite score", f"{p.overall_score_role:.1f}/100")
    b.metric("Pressure strike rate", f"{p.pressure_sr:.1f}")
    c.metric("Strong-opposition pressure SR", f"{p.strong_pressure_sr:.1f}")
    d.metric("Strong-opposition average", f"{p.strong_avg:.1f}")
    st.write(f"**Evidence sample:** {int(p.matches)} matches across {int(p.seasons)} seasons; {int(p.runs):,} runs in the selected data scope.")
    st.write(f"**Strong-opposition carry rate:** {p.strong_carry_rate:.1%}  ·  **Top-scorer rate:** {p.strong_top_scorer_rate:.1%}  ·  **Repeat rate:** {p.repeat_rate:.1%}")
    fig = px.bar(bat.sort_values("overall_score_role"), x="overall_score_role", y="striker_name", orientation="h", labels={"overall_score_role":"Composite score", "striker_name":"Batter"}, title="Batter composite scores")
    fig.update_layout(yaxis={"categoryorder":"total ascending"}, height=420)
    st.plotly_chart(fig, use_container_width=True)
    st.download_button("Download batter data (CSV)", bat.to_csv(index=False).encode("utf-8"), "superr_top10_batters.csv", "text/csv")

with bowl_tab:
    st.subheader("Top 10 bowlers")
    st.caption("Ranked using the strong-opposition bowler analysis table. Economy is runs conceded per six legal deliveries.")
    display = bowl[["rank", "bowler_name", "matches", "seasons", "pressure_econ", "strong_pressure_econ", "pressure_wkts_per6", "strong_wkts_per6", "strong_dot_pct", "overall_score"]].copy()
    display.columns = ["Rank", "Bowler", "Matches", "Seasons", "Pressure economy", "Strong-opposition economy", "Pressure wickets/6", "Strong-opposition wickets/6", "Strong-opposition dot-ball %", "Composite score"]
    st.dataframe(display.style.format({"Pressure economy":"{:.2f}", "Strong-opposition economy":"{:.2f}", "Pressure wickets/6":"{:.2f}", "Strong-opposition wickets/6":"{:.2f}", "Strong-opposition dot-ball %":"{:.1f}%", "Composite score":"{:.1f}"}), use_container_width=True, hide_index=True)
    selected = st.selectbox("Explore a bowler", bowl["bowler_name"].tolist(), key="bowler")
    p = bowl.loc[bowl.bowler_name == selected].iloc[0]
    a,b,c,d = st.columns(4)
    a.metric("Composite score", f"{p.overall_score:.1f}/100")
    b.metric("Pressure economy", f"{p.pressure_econ:.2f}")
    c.metric("Strong-opposition economy", f"{p.strong_pressure_econ:.2f}")
    d.metric("Strong-opposition wickets/6", f"{p.strong_wkts_per6:.2f}")
    st.write(f"**Evidence sample:** {int(p.matches)} matches across {int(p.seasons)} seasons; {int(p.legal):,} legal deliveries in the selected data scope.")
    st.write(f"**Strong-opposition dot-ball rate:** {p.strong_dot_pct:.1f}%  ·  **Pressure wickets/6:** {p.pressure_wkts_per6:.2f}  ·  **Reliability factor:** {p.reliability:.3f}")
    fig = px.bar(bowl.sort_values("overall_score"), x="overall_score", y="bowler_name", orientation="h", labels={"overall_score":"Composite score", "bowler_name":"Bowler"}, title="Bowler composite scores")
    fig.update_layout(yaxis={"categoryorder":"total ascending"}, height=420)
    st.plotly_chart(fig, use_container_width=True)
    st.download_button("Download bowler data (CSV)", bowl.to_csv(index=False).encode("utf-8"), "superr_top10_bowlers.csv", "text/csv")

with method_tab:
    st.subheader("Selection framework")
    st.markdown("The committee's agreed evaluation weights are shown below. These weights describe the selection framework; the displayed player composite scores are the scores present in the supplied analysis exports and should not be assumed to be a fresh recalculation of these weights.")
    left, right = st.columns(2)
    with left:
        st.markdown("**Batters**")
        bweights = pd.DataFrame({"Dimension":["Pressure performance", "Team-carrying ability", "Strong-opposition performance", "Consistency & reliability"], "Weight":[30,30,20,20]})
        st.dataframe(bweights, hide_index=True, use_container_width=True)
        st.plotly_chart(px.pie(bweights, names="Dimension", values="Weight", hole=.45), use_container_width=True)
    with right:
        st.markdown("**Bowlers**")
        wweights = pd.DataFrame({"Dimension":["Pressure performance", "Team-carrying / match impact", "Strong-opposition performance", "Consistency & reliability"], "Weight":[35,20,25,20]})
        st.dataframe(wweights, hide_index=True, use_container_width=True)
        st.plotly_chart(px.pie(wweights, names="Dimension", values="Weight", hole=.45), use_container_width=True)
    st.markdown("**Operational pressure proxies**")
    st.markdown("- **Batting:** in a chase, required run rate ≥ 9, five or fewer wickets remaining, or 30 or fewer legal balls remaining; in the first innings, overs 16–20, or over 11 onward with five or fewer wickets remaining.\n- **Bowling:** first-innings overs 16–20; in a chase, a strong batting position (required rate ≤ 8, at least six wickets in hand and 60 or fewer legal balls remaining), or 30 or fewer legal balls remaining.\n- These are reproducible match-state proxies, not direct measurements of psychological stress or win probability.")
    st.markdown("**Strong-opposition analysis**")
    st.markdown("The strong-opposition tables contain the comparison metrics and composite scores used for the displayed shortlists. Opposition-strength cut-offs and any sensitivity analysis should be interpreted in line with the accompanying methodology report.")
    st.info("Umran Malik is retained as a high-upside development selection. The selection rationale is based on pace and wicket-taking potential, while recognising that consistency and pressure execution remain development areas.")

st.divider()
st.caption("Prepared for SupeRR Selector Season 2 — Round 1. Use the accompanying methodology report for full data definitions, eligibility rules and limitations. Model outputs are evidence-based decision support, not guarantees of future performance or player availability.")
