import streamlit as st
from app_pages import dashboard, home, chat, summary

def main() :
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    if st.session_state.page == "dashboard":
        dashboard.dashboard()
    elif st.session_state.page == "page1":
        home.home()
    elif st.session_state.page == "page2":
        chat.chat()
    elif st.session_state.page == "page3":
        summary.summary()
    
if __name__ == "__main__":
    main()
