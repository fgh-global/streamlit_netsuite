import streamlit as st
import os
from functions.variables import database_schema_variables, destination_selection
from functions.env_utils import display_sidebar_config

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
    # Display Snowflake credentials in the sidebar
    display_sidebar_config()
    
    # Only show data connection variables if credentials are provided
    if st.session_state.snowflake_username and st.session_state.snowflake_password:
        destination = destination_selection()
        database, schema = database_schema_variables()
        
        # Display welcome message
        st.title("NetSuite Dashboard")
        st.markdown("### Welcome! Please select a report to view on the left navigation.")
        
        # Add some additional helpful information
        st.markdown("---")
        st.markdown("**Available Reports:**")
        st.markdown("- **Financial Executive Dashboard**: High-level overview of financial health and trends")
        st.markdown("- **Balance Sheet Report**: Detailed view of assets, liabilities, and equity balances")
        st.markdown("- **Income Statement Report**: Comprehensive breakdown of revenue and expenses")
    else:
        # Show message if credentials are not provided
        st.title("NetSuite Dashboard")
        st.warning("Please enter your Snowflake username and password in the sidebar to view reports.")
