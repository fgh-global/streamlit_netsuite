import os
import streamlit as st
from pathlib import Path

def setup_snowflake_connection():
    """
    Set up Snowflake connection configuration.
    
    If .streamlit/secrets.toml exists, it will use st.connection.
    Otherwise, it will use st.experimental_connection with environment variables.
    
    Returns:
        The Snowflake connection object that can be used for queries.
    """
    # Check if .streamlit/secrets.toml exists
    secrets_path = Path(".streamlit/secrets.toml")
    
    if secrets_path.exists():
        # If secrets.toml exists, use the standard connection API
        return st.connection('snowflake')
        
    else:
        # If secrets.toml doesn't exist, set up connection from environment variables
        return st.connection(
            "", 
            type='snowflake', 
            account=os.environ.get("SNOWFLAKE_ACCOUNT"),
            user=os.environ.get("SNOWFLAKE_USER"),
            password=os.environ.get("SNOWFLAKE_PASSWORD"),
            role=os.environ.get("SNOWFLAKE_ROLE"),
            warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
            database=os.environ.get("SNOWFLAKE_DATABASE"),
            schema=os.environ.get("SNOWFLAKE_SCHEMA"),
            client_session_keep_alive=os.environ.get("SNOWFLAKE_CLIENT_SESSION_KEEP_ALIVE", "true").lower() == "true"
        )
