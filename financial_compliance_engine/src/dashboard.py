import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sourcing import DataSourcer
from analytics import AnalyticsEngine
from data_models import FinancialStatement
from legal_monitoring import LegalDataIngestor, LegalAnalyzer
from nfra_engine import NFRAChatbot

# Page Config
st.set_page_config(page_title="AI Financial Analytics Tool", layout="wide")

# Title
st.title("AI Financial Compliance & Analytics Engine")

# Sidebar
st.sidebar.header("Configuration")
company_name = st.sidebar.text_input("Company Name/Symbol", "DEMO_CORP")
analysis_mode = st.sidebar.selectbox("Analysis Mode", ["Executive Overview", "Financial Performance", "Risk & Anomalies", "Governance", "Legal Monitoring", "NFRA Assistant"])

# Initialize Engines
sourcer = DataSourcer()
analytics = AnalyticsEngine()
legal_ingestor = LegalDataIngestor()
legal_analyzer = LegalAnalyzer()
chatbot = NFRAChatbot()

if st.sidebar.button("Run Analysis"):
    with st.spinner("Fetching and Analyzing Data..."):
        # 1. Fetch Data
        market_data = sourcer.fetch_market_data(company_name)
        audit_history = sourcer.fetch_audit_history(company_name)
        governance = sourcer.fetch_governance_data(company_name)
        
        # Mock Financial Statement Data for Ratios
        financial_data = {
            'balance_sheet': {
                'Total Assets': {'current': 10000},
                'Current Assets': {'current': 4000},
                'Current Liabilities': {'current': 3000},
                'Retained Earnings': {'current': 2000},
                'Total Equity': {'current': 5000},
                'Total Liabilities': {'current': 5000}
            },
            'income_statement': {
                'Revenue': {'current': 15000},
                'EBIT': {'current': 2500},
                'Profit': {'current': 1800}
            }
        }
        
        # 2. Run Analytics
        risk_metrics = analytics.calculate_risk_indicators(financial_data)
        prediction = analytics.predict_future_performance(market_data)
        
        # Generate Mock Transaction Data for Anomaly Detection
        np.random.seed(42)
        transactions = pd.DataFrame({
            'Transaction_ID': range(1, 101),
            'Amount': np.concatenate([np.random.normal(1000, 100, 95), np.random.normal(10000, 500, 5)]) # 5 anomalies
        })
        analyzed_transactions = analytics.detect_anomalies(transactions)

        # Store in session state
        st.session_state['data'] = {
            'market': market_data,
            'audit': audit_history,
            'governance': governance,
            'risk': risk_metrics,
            'prediction': prediction,
            'anomalies': analyzed_transactions
        }
        st.success("Analysis Complete!")

# Display dashboard if data exists
if 'data' in st.session_state:
    data = st.session_state['data']
    
    if analysis_mode == "Executive Overview":
        col1, col2, col3 = st.columns(3)
        col1.metric("Compliance Status", "Conditional", "2 Flags")
        col2.metric("Altman Z-Score", data['risk']['Altman_Z_Score'], data['risk']['Z_Score_Zone'])
        col3.metric("Stock Trend", data['prediction']['Trend'])
        
        st.subheader("Market Performance")
        st.line_chart(data['market'].set_index('Date')['Close'])
    
    elif analysis_mode == "Financial Performance":
        st.subheader("Key Ratios")
        ratios = data['risk']['Performance_Ratios']
        c1, c2, c3 = st.columns(3)
        c1.metric("ROE", ratios['ROE'])
        c2.metric("Current Ratio", ratios['Current_Ratio'])
        c3.metric("Debt-to-Equity", ratios['Debt_to_Equity'])
        
        st.subheader("Predictive Analytics")
        st.info(data['prediction']['Forecast_30d'])
    
    elif analysis_mode == "Risk & Anomalies":
        st.subheader("Anomaly Detection (Isolation Forest)")
        anomalies = data['anomalies'][data['anomalies']['Is_Anomaly'] == True]
        st.warning(f"Detected {len(anomalies)} anomalous transactions out of {len(data['anomalies'])}")
        
        # Scatter plot
        fig = px.scatter(data['anomalies'], x='Transaction_ID', y='Amount', color='Is_Anomaly', 
                         title="Transaction Anomaly Detection", color_discrete_map={True: 'red', False: 'blue'})
        st.plotly_chart(fig)
        
        st.dataframe(anomalies)
        
        st.subheader("Audit History")
        st.table(pd.DataFrame(data['audit']))

    elif analysis_mode == "Governance":
        st.subheader("Board Composition")
        board_df = pd.DataFrame(data['governance']['board_members'])
        st.table(board_df)
        
        st.subheader("Committee Structures")
        st.json(data['governance']['committees'])
    
    elif analysis_mode == "Legal Monitoring":
        st.subheader("Real-Time Legal & Enforcement Feed")
        
        if st.button("Refresh Feed"):
             # Fetch and Analyze
             raw_feed = legal_ingestor.fetch_live_feed()
             analyzed_feed = [legal_analyzer.analyze_event(event) for event in raw_feed]
             st.session_state['legal_feed'] = analyzed_feed
        
        if 'legal_feed' in st.session_state:
            feed = st.session_state['legal_feed']
            
            # Filters
            col1, col2 = st.columns(2)
            min_score = col1.slider("Minimum Risk Score", 0, 100, 0)
            source_filter = col2.multiselect("Filter Source", list(set(e['source'] for e in feed)), default=list(set(e['source'] for e in feed)))
            
            filtered_feed = [e for e in feed if e['risk_score'] >= min_score and e['source'] in source_filter]
            
            st.metric("Active Alerts", len(filtered_feed), f"{len([e for e in filtered_feed if e['risk_level'] == 'CRITICAL'])} Critical")
            
            for event in filtered_feed:
                # Color code based on risk
                color = "red" if event['risk_level'] == 'CRITICAL' else "orange" if event['risk_level'] == 'HIGH' else "blue"
                
                with st.expander(f"[{event['risk_level']}] {event['title']} ({event['source']})"):
                    st.write(f"**Timestamp:** {event['timestamp']}")
                    st.write(f"**Content:** {event['content']}")
                    st.write(f"**Risk Score:** {event['risk_score']}")
                    st.write("**Identified Entities:**")
                    st.json(event['entities'])
                    st.write("**Risk Factors:**")
                    st.write(", ".join(event['risk_factors']))
                    st.markdown(f"[View Document]({event['link']})")
        else:
            st.info("Click 'Refresh Feed' to view live enforcement data.")
    
    elif analysis_mode == "NFRA Assistant":
        st.subheader("NFRA Document Query Assistant (AI Chatbot)")
        
        st.markdown("""
        **Capabilities:**  
        ✅ Semantic search over NFRA circulars and Audit Standards  
        ✅ Secure compliance logging  
        ✅ Source citation
        """)
        
        # Chat Interface
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User Input
        if prompt := st.chat_input("Ask a reasonable question about NFRA guidelines..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing documents..."):
                    response = chatbot.query_knowledge_base(prompt)
                    answer = response['answer']
                    st.markdown(answer)
                    
                    # Show sources in expander
                    with st.expander("View Source Documents"):
                        for doc in response['sources']:
                            st.info(f"**{doc['metadata']['source']}** (p. {doc['metadata']['page']}): {doc['content']}")
            
            st.session_state.messages.append({"role": "assistant", "content": answer})

else:
    st.info("Click 'Run Analysis' to generate insights.")
