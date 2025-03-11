import streamlit as st
import os
from functions.variables import database_schema_variables, destination_selection
# from functions.env_utils import setup_snowflake_connection

# Initialize authentication state if not already set
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Get password from secrets or environment variables
def get_password():
    try:
        return st.secrets["auth"]["password"]
    except:
        # Default to environment variable or a fallback password
        return os.environ.get("STREAMLIT_AUTH_PASSWORD", "default_password")

# Authentication logic
if not st.session_state.authenticated:
    st.title("Login Required")
    st.write("Please enter the password to access the NetSuite dashboard.")
    
    password_input = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if password_input == get_password():
            st.session_state.authenticated = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Incorrect password")
else:
    # Only set up connection and show content if authenticated
    # Set up Snowflake connection from environment variables if secrets.toml doesn't exist
    # Store the connection in session_state so it can be accessed by other parts of the app
    # st.session_state.snowflake_conn = setup_snowflake_connection()

    st.sidebar.header('Data Connection Variables')
    destination = destination_selection()
    database, schema = database_schema_variables()

    # Read the README contents
    with open("README.md", "r") as f:
        readme_content = f.read()

    # Render the README as markdown in the app
    st.markdown(readme_content)
