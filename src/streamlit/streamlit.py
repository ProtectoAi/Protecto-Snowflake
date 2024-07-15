import streamlit as st
import snowflake.connector
import requests
import json
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import SnowparkSQLException

# Constants
NETWORK_RULE_NAME = 'protecto_network_rule'
EXTERNAL_ACCESS_INTEGRATION_NAME = 'protecto_access_integration'
PROTECTO_API_URL = "https://trial.protecto.ai/api/vault/mask"

# Styles
st.markdown("""
<style>
    .main-title { color: black; text-align: center; font-size: 3em; font-weight: bold; margin-bottom: 30px; }
    .section-title { color: black; font-size: 1.5em; font-weight: bold; margin-top: 20px; margin-bottom: 10px; }
    .info-text { color: #3b3b3b; }
    .stButton>button { 
        background-color: #000000; 
        color: white; 
        padding: 10px 20px; 
        border: none; 
        border-radius: 5px; 
        cursor: pointer; 
        transition: background-color 0.3s;
    }
    .stButton>button:hover { background-color: #5c5c5c; }
    .stSelectbox>div>div { background-color: #FFFFFF; color: black; }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Snowflake session
session = get_active_session()

def navigate_to(page):
    st.session_state.page = page

def create_network_rule():
    try:
        check_rule_sql = f"SHOW NETWORK RULES LIKE '{NETWORK_RULE_NAME}'"
        result = session.sql(check_rule_sql).collect()

        if result:
            st.info(f"Network rule '{NETWORK_RULE_NAME}' already exists. It will be replaced.")

        create_rule_sql = f"""
        CREATE OR REPLACE NETWORK RULE {NETWORK_RULE_NAME}
        MODE = EGRESS
        TYPE = HOST_PORT
        VALUE_LIST = ('trial.protecto.ai');
        """
        session.sql(create_rule_sql).collect()
        
        verify_result = session.sql(check_rule_sql).collect()
        
        if verify_result:
            st.success(f"Network rule '{NETWORK_RULE_NAME}' has been successfully created or replaced.")
        else:
            st.warning("Network rule creation was executed, but verification failed. Please check manually.")
        
    except SnowparkSQLException as e:
        st.error(f"An error occurred while creating the network rule: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

def store_protecto_auth_key():
    auth_key = st.text_input("Enter your Protecto API authentication key:", type="password")
    
    if not auth_key:
        st.warning("Please enter an authentication key.")
        return

    try:
        create_secret_sql = f"""
        CREATE OR REPLACE SECRET oauth_token
        TYPE = GENERIC_STRING
        SECRET_STRING = '{auth_key}';
        """
        session.sql(create_secret_sql).collect()

        create_integration_sql = f"""
        CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION {EXTERNAL_ACCESS_INTEGRATION_NAME}
        ALLOWED_NETWORK_RULES = ({NETWORK_RULE_NAME})
        ENABLED = true;
        """
        session.sql(create_integration_sql).collect()

        st.success("Authentication key stored securely and external access integration created successfully.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

def check_active_subscription():
    try:
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer <YOUR_BEARER_TOKEN>"
        }

        body = {
            "auth_key": "<Protecto_API_AUTH_KEY>"
        }

        response = requests.put(PROTECTO_API_URL, json=body, headers=headers)
        response.raise_for_status()

        masked_result = response.json()
        st.json(masked_result)
        st.success("Subscription is active and API is working correctly.")
    except requests.exceptions.RequestException as error:
        st.error(f"API request failed: {error}")
    except json.JSONDecodeError as error:
        st.error(f"JSON decoding error: {error}")
    except Exception as error:
        st.error(f"An unexpected error occurred: {error}")

def get_databases_and_schemas():
    databases_query = "SHOW DATABASES"
    databases_result = session.sql(databases_query).collect()
    databases = [row['name'] for row in databases_result]

    selected_db = st.selectbox("Select a database", databases)

    schemas_query = f"SHOW SCHEMAS IN DATABASE {selected_db}"
    schemas_result = session.sql(schemas_query).collect()
    schemas = [row['name'] for row in schemas_result]

    selected_schema = st.selectbox("Select a schema", schemas)

    st.write(f"Selected Database: {selected_db}")
    st.write(f"Selected Schema: {selected_schema}")

    return selected_db, selected_schema

def home_page():
    # st.markdown(page_bg_color, unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>Protecto</h1>", unsafe_allow_html=True)
    st.markdown("<p class='info-text'>Protecto identifies and masks sensitive data while maintaining context and semantic meaning, ensuring accuracy in your LLMs/Gen AI apps.</p>", unsafe_allow_html=True)
    st.button('Setup', on_click=lambda: navigate_to('setup'))

def setup_page():
    st.markdown("<h1 class='main-title'>Setup Page</h1>", unsafe_allow_html=True)

    st.markdown("<h2 class='section-title'>1. Check Network Permission</h2>", unsafe_allow_html=True)
    st.button('Create Network Rule', on_click=create_network_rule)

    st.markdown("<h2 class='section-title'>2. Store Protecto AI's API Key</h2>", unsafe_allow_html=True)
    store_protecto_auth_key()

    st.markdown("<h2 class='section-title'>3. Check Active Subscription</h2>", unsafe_allow_html=True)
    st.button('Check Subscription', on_click=check_active_subscription)

    st.markdown("<h2 class='section-title'>4. Select Database and Schema</h2>", unsafe_allow_html=True)
    if session:
        get_databases_and_schemas()
    else:
        st.error("No active Snowflake session found. Please ensure you're connected to Snowflake.")

    st.button('Go back to Home', on_click=lambda: navigate_to('home'))

def main():
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'setup':
        setup_page()

if __name__ == "__main__":
    main()