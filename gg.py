import streamlit as st
import pandas as pd
import time

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Social Media Analytics Pro+",
    page_icon="🚀",
    layout="wide"
)

# =================================================
# THEME TOGGLE (DARK / LIGHT)
# =================================================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

theme = st.sidebar.radio(
    "🌗 Theme Mode",
    ["dark", "light"],
    index=0 if st.session_state.theme == "dark" else 1
)
st.session_state.theme = theme

# =================================================
# CSS BASED ON THEME
# =================================================
if theme == "dark":
    bg = "#141E30"
    fg = "white"
else:
    bg = "#f4f6fb"
    fg = "#111111"

st.markdown(f"""
<style>
.main {{
    background: {bg};
    color: {fg};
    animation: fadeIn 1.2s ease-in;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

.gradient-text {{
    background: linear-gradient(90deg,#00c6ff,#0072ff,#7f00ff,#e100ff);
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 6s infinite linear;
}}

@keyframes gradientMove {{
    0% {{ background-position: 0%; }}
    100% {{ background-position: 300%; }}
}}

.metric-card {{
    padding: 20px;
    border-radius: 18px;
    color: white;
    text-align: center;
    background: linear-gradient(135deg,#667eea,#764ba2);
    box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
}}

.metric-card:hover {{
    transform: translateY(-8px) scale(1.03);
}}

.section {{
    margin-top: 30px;
    animation: slideUp 0.9s ease;
}}

@keyframes slideUp {{
    from {{ transform: translateY(40px); opacity: 0; }}
    to {{ transform: translateY(0); opacity: 1; }}
}}
</style>
""", unsafe_allow_html=True)

# =================================================
# LOAD DATA
# =================================================
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_engagement.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# =================================================
# DERIVED METRICS
# =================================================
df["revenue_generated"] = df["ad_spend"] * (1 + df["roi"])

# =================================================
# SIDEBAR FILTERS
# =================================================
st.sidebar.markdown("## 🎛️ Filters")

platform_filter = st.sidebar.multiselect("📱 Platform", df["platform"].unique(), df["platform"].unique())
content_filter = st.sidebar.multiselect("🖼️ Content", df["content_type"].unique(), df["content_type"].unique())
year_filter = st.sidebar.multiselect("📅 Year", df["year"].unique(), df["year"].unique())

filtered_df = df[
    (df["platform"].isin(platform_filter)) &
    (df["content_type"].isin(content_filter)) &
    (df["year"].isin(year_filter))
]

# =================================================
# HEADER
# =================================================
st.markdown("""
<h1 class="gradient-text" style="text-align:center;">
🚀 Social Media Analytics Pro+
</h1>
<p style="text-align:center;font-size:18px;">
Next-level interactive dashboard with animations & insights
</p>
""", unsafe_allow_html=True)

# =================================================
# COUNT-UP KPI FUNCTION 🔥
# =================================================
def count_up(label, value, prefix="", suffix=""):
    placeholder = st.empty()
    for i in range(1, 21):
        display_val = int(value * i / 20)
        placeholder.metric(label, f"{prefix}{display_val}{suffix}")
        time.sleep(0.03)

# =================================================
# KPI SECTION (COUNT-UP ANIMATION)
# =================================================
st.markdown("### 🔑 Key Metrics")

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    count_up("🔥 Total Engagement", filtered_df["engagement"].sum())

with k2:
    count_up("📈 Avg Engagement Rate", filtered_df["engagement_rate"].mean(), suffix="%")

with k3:
    count_up("💰 Ad Spend", filtered_df["ad_spend"].sum(), prefix="₹ ")

with k4:
    count_up("💸 Revenue Generated", filtered_df["revenue_generated"].sum(), prefix="₹ ")

with k5:
    count_up("🚀 Avg ROI", filtered_df["roi"].mean())

# =================================================
# STORY TABS
# =================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📱 Engagement Story", "🖼️ Content Story", "💰 Campaign Story", "⏰ Time Story"]
)

# ---------------- TAB 1 ----------------
with tab1:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    platform_eng = filtered_df.groupby("platform")["engagement_rate"].mean().reset_index()
    st.bar_chart(platform_eng, x="platform", y="engagement_rate")
    best_platform = platform_eng.loc[platform_eng["engagement_rate"].idxmax(), "platform"]
    st.success(f"🏆 Best Platform: **{best_platform}**")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TAB 2 ----------------
with tab2:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    content_perf = filtered_df.groupby("content_type")["engagement"].mean().reset_index()
    st.bar_chart(content_perf, x="content_type", y="engagement")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TAB 3 ----------------
with tab3:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    camp = filtered_df[filtered_df["campaign_name"].notna()]
    camp_sum = camp.groupby("campaign_name")[["revenue_generated","roi"]].mean().reset_index()
    st.bar_chart(camp_sum, x="campaign_name", y="revenue_generated")
    st.bar_chart(camp_sum, x="campaign_name", y="roi")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TAB 4 ----------------
with tab4:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    hourly = filtered_df.groupby("post_hour")["engagement"].mean().reset_index()
    st.line_chart(hourly, x="post_hour", y="engagement")
    best_hour = hourly.loc[hourly["engagement"].idxmax(),"post_hour"]
    st.success(f"⏰ Best Time to Post: **{best_hour}:_**
