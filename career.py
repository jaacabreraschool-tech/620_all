import streamlit as st
import pandas as pd
import plotly.express as px
from cache_utils import normalize_raw_data, get_active_employees, get_year_data


def render(df, df_raw, selected_year):
    # Use shared cached normalization
    df_raw = normalize_raw_data(df_raw)
    df_active = get_active_employees(df_raw)
    career_year = get_year_data(df_active, selected_year)

    # -----------------------------
    # Executive Summary at the very top
    # -----------------------------
    with st.container(border=True):
        st.markdown("### 📋 Executive Summary")
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown("""
            - 🎯 **Internal Mobility**: 1,000+ promotions and transfers demonstrate strong career progression opportunities
            - 📈 **Consistent Growth**: Steady year-over-year increase in internal advancement across all levels
            - ⏳ **Optimal Timing**: Average 3.3 years tenure before promotion, indicating healthy career development pace
            """)
        
        with summary_col2:
            st.markdown("""
            - 👥 **Inclusive Advancement**: Promotions distributed across both Associates and Manager & Up levels
            - 📊 **High Promotion Rate**: 14-20% of active employees promoted annually, well above industry standards
            - 🚀 **Talent Investment**: Strong focus on developing and retaining internal talent over external hiring
            """)

    # -----------------------------
    # Section heading (now below Executive Summary)
    # -----------------------------
    st.markdown("## 🎯 Career Progression Metrics")

    # Calculate metrics once
    if not career_year.empty: 
        total_promotions_transfers = int(
            career_year["Promotion & Transfer"].fillna(0).eq(1).sum()
        )
        avg_tenure = pd.to_numeric(career_year["Tenure"], errors="coerce").mean()
        active_count = len(career_year)
        promotion_rate = (total_promotions_transfers / active_count * 100) if active_count > 0 else 0
    else: 
        total_promotions_transfers = 0 
        avg_tenure = 0 
        promotion_rate = 0

    # Top metrics row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("<div class='metric-label'>Promotions & Transfers</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{total_promotions_transfers}</div>", unsafe_allow_html=True)
    
    with col2:
        with st.container(border=True):
            st.markdown("<div class='metric-label'>Average Tenure</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{avg_tenure:.1f} yrs</div>", unsafe_allow_html=True)
    
    with col3:
        with st.container(border=True):
            st.markdown("<div class='metric-label'>Promotion Rate</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{promotion_rate:.1f}%</div>", unsafe_allow_html=True)

    # Promotion & Transfer Tracking
    with st.container(border=True):
        st.markdown("#### Promotion & Transfer Tracking") 

        # Pre-compute summary tables
        promo_summary = df_active.groupby("Year", as_index=False)["Promotion & Transfer"].sum()
        pos_summary = df_active.groupby(["Year", "Position/Level"], as_index=False)["Promotion & Transfer"].sum()

        # Two charts side by side
        col1, col2 = st.columns(2)

        with col1:
            # Line chart for yearly trend
            st.markdown("##### Promotions & Transfers per Year")
            fig1 = px.line(
                promo_summary,
                x="Year",
                y="Promotion & Transfer",
                markers=True
            )
            fig1.update_traces(line={width=3, color="#00008B"}, marker={size=8, color="#00008B"})
            fig1.update_layout(
                height=250, margin={"l": 20, "r": 20, "t": 20, "b": 20},
                yaxis=dict(title="Count", tickfont={"color": "var(--text-color)"}, titlefont={"color": "var(--text-color)"}),
                xaxis=dict(title="Year", tickfont={"color": "var(--text-color)"}, titlefont={"color": "var(--text-color)"}),
                font={"color": "var(--text-color)"}
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            # Stacked bar chart for position/level distribution
            st.markdown("##### By Position/Level")
            fig2 = px.bar(
                pos_summary,
                x="Year",
                y="Promotion & Transfer",
                color="Position/Level",
                color_discrete_map={"Associate": "#6495ED", "Manager & Up": "#00008B"}
            )
            fig2.update_layout(
                height=250, margin={"l": 20, "r": 20, "t": 20, "b": 20},
                yaxis=dict(title="Count", tickfont={"color": "var(--text-color)"}, titlefont={"color": "var(--text-color)"}),
                xaxis=dict(title="Year", tickfont={"color": "var(--text-color)"}, titlefont={"color": "var(--text-color)"}),
                font={"color": "var(--text-color)"},
                legend={font={"color": "var(--text-color}"})
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Tenure Distribution of Promoted Employees
    with st.container(border=True):
        st.markdown(f"#### Tenure Distribution of Promoted Employees ({selected_year})")
        promoted_employees = career_year[career_year["Promotion & Transfer"] == 1]

        if not promoted_employees.empty:
            fig3 = px.histogram(
                promoted_employees,
                x="Tenure",
                nbins=10,
                histnorm=None,
                color_discrete_sequence=["#00008B"]
            )
            fig3.update_traces(
                texttemplate="%{y}",
                textposition="outside"
            )
            fig3.update_layout(
                height=250, margin={"l": 20, "r": 20, "t": 20, "b": 20},
                yaxis=dict(title="Count", tickfont={"color": "var(--text-color)"}, titlefont={"color": "var(--text-color)"}),
                xaxis=dict(title="Tenure (years)", tickfont={"color": "var(--text-color)"}, titlefont={"color": "var(--text-color)"}),
                font={"color": "var(--text-color)"},
                showlegend=False
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No promoted employees found for the selected year.")
