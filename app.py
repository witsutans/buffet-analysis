import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime
import re

st.set_page_config(
    page_title="Hotel Amber 85 - Buffet Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────
# ปรับแต่ง UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #f0f4f9 !important;
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    min-width: 200px !important;
    max-width: 200px !important;
    box-shadow: 2px 0 8px rgba(0,0,0,0.04);
}
[data-testid="stSidebarCollapseButton"], button[kind="header"] {
    display: none !important;
}

[data-testid="stSidebar"] > div:first-child { padding: 0.5rem 0.6rem !important; }
[data-testid="stSidebar"] * { font-family: 'DM Sans', sans-serif !important; }
[data-testid="block-container"] { padding: 1.25rem 2rem 2rem 2rem; max-width: 100%; }

[data-testid="stAppViewBlockContainer"] { background-color: #f0f4f9 !important; }

/* ปุ่ม Navigation ใน Sidebar */
[data-testid="stSidebar"] button {
    background: transparent !important;
    border: none !important;
    color: #64748b !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    border-radius: 7px !important;
    padding: 7px 10px !important;
    display: flex !important;
    justify-content: flex-start !important;
    text-align: left !important;
}
[data-testid="stSidebar"] button[kind="primary"] {
    background: #eff6ff !important;
    color: #2563eb !important;
    border-left: 3px solid #2563eb !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] button:hover {
    background: #f8fafc !important;
    color: #1e293b !important;
}
[data-testid="stSidebar"] button div, 
[data-testid="stSidebar"] button div p {
    display: flex !important;
    justify-content: flex-start !important;
    text-align: left !important;
    width: 100% !important;
}

/* KPI */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 10px 8px; 
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    min-height: 105px !important; 
    height: auto !important; 
    overflow: visible !important; 
}
[data-testid="stMetricLabel"] {
    overflow: visible !important;
}
[data-testid="stMetricLabel"] > div {
    white-space: normal !important; 
    overflow: visible !important;
    text-overflow: clip !important; 
    display: flex !important;
    flex-wrap: wrap !important;
    margin-bottom: 2px;
}
[data-testid="stMetricLabel"] p {
    color: #94a3b8 !important;
    font-size: 10px !important;
    text-transform: uppercase;
    letter-spacing: 0.01em !important;
    margin: 0 !important;
    line-height: 1.1 !important;
}
[data-testid="stMetricValue"] {
    color: #1e293b !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1.35rem !important; 
    font-weight: 600 !important;
    margin-top: 4px;
}
[data-testid="stMetricDelta"] {
    overflow: visible !important;
}
[data-testid="stMetricDelta"] > div {
    white-space: normal !important; 
    overflow: visible !important;
    text-overflow: clip !important;
    display: flex !important;
    flex-wrap: wrap !important;
}
[data-testid="stMetricDelta"] * {
    font-size: 10px !important;
    line-height: 1.1 !important;
}

