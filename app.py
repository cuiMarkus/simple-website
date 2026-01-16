import streamlit as st
import pandas as pd
import time

# Custom CSS for animated Tails
st.markdown("""
<style>
.tails-sprite {
    width: 64px;
    height: 64px;
    background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
        <circle cx="32" cy="32" r="28" fill="%23FFA500"/>
        <circle cx="20" cy="25" r="3" fill="%23000"/>
        <circle cx="44" cy="25" r="3" fill="%23000"/>
        <path d="M 20 40 Q 32 48 44 40" stroke="%23000" stroke-width="2" fill="none"/>
        <circle cx="15" cy="15" r="8" fill="%23FFA500"/>
        <circle cx="49" cy="15" r="8" fill="%23FFA500"/>
        <circle cx="10" cy="10" r="5" fill="%23FFA500"/>
        <circle cx="54" cy="10" r="5" fill="%23FFA500"/>
        <circle cx="8" cy="8" r="3" fill="%23FFF"/>
        <circle cx="56" cy="8" r="3" fill="%23FFF"/>
    </svg>') no-repeat center;
    background-size: contain;
    animation: tails-sprite-animation 0.8s steps(4) infinite, float 3s ease-in-out infinite;
}

.tails-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.tails-container:hover {
    transform: scale(1.2);
}

@keyframes tails-sprite-animation {
    0% { transform: translateX(0) rotate(0deg); }
    25% { transform: translateX(-5px) rotate(-5deg); }
    50% { transform: translateX(0) rotate(0deg); }
    75% { transform: translateX(5px) rotate(5deg); }
    100% { transform: translateX(0) rotate(0deg); }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.tails-message {
    background: linear-gradient(135deg, #FFA500 0%, #FF6347 100%);
    color: white;
    padding: 10px 15px;
    border-radius: 20px;
    font-size: 14px;
    margin: 10px 0;
    text-align: center;
    animation: fadeIn 0.5s ease-in;
    font-weight: bold;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.tails-button {
    background: linear-gradient(135deg, #FFA500 0%, #FF6347 100%);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.tails-button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(255, 165, 0, 0.4);
}
</style>
""", unsafe_allow_html=True)

# Page config
st.set_page_config(
    page_title="My Simple Streamlit Website",
    page_icon="🌐",
    layout="centered"
)

# Title and description
st.title("🌐 My Simple Streamlit Website")
st.write("Welcome! This is a simple website built using Streamlit.")

# Animated Tails the Fox
st.markdown("""
<div class="tails-container">
    <div class="tails-sprite"></div>
</div>
""", unsafe_allow_html=True)

# Tails message
if 'tails_message' not in st.session_state:
    st.session_state.tails_message = ""

tails_messages = [
    "Hi! I'm Tails! ", 
    "Da mint :3",
    "Nice keyword analysis! 🔍",
    "hehe >:3 ",
    "Data is awesome! 📈"
]

if st.button("🦊 Talk to Tails!", key="tails_button"):
    import random
    st.session_state.tails_message = random.choice(tails_messages)

if st.session_state.tails_message:
    st.markdown(f'<div class="tails-message">{st.session_state.tails_message}</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Keyword Dashboard", "About", "Contact"])

# Pages
if page == "Home":
    st.subheader("🏠 Home")
    st.write("This is the home page.")
    
    name = st.text_input("What's your name?")
    if name:
        st.success(f"Hello, {name}! 👋")

    if st.button("Click me"):
        st.balloons()

elif page == "Keyword Dashboard":
    st.subheader("🔍 Keyword Dashboard")
    st.caption("Source: testout.csv - Keyword frequency analysis")

    @st.cache_data
    def load_keyword_data():
        try:
            df = pd.read_csv("testout.csv", encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv("testout.csv", encoding='cp949')
        return df

    keyword_df = load_keyword_data()
    df = keyword_df.copy()
    
    # Get date columns (all columns except the first one which is '키워드')
    date_columns = df.columns[1:]
    
    # Sidebar filters
    st.sidebar.header("Filters")
    search = st.sidebar.text_input("Search keywords")
    
    # Date range selector
    if len(date_columns) > 0:
        selected_dates = st.sidebar.multiselect(
            "Select dates",
            options=date_columns.tolist(),
            default=date_columns.tolist()[:min(7, len(date_columns))]  # Show last 7 days by default
        )
    else:
        selected_dates = date_columns
    
    # Filter data
    if search:
        df = df[df['키워드'].str.contains(search, case=False, na=False)]
    
    if selected_dates:
        columns_to_keep = ['키워드'] + selected_dates
        df = df[columns_to_keep]
    
    # Summary statistics
    if not df.empty and selected_dates:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_keywords = len(df)
            st.metric("Total Keywords", total_keywords)
        
        with col2:
            total_mentions = df[selected_dates].sum().sum()
            st.metric("Total Mentions", int(total_mentions))
        
        with col3:
            avg_mentions = df[selected_dates].sum().mean()
            st.metric("Avg Mentions/Keyword", f"{avg_mentions:.1f}")
        
        with col4:
            if len(selected_dates) > 1:
                latest_date = selected_dates[-1]
                previous_date = selected_dates[-2] if len(selected_dates) > 1 else selected_dates[0]
                latest_total = df[latest_date].sum()
                previous_total = df[previous_date].sum()
                change = latest_total - previous_total
                st.metric("Change vs Previous", f"{change:+d}")
            else:
                st.metric("Latest Day", df[selected_dates].sum().sum())
    
    # Calculate total frequency for each keyword
    if not df.empty and selected_dates:
        df['총 빈도수'] = df[selected_dates].sum(axis=1)
        df_sorted = df.sort_values('총 빈도수', ascending=False)
        
        # Top keywords section
        st.subheader("📊 Top Keywords")
        
        # Display top keywords in columns
        top_n = st.slider("Number of top keywords to show", 5, 20, 10)
        top_keywords = df_sorted.head(top_n)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Bar chart of top keywords
            st.bar_chart(top_keywords.set_index('키워드')['총 빈도수'])
        
        with col2:
            # Table of top keywords
            st.dataframe(top_keywords[['키워드', '총 빈도수']].reset_index(drop=True))
        
        # Trend analysis for top keywords
        st.subheader("📈 Keyword Trends")
        selected_keyword = st.selectbox("Select keyword for trend analysis", options=top_keywords['키워드'].tolist())
        
        if selected_keyword:
            keyword_data = df[df['키워드'] == selected_keyword]
            if not keyword_data.empty:
                trend_data = keyword_data[selected_dates].iloc[0]
                st.line_chart(trend_data)
                
                # Show detailed stats for selected keyword
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Frequency", int(trend_data.sum()))
                with col2:
                    st.metric("Average Daily", f"{trend_data.mean():.1f}")
                with col3:
                    st.metric("Peak Day", f"{trend_data.max()} on {trend_data.idxmax()}")
    
    # Raw data section
    with st.expander("🔍 View raw data"):
        st.dataframe(df)

elif page == "About":
    st.subheader("ℹ️ About")
    st.write(
        "This website is built with **Streamlit**, "
        "a Python framework for creating web apps quickly."
    )

elif page == "Contact":
    st.subheader("📧 Contact")
    st.write("You can reach me at:")
    st.write("- Email: p20901@sw.hs.kr")
    st.write("- GitHub: https://github.com/cuiMarkus")









