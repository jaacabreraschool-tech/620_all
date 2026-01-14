import streamlit as st
import pandas as pd
import os

def display_profile_photo(photo_path, width=150, shape="circle"):
    """Helper function to display profile photos with consistent styling"""
    if os.path.exists(photo_path):
        if shape == "square":
            st.markdown(f'<style>.square-photo {{ border: 3px solid #00008B; }} </style>', unsafe_allow_html=True)
        st.image(photo_path, width=width, use_container_width=False)
    else:
        st.markdown("<h1 style='text-align: center;'>👤</h1>", unsafe_allow_html=True)
        st.caption(f"Photo not found: {photo_path}")

def render(df, df_raw, selected_year):
    st.markdown("## 📚 About This Dashboard")
    
    # -----------------------------
    # Project Overview
    # -----------------------------
    with st.container(border=True):
        st.markdown("### 📊 Project Overview & Objectives")
        
        st.markdown("""
        #### Purpose
        This interactive HR Analytics Dashboard provides comprehensive workforce insights to support 
        data-driven decision-making in human resource management. Developed as a final project for 
        **MBAN620 CGON01 - Business Data Visualization** at Mapúa University Makati, this platform 
        consolidates 6 years of HR data (2020-2025) covering 1,400+ employees.
        
        #### Key Objectives
        - 📈 **Real-time Visibility**: Monitor workforce composition, demographics, and trends
        - 🔍 **Predictive Analytics**: Identify drivers of attrition and promotion using machine learning
        - 🎯 **Strategic Planning**: Support data-driven workforce planning and talent management
        - 💡 **Actionable Insights**: Provide executive summaries and recommendations for HR strategy
        
        #### Dashboard Scope
        - **Data Period**: 2020-2025 (6 years of longitudinal data)
        - **Employee Records**: 1,400+ total headcount
        - **Metrics Tracked**: 50+ KPIs across 4 analytical domains
        - **Update Frequency**: Real-time with year selector functionality
        """)
    
    # -----------------------------
    # Methodology & Tools
    # -----------------------------
    with st.container(border=True):
        st.markdown("### 🔬 Methodology & Tools")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Data Sources
            - **HRIS Data**: Employee demographics, tenure, position levels
            - **Engagement Surveys**: 10 dimensions across Outstanding, Average, Needs Improvement
            - **Attrition Records**: Voluntary vs. involuntary turnover tracking
            - **Performance Data**: Promotion and transfer records
            
            #### Analytical Techniques
            - **Descriptive Analytics**: Workforce composition, headcount trends, demographic distribution
            - **Diagnostic Analytics**: Attrition patterns, retention analysis by segment
            - **Predictive Analytics**: Random Forest models for driver analysis (attrition & promotion)
            - **Prescriptive Analytics**: Strategic recommendations based on insights
            """)
        
        with col2:
            st.markdown("""
            #### Technology Stack
            - **Programming**: Python 3.11+
            - **Dashboard Framework**: Streamlit 1.30+
            - **Data Processing**: Pandas, NumPy
            - **Visualization**: Plotly, Plotly Express
            - **Machine Learning**: Scikit-learn (Random Forest Classifier)
            - **Data Storage**: Excel (HR_Analysis_Output.xlsx, engagement/participation data)
            
            #### Key Features
            - Interactive year selector (2020-2025)
            - Executive summaries per tab
            - Bordered containers for visual clarity
            - Standardized color scheme across all tabs
            - Theme-compatible (light/dark mode support)
            """)
    
    # -----------------------------
    # Strategic Recommendations (MAIN FOCUS)
    # -----------------------------
    with st.container(border=True):
        st.markdown("### 🎯 Strategic Recommendations")
        
        st.markdown("""
        Based on comprehensive analysis of 6 years of HR data across 1,400+ employees, 
        we recommend three high-impact initiatives to strengthen workforce management:
        """)
        
        # Recommendation 1
        with st.expander("**1. Strengthen Gen Z Retention Programs** 🚀", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                **Current State:**
                - Gen Z represents 28% of workforce (growing segment)
                - Shorter average tenure compared to Millennials
                - Higher attrition risk in first 2 years
                
                **Recommendation:**
                Implement targeted retention initiatives:
                - Mentorship programs pairing Gen Z with senior staff
                - Clear 6-month career milestone checkpoints
                - Flexible work arrangements and work-life balance policies
                - Quarterly feedback cycles (vs. annual reviews)
                - Skills development stipends for continuous learning
                """)
            
            with col2:
                st.markdown("""
                **Expected Impact:**
                - 15-20% reduction in Gen Z attrition
                - 25% improvement in early-career engagement
                - $500K annual cost savings
                
                **Timeline:** 6 months
                
                **Investment:** $150K
                
                **ROI:** 3.3x
                """)
        
        # Recommendation 2
        with st.expander("**2. Enhance Internal Mobility & Career Pathing** 📈", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                **Current State:**
                - 14-20% annual promotion rate (strong, but improvable)
                - Average 3.3 years to promotion
                - Limited visibility into career progression opportunities
                
                **Recommendation:**
                Create a formal Internal Mobility Framework:
                - Publish transparent career ladders for all roles
                - Implement 6-month job rotation program
                - Quarterly "internal job fair" to showcase opportunities
                - Skills gap analysis and targeted development plans
                - Fast-track program for high-potential employees
                """)
            
            with col2:
                st.markdown("""
                **Expected Impact:**
                - 25% promotion rate within 18 months
                - 2.8 years average time-to-promotion
                - 15% engagement score improvement
                - 30% reduction in external hiring costs
                
                **Timeline:** 12 months
                
                **Investment:** $200K
                
                **ROI:** 4.0x
                """)
        
        # Recommendation 3
        with st.expander("**3. Proactive Attrition Risk Management** 🔍", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                **Current State:**
                - 9% attrition rate (low, but improvable)
                - 70% voluntary exits (indicates controllable factors)
                - Peak attrition in Q1 and post-bonus periods
                
                **Recommendation:**
                Deploy predictive analytics and early intervention:
                - Monthly flight risk scoring using ML model (already built)
                - Quarterly "stay interviews" with at-risk employees
                - Retention bonuses for critical roles during high-risk periods
                - Exit interview insights fed back into retention strategy
                - Manager training on retention conversations
                """)
            
            with col2:
                st.markdown("""
                **Expected Impact:**
                - Reduce voluntary exits from 70% to 60%
                - Prevent 15-20 regrettable departures annually
                - $750K-$1M replacement cost savings
                - 20% manager effectiveness improvement
                
                **Timeline:** 9 months
                
                **Investment:** $100K
                
                **ROI:** 7.5x
                """)
        
        # Summary Table
        st.markdown("---")
        st.markdown("#### 📊 Implementation Summary")
        
        summary_data = {
            "Recommendation": [
                "1. Gen Z Retention Programs",
                "2. Internal Mobility Framework", 
                "3. Attrition Risk Management",
                "**TOTAL**"
            ],
            "Investment": ["$150K", "$200K", "$100K", "**$450K**"],
            "Timeline": ["6 months", "12 months", "9 months", "**9-12 months**"],
            "Expected Savings": ["$500K/year", "$800K/year", "$1M/year", "**$2.3M/year**"],
            "ROI": ["3.3x", "4.0x", "7.5x", "**5.1x**"],
            "Priority": ["🔴 High", "🔴 High", "🟡 Medium", ""]
        }
        
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    # -----------------------------
    # Research Team
    # -----------------------------
    with st.container(border=True):
        st.markdown("### 👨‍🎓 Research Team")
        
        # Add CSS for uniform photo sizing and column heights
        st.markdown("""
        <style>
        [data-testid="stImage"] {
            width: 150px !important;
            height: 150px !important;
            object-fit: cover;
            display: block;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        [data-testid="column"] {
            min-height: 750px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            col1_inner_left, col1_inner_center, col1_inner_right = st.columns([0.2, 0.6, 0.2])
            with col1_inner_center:
                display_profile_photo("angelie.jpg", width=150)
            st.write("")  # Spacing
            st.markdown("""**Angelie D. Agustin**""")
            st.markdown("""
            - Master's Student, MAN
            - Mapúa University Makati
            - Email: angelie.agustin@mapua.edu.ph
            - LinkedIn: https://ph.linkedin.com/in/angelie-agustin
            
            ---
            """, unsafe_allow_html=True)
            st.markdown("""
            <p style='font-size: 14px;'>
            Angelie Agustin is a Business Continuity Consultant focused on operational resilience, 
            regulatory compliance, and data-driven reporting. With a BS in Statistics and an MA in 
            Education (Mathematics), she blends analytical rigor with thoughtful problem-solving. 
            Outside of work, she enjoys travelling, and continuously growing—now pursuing MAN at 
            Mapúa University to deepen her expertise in analytics and decision-making.
            </p>
            """, unsafe_allow_html=True)
        
        with col2:
            col2_inner_left, col2_inner_center, col2_inner_right = st.columns([0.2, 0.6, 0.2])
            with col2_inner_center:
                display_profile_photo("catherine.jpg", width=150)
            st.write("")  # Spacing
            st.markdown("""**Ma. Catherine Pacheco**""")
            st.markdown("""
            - Master's Student, MAN
            - Mapúa University Makati
            - Email: mcpacheco@mymail.mapua.edu.ph
            - LinkedIn: https://www.linkedin.com/in/catherine-p-160717178/
            
            ---
            """, unsafe_allow_html=True)
            st.markdown("""
            <p style='font-size: 14px;'>
            Catherine is a Security and GRC professional with hands-on experience across the Consumer Goods & Services, Finance, FMCG, Manufacturing, Retail, and Utilities industries. She possesses deep expertise in Security Management and Administration, consistently delivering results through end-to-end security project management. And successfully led and supported various SAP, SailPoint, Pathlock, and related technology implementations, system integrations, project enhancements, rollouts, data and system migrations, and upgrades for diverse clients. Whether tackling complex security initiatives or streamlining access governance, Catherine doesn't just meet expectations; she exceeds them and redefines the standards of excellence.
            </p>
            """, unsafe_allow_html=True)
        
        with col3:
            col3_inner_left, col3_inner_center, col3_inner_right = st.columns([0.2, 0.6, 0.2])
            with col3_inner_center:
                display_profile_photo("juliana.jpg", width=150)
            st.write("")  # Spacing
            st.markdown("""**Juliana Amparo A. Cabrera**""")
            st.markdown("""
            - Master's Student, MAN
            - Mapúa University Makati
            - Email: jaacabrera@mymail.mapua.edu.ph
            - LinkedIn: https://www.linkedin.com/in/jaacabrera/
            
            ---
            """, unsafe_allow_html=True)
            st.markdown("""
            <p style='font-size: 14px;'>
            Juliana "Jam" Cabrera is a Software Quality Assurance professional with expertise in testing desktop, web, and mobile applications. Skilled in analyzing business requirements, designing test strategies, and executing manual tests, she ensures the delivery of high-quality solutions across platforms. She holds a degree in Computer Science from Mapúa University and is currently pursuing a Master of Analytics (MAN) at Mapúa University to continuously expand her knowledge and skill set.
            </p>
            """, unsafe_allow_html=True)
    
    # -----------------------------
    # Contact & Resources
    # -----------------------------
    with st.container(border=True):
        st.markdown("### 📧 Contact Information & Resources")
        st.markdown("**GitHub**: https://github.com/jaacabreraschool-tech/MBAN620")
        st.markdown("We welcome feedback to improve this dashboard. **Submit via**: Email above")
    
    # -----------------------------
    # Footer
    # -----------------------------
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    &copy; 2025 Agustin, Pacheco, Cabrera | MBAN620 CGON01 - Business Data Visualization | Mapúa University Makati<br>
    Final Project | Master in Analytics (MAN) | January 2025
    </div>
    """, unsafe_allow_html=True)
