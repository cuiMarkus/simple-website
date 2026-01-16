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
    st.subheader("� Keyword Dashboard")
    st.caption("Source: testout.csv")

    @st.cache_data
    def load_keyword_data():
        try:
            df = pd.read_csv("testout.csv", encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv("testout.csv", encoding='cp949')
        return df

    keyword_df = load_keyword_data()
    df = keyword_df.copy()

    # Search functionality
    search = st.text_input("Search keywords")

    if search:
        df = df[df['키워드'].str.contains(search, case=False, na=False)]

    # Display metrics
    st.metric("Total Keywords", len(df))
    
    # Get date columns (all columns except the first one which is '키워드')
    date_columns = df.columns[1:]
    
    if not df.empty:
        # Calculate total frequency for each keyword
        df['총 빈도수'] = df[date_columns].sum(axis=1)
        
        # Sort by total frequency
        df_sorted = df.sort_values('총 빈도수', ascending=False)
        
        # Display top keywords
        st.subheader("📊 Top Keywords by Total Frequency")
        top_keywords = df_sorted.head(10)
        
        for _, row in top_keywords.iterrows():
            with st.container():
                keyword = row['키워드']
                total_freq = row['총 빈도수']
                st.markdown(f"### **{keyword}**")
                st.metric("Total Frequency", int(total_freq))
                
                # Show frequency chart for this keyword
                freq_data = row[date_columns]
                st.bar_chart(freq_data)
                st.divider()

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









