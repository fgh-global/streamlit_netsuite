import os
import streamlit as st
from pathlib import Path
import snowflake.connector

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
        st.write("Secrets file found. Setting up Snowflake connection from secrets.toml.")
        try:
            conn = snowflake.connector.connect(
                account=st.secrets["snowflake"]["account"],
                user=st.secrets["snowflake"]["user"],
                password=st.secrets["snowflake"]["password"],
                role=st.secrets["snowflake"]["role"],
                warehouse=st.secrets["snowflake"]["warehouse"],
                database=st.secrets["snowflake"]["database"],
                schema=st.secrets["snowflake"]["schema"]
                client_session_keep_alive=st.secrets["snowflake"]["client_session_keep_alive"].lower() == "true"
            )
            st.write("✅ Direct Snowflake connection successful!")
            return conn
        except Exception as e:
            st.error(f"❌ Direct Snowflake connection failed: {str(e)}")
            return None
    else:
        # If secrets.toml doesn't exist, set up connection from environment variables
        st.write("Secrets file not found. Setting up Snowflake connection from environment variables.")
        print("Secrets file not found. Setting up Snowflake connection from environment variables.")
        st.write("SNOWFLAKE_ACCOUNT:", os.environ.get("SNOWFLAKE_ACCOUNT"))
        print("SNOWFLAKE_ACCOUNT:", os.environ.get("SNOWFLAKE_ACCOUNT"))
        # Use experimental_connection with parameters from environment variables
        try:
            conn = snowflake.connector.connect(
                account=os.environ.get("SNOWFLAKE_ACCOUNT"),
                user=os.environ.get("SNOWFLAKE_USER"),
                password=os.environ.get("SNOWFLAKE_PASSWORD"),
                role=os.environ.get("SNOWFLAKE_ROLE"),
                warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
                database=os.environ.get("SNOWFLAKE_DATABASE"),
                schema=os.environ.get("SNOWFLAKE_SCHEMA"),
                client_session_keep_alive=os.environ.get("SNOWFLAKE_CLIENT_SESSION_KEEP_ALIVE", "true").lower() == "true"
            )
            st.write("✅ Direct Snowflake connection successful!")
            return conn
        except Exception as e:
            st.error(f"❌ Direct Snowflake connection failed: {str(e)}")
            return None

