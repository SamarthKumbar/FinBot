import streamlit as st
# Assuming your utility functions are in a 'utils.py' file
from utils import login_user, upload_pdf, ask_question, register_user

st.set_page_config(page_title="Balance Sheet Analyst", layout="wide")
st.title("📊 Chat with Balance Sheets")

# ---------------------------
# 🔐 Session State Initialization
# ---------------------------
# Stores the authentication token
if "token" not in st.session_state:
    st.session_state.token = None
# Manages which auth screen to show: 'login' or 'register'
if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"
# Stores chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------
# 🛂 Authentication Section
# ---------------------------
if st.session_state.token is None:
    # --- Login View ---
    if st.session_state.auth_view == "login":
        st.subheader("🔐 Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                token = login_user(email, password)
                if token:
                    st.session_state.token = token
                    st.success("✅ Login successful")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")

        st.info("Don't have an account?")
        if st.button("Register Here"):
            st.session_state.auth_view = "register"
            st.rerun()

    # --- Registration View ---
    elif st.session_state.auth_view == "register":
        st.subheader("📝 Register New Account")
        with st.form("register_form"):
            email = st.text_input("Email", key="register_email")
            name = st.text_input("Full Name", key="register_name")
            password = st.text_input("Password", type="password", key="register_password")
            role = st.selectbox("Role", ["analyst", "top-management"], key="register_role")

            if st.form_submit_button("Register"):
                try:
                    response = register_user(email, name, password, role)

                    if response and response.status_code == 200:
                        st.success("🎉 Registered successfully! Please return to the login page.")
                    elif response and response.status_code == 400:
                        detail = response.json().get("detail", "Registration error.")
                        if detail == "Email already registered":
                            st.warning("⚠️ This email is already registered. Please log in.")
                        else:
                            st.error(f"Registration failed: {detail}")
                    else:
                        detail = "An unexpected error occurred."
                        try:
                            detail = response.json().get("detail", detail)
                        except Exception:
                            pass # Keep the default error message
                        st.error(f"Registration failed: {detail}")

                except Exception as e:
                    st.error(f"An error occurred during registration: {str(e)}")

        st.info("Already have an account?")
        if st.button("Login Here"):
            st.session_state.auth_view = "login"
            st.rerun()

# ---------------------------
# ✅ Authenticated Application View
# ---------------------------
else:
    st.sidebar.success("Logged in ✅")

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.auth_view = "login" # Reset to login view
        st.session_state.messages = [] # Clear chat history
        st.rerun()

    # Navigation for authenticated user
    nav = st.sidebar.radio("Menu", ["Chat", "Upload PDF"])

    # --- Chat Page ---
    if nav == "Chat":
        st.subheader("💬 Ask a Question")
        st.info("Ask questions about the financial data from the uploaded balance sheets.")

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("What is the total revenue for Q2?"):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.spinner("Thinking..."):
                try:
                    response_data = ask_question(prompt, st.session_state.token)
                    response = response_data.get('answer', '🤖 Sorry, I could not find an answer.')
                except Exception as e:
                    response = f"🤖 Error: Could not get an answer. {str(e)}"

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # --- Upload Page ---
    elif nav == "Upload PDF":
        st.subheader("📎 Upload Balance Sheet (PDF)")
        st.info("Upload a balance sheet PDF to make it available for analysis in the chat.")

        company_name = st.text_input("Company Name")
        report_date = st.date_input("Balance Sheet Date")
        uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

        if st.button("Upload Document"):
            if uploaded_file and company_name and report_date:
                with st.spinner("Processing and uploading..."):
                    try:
                        result = upload_pdf(uploaded_file, st.session_state.token)
                        st.success(result.get("message", "✅ Upload successful"))
                    except Exception as e:
                        st.error(f"Upload failed: {str(e)}")
            else:
                st.warning("Please provide a company name, date, and a PDF file to upload.")