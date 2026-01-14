import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render(df, df_raw, selected_year, df_attrition=None, summary_file="HR Cleaned Data 01.09.26.xlsx"):
    # -----------------------------
    # Executive Summary at the very top
    # -----------------------------
    with st.container(border=True):
        st.markdown("### 📋 Executive Summary")
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown("""
            - 🔒 **Strong Retention**: 91% retention rate demonstrates workforce stability and satisfaction
            - 📉 **Low Attrition**: Consistent 9% attrition rate, well below industry benchmarks
            - 👥 **Gender Parity**: Both females and males show equal retention patterns (~91%)
            """)
        
        with summary_col2:
            st.markdown("""
            - 📊 **Net Growth**: +480 employees gained (2020-2025) despite natural turnover
            - 🚪 **Voluntary Focus**: 70% voluntary exits vs 30% involuntary, indicating healthy workplace culture
            - 🧠 **Generational Stability**: Millennials lead retention, Gen Z improving year-over-year
            """)

    # -----------------------------
    # Section heading (now below Executive Summary)
    # -----------------------------
    st.markdown("## 🔄 Attrition and Retention Metrics")

    # -----------------------------
    # Ensure Retention column exists
    # -----------------------------
    def to_resigned_flag(x):
        s = str(x).strip().upper()
        return 0 if s == "ACTIVE" else 1

    if "ResignedFlag" not in df_raw.columns:
        df_raw["ResignedFlag"] = df_raw["Resignee Checking"].apply(to_resigned_flag)
    if "Retention" not in df_raw.columns:
        df_raw["Retention"] = 1 - df_raw["ResignedFlag"]

    # Normalize values
    df_raw["Gender"] = df_raw["Gender"].str.strip().str.capitalize()
    df_raw["Resignee Checking"] = df_raw["Resignee Checking"].str.strip().str.upper()

    # -----------------------------
    # Create Year column from Calendar Year
    # -----------------------------
    if "Year" not in df_raw.columns and "Calendar Year" in df_raw.columns:
        df_raw["Year"] = pd.to_datetime(df_raw["Calendar Year"]).dt.year

    # -----------------------------
    # Row 0: Summary Metrics (Net Change fixed to use Summary tab col H)
    # -----------------------------
    summary_year = df_raw[df_raw["Year"] == selected_year]

    total_employees = len(summary_year)
    resigned = summary_year["ResignedFlag"].sum()
    retained = summary_year["Retention"].sum()

    retention_rate = (retained / total_employees) * 100 if total_employees > 0 else 0
    attrition_rate = (resigned / total_employees) * 100 if total_employees > 0 else 0

    # Load official Net Change from Summary tab (Column H)
    net_change_to_show = 0  # default
    try:
        summary_df = pd.read_excel(summary_file, sheet_name="Summary")
        summary_df.columns = summary_df.columns.str.strip()
        
        if "Year" in summary_df.columns and "Net Change" in summary_df.columns:
            # Convert Year to integer, handling both datetime and numeric formats
            if pd.api.types.is_datetime64_any_dtype(summary_df["Year"]):
                summary_df["Year"] = summary_df["Year"].dt.year
            else:
                summary_df["Year"] = pd.to_numeric(summary_df["Year"], errors="coerce")
            
            summary_df["Year"] = summary_df["Year"].astype(int)
            summary_df["Net Change"] = pd.to_numeric(summary_df["Net Change"], errors="coerce").fillna(0).astype(int)
            
            # Create lookup dictionary
            year_to_net = summary_df.set_index("Year")["Net Change"].to_dict()
            
            if selected_year in year_to_net:
                net_change_to_show = year_to_net[selected_year]
    except Exception as e:
        st.warning(f"Could not load Net Change from Summary sheet: {str(e)}")
        net_change_to_show = 0

    colA, colB, colC, colD, colE = st.columns(5)
    
    with colA:
        with st.container(border=True):
            st.markdown("<div class='metric-label'>Total Employees</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{total_employees}</div>", unsafe_allow_html=True)
    
    with colB:
        with st.container(border=True):
            st.markdown("<div class='metric-label'>Resigned</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{resigned}</div>", unsafe_allow_html=True)
    
    with colC:
        with st.container(border=True):
            st.markdown("<div class='metric-label'>Retention Rate</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{retention_rate:.1f}%</div>", unsafe_allow_html=True)
    
    with colD:
        with st.container(border=True):
            st.markdown("<div class='metric-label'>Attrition Rate</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{attrition_rate:.1f}%</div>", unsafe_allow_html=True)
    
    with colE:
        with st.container(border=True):
            st.markdown("<div class='metric-label'>Net Change</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{net_change_to_show}</div>", unsafe_allow_html=True)

    st.markdown("<style>h2 { margin-bottom: -0.5rem !important; } </style>", unsafe_allow_html=True)

    # -----------------------------
    # Row 1: Resigned per Year
    # -----------------------------
    with st.container(border=True):
        st.markdown("#### Resigned per Year")
        resigned_per_year = df_raw.groupby("Year")["ResignedFlag"].sum().reset_index(name="Resigned")
        
        # Ensure all years 2020-2025 are included
        all_years = pd.DataFrame({"Year": range(2020, 2026)})
        resigned_per_year = all_years.merge(resigned_per_year, on="Year", how="left").fillna(0)
        resigned_per_year["Resigned"] = resigned_per_year["Resigned"].astype(int)
        resigned_per_year["Year_str"] = resigned_per_year["Year"].astype(str)
        
        fig_resigned = px.bar(resigned_per_year, x="Year_str", y="Resigned",
                              color_discrete_sequence=["#00008B"])
        fig_resigned.update_traces(textposition='outside', texttemplate='%{y:.0f}', 
                                   textfont={"size": 14, "color": "black"})
        fig_resigned.update_xaxes(title_text="Year")
        fig_resigned.update_yaxes(title_text="Number of Resignations", range=[0, max(resigned_per_year["Resigned"]) * 1.15])
        fig_resigned.update_layout(
            height=280,
            margin={"l": 20, "r": 20, "t": 20, "b": 40},
            showlegend=False
        )
        st.plotly_chart(fig_resigned, use_container_width=True, key="resigned_per_year")

    # -----------------------------
    # Row 2: Retention by Gender + Retention by Generation
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### Retention by Gender")
            retention_gender = df_raw.groupby(["Year", "Gender"])["Retention"].sum().reset_index()
            retention_rate_df = df_raw.groupby("Year")["Retention"].mean().reset_index()
            retention_rate_df["RetentionRatePct"] = retention_rate_df["Retention"] * 100
            
            # Standardized gender colors (blue palette - unique shades)
            gender_colors = {"Female": "#6495ED", "Male": "#00008B"}
            
            fig = go.Figure()
            for gender in retention_gender["Gender"].unique():
                subset = retention_gender[retention_gender["Gender"] == gender]
                color = gender_colors.get(gender, "#00008B")
                fig.add_bar(x=subset["Year"], y=subset["Retention"], name=gender,
                            marker_color=color, yaxis="y1")
            fig.add_trace(go.Scatter(x=retention_rate_df["Year"], y=retention_rate_df["RetentionRatePct"],
                                     mode="lines+markers", name="Retention Rate (%)",
                                     line={"color": "orange", "width": 3}, yaxis="y2"))
            fig.update_layout(
                yaxis={
                    "title": "Retained Employees (count)",
                    "side": "left"
                },
                yaxis2={
                    "title": "Retention Rate (%)",
                    "overlaying": "y",
                    "side": "right",
                    "range": [80, 100]
                },
                xaxis={"title": "Year"},
                barmode="group",
                height=280,
                margin={"l": 60, "r": 60, "t": 20, "b": 60},
                legend={"x": 0.5, "y": -0.25, "xanchor": "center", "yanchor": "top", "orientation": "h"}
            )
            st.plotly_chart(fig, use_container_width=True, key="retention_by_gender")

    with col2:
        with st.container(border=True):
            st.markdown("#### Retention by Generation")
            active_df = df_raw[df_raw["Resignee Checking"] == "ACTIVE"]
            
            # Normalize Generation values
            df_raw["Generation"] = df_raw["Generation"].str.strip().str.title()
            
            total_by_year_gen = df_raw[df_raw["Year"].between(2020, 2025)].groupby(["Year", "Generation"]).size().reset_index(name="Total")
            active_by_year_gen = active_df[active_df["Year"].between(2020, 2025)].groupby(["Year", "Generation"]).size().reset_index(name="Active")
            retention_df = pd.merge(total_by_year_gen, active_by_year_gen, on=["Year", "Generation"], how="left")
            retention_df["RetentionRate"] = (retention_df["Active"] / retention_df["Total"]) * 100
            
            # Define generation order (alphabetical)
            generation_order = ["Baby Boomer", "Gen X", "Gen Z", "Millennial"]
            
            # Standardized generation colors - unique blue shades
            generation_colors = {
                "Gen Z": "#87CEEB",           # Sky Blue
                "Millennial": "#4169E1",      # Royal Blue
                "Gen X": "#1E90FF",           # Dodger Blue
                "Baby Boomer": "#00008B",     # Dark Blue
                "Boomer": "#00008B"           # Dark Blue (fallback)
            }
            
            # Convert Generation to categorical with defined order
            retention_df["Generation"] = pd.Categorical(retention_df["Generation"], categories=generation_order, ordered=True)
            
            fig_retention = px.bar(retention_df, x="Year", y="RetentionRate", color="Generation", barmode="group",
                                   text=retention_df["RetentionRate"].round(1).astype(str) + "%",
                                   color_discrete_map=generation_colors,
                                   category_orders={"Generation": generation_order})
            fig_retention.update_layout(
                height=280,
                margin={"l": 20, "r": 20, "t": 20, "b": 60},
                yaxis={"title": "Retention Rate (%)"},
                xaxis={"title": "Year"},
                uniformtext_minsize=10,
                uniformtext_mode="hide",
                legend={"x": 0.5, "y": -0.25, "xanchor": "center", "yanchor": "top", "orientation": "h"}
            )
            st.plotly_chart(fig_retention, use_container_width=True, key="retention_by_generation")

    # -----------------------------
    # Row 3: Attrition Analysis
    # -----------------------------
    with st.container(border=True):
        st.markdown("#### Attrition Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"##### Attrition by Month ({selected_year})")
            attrition_selected = df_raw[(df_raw["Year"] == selected_year) & (df_raw["ResignedFlag"] == 1)].copy()
            attrition_selected["Month"] = pd.to_datetime(attrition_selected["Resignation Date"]).dt.month_name()
            monthly_attrition = (
                attrition_selected.groupby("Month")
                .size()
                .reindex([
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ])
                .reset_index(name="AttritionCount")
            )
            fig_monthly = px.bar(
                monthly_attrition, x="Month", y="AttritionCount", text="AttritionCount",
                color_discrete_sequence=["#00008B"]
            )
            fig_monthly.update_layout(
                height=300,
                margin={"l": 20, "r": 20, "t": 20, "b": 20},
                yaxis={"title": "Attrition Count"},
                xaxis={"title": "Month"},
                uniformtext_minsize=10,
                uniformtext_mode="hide",
                showlegend=False
            )
            st.plotly_chart(fig_monthly, use_container_width=True, key="attrition_by_month")

        with col2:
            st.markdown("##### Attrition by Voluntary vs Involuntary (2020 – 2025)")
            if df_attrition is not None:
                if "Year" not in df_attrition.columns and "Calendar Year" in df_attrition.columns:
                    df_attrition["Year"] = pd.to_datetime(df_attrition["Calendar Year"]).dt.year
                attrition_df = df_attrition[
                    (df_attrition["Year"].between(2020, 2025)) &
                    (df_attrition["Status"].isin(["Voluntary", "Involuntary"]))
                ]
                attrition_counts = attrition_df.groupby(["Year", "Status"]).size().reset_index(name="Count")
                # Standardized colors: Voluntary=Associate/Female, Involuntary=Manager&Up/Male
                fig_attrition = px.bar(
                    attrition_counts, x="Year", y="Count", color="Status", barmode="group", text="Count",
                    color_discrete_map={"Voluntary": "#6495ED", "Involuntary": "#00008B"}
                )
                fig_attrition.update_layout(
                    height=300,
                    margin={"l": 20, "r": 20, "t": 20, "b": 20},
                    yaxis={"title": "Attrition Count"},
                    xaxis={"title": "Year"},
                    uniformtext_minsize=10,
                    uniformtext_mode="hide"
                )
                st.plotly_chart(fig_attrition, use_container_width=True, key="attrition_by_type")
            else:
                st.info("No Voluntary/Involuntary attrition dataset provided yet.")

    # -----------------------------
    # Row 4: Net Talent Gain/Loss (already uses Summary tab Net Change)
    # -----------------------------
    with st.container(border=True):
        st.markdown("#### Net Talent Gain/Loss")

        summary_df_row4 = pd.read_excel(summary_file, sheet_name="Summary")
        net_df = summary_df_row4[["Year", "Joins", "Resignations", "Net Change"]].copy()
        net_df.rename(columns={"Net Change": "NetChange"}, inplace=True)
        net_df["Status"] = net_df["NetChange"].apply(lambda x: "Increase" if x > 0 else "Decrease")
        net_df["Status"] = pd.Categorical(net_df["Status"], categories=["Increase", "Decrease"], ordered=True)
        net_df["Year"] = net_df["Year"].astype(str)

        color_map = {"Increase": "#2E8B57", "Decrease": "#B22222"}
        fig_net = px.bar(
            net_df, x="Year", y="NetChange",
            text=net_df["NetChange"].apply(lambda x: f"{x:+d}"),
            color="Status", color_discrete_map=color_map,
            hover_data={"Joins": True, "Resignations": True, "NetChange": True, "Status": True, "Year": True}
        )
        fig_net.update_layout(
            height=320,
            margin={"l": 20, "r": 20, "t": 20, "b": 20},
            yaxis={"title": "Net Change"},
            xaxis={"title": "Year"},
            uniformtext_minsize=10,
            uniformtext_mode="hide"
        )
        st.plotly_chart(fig_net, use_container_width=True, key="net_talent_change")
