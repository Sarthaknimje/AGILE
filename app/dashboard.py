import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import requests
import os
from google import genai
from google.genai import types

from app.core.config import settings
from app.services.infer import RiskModelService

# Configure Streamlit
st.set_page_config(
    page_title="SPM AI Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .prediction-result {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .ai-analysis {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 Strategic Portfolio Management - AI Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.selectbox("Choose a page:", ["📈 Portfolio Analytics", "🔮 AI Prediction", "🤖 AI Analysis", "📋 Project Management"])

# Initialize Gemini API
@st.cache_resource
def init_gemini():
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyAqpPj7ol_1hehTfD3Js9znEOhpABcQugk"))
        return client
    except Exception as e:
        st.sidebar.error(f"Gemini API not available: {e}")
        return None

gemini_client = init_gemini()

if page == "📈 Portfolio Analytics":
    st.header("📊 Portfolio Analytics Dashboard")
    
    processed = Path(settings.data_dir) / "processed" / "portfolios.csv"
    if not processed.exists():
        st.warning("Dataset not found. Generate data with: python -m app.data.generate")
    else:
        df = pd.read_csv(processed)
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Portfolios", len(df))
        with col2:
            avg_risk = df['risk_level'].value_counts().index[0]
            st.metric("Most Common Risk", avg_risk)
        with col3:
            avg_return = df['avg_return'].mean()
            st.metric("Avg Return", f"{avg_return:.2%}")
        with col4:
            avg_vol = df['volatility'].mean()
            st.metric("Avg Volatility", f"{avg_vol:.2%}")
        
        # Risk Distribution
        st.subheader("🎯 Risk Distribution Analysis")
        fig = px.pie(df, names="risk_level", title="Portfolio Risk Distribution", 
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance Analysis
        st.subheader("📈 Performance Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(df, x="volatility", y="avg_return", color="risk_level",
                           title="Return vs Volatility", hover_data=["sharpe_ratio"])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.box(df, x="risk_level", y="sharpe_ratio", title="Sharpe Ratio by Risk Level")
            st.plotly_chart(fig, use_container_width=True)

elif page == "🔮 AI Prediction":
    st.header("🔮 AI-Powered Risk Prediction")
    st.markdown("Enter your portfolio parameters below to get an AI-powered risk assessment:")
    
    # Create a more user-friendly form
    with st.form("portfolio_prediction"):
        st.subheader("📊 Portfolio Parameters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📈 Performance Metrics**")
            avg_return = st.slider(
                "Average Return (%)", 
                min_value=0.0, max_value=20.0, value=6.0, step=0.1,
                help="Expected annual return percentage"
            )
            volatility = st.slider(
                "Volatility (%)", 
                min_value=0.0, max_value=50.0, value=12.0, step=0.1,
                help="Portfolio volatility (standard deviation)"
            )
            sharpe_ratio = st.slider(
                "Sharpe Ratio", 
                min_value=0.0, max_value=2.0, value=0.35, step=0.01,
                help="Risk-adjusted return ratio"
            )
            size = st.number_input(
                "Portfolio Size ($)", 
                min_value=10000, max_value=10000000, value=1000000, step=10000,
                help="Total portfolio value in dollars"
            )
        
        with col2:
            st.markdown("**⚖️ Asset Allocation**")
            equity_weight = st.slider(
                "Equity Weight (%)", 
                min_value=0.0, max_value=100.0, value=60.0, step=1.0,
                help="Percentage allocated to stocks"
            )
            bond_weight = st.slider(
                "Bond Weight (%)", 
                min_value=0.0, max_value=100.0, value=30.0, step=1.0,
                help="Percentage allocated to bonds"
            )
            alt_weight = st.slider(
                "Alternative Weight (%)", 
                min_value=0.0, max_value=100.0, value=10.0, step=1.0,
                help="Percentage allocated to alternatives"
            )
            
            # Validation
            total_weight = equity_weight + bond_weight + alt_weight
            if abs(total_weight - 100.0) > 0.1:
                st.error(f"Asset weights must sum to 100%. Current total: {total_weight:.1f}%")
        
        with col3:
            st.markdown("**📊 Market Factors**")
            factor_mkt = st.slider(
                "Market Factor", 
                min_value=-2.0, max_value=2.0, value=0.0, step=0.1,
                help="Market beta factor"
            )
            factor_size = st.slider(
                "Size Factor", 
                min_value=-2.0, max_value=2.0, value=0.0, step=0.1,
                help="Small cap vs large cap factor"
            )
            factor_value = st.slider(
                "Value Factor", 
                min_value=-2.0, max_value=2.0, value=0.0, step=0.1,
                help="Value vs growth factor"
            )
            factor_mom = st.slider(
                "Momentum Factor", 
                min_value=-2.0, max_value=2.0, value=0.0, step=0.1,
                help="Momentum factor"
            )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Get AI Prediction", use_container_width=True)
        
        if submitted and abs(total_weight - 100.0) <= 0.1:
            try:
                # Prepare data
                portfolio_data = {
                    "avg_return": avg_return / 100,
                    "volatility": volatility / 100,
                    "sharpe_ratio": sharpe_ratio,
                    "size": float(size),
                    "equity_weight": equity_weight / 100,
                    "bond_weight": bond_weight / 100,
                    "alt_weight": alt_weight / 100,
                    "factor_mkt": factor_mkt,
                    "factor_size": factor_size,
                    "factor_value": factor_value,
                    "factor_mom": factor_mom,
                }
                
                # Get prediction
                svc = RiskModelService()
                prediction = svc.predict([portfolio_data])[0]
                
                # Display results
                st.markdown('<div class="prediction-result">', unsafe_allow_html=True)
                st.subheader("🎯 AI Prediction Results")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    risk_color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                    st.metric("Risk Level", f"{risk_color.get(prediction, '⚪')} {prediction}")
                
                with col2:
                    st.metric("Expected Return", f"{avg_return:.2f}%")
                
                with col3:
                    st.metric("Volatility", f"{volatility:.2f}%")
                
                # Risk visualization
                risk_levels = ["Low", "Medium", "High"]
                risk_values = [0.33, 0.66, 1.0]
                pred_value = {"Low": 0.33, "Medium": 0.66, "High": 1.0}[prediction]
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = pred_value,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Risk Level"},
                    gauge = {
                        'axis': {'range': [None, 1]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 0.33], 'color': "lightgreen"},
                            {'range': [0.33, 0.66], 'color': "yellow"},
                            {'range': [0.66, 1], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': pred_value
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error predicting. Ensure model is trained. Details: {e}")
                st.info("Train model with: python -m app.models.train")

elif page == "🤖 AI Analysis":
    st.header("🤖 Gemini AI Portfolio Analysis")
    
    if gemini_client is None:
        st.error("Gemini API is not available. Please check your API key.")
    else:
        # Get portfolio data from previous prediction or use defaults
        if 'portfolio_data' in locals():
            data = portfolio_data
        else:
            data = {
                "avg_return": 0.06,
                "volatility": 0.12,
                "sharpe_ratio": 0.35,
                "size": 1000000.0,
                "equity_weight": 0.6,
                "bond_weight": 0.3,
                "alt_weight": 0.1,
                "factor_mkt": 0.0,
                "factor_size": 0.0,
                "factor_value": 0.0,
                "factor_mom": 0.0,
            }
        
        st.subheader("📊 Current Portfolio Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            st.json({
                "Expected Return": f"{data['avg_return']:.2%}",
                "Volatility": f"{data['volatility']:.2%}",
                "Sharpe Ratio": f"{data['sharpe_ratio']:.2f}",
                "Portfolio Size": f"${data['size']:,.0f}"
            })
        
        with col2:
            st.json({
                "Equity Allocation": f"{data['equity_weight']:.1%}",
                "Bond Allocation": f"{data['bond_weight']:.1%}",
                "Alternative Allocation": f"{data['alt_weight']:.1%}",
                "Total Allocation": f"{data['equity_weight'] + data['bond_weight'] + data['alt_weight']:.1%}"
            })
        
        if st.button("🧠 Get AI Analysis", use_container_width=True):
            with st.spinner("Gemini AI is analyzing your portfolio..."):
                try:
                    # Create analysis prompt
                    prompt = f"""
                    As a financial advisor and portfolio analyst, please provide a comprehensive analysis of this portfolio:
                    
                    Portfolio Details:
                    - Expected Return: {data['avg_return']:.2%}
                    - Volatility: {data['volatility']:.2%}
                    - Sharpe Ratio: {data['sharpe_ratio']:.2f}
                    - Portfolio Size: ${data['size']:,.0f}
                    - Asset Allocation: {data['equity_weight']:.1%} Equity, {data['bond_weight']:.1%} Bonds, {data['alt_weight']:.1%} Alternatives
                    - Market Factors: Market={data['factor_mkt']:.1f}, Size={data['factor_size']:.1f}, Value={data['factor_value']:.1f}, Momentum={data['factor_mom']:.1f}
                    
                    Please provide:
                    1. Risk assessment and recommendations
                    2. Asset allocation optimization suggestions
                    3. Performance expectations
                    4. Potential improvements
                    5. Market factor analysis
                    
                    Format your response in clear sections with actionable insights.
                    """
                    
                    response = gemini_client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            thinking_config=types.ThinkingConfig(thinking_budget=0)
                        )
                    )
                    
                    st.markdown('<div class="ai-analysis">', unsafe_allow_html=True)
                    st.markdown("## 🤖 Gemini AI Portfolio Analysis")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error getting AI analysis: {e}")

