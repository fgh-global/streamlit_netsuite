import os
import streamlit as st
from pathlib import Path

def display_snowflake_credentials():
    """
    Display Snowflake credentials input in the sidebar.
    This function should be called on all pages to ensure credentials are visible.
    """
    st.sidebar.header('Snowflake Credentials')
    
    # Add username input with session state persistence
    if 'snowflake_username' not in st.session_state:
        st.session_state.snowflake_username = ""
    snowflake_username = st.sidebar.text_input("Username", value=st.session_state.snowflake_username)
    
    # Add password input with session state persistence
    if 'snowflake_password' not in st.session_state:
        st.session_state.snowflake_password = ""
    snowflake_password = st.sidebar.text_input("Password", type="password", value=st.session_state.snowflake_password)
    
    # Add save button to update credentials and refresh
    if st.sidebar.button("Save Credentials"):
        st.session_state.snowflake_username = snowflake_username
        st.session_state.snowflake_password = snowflake_password
        st.rerun()  # This will refresh the app and apply the new credentials

def setup_snowflake_connection():
    """
    Set up Snowflake connection configuration.
    
    Always uses username and password from session state.
    For account, role, and warehouse:
    - Uses values from secrets.toml if it exists
    - Falls back to environment variables if secrets.toml doesn't exist
    
    Returns:
        The Snowflake connection object that can be used for queries, or None if credentials are not provided.
    """
    # Check if credentials are provided in session state
    if hasattr(st.session_state, 'snowflake_username') and st.session_state.snowflake_username and \
       hasattr(st.session_state, 'snowflake_password') and st.session_state.snowflake_password:
        
        # Check if .streamlit/secrets.toml exists for account, role, and warehouse
        secrets_path = Path(".streamlit/secrets.toml")
        
        if secrets_path.exists():
            # If secrets.toml exists, use it for account, role, and warehouse
            # But still use session state for username and password
            try:
                # Create a custom connection with session state credentials
                return st.connection(
                    "", 
                    type='snowflake', 
                    account=st.secrets["connections"]["snowflake"]["account"],
                    user=st.session_state.snowflake_username,
                    password=st.session_state.snowflake_password,
                    role=st.secrets["connections"]["snowflake"]["role"],
                    warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
                    database=st.session_state.database,
                    schema=st.session_state.schema,
                    client_session_keep_alive=True
                )
            except Exception as e:
                st.error(f"Error connecting to Snowflake: {e}")
                return None
        else:
            # If secrets.toml doesn't exist, use environment variables for account, role, and warehouse
            return st.connection(
                "", 
                type='snowflake', 
                account=os.environ.get("SNOWFLAKE_ACCOUNT"),
                user=st.session_state.snowflake_username,
                password=st.session_state.snowflake_password,
                role=os.environ.get("SNOWFLAKE_ROLE"),
                warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
                database=st.session_state.database,
                schema=st.session_state.schema,
                client_session_keep_alive=True
            )
    else:
        # If no credentials in session state, return None
        return None
