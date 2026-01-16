import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="My Simple Streamlit Website",
    page_icon="🌐",
    layout="centered"
)

# Title and description
st.title("🌐 My Simple Streamlit Website")
st.write("Welcome! This is a simple website built using Streamlit.")

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









