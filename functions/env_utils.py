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
    
    # Add role input with session state persistence
    roles = {
        "NETSUITE_REPORTING_ALL": "NETSUITE_REPORTING_ALL",
        "NETSUITE_REPORTING_UK": "NETSUITE_REPORTING_UK"
    }

    if 'snowflake_role' not in st.session_state:
        st.session_state.snowflake_role = ""
    snowflake_role = st.sidebar.selectbox(
        "Select Role",
        options=list(roles.keys()),
        index=0  # Default to first option (NETSUITE_REPORTING_ALL)
    )

    """
    Creates a dropdown for selecting the accounting book.
    Returns the selected accounting book ID.
    """
    # Set default in session state if not already set
    if 'accounting_book' not in st.session_state:
        st.session_state.accounting_book = 1  # Default to IFRS

    # Create mapping of names to IDs
    accounting_books = {
        "IFRS Accounting Book": 1,
        "WPP Account Book": 2
    }
    
    # Create the dropdown using the names
    selected_name = st.sidebar.selectbox(
        "Select Account Book",
        options=list(accounting_books.keys()),
        index=0  # Default to first option (IFRS)
    )

    # Add save button to update credentials and refresh
    if st.sidebar.button("Save Credentials"):
        st.session_state.snowflake_username = snowflake_username
        st.session_state.snowflake_password = snowflake_password
        st.session_state.snowflake_role = snowflake_role
        st.session_state.accounting_book = accounting_books[selected_name]

        # Clear any cached connections when credentials change
        if 'snowflake' in st.session_state:
            del st.session_state['snowflake']
            
        # Clear any cached data
        st.cache_data.clear()
        
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
       hasattr(st.session_state, 'snowflake_password') and st.session_state.snowflake_password and \
       hasattr(st.session_state, 'snowflake_role') and st.session_state.snowflake_role:
        
        # Check if .streamlit/secrets.toml exists for account, role, and warehouse
        secrets_path = Path(".streamlit/secrets.toml")
        
        # # Create a connection ID that includes the credentials to ensure a new connection when credentials change
        # connection_id = f"snowflake_{st.session_state.snowflake_username}_{st.session_state.snowflake_role}"

        st.write("ROLE: ", st.session_state.snowflake_role)
        
        if secrets_path.exists():
            # If secrets.toml exists, use it for account, role, and warehouse
            # But still use session state for username and password
            try:
                # Create a custom connection with session state credentials
                # Set ttl=0 to disable caching and ensure fresh data is always fetched
                conn = st.connection(
                    "", 
                    type='snowflake', 
                    account=st.secrets["connections"]["snowflake"]["account"],
                    user=st.session_state.snowflake_username,
                    password=st.session_state.snowflake_password,
                    role=st.session_state.snowflake_role,
                    warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
                    database=st.session_state.database,
                    schema=st.session_state.schema,
                    client_session_keep_alive=True,
                    ttl=0  # Disable caching to always use fresh data
                )
                
                # Reset the connection to ensure no cached data is used
                conn.reset()
                
                return conn
            except Exception as e:
                st.error(f"Error connecting to Snowflake: {e}")
                return None
        else:
            # If secrets.toml doesn't exist, use environment variables for account, role, and warehouse
            try:
                conn = st.connection(
                    "", 
                    type='snowflake', 
                    account=os.environ.get("SNOWFLAKE_ACCOUNT"),
                    user=st.session_state.snowflake_username,
                    password=st.session_state.snowflake_password,
                    role=st.session_state.snowflake_role,
                    warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
                    database=st.session_state.database,
                    schema=st.session_state.schema,
                    client_session_keep_alive=True,
                    ttl=0  # Disable caching to always use fresh data
                )
                
                # Reset the connection to ensure no cached data is used
                conn.reset()
                
                return conn
            except Exception as e:
                st.error(f"Error connecting to Snowflake: {e}")
                return None
    else:
        # If no credentials in session state, return None
        return None
