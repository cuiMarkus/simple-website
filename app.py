import streamlit as st

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
page = st.sidebar.selectbox("Go to", ["Home", "About", "Contact"])

# Pages
if page == "Home":
    st.subheader("🏠 Home")
    st.write("This is the home page.")
    
    name = st.text_input("What's your name?")
    if name:
        st.success(f"Hello, {name}! 👋")

    if st.button("Click me"):
        st.balloons()

elif page == "News":
    st.subheader("🗞️ News Dashboard")
    st.caption("Source: testout.csv")

    search = st.text_input("Search news")

    df = news_df.copy()

    if search:
        df = df[df.apply(
            lambda row: row.astype(str).str.contains(search, case=False).any(),
            axis=1
        )]

    st.metric("Total Articles", len(df))

    for _, row in df.iterrows():
        with st.container():
            st.markdown(f"### {row.get('title', 'No title')}")
            if 'source' in row:
                st.caption(row.get('source'))
            if 'description' in row:
                st.write(row.get('description'))
            if 'url' in row:
                st.markdown(f"[Read more]({row.get('url')})")
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
    st.write("- Email: example@email.com")
    st.write("- GitHub: https://github.com/yourusername")



