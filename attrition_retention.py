import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def update_month_selection():
    if "All" in st.session_state.resigned_month_dropdown:
        if len(st.session_state.resigned_month_dropdown) > 1:
            st.session_state.resigned_month_dropdown = ["All"]

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

    # Convert Calendar Year to datetime and extract year
    if "Calendar Year" in df_raw.columns:
        df_raw["Calendar Year"] = pd.to_datetime(df_raw["Calendar Year"], errors='coerce')
    
    # Create Year column from Calendar Year
    if "Year" not in df_raw.columns and "Calendar Year" in df_raw.columns:
        df_raw["Year"] = df_raw["Calendar Year"].dt.year

    # -----------------------------
    # Row 0: Summary Metrics (Net Change fixed to use Summary tab col H)
    # -----------------------------
    if selected_year == "All":
        summary_year = df_raw[df_raw["Year"].between(2020, 2025)]
    else:
        summary_year = df_raw[df_raw["Year"] == selected_year]

    # Update: Total Employees is now Active Employees only
    total_employees = summary_year[summary_year["Resignee Checking"] == "ACTIVE"].drop_duplicates(subset=["Full Name"]).shape[0]
    resigned = summary_year["ResignedFlag"].sum()
    retained = summary_year["Retention"].sum()

    retention_rate = (retained / total_employees) * 100 if total_employees > 0 else 0
    attrition_rate = (resigned / total_employees) * 100 if total_employees > 0 else 0

    # Load official Net Change ftotal_employees = len(summary_year[summary_year["Resignee Checking"] == "ACTIVE"])rom Summary tab (Column H)
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
            
            if selected_year == "All":
                net_change_to_show = sum([year_to_net.get(y, 0) for y in range(2020, 2026)])
            elif selected_year in year_to_net:
                net_change_to_show = year_to_net[selected_year]
    except Exception as e:
        st.warning(f"Could not load Net Change from Summary sheet: {str(e)}")
        net_change_to_show = 0

    colA, colB, colC, colD, colE = st.columns(5)
    
    with colA:
        with st.container(border=True):
            st.markdown("<div class='metric-label'>Active Employees</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{total_employees}</div>", unsafe_allow_html=True)
    
    with colB:
        with st.container(border=True):
            st.markdown("<div class='metric-label'>Leavers</div>", unsafe_allow_html=True)
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
    st.markdown("<style>.stContainer { overflow: hidden !important; } </style>", unsafe_allow_html=True)

    # -----------------------------
    # Row 1: Resigned per Year + Retention
    # -----------------------------
    col1, col2 = st.columns(2)

    # Remove fixed height for all containers to avoid scrollbars
    # fixed_container_height = 340

    with col1:
        with st.container(border=True):
            # Header and dropdown in the same line
            month_order = [
                "All", "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            # Add custom CSS for blue dropdown value
            st.markdown("""
            <style>
            /* Blue background for selected values in multiselect */
            .stMultiSelect [data-baseweb="tag"] {
                background-color: #4682B4 !important; /* steel blue */
                color: white !important;
            }
            </style>
            """, unsafe_allow_html=True)
            header_col, dropdown_col = st.columns([2, 1])
            with header_col:
                st.markdown("#### Resigned")
            with dropdown_col:
                if "resigned_month_dropdown" not in st.session_state:
                    st.session_state.resigned_month_dropdown = ["All"]
                selected_month = st.multiselect(
                    "Select Month", month_order, key="resigned_month_dropdown", on_change=update_month_selection
                )
                if not selected_month:
                    selected_month = ["All"]

            # Prepare month column
            # Try both explicit and flexible parsing for Resignation Date
            df_raw["Month"] = pd.to_datetime(
                df_raw["Resignation Date"], errors='coerce', infer_datetime_format=True
            ).dt.month_name()

            # Group raw data by Year and sum resignations, optionally filter by month
            if "All" in selected_month or not selected_month:
                filtered_df = df_raw
            else:
                filtered_df = df_raw[df_raw["Month"].isin(selected_month)]

            resigned_per_year = filtered_df.groupby("Year")["ResignedFlag"].sum().reset_index(name="Resigned")

            # Ensure all years 2020–2025 are included, even if no resignations
            all_years = pd.DataFrame({"Year": range(2020, 2026)})
            resigned_per_year = all_years.merge(resigned_per_year, on="Year", how="left").fillna(0)

            # Clean up datatypes
            resigned_per_year["Resigned"] = resigned_per_year["Resigned"].astype(int)
            resigned_per_year["Year"] = resigned_per_year["Year"].astype(int)
            resigned_per_year["Year_str"] = resigned_per_year["Year"].astype(str)   # string version for categorical x-axis

            # Handle radio button selection
            if selected_year == "All":
                plot_data = resigned_per_year
                color_seq = ["#00008B"]
            else:
                plot_data = resigned_per_year[resigned_per_year["Year"] == selected_year]
                color_seq = ["#00008B"]

            fig_resigned = px.bar(
                plot_data,
                x="Year_str",
                y="Resigned",
                color_discrete_sequence=color_seq
            )
            fig_resigned.update_traces(
                textposition="outside",
                texttemplate="%{y:.0f}",   # show integer values above bars
                textfont={"size": 14, "color": "black"}
            )
            fig_resigned.update_xaxes(
                type="category",
                title_text="Year",
                showticklabels=False  # <-- Hide tick labels
            )
            fig_resigned.update_yaxes(
                title_text="Number of Resignations",
                range=[0, max(plot_data["Resigned"]) * 1.15 if not plot_data.empty else 1]
            )
            fig_resigned.update_layout(
                height=280,
                margin={"l": 20, "r": 20, "t": 20, "b": 40},
                showlegend=False
            )

            # Render chart in Streamlit
            st.plotly_chart(fig_resigned, use_container_width=True, key=f"resigned_per_year_{selected_year}_{selected_month}")

    with col2:
        with st.container(border=True):
            # Add custom CSS for blue selectbox value and selected value display
            st.markdown("""
            <style>
            /* Blue background for selected value in selectbox dropdown */
            .stSelectbox [data-baseweb="select"] div[role="option"][aria-selected="true"] {
                background-color: #4682B4 !important;
                color: white !important;
            }
            /* Blue background for selected value in selectbox input */
            .stSelectbox [data-baseweb="select"] > div {
                background-color: #4682B4 !important;
                color: white !important;
            }
            </style>
            """, unsafe_allow_html=True)
            header_col, dropdown_col = st.columns([2, 1])
            with header_col:
                # Always display the correct header based on dropdown selection
                retention_view_val = st.session_state.get("retention_view_dropdown", "Gender")
                st.markdown(f"#### Retention by {retention_view_val}")
            with dropdown_col:
                retention_view = st.selectbox("View Retention By", ["Gender", "Generation"], key="retention_view_dropdown")
    

            if retention_view == "Gender":
                # Retention by Gender
                if selected_year == "All":
                    retention_gender = df_raw[df_raw["Year"].between(2020, 2025)].groupby(["Year", "Gender"])["Retention"].sum().reset_index()
                    retention_rate_df = df_raw[df_raw["Year"].between(2020, 2025)].groupby("Year")["Retention"].mean().reset_index()
                else:
                    retention_gender = df_raw[df_raw["Year"] == selected_year].groupby(["Year", "Gender"])["Retention"].sum().reset_index()
                    retention_rate_df = df_raw[df_raw["Year"] == selected_year].groupby("Year")["Retention"].mean().reset_index()
                retention_rate_df["RetentionRatePct"] = retention_rate_df["Retention"] * 100

                gender_colors = {"Female": "#6495ED", "Male": "#00008B"}

                if retention_gender.empty:
                    st.warning(f"No retention data available for {selected_year}")
                else:
                    retention_gender["Year_str"] = retention_gender["Year"].astype(str)
                    retention_rate_df["Year_str"] = retention_rate_df["Year"].astype(str)
                    fig = go.Figure()
                    for gender in retention_gender["Gender"].unique():
                        subset = retention_gender[retention_gender["Gender"] == gender]
                        color = gender_colors.get(gender, "#00008B")
                        fig.add_bar(x=subset["Year_str"], y=subset["Retention"], name=gender,
                                    marker_color=color, yaxis="y1")
                    fig.add_trace(go.Scatter(x=retention_rate_df["Year_str"], y=retention_rate_df["RetentionRatePct"],
                                             mode="lines+markers", name="Retention Rate (%)",
                                             line={"color": "orange", "width": 3}, yaxis="y2"))
                    fig.update_layout(
                        height=260,
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
                        xaxis={
                            "title": "Year",
                            "type": "category",
                            "tickmode": "array",
                            "tickvals": retention_gender["Year_str"].unique(),
                            "ticktext": retention_gender["Year_str"].unique(),
                            "showticklabels": False  # <-- Hide tick labels
                        },
                        barmode="group",
                        margin={"l": 60, "r": 60, "t": 20, "b": 110},
                        legend={
                            "x": 0.5,
                            "y": -0.55,
                            "xanchor": "center",
                            "yanchor": "top",
                            "orientation": "h"
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True, key="retention_by_gender")
            else:
                # Retention by Generation
                if selected_year == "All":
                    total_by_year_gen = df_raw[df_raw["Year"].between(2020, 2025)].groupby(["Year", "Generation"]).size().reset_index(name="Total")
                    active_df = df_raw[df_raw["Resignee Checking"] == "ACTIVE"]
                    active_by_year_gen = active_df[active_df["Year"].between(2020, 2025)].groupby(["Year", "Generation"]).size().reset_index(name="Active")
                else:
                    total_by_year_gen = df_raw[df_raw["Year"] == selected_year].groupby(["Year", "Generation"]).size().reset_index(name="Total")
                    active_df = df_raw[df_raw["Resignee Checking"] == "ACTIVE"]
                    active_by_year_gen = active_df[active_df["Year"] == selected_year].groupby(["Year", "Generation"]).size().reset_index(name="Active")
                retention_df = pd.merge(total_by_year_gen, active_by_year_gen, on=["Year", "Generation"], how="left")
                retention_df["RetentionRate"] = (retention_df["Active"] / retention_df["Total"]) * 100

                generation_order = ["Baby Boomer", "Gen X", "Gen Z", "Millennial"]
                generation_colors = {
                    "Gen Z": "#87CEEB",
                    "Millennial": "#4169E1",
                    "Gen X": "#1E90FF",
                    "Baby Boomer": "#00008B",
                    "Boomer": "#00008B"
                }
                retention_df["Generation"] = pd.Categorical(retention_df["Generation"], categories=generation_order, ordered=True)

                if retention_df.empty:
                    st.warning(f"No generation data available for {selected_year}")
                else:
                    fig_retention = px.bar(
                        retention_df, x="Year", y="RetentionRate", color="Generation", barmode="group",
                        text=retention_df["RetentionRate"].round(1).astype(str) + "%",
                        color_discrete_map=generation_colors,
                        category_orders={"Generation": generation_order}
                    )
                    fig_retention.update_layout(
                        height=280,
                        margin={"l": 20, "r": 20, "t": 20, "b": 110},
                        yaxis={"title": "Retention Rate (%)"},
                        xaxis={
                            "title": "Year",
                            "showticklabels": False  # <-- Hide tick labels
                        },
                        uniformtext_minsize=10,
                        uniformtext_mode="hide",
                        legend={
                            "x": 0.5,
                            "y": -0.55,
                            "xanchor": "center",
                            "yanchor": "top",
                            "orientation": "h"
                        }
                    )
                    st.plotly_chart(fig_retention, use_container_width=True, key="retention_by_generation")
                    st.markdown("<div style='height:1px'></div>", unsafe_allow_html=True)

    # -----------------------------
    # Row 2: Attrition by Month + Attrition by Voluntary vs Involuntary
    # -----------------------------
    col1, col2 = st.columns(2)

    def update_attrition_month_selection():
        if "All" in st.session_state.attrition_month_dropdown and len(st.session_state.attrition_month_dropdown) > 1:
            st.session_state.attrition_month_dropdown = ["All"]

    # Set a fixed height for both containers (e.g., 370)
    #fixed_attrition_height = 520

    with col1:
        with st.container(border=True):
            # Header and dropdown in the same line
            header_col, attrition_month_col = st.columns([2, 1])
            with header_col:
                st.markdown("#### Attrition")
            with attrition_month_col:
                # Add custom CSS for blue dropdown value
                st.markdown("""
                <style>
                .stMultiSelect [data-baseweb="tag"] {
                    background-color: #4682B4 !important;
                    color: white !important;
                }
                </style>
                """, unsafe_allow_html=True)
                if "attrition_month_dropdown" not in st.session_state:
                    st.session_state.attrition_month_dropdown = ["All"]
                selected_attrition_month = st.multiselect(
                    "Select Month", month_order, key="attrition_month_dropdown", on_change=update_attrition_month_selection
                )
                if not selected_attrition_month:
                    selected_attrition_month = ["All"]

            # Filter attrition_selected by selected months, but prevent "All" and months at the same time
            if selected_year == "All":
                attrition_selected = df_raw[(df_raw["Year"].between(2020, 2025)) & (df_raw["ResignedFlag"] == 1)].copy()
            else:
                attrition_selected = df_raw[(df_raw["Year"] == selected_year) & (df_raw["ResignedFlag"] == 1)].copy()

            attrition_selected["Month"] = pd.to_datetime(attrition_selected["Resignation Date"], errors='coerce').dt.month_name()

            # Only filter if "All" is not selected
            if "All" not in selected_attrition_month:
                attrition_selected = attrition_selected[attrition_selected["Month"].isin(selected_attrition_month)]
                months_to_plot = selected_attrition_month
            else:
                months_to_plot = [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ]

            if attrition_selected.empty:
                st.warning(f"No attrition data available for {selected_year}")
            else:
                monthly_attrition = (
                    attrition_selected.groupby("Month")
                    .size()
                    .reindex(months_to_plot)
                    .reset_index(name="AttritionCount")
                )
                fig_monthly = px.bar(
                    monthly_attrition, x="Month", y="AttritionCount", text="AttritionCount",
                    color_discrete_sequence=["#00008B"]
                )
                fig_monthly.update_layout(
                    height=280,
                    margin={"l": 20, "r": 20, "t": 20, "b": 20},
                    yaxis={"title": "Attrition Count"},
                    xaxis={"title": "Month", "type": "category", "categoryorder": "array", "categoryarray": months_to_plot},
                    uniformtext_minsize=10,
                    uniformtext_mode="hide",
                    showlegend=False
                )
                st.plotly_chart(fig_monthly, use_container_width=True, key=f"attrition_by_month_{selected_year}_{selected_attrition_month}")

    with col2:
        with st.container(border=True):
            st.markdown("##### Attrition by Voluntary vs Involuntary")
            if df_attrition is not None:
                # Convert Calendar Year to datetime and extract year
                if "Calendar Year" in df_attrition.columns:
                    df_attrition["Calendar Year"] = pd.to_datetime(df_attrition["Calendar Year"], errors='coerce')

                if "Year" not in df_attrition.columns and "Calendar Year" in df_attrition.columns:
                    df_attrition["Year"] = df_attrition["Calendar Year"].dt.year

                # Filter for selected year only
                if selected_year == "All":
                    attrition_df = df_attrition[
                        (df_attrition["Year"].between(2020, 2025)) &
                        (df_attrition["Status"].isin(["Voluntary", "Involuntary"]))
                    ]
                else:
                    attrition_df = df_attrition[
                        (df_attrition["Year"] == selected_year) &
                        (df_attrition["Status"].isin(["Voluntary", "Involuntary"]))
                    ]

                if attrition_df.empty:
                    st.warning(f"No voluntary/involuntary attrition data available for {selected_year}")
                else:
                    attrition_counts = attrition_df.groupby(["Status"]).size().reset_index(name="Count")

                    fig_attrition = px.bar(
                        attrition_counts, x="Status", y="Count", color="Status", barmode="group", text="Count",
                        color_discrete_map={"Voluntary": "#6495ED", "Involuntary": "#00008B"}
                    )
                    fig_attrition.update_layout(
                        height=280,  # Match Attrition by Month chart height
                        margin={"l": 20, "r": 20, "t": 20, "b": 20},
                        yaxis={"title": "Attrition Count"},
                        xaxis={"title": "Status"},
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
        
        # Convert Year in summary to integer
        if pd.api.types.is_datetime64_any_dtype(summary_df_row4["Year"]):
            summary_df_row4["Year"] = summary_df_row4["Year"].dt.year
        else:
            summary_df_row4["Year"] = pd.to_numeric(summary_df_row4["Year"], errors="coerce").astype(int)
        
        net_df = summary_df_row4[["Year", "Joins", "Resignations", "Net Change"]].copy()
        net_df.rename(columns={"Net Change": "NetChange"}, inplace=True)
        net_df["Status"] = net_df["NetChange"].apply(lambda x: "Increase" if x > 0 else "Decrease")
        net_df["Status"] = pd.Categorical(net_df["Status"], categories=["Increase", "Decrease"], ordered=True)
        net_df["YearStr"] = net_df["Year"].astype(str)
        # Filter for selected year(s)
        if selected_year == "All":
            net_df = net_df[net_df["Year"].between(2020, 2025)]
        else:
            net_df = net_df[net_df["Year"] == selected_year]
        color_map = {"Increase": "#2E8B57", "Decrease": "#B22222"}
        fig_net = px.bar(
            net_df, x="YearStr", y="NetChange",
            text=net_df["NetChange"].apply(lambda x: f"{x:+d}"),
            color="Status", color_discrete_map=color_map,
            hover_data={"Joins": True, "Resignations": True, "NetChange": True, "Status": True, "Year": True}
        )
        fig_net.update_layout(
            height=280,
            margin={"l": 20, "r": 20, "t": 20, "b": 20},
            yaxis={"title": "Net Change"},
            xaxis={
                "title": "Year",
                "type": "category",  # Force categorical axis to avoid fractional ticks
                "tickmode": "array",
                "tickvals": net_df["YearStr"].tolist(),
                "ticktext": net_df["YearStr"].tolist()
            },
            uniformtext_minsize=10,
            uniformtext_mode="hide"
        )
        st.plotly_chart(fig_net, use_container_width=True, key="net_talent_change")

if __name__ == "__main__":
    # Load data for standalone run
    df = pd.read_excel("HR_Analysis_Output.xlsx", sheet_name=None)
    df_raw = pd.read_excel("HR Cleaned Data 01.09.26.xlsx", sheet_name="Data")
    df_attrition = pd.read_excel("Attrition-Vol and Invol.xlsx")
    # Default year for standalone
    selected_year = "All"
    # Do NOT call st.radio here or anywhere else except inside render()
    render(df, df_raw, selected_year, df_attrition)

