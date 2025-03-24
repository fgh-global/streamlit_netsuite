import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
import datetime
from functions.env_utils import setup_snowflake_connection

# Grab global variables
destination = st.session_state.destination
database = st.session_state.database 
schema = st.session_state.schema

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

def convert_date_string(date_str):
    """
    Converts a string date like '2023-10-31' to a datetime object.
    Works with both individual strings and pandas Series/columns.
    """
    if isinstance(date_str, pd.Series):
        # If it's already a datetime series, return as is
        if pd.api.types.is_datetime64_any_dtype(date_str):
            return date_str
        # Otherwise convert from string
        return pd.to_datetime(date_str)
    elif isinstance(date_str, str):
        try:
            # For individual strings
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            # Try with different format if the first one fails
            return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()
    else:
        # Return as is if it's already a datetime
        return date_str

def query_results(destination, database, schema, model='bs'):
    # No caching at this level - rely on the connection's caching mechanism

    if destination == "BigQuery" and model == "bs":
        if database is None or schema is None:
            st.warning("Results will be displayed once your database and schema are provided.")
        else:
            # Get the accounting book ID from session state
            accounting_book_id = st.session_state.get('accounting_book', 1)
            
            query = run_query(
                "select "\
                    "balance_sheet_sort_helper, "\
                    "accounting_period_name, "\
                    "accounting_period_ending, "\
                    "account_category, "\
                    "account_name, "\
                    "account_type_name, "\
                    "round(sum(converted_amount),2) as balance "\
                "from `" + database + "." + schema + ".netsuite2__balance_sheet` "\
                "where accounting_book_id = " + str(accounting_book_id) + " "\
                "group by 1,2,3,4,5,6 order by balance_sheet_sort_helper"
            )

    if destination == "BigQuery" and model == "is":
        if database is None or schema is None:
            st.error("Results will be displayed once your database and schema are provided.")
        else:
            query = run_query(
                "select "\
                    "income_statement_sort_helper, "\
                    "accounting_period_name, "\
                    "accounting_period_ending, "\
                    "account_category, "\
                    "account_name, "\
                    "account_type_name, "\
                    "round(sum(converted_amount),2) as balance "\
                "from `" + database + "." + schema + ".netsuite2__income_statement` "\
                "group by 1,2,3,4,5,6 order by income_statement_sort_helper"
            )

    if destination == "Snowflake" and model == "bs":
        if database is None or schema is None:
            st.warning("Results will be displayed once your database and schema are provided.")
        else:
            # Get connection with current credentials
            conn = setup_snowflake_connection()
            
            # Only proceed if we have a valid connection
            if conn is not None:
                # Get the accounting book ID from session state
                accounting_book_id = st.session_state.get('accounting_book', 1)
                
                # Use ttl=0 to always fetch fresh data
                dataframe_results = conn.query(
                    "select "\
                        "balance_sheet_sort_helper, "\
                        "accounting_period_name, "\
                        "accounting_period_ending, "\
                        "account_category, "\
                        "account_name, "\
                        "account_type_name, "\
                        "round(sum(converted_amount),2) as balance "\
                    "from " + database + "." + schema + ".netsuite2__balance_sheet "\
                    "where accounting_book_id = " + str(accounting_book_id) + " "\
                    "group by 1,2,3,4,5,6 order by balance_sheet_sort_helper",
                    ttl=0  # Always fetch fresh data
                )
                
                dataframe_results.columns = dataframe_results.columns.str.lower()

                st.write(
                    "select "\
                        "balance_sheet_sort_helper, "\
                        "accounting_period_name, "\
                        "accounting_period_ending, "\
                        "account_category, "\
                        "account_name, "\
                        "account_type_name, "\
                        "round(sum(converted_amount),2) as balance "\
                    "from " + database + "." + schema + ".netsuite2__balance_sheet "\
                    "where accounting_book_id = " + str(accounting_book_id) + " "\
                    "group by 1,2,3,4,5,6 order by balance_sheet_sort_helper",
                )
                
                # Handle date conversion properly
                if 'accounting_period_ending' in dataframe_results.columns:
                    dataframe_results['accounting_period_ending'] = convert_date_string(dataframe_results['accounting_period_ending'])
                
                query = dataframe_results
            else:
                # Return empty dataframe if no valid connection
                st.error("Unable to connect to Snowflake. Please check your credentials.")
                query = pd.DataFrame()

    if destination == "Snowflake" and model == "is":
        if database is None or schema is None:
            st.warning("Results will be displayed once your database and schema are provided.")
        else:
            # Get connection with current credentials
            conn = setup_snowflake_connection()
            
            # Only proceed if we have a valid connection
            if conn is not None:
                # Get the accounting book ID from session state
                accounting_book_id = st.session_state.get('accounting_book', 1)
                
                # Use ttl=0 to always fetch fresh data
                dataframe_results = conn.query(
                    "select "\
                        "income_statement_sort_helper, "\
                        "accounting_period_name, "\
                        "accounting_period_ending, "\
                        "account_category, "\
                        "account_name, "\
                        "account_type_name, "\
                        "round(sum(converted_amount),2) as balance "\
                    "from " + database + "." + schema + ".netsuite2__income_statement "\
                    "where accounting_book_id = " + str(accounting_book_id) + " "\
                    "group by 1,2,3,4,5,6 order by income_statement_sort_helper",
                    ttl=0  # Always fetch fresh data
                )

                st.write(
                    "select "\
                        "income_statement_sort_helper, "\
                        "accounting_period_name, "\
                        "accounting_period_ending, "\
                        "account_category, "\
                        "account_name, "\
                        "account_type_name, "\
                        "round(sum(converted_amount),2) as balance "\
                    "from " + database + "." + schema + ".netsuite2__income_statement "\
                    "where accounting_book_id = " + str(accounting_book_id) + " "\
                    "group by 1,2,3,4,5,6 order by income_statement_sort_helper",
                )

                dataframe_results.columns = dataframe_results.columns.str.lower()

                # Handle date conversion properly
                if 'accounting_period_ending' in dataframe_results.columns:
                    dataframe_results['accounting_period_ending'] = convert_date_string(dataframe_results['accounting_period_ending'])

                query = dataframe_results
            else:
                # Return empty dataframe if no valid connection
                st.error("Unable to connect to Snowflake. Please check your credentials.")
                query = pd.DataFrame()

    if destination == "Dunder Mifflin Sample Data" and model == "is":
        query = pd.read_csv('data/dunder_mifflin_income_statement.csv')

        ## Convert csv fields for time conversions later on
        query['accounting_period_ending'] = pd.to_datetime(query['accounting_period_ending'])

    if destination == "Dunder Mifflin Sample Data" and model == "bs":
        query = pd.read_csv('data/dunder_mifflin_balance_sheet.csv')

        ## Convert csv fields for time conversions later on
        query['accounting_period_ending'] = pd.to_datetime(query['accounting_period_ending'])

    # Safely convert date column regardless of its current type
        if 'accounting_period_ending' in query.columns:
            query['accounting_period_ending'] = convert_date_string(query['accounting_period_ending'])
            # Convert to date format if it's datetime
            if pd.api.types.is_datetime64_any_dtype(query['accounting_period_ending']):
                query['accounting_period_ending'] = query['accounting_period_ending'].dt.date
    
    if model == 'bs':
        data = query

        # Get the data into the app and specify any datatypes if needed.
        data_load_state = st.text('Loading data...')
        data['accounting_period_ending'] = data['accounting_period_ending'].dt.date
        data_load_state.text("Done! (using fresh data)")
    if model == 'is':
        data = query
        # Get the data into the app and specify any datatypes if needed.
        data_load_state = st.text('Loading data...')
        data['accounting_period_ending'] = data['accounting_period_ending'].dt.date
        data_load_state.text("Done! (using fresh data)")
        
    return data
