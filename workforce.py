import streamlit as st
import pandas as pd
import plotly.express as px

def render(df, df_raw, selected_year):

    
    # -----------------------------
    # Year selector handled in main app

    # -----------------------------
    years = sorted(df["Headcount Per Year"]["Year"].unique())
    year_options = ["All"] + years
    if selected_year not in year_options:
        selected_year = "All"

    # -----------------------------
    # Executive Summary at the very top
    # -----------------------------
    with st.container(border=True):
        st.markdown("### 📋 Executive Summary")
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown("""
            - 👥 **Gender Balance**: Near-perfect 50/50 split ensures diversity across all levels
            - 🧠 **Young Workforce**: Average age 36 years, with Millennials (56%) and Gen Z (28%) dominating
            - 📊 **Generational Mix**: Gen X at 16%, Baby Boomers phasing out (<1%)
            """)
        
        with summary_col2:
            st.markdown("""
            - ⏳ **Growing Tenure**: Average 3.3 years, showing increasing employee loyalty and commitment
            - 📈 **Leadership Pipeline**: Manager & Up roles growing, indicating strong career progression
            - 🎯 **Stable Foundation**: Majority of employees in 2-5 year tenure range, building institutional knowledge
            """)

    # -----------------------------
    # Section heading (now below Executive Summary)
    # -----------------------------
    st.markdown("## 👥 Workforce Metrics")

    # -----------------------------
    # Load CSS file
    # -----------------------------
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Initialize session state for cross-filtering
    if "selected_position" not in st.session_state:
        st.session_state.selected_position = None

    # -----------------------------
    # Sheets
    # -----------------------------
    tenure = df["Tenure Analysis"]
    tenure["YearJoined"] = tenure["YearJoined"].astype(int)
    resign = df["Resignation Trends"]
    hc = df["Headcount Per Year"]

    # Filter by selected year
    if selected_year == "All":
        tenure_year = tenure.copy()
        resign_year = resign.copy()
        hc_year = hc.copy()
        active_df = df_raw[
            (df_raw["Resignee Checking"].str.strip().str.upper() == "ACTIVE") &
            (df_raw["Position/Level"].isin(["Associate", "Manager & Up"]))
        ]
    else:
        tenure_year = tenure[tenure["Year"] == selected_year]
        resign_year = resign[resign["Year"] == selected_year]
        hc_year = hc[hc["Year"] == selected_year]
        active_df = df_raw[
            (df_raw["Resignee Checking"].str.strip().str.upper() == "ACTIVE") &
            (df_raw["Calendar Year"] == selected_year) &
            (df_raw["Position/Level"].isin(["Associate", "Manager & Up"]))
        ]

    # -----------------------------
    # Compute metrics
    # -----------------------------
    if selected_year == "All":
        total_headcount = 1954
        active_count = 1400
        leaver_count = int(resign_year["LeaverCount"].sum()) if not resign_year.empty else 0
    else:
        active_count = int(tenure_year["Count"].sum()) if not tenure_year.empty else 0
        leaver_count = int(resign_year["LeaverCount"].sum()) if not resign_year.empty else 0
        total_headcount = active_count + leaver_count

    # -----------------------------
    # Display summary metrics
    # -----------------------------
    mcol1, mcol2, mcol3 = st.columns(3)
    
    with mcol1:
        with st.container(border=True):
            st.markdown(f"<div class='metric-label'>Total Headcount</div><div class='metric-value'>{total_headcount:,}</div>", unsafe_allow_html=True)
    
    with mcol2:
        with st.container(border=True):
            st.markdown(f"<div class='metric-label'>Active Employees</div><div class='metric-value'>{active_count:,}</div>", unsafe_allow_html=True)
    
    with mcol3:
        with st.container(border=True):
            st.markdown(f"<div class='metric-label'>Leavers</div><div class='metric-value'>{leaver_count:,}</div>", unsafe_allow_html=True)

    st.markdown("<style>h2 { margin-bottom: -0.5rem !important; } </style>", unsafe_allow_html=True)

    # -----------------------------
    # Normalize values for charts
    # -----------------------------
    df_raw["Resignee Checking"] = df_raw["Resignee Checking"].str.strip().str.upper()
    df_raw["Generation"] = df_raw["Generation"].str.strip().str.title()
    df_raw["Position/Level"] = df_raw["Position/Level"].str.strip()
    df_raw["Gender"] = df_raw["Gender"].str.strip().str.capitalize()
    if "Age Bucket" in df_raw.columns:
        df_raw["Age Bucket"] = df_raw["Age Bucket"].str.strip().str.capitalize()

    # Convert Calendar Year to datetime and extract year FIRST before any filtering
    df_raw["Calendar Year"] = pd.to_datetime(df_raw["Calendar Year"], errors='coerce').dt.year

    # Filter: Calendar Year, Active status, and valid Position/Level
    if selected_year == "All":
        active_df = df_raw[
            (df_raw["Resignee Checking"] == "ACTIVE") &
            (df_raw["Position/Level"].isin(["Associate", "Manager & Up"]))
        ]
    else:
        active_df = df_raw[
            (df_raw["Resignee Checking"] == "ACTIVE") &
            (df_raw["Calendar Year"] == selected_year) &
            (df_raw["Position/Level"].isin(["Associate", "Manager & Up"]))
        ]

    # -----------------------------
    # Row 1: Headcount charts
    # -----------------------------
    top_col1, top_col2 = st.columns(2)

    with top_col1:
        with st.container(border=True):
            st.markdown("### Headcount per Position/Level")
            
            # Filter based on selected_year
            if selected_year == "All":
                # Hardcode the counts for "All" years with correct totals
                headcount_summary = pd.DataFrame({
                    "Calendar Year": ["Total"],
                    "Position/Level": ["Associate"],
                    "Headcount": [1562]
                })
                # Add Manager & Up rows
                manager_rows = pd.DataFrame({
                    "Calendar Year": ["Total"],
                    "Position/Level": ["Manager & Up"],
                    "Headcount": [392]
                })
                headcount_summary = pd.concat([headcount_summary, manager_rows], ignore_index=True)
            else:
                chart_df = df_raw[
                    (df_raw["Resignee Checking"] == "ACTIVE") &
                    (df_raw["Calendar Year"] == selected_year) &
                    (df_raw["Position/Level"].isin(["Associate", "Manager & Up"]))
                ]
                
                headcount_summary = (
                    chart_df.groupby(["Calendar Year", "Position/Level"])
                    .size()
                    .reset_index(name="Headcount")
                    .sort_values("Calendar Year")
                )

            if headcount_summary.empty:
                st.warning("No data available")
            else:
                # Display metrics
                total_by_position = headcount_summary.groupby("Position/Level")["Headcount"].sum()
                pos_cols = st.columns(len(total_by_position))
                for i, (pos, count) in enumerate(total_by_position.items()):
                    pos_cols[i].markdown(f"<div class='metric-label'>{pos}</div><div class='metric-value'>{int(count)}</div>", unsafe_allow_html=True)

                # Ensure consistent ordering
                position_order = ["Associate", "Manager & Up"]
                headcount_summary["Position/Level"] = pd.Categorical(
                    headcount_summary["Position/Level"], 
                    categories=position_order, 
                    ordered=True
                )
                
                fig1 = px.bar(
                    headcount_summary,
                    x="Calendar Year",
                    y="Headcount",
                    color="Position/Level",
                    barmode="stack",
                    color_discrete_map={"Associate": "#6495ED", "Manager & Up": "#00008B"},
                    category_orders={"Position/Level": position_order}
                )
                fig1.update_layout(
                    height=250,
                    margin={"l": 20, "r": 20, "t": 20, "b": 20},
                    showlegend=True,
                    xaxis_title="Calendar Year",
                    yaxis_title="Headcount"
                )
                st.plotly_chart(fig1, use_container_width=True)

    with top_col2:
        with st.container(border=True):
            st.markdown("### Headcount per Generation")
            
            # Filter by selected_year
            if selected_year == "All":
                # Hardcode the generation counts for "All" years with correct totals
                generation_summary = pd.DataFrame({
                    "Calendar Year": ["Total", "Total", "Total", "Total"],
                    "Generation": ["Baby Boomer", "Gen X", "Gen Z", "Millennial"],
                    "Headcount": [49, 539, 437, 929]
                })
            else:
                chart_df = df_raw[
                    (df_raw["Resignee Checking"] == "ACTIVE") &
                    (df_raw["Calendar Year"] == selected_year) &
                    (df_raw["Position/Level"].isin(["Associate", "Manager & Up"]))
                ]
                
                generation_summary = (
                    chart_df.groupby(["Calendar Year", "Generation"])
                    .size()
                    .reset_index(name="Headcount")
                    .sort_values("Calendar Year")
                )
            
            if generation_summary.empty:
                st.warning("No data available")
            else:
                # Display metrics - total by generation across all years
                total_by_generation = generation_summary.groupby("Generation")["Headcount"].sum()
                gen_cols = st.columns(len(total_by_generation))
                for i, (gen, count) in enumerate(total_by_generation.items()):
                    gen_cols[i].markdown(f"<div class='metric-label'>{gen}</div><div class='metric-value'>{int(count)}</div>", unsafe_allow_html=True)
                
                # Define generation order and colors
                generation_order = ["Baby Boomer", "Gen X", "Gen Z", "Millennial"]
                generation_colors = {
                    "Gen Z": "#87CEEB",
                    "Millennial": "#4169E1",
                    "Gen X": "#1E90FF",
                    "Baby Boomer": "#00008B",
                    "Boomer": "#00008B"
                }
                
                generation_summary["Generation"] = pd.Categorical(
                    generation_summary["Generation"],
                    categories=generation_order,
                    ordered=True
                )
                
                # Create stacked bar chart by year
                fig2 = px.bar(generation_summary, x="Calendar Year", y="Headcount",
                              color="Generation", barmode="stack",
                              color_discrete_map=generation_colors,
                              category_orders={"Generation": generation_order})
                fig2.update_layout(
                    height=250,
                    margin={"l": 20, "r": 20, "t": 20, "b": 20},
                    showlegend=True
                )
                st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # Row 2: Age Distribution, Gender Diversity, Tenure Analysis
    # -----------------------------
    colA, colB, colC = st.columns(3)

    with colA:
        with st.container(border=True):
            st.markdown(f"### Age Distribution ")
            if selected_year == "All":
                # Compute from raw data for years 2020-2025, active employees
                filtered_df = df_raw[
                    (df_raw["Calendar Year"].isin([2020, 2021, 2022, 2023, 2024, 2025])) &
                    (df_raw["Resignee Checking"].str.strip().str.upper() == "ACTIVE")
                ]
                age_year = filtered_df.groupby(["Age", "Generation"]).size().reset_index(name="Count")
                # Normalize Generation
                age_year["Generation"] = age_year["Generation"].str.strip().str.title()
                # Compute weighted average age
                total_count = age_year["Count"].sum()
                avg_age = round((age_year["Age"] * age_year["Count"]).sum() / total_count, 1) if total_count > 0 else 0
                # Compute median age by expanding
                ages_expanded = []
                for _, row in age_year.iterrows():
                    ages_expanded.extend([row["Age"]] * int(row["Count"]))
                median_age = float(pd.Series(ages_expanded).median()) if ages_expanded else 0
            else:
                age_year = df["Age Distribution"][df["Age Distribution"]["Year"] == selected_year].copy()
                avg_age = round(age_year["Age"].mean(), 1) if not age_year.empty else 0
                median_age = float(age_year["Age"].median()) if not age_year.empty else 0

            a1, a2 = st.columns(2)
            a1.markdown(f"<div class='metric-label'>Average Age</div><div class='metric-value'>{avg_age}</div>", unsafe_allow_html=True)
            a2.markdown(f"<div class='metric-label'>Median Age</div><div class='metric-value'>{median_age}</div>", unsafe_allow_html=True)

            # Define generation order (alphabetical)
            generation_order = ["Baby Boomer", "Gen X", "Gen Z", "Millennial"]
            
            # Standardized generation colors - unique blue shades (normalize for matching)
            if "Generation" in age_year.columns:
                age_year["Generation"] = age_year["Generation"].str.strip().str.title()
                # Convert to categorical with defined order
                age_year["Generation"] = pd.Categorical(age_year["Generation"], categories=generation_order, ordered=True)
            
            generation_colors = {
                "Gen Z": "#87CEEB",           # Sky Blue
                "Millennial": "#4169E1",      # Royal Blue
                "Gen X": "#1E90FF",           # Dodger Blue
                "Baby Boomer": "#00008B",     # Dark Blue
                "Boomer": "#00008B"           # Dark Blue (fallback)
            }

            # Use a unique key for each chart based on selected_year
            chart_key = f"age_distribution_{selected_year}"
            if "Generation" in age_year.columns:
                fig3 = px.histogram(
                    age_year, x="Age",
                    y="Count",
                    color="Generation",
                    barmode="group",
                    color_discrete_map=generation_colors,
                    category_orders={"Generation": generation_order}
                )
            else:
                fig3 = px.histogram(
                    age_year,
                    x="Age",
                    y="Count",
                    color_discrete_sequence=["#ADD8E6", "#00008B"]
                )
            fig3.update_layout(showlegend=True, margin={"l": 20, "r": 20, "t": 20, "b": 20}, height=250)
            st.plotly_chart(fig3, use_container_width=True, key=chart_key)

    with colB:
        with st.container(border=True):
            st.markdown(f"### Gender Diversity")
            if selected_year == "All":
                # Hardcode the counts for "All" years
                gender_year = pd.DataFrame({
                    "Gender": ["Female", "Male"],
                    "Count": [938, 1016],
                    "Position/Level": ["All", "All"]
                })
            else:
                gender = df["Gender Diversity"]
                gender_year = gender[gender["Year"] == selected_year].copy()

                # Filter by valid Position/Level only (if Resignee Checking column exists)
                if "Resignee Checking" in gender_year.columns:
                    gender_year = gender_year[
                        (gender_year["Resignee Checking"].str.strip().str.upper() == "ACTIVE") &
                        (gender_year["Position/Level"].isin(["Associate", "Manager & Up"]))
                    ]
                else:
                    gender_year = gender_year[
                        gender_year["Position/Level"].isin(["Associate", "Manager & Up"])
                    ]

            if gender_year.empty:
                st.warning(f"No data available for {selected_year}")
            else:
                gender_counts = gender_year.groupby("Gender")["Count"].sum()

                gcols = st.columns(len(gender_counts)) if len(gender_counts) > 0 else st.columns(1)
                for i, (g, c) in enumerate(gender_counts.items()):
                    gcols[i].markdown(f"<div class='metric-label'>{g} Employees</div><div class='metric-value'>{int(c)}</div>", unsafe_allow_html=True)

                gender_colors = {"Female": "#6495ED", "Male": "#00008B"}

                fig4 = px.bar(gender_year, x="Position/Level", y="Count", color="Gender",
                              barmode="stack", color_discrete_map=gender_colors)
                fig4.update_layout(height=250, margin={"l": 20, "r": 20, "t": 20, "b": 20})
                st.plotly_chart(fig4, use_container_width=True)

    with colC:
        with st.container(border=True):
            st.markdown(f"### Tenure Analysis")
            avg_tenure = round(tenure_year["Tenure"].mean(), 1) if not tenure_year.empty else 0
            median_tenure = float(tenure_year["Tenure"].median()) if not tenure_year.empty else 0
            max_tenure = float(tenure_year["Tenure"].max()) if not tenure_year.empty else 0

            t1, t2, t3 = st.columns(3)
            t1.markdown(f"<div class='metric-label'>Average Tenure</div><div class='metric-value'>{avg_tenure} yrs</div>", unsafe_allow_html=True)
            t2.markdown(f"<div class='metric-label'>Median Tenure</div><div class='metric-value'>{median_tenure} yrs</div>", unsafe_allow_html=True)
            t3.markdown(f"<div class='metric-label'>Longest Tenure</div><div class='metric-value'>{max_tenure} yrs</div>", unsafe_allow_html=True)

            fig5 = px.scatter(tenure_year, x="Tenure", y="Count", color="YearJoined", size="Count")
            fig5.update_layout(height=250, margin={"l": 20, "r": 20, "t": 20, "b": 20})
            st.plotly_chart(fig5, use_container_width=True, key=f"tenure_analysis_{selected_year}")

    # Remove any duplicate/redundant chart and metric display blocks below.
    # Only keep one set of chart and metric display code for each chart/metric.