elif page == "📋 Project Management":
    st.header("📋 Agile Project Management")
    
    # Try to fetch Jira issues from API
    try:
        response = requests.get("http://localhost:8000/jira/issues")
        if response.status_code == 200:
            issues = response.json()
            
            st.subheader(f"📊 Project Overview - {len(issues)} Issues")
            
            if issues:
                # Create DataFrame for better display
                df_issues = pd.DataFrame(issues)
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Issues", len(issues))
                with col2:
                    priority_counts = df_issues['priority'].value_counts()
                    st.metric("High Priority", priority_counts.get('High', 0))
                with col3:
                    type_counts = df_issues['issue_type'].value_counts()
                    st.metric("Stories", type_counts.get('Story', 0))
                with col4:
                    recent_issues = len(df_issues[df_issues['created_at'] > '2024-01-01'])
                    st.metric("Recent Issues", recent_issues)
                
                # Display issues in a nice table
                st.subheader("📋 Current Issues")
                st.dataframe(
                    df_issues[['id', 'issue_type', 'summary', 'priority', 'created_at']],
                    use_container_width=True
                )
            else:
                st.info("No issues found. Import some data using the API.")
        else:
            st.error("Could not connect to API. Make sure the server is running.")
    except Exception as e:
        st.error(f"Error fetching project data: {e}")
    
    st.subheader("🔗 Quick Links")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)")
    with col2:
        st.markdown("**Import CSV:** Use POST /jira/import endpoint")

# Footer
st.markdown("---")
st.markdown("🚀 **Strategic Portfolio Management AI Dashboard** | Built with Streamlit, FastAPI, and Gemini AI")