/* คลาสตาราง หัวข้อ กล่องข้อความ */
[data-testid="stDataFrame"] { background: #ffffff; border-radius: 10px; }
[data-testid="stSelectbox"] > div > div { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; }

.page-title { font-size: 28px !important; font-weight: 700; color: #1e293b; font-family: 'DM Sans', sans-serif; margin-bottom: 2px; }
.page-sub { font-size: 12px; color: #94a3b8; margin-bottom: 1rem; }
.section-label { font-size: 10px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2563eb; margin-bottom: 6px; margin-top: 4px; }
.comment-card { background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #cbd5e1; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; color: #64748b; font-size: 13px; font-style: italic; }
.verdict-true  { background: #f0fdf4; border: 1px solid #86efac; border-left: 3px solid #22c55e; border-radius: 7px; padding: 8px 12px; color: #15803d; font-size: 11px; font-weight: 600; margin-bottom: 10px; letter-spacing: 0.03em; }
.verdict-false { background: #fef2f2; border: 1px solid #fca5a5; border-left: 3px solid #ef4444; border-radius: 7px; padding: 8px 12px; color: #b91c1c; font-size: 11px; font-weight: 600; margin-bottom: 10px; letter-spacing: 0.03em; }
.verdict-rec   { background: #eff6ff; border: 1px solid #93c5fd; border-left: 3px solid #2563eb; border-radius: 7px; padding: 8px 12px; color: #1d4ed8; font-size: 11px; font-weight: 600; margin-bottom: 10px; letter-spacing: 0.03em; }
.verdict-warn  { background: #fffbeb; border: 1px solid #fcd34d; border-left: 3px solid #f59e0b; border-radius: 7px; padding: 8px 12px; color: #b45309; font-size: 11px; font-weight: 600; margin-bottom: 10px; letter-spacing: 0.03em; }

.zone-box-blue { background: #eff6ff; border: 1px solid #bfdbfe; border-left: 4px solid #2563eb; border-radius: 10px; padding: 16px 18px; }
.zone-box-orange { background: #fff7ed; border: 1px solid #fed7aa; border-left: 4px solid #f97316; border-radius: 10px; padding: 16px 18px; }
.day-pill { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; margin-right: 4px; }
.pill-weekend { background: #fff7ed; color: #ea580c; border: 1px solid #fdba74; }
.pill-weekday { background: #eff6ff; color: #2563eb; border: 1px solid #93c5fd; }
hr.div { border: 1px solid #e2e8f0; margin: 12px 0; }
.insight-box { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 18px; margin-top: 8px; font-size: 12px; color: #64748b; line-height: 1.75; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
</style>
""", unsafe_allow_html=True)

# ── Plotly BASE theme ─────────────────────────────────────────
BASE = dict(
    paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
    font=dict(family="DM Sans, sans-serif", color="#64748b", size=11),
    margin=dict(l=10, r=10, t=38, b=10),
    legend=dict(bgcolor="#f8fafc", bordercolor="#e2e8f0", borderwidth=1, font=dict(color="#475569", size=11)),
    title_font=dict(color="#1e293b", size=13, family="DM Sans"),
)
_AX = dict(gridcolor="#f1f5f9", linecolor="#e2e8f0", tickfont=dict(color="#94a3b8", size=11))
def ax(**kw): return {**_AX, **kw}

BLUE   = "#2563eb"
ORANGE = "#f97316"
GREEN  = "#22c55e"
PINK   = "#b854b2"
Black  = "#000000"
RED    = "#ef4444"
PURPLE = "#8b5cf6"
TEAL   = "#14b8a6"
YELLOW = "#f59e0b"
DAY_ORDER = ["Friday", "Saturday", "Sunday", "Tuesday", "Wednesday"]
DAY_COLORS = {"Friday": BLUE, "Saturday": PURPLE, "Sunday": RED, "Tuesday": PINK, "Wednesday": TEAL}

# ── Data Loading ──────────────────────────────────────────────
@st.cache_data
def load():
    try:
        m = pd.read_csv('clean_dataset.csv')
    except FileNotFoundError:
        st.error("ไม่พบไฟล์ clean_dataset.csv - กรุณารันไฟล์ทำความสะอาดข้อมูลก่อน")
        st.stop()

    for col in ['queue_start', 'queue_end', 'meal_start', 'meal_end']:
        m[col] = pd.to_datetime(m[col], errors='coerce')
        
    m['date'] = pd.to_datetime(m['date'])
    m['hour'] = m['meal_start'].dt.hour
    m['Guest_type'] = m['Guest_type'].fillna('Unknown')
    return m

# Data preparation
# df_tables: ข้อมูลที่กระจายแถวโต๊ะร่วมกันแล้ว (ใช้เวลานับโต๊ะ)
# df_unique: ข้อมูลที่กรองให้เหลือ 1 กลุ่มต่อ 1 บรรทัด (ใช้เวลานับจำนวนคน/กลุ่ม)
df_tables = load()
df_unique = df_tables.drop_duplicates(subset=['date', 'service_no.']).copy()

df      = df_unique.copy()
seated  = df[df['meal_min'].notna() & (df['meal_min'] > 0)]
wi      = seated[seated['Guest_type'] == 'Walk-in']
ih      = seated[seated['Guest_type'] == 'In-house']
queued  = df[df['is_queued']]

# ── Computed Metrics ──────────────────────────────────────────
# ภาพรวมจำนวนกลุ่มและคน
total_groups     = len(df_unique)
total_pax        = int(df_unique['pax'].sum())
total_walkaways  = int(df_unique['is_walkaway'].sum())
total_queued     = int(df_unique['is_queued'].sum())

# เวลาเฉลี่ยในการทาน (เทียบ Walk-in vs In-house)
avg_meal_wi      = round(wi['meal_min'].mean(), 1) if not wi.empty else 0
avg_meal_ih      = round(ih['meal_min'].mean(), 1) if not ih.empty else 0
diff_meal        = round(abs(avg_meal_wi - avg_meal_ih), 1)

# เวลาเฉลี่ยในการรอคิว (Queue Wait Time)
avg_wait_ih      = round(queued[queued['Guest_type'] == 'In-house']['wait_min'].mean(), 1)
avg_wait_wi      = round(queued[queued['Guest_type'] == 'Walk-in']['wait_min'].mean(), 1)

# ประเมินผลกระทบหากใช้กฎจำกัดเวลา 90 นาที (Action 1 / Task 3)
wi_over_90       = int((wi['meal_min'] > 90).sum())
ih_over_90       = int((ih['meal_min'] > 90).sum())
wi_total         = len(wi)
wi_over_90_pct   = round((wi_over_90 / wi_total) * 100) if wi_total > 0 else 0
wi_under_pct     = 100 - wi_over_90_pct

# คำนวณ Capacity ที่ได้คืน หากตัดเวลาส่วนที่เกิน 90 นาทีของ Walk-in ออก
table_min_saved  = round(wi[wi['meal_min'] > 90]['meal_min'].sub(90).sum())
avg_turn_wi      = round(wi['meal_min'].mean(), 1)
extra_turns      = round(table_min_saved / avg_turn_wi) if avg_turn_wi > 0 else 0

# แยกวันธรรมดา vs เสาร์อาทิตย์
date_range       = f"{df['date'].min().strftime('%b %d')} - {df['date'].max().strftime('%d, %Y')}"
num_days         = df['date'].nunique()

wa_wknd = int((df_unique['is_walkaway'] & df_unique['is_weekend']).sum())
wa_wkdy = int((df_unique['is_walkaway'] & ~df_unique['is_weekend']).sum())
q_wknd  = int((df_unique['is_queued'] & df_unique['is_weekend']).sum())
q_wkdy  = int((df_unique['is_queued'] & ~df_unique['is_weekend']).sum())

fri_g = len(df_unique[df_unique['day_name'] == 'Friday'])
tue_g = len(df_unique[df_unique['day_name'] == 'Tuesday'])
wed_g = len(df_unique[df_unique['day_name'] == 'Wednesday'])

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 10px 2px 6px 2px'>
      <div style='font-size:24px;font-weight:700;color:#1e293b;font-family:"DM Sans",sans-serif'>Amber 85</div>
      <div style='font-size:10px;color:#94a3b8;margin-top:1px'>Buffet · Mar 2026</div>
    </div>
    <hr style='border:1px solid #e2e8f0;margin:6px 0 8px 0'>
    <div style='font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#94a3b8;padding: 0 2px;margin-bottom:4px'>Navigation</div>
    """, unsafe_allow_html=True)

    pages = {
        "Overview": "overview",
        "Per-Day Breakdown": "perday",
        "Task 1 - Staff Comments": "task1",
        "Task 2 - Proposed Actions": "task2",
        "Task 3 - Recommendation": "task3",
    }

    if "page" not in st.session_state:
        st.session_state.page = "overview"

    for label, key in pages.items():
        is_active = st.session_state.page == key
        if st.button(label, key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.page = key
            st.rerun()

page = st.session_state.page


# PAGE: OVERVIEW

if page == "overview":
    st.markdown(f'<div class="page-title">Overview Dashboard</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">{date_range} · {num_days} days · Atmind Data Analytics Test 2026</div>', unsafe_allow_html=True)

    # 1. KPI Cards
    walkaway_trend = f"{wa_wknd} on weekends"
    queue_trend = f"{q_wknd} on weekends"

    k = st.columns(6)
    k[0].metric("Total Groups", str(total_groups))
    k[1].metric("Total Pax", str(total_pax))
    k[2].metric("Walk-aways", str(total_walkaways), walkaway_trend, delta_color="inverse")
    k[3].metric("Groups Queued", str(total_queued), queue_trend, delta_color="inverse")
    k[4].metric("Walk-in Avg Meal", f"{avg_meal_wi:.0f} min", f"{diff_meal:.0f} min > In-house", delta_color="inverse")
    k[5].metric("In-house Avg Meal", f"{avg_meal_ih:.0f} min")

    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # 2. กราฟภาพรวมจำนวนกลุ่มต่อวัน
    with col1:
        st.markdown('<div class="section-label">Groups per Day</div>', unsafe_allow_html=True)
        gpd = df.groupby(['day_name','is_weekend']).size().reset_index(name='Groups')
        gpd.columns = ['Day','Wknd','Groups']
        gpd['do'] = gpd['Day'].map({d: i for i, d in enumerate(DAY_ORDER)})
        gpd = gpd.sort_values('do')
        fig = go.Figure(go.Bar(
            x=gpd['Day'], y=gpd['Groups'],
            marker_color=[DAY_COLORS.get(d, BLUE) for d in gpd['Day']], width=0.5,
            text=gpd['Groups'], textposition='outside',
            textfont=dict(color='#1e293b', size=12, family='DM Mono'), hoverinfo='none'
        ))
        fig.update_layout(**BASE, title="Groups Served Per Day", showlegend=False,
                          xaxis_title="Groups", yaxis_title="Groups Served Per Day",
                          xaxis=ax(type='category'), yaxis=ax(range=[0, max(gpd['Groups'])*1.2]))
        st.plotly_chart(fig, use_container_width=True)

    # 3. กราฟสัดส่วน Walk-in vs In-house
    with col2:
        st.markdown('<div class="section-label">Guest Type Split</div>', unsafe_allow_html=True)
        gt_day = seated.groupby(['day_name','Guest_type']).size().reset_index(name='n')
        gt_day['do'] = gt_day['day_name'].map({d: i for i, d in enumerate(DAY_ORDER)})
        gt_day = gt_day.sort_values('do')
        fig2 = go.Figure()
        for gt, col in [('In-house', BLUE), ('Walk-in', ORANGE)]:
            s = gt_day[gt_day['Guest_type'] == gt]
            text_vals = [str(int(v)) if v > 0 else "" for v in s['n']] # กรองค่า 0 ทิ้ง
            fig2.add_trace(go.Bar(name=gt, x=s['day_name'], y=s['n'], marker_color=col, width=0.35,
                                  text=text_vals, textposition='inside',
                                  textfont=dict(color='#ffffff', size=12, family='DM Mono'),hoverinfo='none'))
        fig2.update_layout(**BASE, title="Walk-in vs In-house Per Day", barmode='stack', yaxis_title="Groups", yaxis=ax())
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    # 4. กราฟกระจายตัวระยะเวลาทานอาหาร
    with col3:
        st.markdown('<div class="section-label">Meal Duration Distribution</div>', unsafe_allow_html=True)
        fig3 = go.Figure()
        for gt, col in [('Walk-in', ORANGE), ('In-house', BLUE)]:
            s = seated[seated['Guest_type'] == gt]
            fig3.add_trace(go.Histogram(name=gt, x=s['meal_min'], 
                                        xbins=dict(start=0, end=400, size=15), # 🌟 บังคับแท่งกว้าง 15 นาทีเท่ากัน
                                        marker_color=col, opacity=0.7,
                                        hovertemplate="%{x} min<br>%{y} groups<br>" + gt + "<extra></extra>"))
        fig3.add_vline(x=90, line_dash='dash', line_color=RED, line_width=1.5, annotation_text="90 min", annotation_font_color=RED, annotation_font_size=11)
        fig3.update_layout(**BASE, title="Meal Duration - Walk-in Sits Longer", barmode='overlay', xaxis_title="Duration (min)", yaxis_title="Groups", yaxis=ax())
        st.plotly_chart(fig3, use_container_width=True)

    # 5. กราฟภาพรวมโต๊ะที่ถูกใช้งานรายชั่วโมง
    with col4:
        st.markdown('<div class="section-label">Tables Occupied Per Hour (All Days)</div>', unsafe_allow_html=True)
        tbl = df_tables[df_tables['meal_min'].notna()].groupby(['day_name','hour'])['table_no.'].nunique().reset_index()
        tbl['do'] = tbl['day_name'].map({d: i for i, d in enumerate(DAY_ORDER)})
        tbl = tbl.sort_values(['do','hour'])
        fig4 = go.Figure()
        for day in DAY_ORDER:
            s = tbl[tbl['day_name'] == day]
            fig4.add_trace(go.Scatter(name=day, x=s['hour'], y=s['table_no.'], mode='lines+markers',
                                      line=dict(color=DAY_COLORS.get(day, BLUE), width=2), marker=dict(size=4),
                                      hovertemplate="%{x}:00<br>%{y} Tables<extra></extra>"))
        fig4.add_hline(y=28, line_dash='dash', line_color=RED, line_width=1, annotation_text="~Full capacity (28)", annotation_font_color=RED, annotation_font_size=10)
        fig4.update_layout(**BASE, title="Tables in Use by Hour - Busy Every Day", xaxis_title="Time (hour)", yaxis_title="Tables", xaxis=ax(tickmode='linear', dtick=1), yaxis=ax())
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <b style="color:#1e293b">Key Observations:</b><br>
    • Walk-aways happen mostly on weekends (<b style="color:#ef4444">{wa_wknd} groups</b> on Sat/Sun). Weekdays have only {wa_wkdy} walk-aways.<br>
    • Walk-in guests sit for <b style="color:#f97316">{avg_meal_wi:.1f} min</b> on average. In-house guests sit for <b style="color:#2563eb">{avg_meal_ih:.1f} min</b>.<br>
    • The Indoor zone is full from 6 AM to 11 AM, which means there are no tables for In-house guests.
    </div>
    """, unsafe_allow_html=True)


# PAGE: PER-DAY BREAKDOWN

elif page == "perday":
    st.markdown('<div class="page-title">Per-Day Breakdown</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Select a day to explore detailed metrics</div>', unsafe_allow_html=True)

    # ตัวเลือกกรองข้อมูลตามวัน
    day_options = ["All Days"] + DAY_ORDER
    sel_day = st.selectbox("Select Day", day_options, index=0)

    if sel_day == "All Days":
        df_day = df.copy()
        df_tables_day = df_tables.copy()
        seated_day = seated.copy()
        wi_day = wi.copy()
        ih_day = ih.copy()
        queued_day = queued.copy()
        day_label = "All Days (5 Days Combined)"
    else:
        df_day = df[df['day_name'] == sel_day]
        df_tables_day = df_tables[df_tables['day_name'] == sel_day]
        seated_day = seated[seated['day_name'] == sel_day]
        wi_day = wi[wi['day_name'] == sel_day]
        ih_day = ih[ih['day_name'] == sel_day]
        queued_day = queued[queued['day_name'] == sel_day]
        date_str = df_day['date'].iloc[0].strftime('%b %d, %Y') if len(df_day) > 0 else ""
        is_wknd = sel_day in ('Saturday', 'Sunday')
        wknd_pill = f'<span class="day-pill {"pill-weekend" if is_wknd else "pill-weekday"}">{"Weekend" if is_wknd else "Weekday"}</span>'
        day_label = f"{sel_day} {date_str} {wknd_pill}"

    st.markdown(f"<div style='font-size:13px;color:#475569;margin-bottom:12px'>{day_label}</div>", unsafe_allow_html=True)

    # คำนวณ KPI เฉพาะวันที่เลือก
    d_groups   = len(df_day)
    d_pax      = int(df_day['pax'].sum())
    d_walkaway = int(df_day['is_walkaway'].sum())
    d_queued   = int(df_day['is_queued'].sum())
    d_wi_avg   = round(wi_day['meal_min'].mean(), 1) if len(wi_day) > 0 else 0
    d_ih_avg   = round(ih_day['meal_min'].mean(), 1) if len(ih_day) > 0 else 0

    if d_wi_avg > 0 and d_ih_avg > 0:
        d_diff = abs(d_wi_avg - d_ih_avg)
        wi_delta_text = f"{d_diff:.0f} min > In-house"
    else:
        wi_delta_text = None

    k = st.columns(6)
    k[0].metric("Total Groups", str(d_groups))
    k[1].metric("Total Pax", str(d_pax))
    k[2].metric("Walk-aways", str(d_walkaway))
    k[3].metric("Groups Queued", str(d_queued))
    
    if wi_delta_text:
        k[4].metric("Walk-in Avg Meal",  f"{d_wi_avg:.0f} min", wi_delta_text, delta_color="inverse")
    else:
        k[4].metric("Walk-in Avg Meal",  f"{d_wi_avg:.0f} min" if d_wi_avg else "N/A")
        
    k[5].metric("In-house Avg Meal", f"{d_ih_avg:.0f} min" if d_ih_avg else "N/A")

    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-label">Groups Active by Hour</div>', unsafe_allow_html=True)
        hourly = (df_day[df_day['meal_min'].notna()]
                  .groupby(['hour','Guest_type']).size().unstack('Guest_type', fill_value=0).reset_index())
        fig = go.Figure()
        for gt, col in [('In-house', BLUE), ('Walk-in', ORANGE)]:
            if gt in hourly.columns:
                fig.add_trace(go.Bar(name=gt, x=hourly['hour'], y=hourly[gt],
                                     marker_color=col, width=0.35, text=hourly[gt], textposition='outside',
                                     textfont=dict(color='#1e293b', size=10, family='DM Mono'), hoverinfo='none'))
        fig.update_layout(**BASE, title="Groups Seated by Hour", barmode='group',
                          xaxis_title="Time (hour)", yaxis_title="Groups",
                          xaxis=ax(tickmode='linear', dtick=1), yaxis=ax(range=[0, max(hourly.max(numeric_only=True))*1.2 if not hourly.empty else 10]))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-label">Meal Duration Distribution</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        for gt, col in [('Walk-in', ORANGE), ('In-house', BLUE)]:
            s = seated_day[seated_day['Guest_type'] == gt]
            if len(s) > 0:
                fig2.add_trace(go.Histogram(name=gt, x=s['meal_min'],
                                            xbins=dict(start=0, end=400, size=15), # 🌟 บังคับแท่งกว้าง 15 นาทีเท่ากัน
                                            marker_color=col, opacity=0.75,
                                            hovertemplate="%{x} min<br>%{y} groups<br>" + gt + "<extra></extra>"))
        fig2.add_vline(x=90, line_dash='dash', line_color=RED, line_width=1.5, annotation_text="90 min", annotation_font_color=RED, annotation_font_size=11)
        fig2.update_layout(**BASE, title="Meal Duration by Guest Type", barmode='overlay', xaxis_title="Duration (min)", yaxis_title="Groups", yaxis=ax())
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-label">Zone Usage</div>', unsafe_allow_html=True)
        zone_gt = (df_tables_day[df_tables_day['meal_min'].notna()]
                   .groupby(['zone','Guest_type'])['service_no.'].nunique().reset_index(name='n'))
        zone_gt = zone_gt[zone_gt['zone'].isin(['Indoor','Outdoor'])]
        fig3 = go.Figure()
        for gt, col in [('In-house', BLUE), ('Walk-in', ORANGE)]:
            s = zone_gt[zone_gt['Guest_type'] == gt]
            fig3.add_trace(go.Bar(name=gt, x=s['zone'], y=s['n'], marker_color=col, width=0.35, text=s['n'], textposition='outside',
                                  textfont=dict(color='#1e293b', size=12, family='DM Mono'), hoverinfo='none')) 
        fig3.update_layout(**BASE, title="Zone Usage by Guest Type", barmode='group', yaxis_title="Groups", yaxis=ax(range=[0, max(zone_gt['n'])*1.3 if not zone_gt.empty else 10]))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        if d_queued > 0 and len(queued_day) > 0:
            st.markdown('<div class="section-label">Queue Wait Time</div>', unsafe_allow_html=True)
            fig4 = go.Figure()
            for gt, col in [('In-house', BLUE), ('Walk-in', ORANGE)]:
                s = queued_day[queued_day['Guest_type'] == gt]
                if len(s) > 0:
                    fig4.add_trace(go.Histogram(name=gt, x=s['wait_min'], nbinsx=12, marker_color=col, opacity=0.75, hovertemplate="%{x} min<br>%{y} groups<br>" + gt + "<extra></extra>"))
            fig4.update_layout(**BASE, title="Queue Wait Time Distribution", barmode='overlay', xaxis_title="Wait (min)", yaxis_title="Groups", yaxis=ax())
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.markdown('<div class="section-label">Queue Status</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="verdict-true" style="margin-top:32px">
            No queuing on this day. All guests were seated directly.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='div'>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Group-Level Summary</div>', unsafe_allow_html=True)
    
    # ตารางดูข้อมูลดิบระดับกลุ่ม
    with st.expander("View Raw Group-Level Data (Click to expand)"):
        summary_cols = ['day_name','service_no.','pax','Guest_type','zone','wait_min','meal_min','is_walkaway']
        show_df = df_day[summary_cols].copy()
        show_df.columns = ['Day','Service#','Pax','Guest Type','Zone','Wait (min)','Meal (min)','Walk-away']
        show_df['Wait (min)'] = show_df['Wait (min)'].round(1)
        show_df['Meal (min)'] = show_df['Meal (min)'].round(1)
        st.dataframe(show_df, use_container_width=True, height=280)


# TASK 1

elif page == "task1":
    st.markdown('<div class="page-title">Task 1 - Staff Comments Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Verify each staff comment with data evidence</div>', unsafe_allow_html=True)

    # ── Comment 1: เรื่องการรอคิวและ Walk-away ──────────────────
    st.markdown('<div class="section-label">Comment 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="comment-card">"In-house customers are unhappy that they have to wait for a table. Walk-in customers are also unhappy — queue up for a long time and leave."</div>', unsafe_allow_html=True)
    
    st.markdown(
        f'<div class="verdict-true">TRUE. In-house guests wait {avg_wait_ih} minutes on average. Walk-in guests wait {avg_wait_wi} minutes. There were {total_walkaways} walk-aways.</div>',
        unsafe_allow_html=True
    )
    st.markdown(f"""
    <div class="verdict-warn">NOTE: Most walk-aways happen on weekends ({wa_wknd} groups). Weekdays only have {wa_wkdy} walk-aways and {q_wkdy} queued groups. Long wait times are mostly a weekend problem.</div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        # กราฟแสดงเวลารอคิวเฉลี่ย
        wq = queued.groupby('Guest_type')['wait_min'].mean().reset_index()
        fig = go.Figure(go.Bar(
            x=wq['Guest_type'], y=wq['wait_min'].round(1), marker_color=[BLUE, ORANGE], width=0.4,
            text=wq['wait_min'].round(1).astype(str), textposition='outside', textfont=dict(color='#1e293b', size=13, family='DM Mono'), hoverinfo='none' 
        ))
        fig.update_layout(**BASE, title="Avg Queue Wait Time (Queued Groups Only)", yaxis_title="Wait (min)", showlegend=False, yaxis=ax(range=[0, 52]))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # กราฟแสดงยอด Walk-away แยกตามวัน
        wa = df[df['is_walkaway']].groupby(['day_name','Guest_type']).size().reset_index(name='n')
        wa['do'] = wa['day_name'].map({d: i for i, d in enumerate(DAY_ORDER)})
        wa = wa.sort_values('do')
        fig2 = go.Figure()
        for gt, col in [('In-house', BLUE), ('Walk-in', ORANGE)]:
            s = wa[wa['Guest_type'] == gt]
            if len(s) > 0:
                fig2.add_trace(go.Bar(name=gt, x=s['day_name'], y=s['n'], marker_color=col, width=0.35, text=s['n'], textposition='outside', textfont=dict(color='#1e293b', size=12, family='DM Mono'), hoverinfo='none')) 
        fig2.update_layout(**BASE, title="Walk-aways by Day", barmode='group', yaxis_title="Groups", yaxis=ax(range=[0, max(wa['n'])*1.3 if not wa.empty else 16]))
        st.plotly_chart(fig2, use_container_width=True)

    # กราฟแสดงช่วงเวลาที่มีคน Walk-away มากที่สุด
    wa_df = df[df['is_walkaway']].copy()
    wa_df['q_hour'] = pd.to_datetime(wa_df['queue_start']).dt.hour
    wa_hour = wa_df.groupby(['q_hour','Guest_type']).size().unstack('Guest_type', fill_value=0).reset_index()
    fig_wa = go.Figure()
    for gt, col in [('In-house', BLUE), ('Walk-in', ORANGE)]:
        if gt in wa_hour.columns:
            text_vals = [str(int(v)) if v > 0 else "" for v in wa_hour[gt]] 
            fig_wa.add_trace(go.Bar(name=gt, x=wa_hour['q_hour'], y=wa_hour[gt], marker_color=col, width=0.4, text=text_vals, textposition='inside', textfont=dict(color='#ffffff', size=12, family='DM Mono'), hoverinfo='none')) 
    fig_wa.update_layout(**BASE, title="Walk-aways by Hour - Peak Abandonment Window", barmode='stack', xaxis_title="Time (hour)", yaxis_title="Walk-aways", xaxis=ax(tickmode='linear', dtick=1), yaxis=ax(range=[0, 12]))
    st.plotly_chart(fig_wa, use_container_width=True)

    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    # ── Comment 2: เรื่องปริมาณลูกค้าในวันธรรมดา ──────────────────
    st.markdown('<div class="section-label">Comment 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="comment-card">"We are very busy every day of the week. Impossible to sustain this."</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="verdict-true">TRUE. Weekdays are almost as busy as weekends. For example, Tuesday has {tue_g} groups and Wednesday has {wed_g} groups, which is close to Friday ({fri_g} groups). The restaurant is near full capacity every day.</div>', unsafe_allow_html=True)

    c2a, c2b = st.columns(2)
    with c2a:
        # กราฟเปรียบเทียบจำนวนกลุ่มที่มารับบริการในแต่ละวัน
        gpd = df.groupby(['day_name','is_weekend']).size().reset_index(name='Groups')
        gpd.columns = ['Day','Wknd','Groups']
        gpd['do'] = gpd['Day'].map({d: i for i, d in enumerate(DAY_ORDER)})
        gpd = gpd.sort_values('do')
        fig3 = go.Figure(go.Bar(
            x=gpd['Day'], y=gpd['Groups'], marker_color=[DAY_COLORS.get(d, BLUE) for d in gpd['Day']], width=0.5, text=gpd['Groups'], textposition='outside', textfont=dict(color='#1e293b', size=13, family='DM Mono'), hoverinfo='none' 
        ))
        fig3.update_layout(**BASE, title="Groups Per Day - High Volume Every Day", showlegend=False, yaxis_title="Groups", yaxis=ax(range=[0, 105]))
        st.plotly_chart(fig3, use_container_width=True)

    with c2b:
        # กราฟเปรียบเทียบจำนวน Pax รวมในแต่ละวัน
        pax_day = df[df['pax'] > 0].groupby(['day_name','Guest_type'])['pax'].sum().reset_index()
        pax_day['do'] = pax_day['day_name'].map({d: i for i, d in enumerate(DAY_ORDER)})
        pax_day = pax_day.sort_values('do')
        fig3b = go.Figure()
        for gt, col in [('In-house', BLUE), ('Walk-in', ORANGE)]:
            s = pax_day[pax_day['Guest_type'] == gt]
            text_vals = [str(int(v)) if v > 0 else "" for v in s['pax']] 
            fig3b.add_trace(go.Bar(name=gt, x=s['day_name'], y=s['pax'], marker_color=col, text=text_vals, textposition='inside', textfont=dict(color='#ffffff', size=12, family='DM Mono'), hoverinfo='none')) 
        fig3b.update_layout(**BASE, title="Total Pax Per Day - Busy Across All Days", barmode='stack', yaxis_title="Pax", yaxis=ax())
        st.plotly_chart(fig3b, use_container_width=True)

    # กราฟแสดงปริมาณโต๊ะที่ใช้แยกรายชั่วโมง
    tbl2 = df_tables[df_tables['meal_min'].notna()].groupby(['day_name','hour'])['table_no.'].nunique().reset_index()
    tbl2['do'] = tbl2['day_name'].map({d: i for i, d in enumerate(DAY_ORDER)})
    tbl2 = tbl2.sort_values(['do','hour'])
    fig_occ = go.Figure()
    for day in DAY_ORDER:
        s = tbl2[tbl2['day_name'] == day]
        fig_occ.add_trace(go.Scatter(name=day, x=s['hour'], y=s['table_no.'], mode='lines+markers', line=dict(color=DAY_COLORS[day], width=2), marker=dict(size=5), hovertemplate="%{x}:00<br>%{y} Tables<extra></extra>")) 
    fig_occ.add_hline(y=28, line_dash='dash', line_color=RED, line_width=1.5, annotation_text="Full capacity (28 tables)", annotation_font_color=RED, annotation_font_size=11)
    fig_occ.update_layout(**BASE, title="Tables Occupied Per Hour - Near-Full Capacity Every Day", xaxis_title="Time (hour)", yaxis_title="Tables in Use", xaxis=ax(tickmode='linear', dtick=1), yaxis=ax())
    st.plotly_chart(fig_occ, use_container_width=True)

    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    # ── Comment 3: เรื่อง Walk-in นั่งแช่ ──────────────────
    st.markdown('<div class="section-label">Comment 3</div>', unsafe_allow_html=True)
    st.markdown('<div class="comment-card">"Walk-in customers sit the whole day. Not enough tables. Queue very long."</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="verdict-true">TRUE. Walk-in guests sit for {avg_meal_wi:.0f} minutes on average. This is {diff_meal:.0f} minutes longer than In-house guests. Also, {wi_over_90_pct}% of Walk-in guests stay longer than 90 minutes.</div>',
        unsafe_allow_html=True
    )

    c3, c4 = st.columns(2)
    with c3:
        # กราฟ Histogram จัดกลุ่มเวลา 60, 90, 120 นาที
        bins = [0, 60, 90, 120, 150, 999]
        labels = ['≤60', '61-90', '91-120', '121-150', '>150']
        wi2 = wi.copy()
        wi2['g'] = pd.cut(wi2['meal_min'], bins=bins, labels=labels)
        dist = wi2['g'].value_counts().reindex(labels).reset_index()
        dist.columns = ['Dur','N']
        fig4 = go.Figure(go.Bar(
            x=dist['Dur'], y=dist['N'], marker_color=[GREEN, TEAL, ORANGE, RED, RED], width=0.55,
            text=dist['N'], textposition='outside', textfont=dict(color='#1e293b', size=12, family='DM Mono'), hoverinfo='none' 
        ))
        fig4.add_vline(x=2.5, line_dash='dash', line_color=RED, line_width=2, annotation_text=f"{wi_over_90_pct}% stay >90 min", annotation_font_color=RED, annotation_font_size=11, annotation_position="top right")
        fig4.update_layout(**BASE, title=f"Walk-in Duration - {wi_over_90_pct}% Stay >90 Min", showlegend=False, yaxis_title="Groups", yaxis=ax(range=[0, 100]))
        st.plotly_chart(fig4, use_container_width=True)

    with c4:
        # กราฟ Scatter แสดงพฤติกรรมนั่งแต่เช้า
        wi_scatter = wi.copy()
        wi_scatter['start_h'] = pd.to_datetime(wi_scatter['meal_start']).dt.hour + pd.to_datetime(wi_scatter['meal_start']).dt.minute / 60
        wi_scatter['time_str'] = wi_scatter['meal_start'].dt.strftime('%H:%M')

        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=wi_scatter['start_h'], y=wi_scatter['meal_min'], mode='markers', marker=dict(color=ORANGE, size=6, opacity=0.6),
            name='Walk-in group', customdata=wi_scatter['time_str'], hovertemplate="Start: %{customdata}<br>Duration: %{y} min<extra></extra>" 
        ))
        fig5.add_hline(y=90, line_dash='dash', line_color=RED, line_width=1.5, annotation_text="90 min limit", annotation_font_color=RED, annotation_font_size=10)
        fig5.update_layout(**BASE, title="Walk-in: Start Time vs Duration - Early Sitters Stay Longest", xaxis_title="Start Time (hour)", yaxis_title="Duration (min)", xaxis=ax(range=[5.5, 12.5], tickmode='linear', dtick=1), yaxis=ax(range=[0, wi['meal_min'].max() * 1.1]))
        st.plotly_chart(fig5, use_container_width=True)

    # กราฟเปรียบเทียบสถิติ (Mean, Median, 75th percentile)
    metrics_ = ['Avg', 'Median', '75th pct', 'Max']
    wi_vals  = [round(wi['meal_min'].mean()), round(wi['meal_min'].median()), round(wi['meal_min'].quantile(0.75)), round(wi['meal_min'].max())]
    ih_vals  = [round(ih['meal_min'].mean()), round(ih['meal_min'].median()), round(ih['meal_min'].quantile(0.75)), round(ih['meal_min'].max())]
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(name='Walk-in', x=metrics_, y=wi_vals, marker_color=ORANGE, width=0.35, text=wi_vals, textposition='outside', textfont=dict(color='#1e293b', size=11, family='DM Mono'), hoverinfo='none')) 
    fig6.add_trace(go.Bar(name='In-house', x=metrics_, y=ih_vals, marker_color=BLUE, width=0.35, text=ih_vals, textposition='outside', textfont=dict(color='#1e293b', size=11, family='DM Mono'), hoverinfo='none')) 
    fig6.update_layout(**BASE, title="Meal Duration Stats - Walk-in Consistently Longer", barmode='group', yaxis_title="Duration (min)", yaxis=ax(range=[0, max(max(wi_vals), max(ih_vals)) * 1.2]))
    st.plotly_chart(fig6, use_container_width=True)


# TASK 2

elif page == "task2":
    st.markdown('<div class="page-title">Task 2 - Why Proposed Actions Won\'t Work</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Disprove each recommended action with data</div>', unsafe_allow_html=True)

    # ── Action 1: ลดเวลาทาน ──────────────────────────────
    st.markdown('<div class="section-label">Action 1 - Reduce Seating Time (5hr to less)</div>', unsafe_allow_html=True)
    st.markdown('<div class="verdict-false">NOT ENOUGH. A shorter time limit will upset In-house guests too. It also does not fix the main problems, which are slow table turnover and too many guests on weekends.</div>', unsafe_allow_html=True)

    c1a, c1b = st.columns(2)
    with c1a:
        # กราฟแท่งจำลองผลกระทบหากลดเวลาทานลงเหลือ 60-180 นาที
        limits = [60, 90, 120, 150, 180]
        wi_aff = [(wi['meal_min'] > l).sum() for l in limits]
        ih_aff = [(ih['meal_min'] > l).sum() for l in limits]
        limits_str = [str(l) for l in limits]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Walk-in', x=limits_str, y=wi_aff, marker_color=ORANGE, width=0.35, text=wi_aff, textposition='outside', textfont=dict(color='#1e293b', size=12, family='DM Mono'), hoverinfo='none')) 
        fig.add_trace(go.Bar(name='In-house', x=limits_str, y=ih_aff, marker_color=BLUE, width=0.35, text=ih_aff, textposition='outside', textfont=dict(color='#1e293b', size=12, family='DM Mono'), hoverinfo='none')) 
        fig.update_layout(**BASE, title="Groups Affected by Each Time Limit", barmode='group', yaxis_title="Groups", xaxis_title="Seating Limit (min)", xaxis=ax(type='category'), yaxis=ax(range=[0, max(wi_aff)*1.3 if len(wi_aff) > 0 else 150]))
        st.plotly_chart(fig, use_container_width=True)

    with c1b:
        # กราฟเส้นแสดงภาพรวมกลุ่มลูกค้าทั้งหมดที่จะได้รับผลกระทบ
        rev_risk = []
        for lim in limits:
            wi_cut = (wi['meal_min'] > lim).sum()
            ih_cut = (ih['meal_min'] > lim).sum()
            rev_risk.append({'limit': str(lim), 'total_affected': wi_cut + ih_cut})
        rdf = pd.DataFrame(rev_risk)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=rdf['limit'], y=rdf['total_affected'], mode='lines+markers+text', line=dict(color=RED, width=2.5), marker=dict(size=8, color=RED), text=rdf['total_affected'], textposition='top center', textfont=dict(color='#1e293b', size=11, family='DM Mono'), name='Total Affected', hoverinfo='none')) 
        fig2.update_layout(**BASE, title="Total Groups Affected vs Time Limit", xaxis_title="Seating Limit (min)", yaxis_title="Groups Affected", xaxis=ax(type='category'), showlegend=False, yaxis=ax(range=[0, max(rdf['total_affected'])*1.3 if len(rdf) > 0 else 250]))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <b style="color:#1e293b">Why it fails:</b> A 90-minute limit affects {wi_over_90} Walk-in groups ({wi_over_90_pct}%) and {ih_over_90} In-house groups. This punishes hotel guests who already paid for their stay. A 60-minute limit is too rushed for everyone. Also, the real issue is the high number of guests on weekends, not just how long they sit.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    # ── Action 2: เพิ่มราคา ──────────────────────────────
    st.markdown('<div class="section-label">Action 2 - Increase Price to 259 Every Day</div>', unsafe_allow_html=True)
    st.markdown('<div class="verdict-false">WILL NOT WORK. Higher prices do not make people eat faster. Adding 100฿ on weekdays only hurts loyal In-house guests and does not free up more tables.</div>', unsafe_allow_html=True)

    c2a, c2b = st.columns(2)
    with c2a:
        # กราฟ Scatter ดูความสัมพันธ์ระหว่าง ราคาวันธรรมดา/หยุด กับ ระยะเวลาทาน
        price_meal = (seated.groupby(['day_name','is_weekend','Guest_type'])['meal_min'].mean().round(1).reset_index())
        price_meal['price'] = price_meal['is_weekend'].map({True: 199, False: 159})
        price_meal_wi = price_meal[price_meal['Guest_type'] == 'Walk-in']
        price_meal_ih = price_meal[price_meal['Guest_type'] == 'In-house']

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=price_meal_wi['price'], y=price_meal_wi['meal_min'], mode='markers+text', name='Walk-in', marker=dict(color=ORANGE, size=14), text=price_meal_wi['day_name'], textposition='top center', textfont=dict(color='#c9d1d9', size=10), hovertemplate="Price: %{x} ฿<br>Duration: %{y} min<extra></extra>"))
        fig3.add_trace(go.Scatter(x=price_meal_ih['price'], y=price_meal_ih['meal_min'], mode='markers+text', name='In-house', marker=dict(color=BLUE, size=14), text=price_meal_ih['day_name'], textposition='top center', textfont=dict(color='#c9d1d9', size=10), hovertemplate="Price: %{x} ฿<br>Duration: %{y} min<extra></extra>"))
        fig3.add_vline(x=259, line_dash='dot', line_color=YELLOW, line_width=1, annotation_text="Proposed: 259฿", annotation_font_color=YELLOW, annotation_font_size=10)
        fig3.update_layout(**BASE, title="Price vs Meal Duration - No Correlation", xaxis_title="Price (฿)", yaxis_title="Avg Meal Duration (min)", xaxis=ax(range=[140, 275]), yaxis=ax(range=[30, 100]))
        st.plotly_chart(fig3, use_container_width=True)

    with c2b:
        # กราฟแท่ง Stack จำลองผลกระทบส่วนต่าง 100 บาท ต่อกลุ่มลูกค้า
        segs  = ['Walk-in\nWeekend', 'Walk-in\nWeekday', 'In-house\nWeekend', 'In-house\nWeekday']
        old_p = [199, 159, 199, 159]
        cols_ = [ORANGE, ORANGE, BLUE, BLUE]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name='Current Price', x=segs, y=old_p, marker_color='#e2e8f0', text=[f'{p}฿' for p in old_p], textposition='inside', textfont=dict(color='#8b949e', size=12), hoverinfo='none')) 
        fig4.add_trace(go.Bar(name='+100฿ Hike', x=segs, y=[259 - p for p in old_p], marker_color=cols_, text=[f'+{259-p}฿' for p in old_p], textposition='inside', textfont=dict(color='#ffffff', size=12, family='DM Mono'), hoverinfo='none')) 
        fig4.update_layout(**BASE, title="Price Hike Impact by Segment", barmode='stack', yaxis_title="Price (฿)", yaxis=ax(range=[0, 310]))
        st.plotly_chart(fig4, use_container_width=True)

    wi_wknd_avg = round(wi[wi['is_weekend']]['meal_min'].mean()) if not wi[wi['is_weekend']].empty else 0
    wi_wkdy_avg = round(wi[~wi['is_weekend']]['meal_min'].mean()) if not wi[~wi['is_weekend']].empty else 0

    st.markdown(f"""
    <div class="insight-box">
    <b style="color:#1e293b">Why it fails:</b> Weekend Walk-in guests pay 199฿ and sit for ~{wi_wknd_avg} mins. Weekday Walk-in guests pay 159฿ and sit for ~{wi_wkdy_avg} mins. The price difference does not change how long they stay. Raising the price to 259฿ means a big increase for weekday and In-house guests. This will upset them but won't solve the table shortage.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    # ── Action 3: แทรกคิว ──────────────────────────────
    st.markdown('<div class="section-label">Action 3 - Queue Skipping for In-house Guests</div>', unsafe_allow_html=True)
    st.markdown('<div class="verdict-false">NOT ENOUGH. Skipping the queue does not help if there are no empty tables. The Indoor zone is full almost all morning.</div>', unsafe_allow_html=True)

    c3a, c3b = st.columns(2)
    with c3a:
        # กราฟเวลารอคิว
        fig5 = go.Figure()
        for gt, col in [('In-house', BLUE), ('Walk-in', ORANGE)]:
            s = queued[queued['Guest_type'] == gt]
            if len(s) > 0:
                fig5.add_trace(go.Histogram(name=gt, x=s['wait_min'], nbinsx=12, marker_color=col, opacity=0.75, hovertemplate="%{x} min<br>%{y} groups<br>" + gt + "<extra></extra>")) 
        fig5.update_layout(**BASE, title=f"Queue Wait - In-house Still Waits {avg_wait_ih} min Avg", barmode='overlay', xaxis_title="Wait (min)", yaxis_title="Groups", yaxis=ax())
        st.plotly_chart(fig5, use_container_width=True)

    with c3b:
        # กราฟแสดงปริมาณการใช้โต๊ะโซน Indoor พิสูจน์ว่าโต๊ะเต็มความจุ
        indoor_by_hour = (df_tables[df_tables['meal_min'].notna() & (df_tables['zone'] == 'Indoor')]
                          .groupby('hour')['table_no.'].nunique().reset_index())
        indoor_by_hour.columns = ['hour', 'tables_used']
        indoor_by_hour['capacity_pct'] = (indoor_by_hour['tables_used'] / 12 * 100).round(0)

        fig6 = go.Figure()
        fig6.add_trace(go.Bar(x=indoor_by_hour['hour'], y=indoor_by_hour['tables_used'],
                              marker_color=[RED if v >= 12 else ORANGE if v >= 10 else BLUE
                                            for v in indoor_by_hour['tables_used']],
                              width=0.6,
                              text=[f"{v}/12" for v in indoor_by_hour['tables_used']],
                              textposition='outside',
                              textfont=dict(color='#1e293b', size=11, family='DM Mono'),
                              hoverinfo='none')) 
        fig6.add_hline(y=12, line_dash='dash', line_color=RED, line_width=1.5)
        
        fig6.update_layout(**BASE, title="Indoor Zone Occupancy by Hour - At Capacity All Morning",
                           xaxis_title="Time (hour)", yaxis_title="Tables in Use",
                           xaxis=ax(tickmode='linear', dtick=1),
                           yaxis=ax(range=[0, 20]), showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)

    # กราฟแสดงสัดส่วน Guest Type ในแต่ละ Zone
    zone_gt = (df[df['meal_min'].notna()].groupby(['zone','Guest_type']).size().reset_index(name='n'))
    zone_gt = zone_gt[zone_gt['zone'].isin(['Indoor','Outdoor'])]
    fig7 = go.Figure()
    for gt, col in [('In-house', BLUE), ('Walk-in', ORANGE)]:
        s = zone_gt[zone_gt['Guest_type'] == gt]
        fig7.add_trace(go.Bar(name=gt, x=s['zone'], y=s['n'], marker_color=col, width=0.35, text=s['n'], textposition='outside', textfont=dict(color='#1e293b', size=12, family='DM Mono'), hoverinfo='none')) 
    fig7.update_layout(**BASE, title="Walk-in Occupies Indoor Zone - Competing with In-house", barmode='group', yaxis_title="Groups", yaxis=ax(range=[0, max(zone_gt['n'])*1.3 if not zone_gt.empty else 180]))
    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b style="color:#1e293b">Why it fails:</b> The Indoor zone is full (12/12 tables) starting from 6 AM. Walk-in guests use many of these tables. If In-house guests skip the line, they still have nowhere to sit. The real problem is a lack of reserved tables for In-house guests.
    </div>
    """, unsafe_allow_html=True)


# TASK 3

elif page == "task3":
    st.markdown('<div class="page-title">Task 3 - Recommended Solution</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Build on Action 3 - but make it actually work</div>', unsafe_allow_html=True)

    st.markdown('<div class="verdict-rec">RECOMMENDATION: Reserve the Indoor Zone only for In-house guests. Add a gentle 90-minute time limit for Walk-in guests in the Outdoor Zone.</div>', unsafe_allow_html=True)

    wi_under_90 = wi_total - wi_over_90

    # ประเมินผลลัพธ์ของ Recommendation
    km = st.columns(4)
    km[0].metric("Affected Walk-ins", f"{wi_over_90_pct}%", f"{wi_over_90} groups (>90 min)")
    km[1].metric("Unaffected Walk-ins", f"{wi_under_pct}%", f"{wi_under_90} groups (leave naturally)")
    km[2].metric("Recovered Time", f"~{table_min_saved:,} min", f"over {num_days} days")
    km[3].metric("Extra Capacity", f"~{extra_turns} groups", "can be served")

    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # กราฟแสดงพฤติกรรมการแย่งโต๊ะ Indoor เพื่อ support การแบ่ง Zone
        indoor_gt_hour = (df_tables[df_tables['meal_min'].notna() & (df_tables['zone'] == 'Indoor')]
                          .groupby(['hour','Guest_type'])['service_no.'].nunique()
                          .unstack('Guest_type', fill_value=0).reset_index())
        fig1 = go.Figure()
        for gt, col in [('In-house', BLUE), ('Walk-in', ORANGE)]:
            if gt in indoor_gt_hour.columns:
                text_vals = [str(int(v)) if v > 0 else "" for v in indoor_gt_hour[gt]] 
                fig1.add_trace(go.Bar(name=gt, x=indoor_gt_hour['hour'], y=indoor_gt_hour[gt], marker_color=col, width=0.35, text=text_vals, textposition='inside', textfont=dict(color='#ffffff', size=12, family='DM Mono'), hoverinfo='none')) 
        fig1.update_layout(**BASE, title="Indoor Zone: Walk-in Takes In-house Tables", barmode='stack', xaxis_title="Time (hour)", yaxis_title="Groups in Indoor", xaxis=ax(tickmode='linear', dtick=1), yaxis=ax())
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # เปรียบเทียบผลกระทบจำกัด 90 นาทีต่อกลุ่ม Walk-in
        fig2 = go.Figure(go.Bar(
            x=['Leave naturally\n(≤90 min)', 'Affected by\n90-min limit (>90 min)'],
            y=[(wi_total - wi_over_90), wi_over_90], marker_color=[GREEN, ORANGE], width=0.35,
            text=[f'{(wi_total - wi_over_90)} groups\n({wi_under_pct}%)', f'{wi_over_90} groups\n({wi_over_90_pct}%)'], textposition='outside', textfont=dict(color='#1e293b', size=12, family='DM Mono'), hoverinfo='none' 
        ))
        fig2.update_layout(**BASE, title=f"90-Min Limit Impact - {wi_under_pct}% of Walk-in Unaffected", showlegend=False, yaxis_title="Groups", yaxis=ax(range=[0, max((wi_total - wi_over_90), wi_over_90) * 1.3 if wi_total > 0 else 100]))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # กราฟแสดงความหนาแน่นรายชั่วโมง
        hourly_all = (df[df['meal_min'].notna()].groupby(['hour','Guest_type']).size().unstack('Guest_type', fill_value=0).reset_index())
        hours = hourly_all['hour'].tolist() if not hourly_all.empty else []
        ih_cnt = hourly_all.get('In-house', pd.Series([0]*len(hourly_all))).tolist() if not hourly_all.empty else []
        wi_cnt = hourly_all.get('Walk-in', pd.Series([0]*len(hourly_all))).tolist() if not hourly_all.empty else []
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name='In-house', x=hours, y=ih_cnt, marker_color=BLUE, width=0.35, text=ih_cnt, textposition='outside', textfont=dict(color='#1e293b', size=10, family='DM Mono'), hoverinfo='none')) 
        fig3.add_trace(go.Bar(name='Walk-in', x=hours, y=wi_cnt, marker_color=ORANGE, width=0.35, text=wi_cnt, textposition='outside', textfont=dict(color='#1e293b', size=10, family='DM Mono'), hoverinfo='none')) 
        fig3.add_vrect(x0=7.6, x1=9.4, fillcolor=RED, opacity=0.06, line_width=0, annotation_text="Peak pressure 8-9am", annotation_font_color=RED, annotation_font_size=10)
        fig3.update_layout(**BASE, title="All Days: Groups Active by Hour", barmode='group', xaxis_title="Time (hour)", yaxis_title="Groups", xaxis=ax(tickmode='linear', dtick=1), yaxis=ax(range=[0, max(max(ih_cnt) if ih_cnt else 0, max(wi_cnt) if wi_cnt else 0) * 1.2 + 10]))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # กราฟ Scatter จัดกลุ่มเวลาที่เกิน 90 นาที
        wi_scatter = wi.copy()
        wi_scatter['start_h'] = (pd.to_datetime(wi_scatter['meal_start']).dt.hour + pd.to_datetime(wi_scatter['meal_start']).dt.minute / 60)
        wi_scatter['time_str'] = wi_scatter['meal_start'].dt.strftime('%H:%M')

        fig4 = go.Figure()
        s_under = wi_scatter[wi_scatter['meal_min'] <= 90]
        s_over = wi_scatter[wi_scatter['meal_min'] > 90]

        fig4.add_trace(go.Scatter(x=s_under['start_h'], y=s_under['meal_min'], mode='markers', name='≤90 min', marker=dict(color=GREEN, size=6, opacity=0.7), customdata=s_under['time_str'], hovertemplate="Start: %{customdata}<br>Duration: %{y} min<extra></extra>"))
        fig4.add_trace(go.Scatter(x=s_over['start_h'], y=s_over['meal_min'], mode='markers', name='>90 min', marker=dict(color=RED, size=7, opacity=0.8), customdata=s_over['time_str'], hovertemplate="Start: %{customdata}<br>Duration: %{y} min<extra></extra>"))
        fig4.add_hline(y=90, line_dash='dash', line_color=YELLOW, line_width=1.5, annotation_text="90-min limit here", annotation_font_color=YELLOW, annotation_font_size=10)
        
        fig4.update_layout(**BASE, title=f"Walk-in Duration Scatter - Only {wi_over_90_pct}% Need Reminding", xaxis_title="Start Time (hour)", yaxis_title="Duration (min)", xaxis=ax(range=[5.5, 12.5], tickmode='linear', dtick=1), yaxis=ax(range=[0, wi['meal_min'].max() * 1.1 if not wi.empty else 100]))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<hr class='div'>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Zone Plan</div>', unsafe_allow_html=True)

    zc1, zc2 = st.columns(2)
    with zc1:
        st.markdown(f"""
<div class="zone-box-blue">
<div style='color:#2563eb;font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:10px'>Indoor - In-house Exclusive</div>
<div style='color:#475569;font-size:13px;line-height:2'>
Tables 1A/B - 6A/B &nbsp;·&nbsp; <b style="color:#1e293b">12 units</b><br>
Always reserved · No Walk-in assigned<br>
Staff escorts In-house directly - no queue<br>
<br>
<span style='color:#2563eb;font-size:12px'>→ Eliminates In-house wait time entirely<br>→ Builds on Action 3 but solves the root cause</span>
</div></div>""", unsafe_allow_html=True)

    with zc2:
        st.markdown(f"""
<div class="zone-box-orange">
<div style='color:#f97316;font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:10px'>Outdoor - Walk-in (90-min soft limit)</div>
<div style='color:#475569;font-size:13px;line-height:2'>
Tables 7-15 &nbsp;·&nbsp; <b style="color:#1e293b">17 units</b><br>
90-min guideline printed on queue card<br>
Friendly staff reminder at 80 minutes<br>
<br>
<span style='color:#f97316;font-size:12px'>→ Recovers ~{table_min_saved:,} table-minutes over {num_days} days<br>→ Only {wi_over_90_pct}% of Walk-in groups need reminder</span>
</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="insight-box">
    <b style="color:#1e293b">Why this solution works:</b><br>
    <br>
    • <b style="color:#2563eb">Fixes the real problem</b>: In-house guests need guaranteed seats, not just a shorter line. Reserving the Indoor zone gives them a place to sit immediately.<br>
    • <b style="color:#22c55e">Small impact on guests</b>: {wi_under_pct}% of Walk-in guests already leave before 90 minutes. Only {wi_over_90_pct}% ({wi_over_90} groups) will need a friendly reminder.<br>
    • <b style="color:#f59e0b">No extra costs</b>: Changing where people sit does not cost money. You can test this on weekends first.<br>
    • <b style="color:#1e293b">Normal hotel practice</b>: Reserving seats for hotel guests is normal for buffets. It is easier than changing prices or rebuilding the restaurant.<br>
    <br>
    <b style="color:#1e293b">How to start:</b> Try this on weekends first. If it works well, you can use it every day. Monitor the number of walk-aways to see if the plan is working.
    </div>
    """, unsafe_allow_html=True)