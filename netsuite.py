import streamlit as st
from functions.variables import database_schema_variables, destination_selection
from functions.env_utils import setup_snowflake_connection

# Set up Snowflake connection from environment variables if secrets.toml doesn't exist
# Store the connection in session_state so it can be accessed by other parts of the app
st.session_state.snowflake_conn = setup_snowflake_connection()

st.sidebar.header('Data Connection Variables')
destination = destination_selection()
database, schema = database_schema_variables()

# Read the README contents
with open("README.md", "r") as f:
    readme_content = f.read()

# Render the README as markdown in the app
st.markdown(readme_content)
