import streamlit as st

def destination_selection():
    # Hard code destination to "Snowflake" instead of showing a selectbox
    destination = "Snowflake"
    st.session_state.destination = destination
    return destination

def database_schema_variables():
    # Hard code database and schema values instead of showing text input fields
    database = "PC_FIVETRAN_DB"
    schema = "DBT_FIVETRAN_NETSUITE"
    
    # Set session state variables
    st.session_state.database = database
    st.session_state.schema = schema
    
    return database, schema
