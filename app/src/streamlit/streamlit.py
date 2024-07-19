import streamlit as st
import snowflake.connector
import requests
import json
import tempfile
import os
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import SnowparkSQLException

# Constants
NETWORK_RULE_NAME = 'protecto_network_rule'
EXTERNAL_ACCESS_INTEGRATION_NAME = 'protecto_access_integration'
PROTECTO_API_URL = "https://trial.protecto.ai/api/vault/mask"


# Snowflake session
session = get_active_session()


###################################
# All Config Settings Here
if 'network_rule_created' not in st.session_state:
    st.session_state.network_rule_created = False
    
if 'store_protecto_api_key' not in st.session_state:
    st.session_state.store_protecto_api_key = False

    
if 'store_active_subscription_status' not in st.session_state:
    st.session_state.store_active_subscription_status = False

    
if 'store_is_registered_udfs' not in st.session_state:
    st.session_state.store_is_registered_udfs = False



def get_status_details(session, database_name, schema_name, table_name):
    # Check if table exists
    st.write(f"See all Status Permissions: {database_name} | {schema_name} | {table_name}")
    check_table_sql = f"""
    SELECT COUNT(*)
    FROM {database_name}.{schema_name}.{table_name}
    """
    
    result = session.sql(check_table_sql).collect()
    st.write(result)
    table_exists = result[0][0] > 0

    if table_exists:
        st.write(f"Table '{table_name}' exists.")
        
        # Pull data from the table
        pull_data_sql = f"""
        SELECT * FROM {database_name}.{schema_name}.{table_name}
        """
        
        try:
            data = session.sql(pull_data_sql).collect()
            
            if data:
                # Convert to a list of dictionaries for easier handling
                columns = ["Check Network Permission", "Procteto AI Secret", "Active Subscription", "Registered Function", "Helper Function"]
                data_dict = [dict(zip(columns, row)) for row in data]
                
                st.write("Data from the table:")
                st.write(data_dict)
                return data_dict
            else:
                st.write("The table is empty.")
                return []
        except Exception as e:
            st.write(f"Error pulling data: {str(e)}")
            return None
    else:
        st.write(f"Table '{table_name}' does not exist.")
        return None


def get_initial_data_status(selected_db_schema):
    session_user = get_active_session()
    if session_user and selected_db_schema:
        # Get if configurations done
        # Get UDF Registeration done ?
        # Show the Execution Part
        permissions_data = get_status_details(session_user, selected_db_schema[0], selected_db_schema[1], "permission_check")
        st.write(permissions_data)
        if permissions_data:
            st.toast('Permission Exist','✅')
            return True
        else:
            st.warning("Permission Doesn't Exist")
            return False











def execute_file_from_stage():
    file_stage_path = '@"PROTECTOPACKAGE"."V1"."V1_FUNCTIONS"/demo.py'
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download the file to the temporary directory
        local_file_path = os.path.join(temp_dir, 'demo.py')
        session.file.get(file_stage_path, temp_dir)
        
        # Read the content of the downloaded file
        with open(local_file_path, 'r') as file:
            file_content = file.read()
        
        # Create a new module
        import types
        demo_module = types.ModuleType('demo')
        
        # Execute the content in the context of the new module
        exec(file_content, demo_module.__dict__)
        
        # Return the module
        return demo_module


# All Helper Function
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

def get_databases_and_schemas_for_register():
    databases_query = "SHOW DATABASES"
    databases_result = session.sql(databases_query).collect()
    databases = [row['name'] for row in databases_result]

    selected_db = st.selectbox("Select a database", databases, key="selectbox_5")

    schemas_query = f"SHOW SCHEMAS IN DATABASE {selected_db}"
    schemas_result = session.sql(schemas_query).collect()
    schemas = [row['name'] for row in schemas_result]

    selected_schema = st.selectbox("Select a schema", schemas, key="selectbox_6")

    st.write(f"Selected Database: {selected_db}")
    st.write(f"Selected Schema: {selected_schema}")

    return selected_db, selected_schema


def register_udfs():
    st.write("yet to register")
    return None
    


def check_registered_udf(selected_db_schema):
    st.write(f"Selected DB: {selected_db_schema[0]}, Schema: {selected_db_schema[1]}")
    
    # Create GET_ALL_UDFS function
    get_all_udfs_function = f"""
    CREATE OR REPLACE FUNCTION GET_ALL_UDFS({selected_db_schema[0]} STRING, {selected_db_schema[1]} STRING)
    RETURNS TABLE (
        FUNCTION_NAME STRING,
        FUNCTION_LANGUAGE STRING,
        VOLATILITY STRING,
        DATA_TYPE STRING,
        ARGUMENT_SIGNATURE STRING
    )
    AS
    $$
        SELECT 
            FUNCTION_NAME,
            FUNCTION_LANGUAGE,
            VOLATILITY,
            DATA_TYPE,
            ARGUMENT_SIGNATURE
        FROM 
            INFORMATION_SCHEMA.FUNCTIONS
        WHERE 
            FUNCTION_CATALOG = {selected_db_schema[0]}
            AND FUNCTION_SCHEMA = {selected_db_schema[1]}
            AND FUNCTION_LANGUAGE != 'INTERNAL'
    $$;
    """
    session.sql(get_all_udfs_function).collect()
    # st.write("GET_ALL_UDFS function created successfully")

    # Test GET_ALL_UDFS function
    test_get_all_udfs = f"SELECT * FROM TABLE(GET_ALL_UDFS('{selected_db_schema[0]}', '{selected_db_schema[1]}'))"
    result_test = session.sql(test_get_all_udfs).collect()
    # st.write(f"GET_ALL_UDFS test result: {result_test}")

    # Create EXECUTE_GET_UDFS function with error handling
    execute_get_udfs_function = f"""
    CREATE OR REPLACE FUNCTION EXECUTE_GET_UDFS({selected_db_schema[0]} STRING, {selected_db_schema[1]} STRING)
    RETURNS STRING
    AS
    $$
        SELECT COALESCE(
            LISTAGG(
                'Function Name: ' || FUNCTION_NAME || 
                ', Language: ' || FUNCTION_LANGUAGE || 
                ', Volatility: ' || VOLATILITY || 
                ', Return Type: ' || DATA_TYPE || 
                ', Argument Signature: ' || ARGUMENT_SIGNATURE
            ) WITHIN GROUP (ORDER BY FUNCTION_NAME),
            'No UDFs found'
        )
        FROM TABLE(GET_ALL_UDFS({selected_db_schema[0]}, {selected_db_schema[1]}))
    $$;
    """
    session.sql(execute_get_udfs_function).collect()
    # st.write("EXECUTE_GET_UDFS function created successfully")

    # Execute the EXECUTE_GET_UDFS function
    execute_query = f"SELECT EXECUTE_GET_UDFS('{selected_db_schema[0]}', '{selected_db_schema[1]}')"
    # st.write(f"Executing query: {execute_query}")
    result_udf = session.sql(execute_query).collect()
    st.write(len(result_udf))
    if result_udf and len(result_udf) > 0:
        udf_string = result_udf[0][0]
        # st.write(f"Raw result: {udf_string}")
        
        # Parse the string to extract function names
        function_info_list = udf_string.split("Function Name: ")
        function_names = []
        
        for info in function_info_list[1:]:  # Skip the first empty element
            name = info.split(",")[0].strip()
            function_names.append(name)
        
        st.write("Found UDFs:")
        st.write(function_names)
        
        # Function to check if a specific UDF exists
        def udf_exists(udf_name):
            return udf_name in function_names

        
        udf_to_check = "PROTECTO_UNMASK"  # Replace with the function you want to check
        if udf_exists(udf_to_check):
            st.write(f"The function {udf_to_check} exists.")
            # check for all UDFs
            st.button('Document', on_click=lambda: navigate_to('document'))
            
            
        else:
            st.write(f"The function {udf_to_check} does not exist.")
            st.button('Setup', on_click=lambda: navigate_to('setup'))
            # st.button('Register Now', on_click=register_udfs)
        
        st.write("Have Registered UDPs")
    else:
        st.write("No results returned from EXECUTE_GET_UDFS")

    # Execute the EXECUTE_GET_UDFS function
    # execute_query = f"SELECT EXECUTE_GET_UDFS('{selected_db_schema[0]}', '{selected_db_schema[1]}')"
    # result = session.sql(execute_query).collect()



def get_all_registered_udfs(selected_db_schema):
    st.write(f"Selected DB: {selected_db_schema[0]}, Schema: {selected_db_schema[1]}")
    
    # Create GET_ALL_UDFS function
    get_all_udfs_function = f"""
    CREATE OR REPLACE FUNCTION GET_ALL_UDFS({selected_db_schema[0]} STRING, {selected_db_schema[1]} STRING)
    RETURNS TABLE (
        FUNCTION_NAME STRING,
        FUNCTION_LANGUAGE STRING,
        VOLATILITY STRING,
        DATA_TYPE STRING,
        ARGUMENT_SIGNATURE STRING
    )
    AS
    $$
        SELECT 
            FUNCTION_NAME,
            FUNCTION_LANGUAGE,
            VOLATILITY,
            DATA_TYPE,
            ARGUMENT_SIGNATURE
        FROM 
            INFORMATION_SCHEMA.FUNCTIONS
        WHERE 
            FUNCTION_CATALOG = {selected_db_schema[0]}
            AND FUNCTION_SCHEMA = {selected_db_schema[1]}
            AND FUNCTION_LANGUAGE != 'INTERNAL'
    $$;
    """
    session.sql(get_all_udfs_function).collect()
    # st.write("GET_ALL_UDFS function created successfully")

    # Test GET_ALL_UDFS function
    test_get_all_udfs = f"SELECT * FROM TABLE(GET_ALL_UDFS('{selected_db_schema[0]}', '{selected_db_schema[1]}'))"
    result_test = session.sql(test_get_all_udfs).collect()
    # st.write(f"GET_ALL_UDFS test result: {result_test}")

    # Create EXECUTE_GET_UDFS function with error handling
    execute_get_udfs_function = f"""
    CREATE OR REPLACE FUNCTION EXECUTE_GET_UDFS({selected_db_schema[0]} STRING, {selected_db_schema[1]} STRING)
    RETURNS STRING
    AS
    $$
        SELECT COALESCE(
            LISTAGG(
                'Function Name: ' || FUNCTION_NAME || 
                ', Language: ' || FUNCTION_LANGUAGE || 
                ', Volatility: ' || VOLATILITY || 
                ', Return Type: ' || DATA_TYPE || 
                ', Argument Signature: ' || ARGUMENT_SIGNATURE
            ) WITHIN GROUP (ORDER BY FUNCTION_NAME),
            'No UDFs found'
        )
        FROM TABLE(GET_ALL_UDFS({selected_db_schema[0]}, {selected_db_schema[1]}))
    $$;
    """
    session.sql(execute_get_udfs_function).collect()
    # st.write("EXECUTE_GET_UDFS function created successfully")

    # Execute the EXECUTE_GET_UDFS function
    execute_query = f"SELECT EXECUTE_GET_UDFS('{selected_db_schema[0]}', '{selected_db_schema[1]}')"
    # st.write(f"Executing query: {execute_query}")
    result_udf = session.sql(execute_query).collect()
    st.write(len(result_udf))
    if result_udf and len(result_udf) > 0:
        udf_string = result_udf[0][0]
        # st.write(f"Raw result: {udf_string}")
        
        # Parse the string to extract function names
        function_info_list = udf_string.split("Function Name: ")
        function_names = []
        
        for info in function_info_list[1:]:  # Skip the first empty element
            name = info.split(",")[0].strip()
            function_names.append(name)
        
        st.write("Found UDFs:")
        st.write(function_names)
        
        # Function to check if a specific UDF exists
        def udf_exists(udf_name):
            return udf_name in function_names

        
        udf_to_check = "PROTECTO_UNMASK"  # Replace with the function you want to check
        if udf_exists(udf_to_check):
            st.write(f"The function {udf_to_check} exists.")
            # check for all UDFs
            st.button('Document', on_click=lambda: navigate_to('document'))
            
            
        else:
            st.write(f"The function {udf_to_check} does not exist.")
            st.button('Setup', on_click=lambda: navigate_to('setup'))
            # st.button('Register Now', on_click=register_udfs)
        
        st.write("Have Registered UDPs")
    else:
        st.write("No results returned from EXECUTE_GET_UDFS")



def create_status():
    selected_db_schema = get_databases_and_schemas()
    is_permission = get_status_details(session, selected_db_schema[0], selected_db_schema[1], "permission_check")
    is_registered = check_registered_udf(selected_db_schema)
    # st.button('Check', on_click=check_active_subscription)
    if is_registered:
        return True
    else:
        return False
    




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


def navigate_to(page):
    st.session_state.page = page



def check_table_and_pull_data(session, database_name, schema_name, table_name):
    # Check if table exists
    check_table_sql = f"""
    SELECT COUNT(*)
    FROM {database_name}.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = '{schema_name}'
    AND TABLE_NAME = '{table_name}'
    """
    
    result = session.sql(check_table_sql).collect()
    table_exists = result[0][0] > 0

    if table_exists:
        st.write(f"Table '{table_name}' exists.")
        
        # Pull data from the table
        pull_data_sql = f"""
        SELECT * FROM {database_name}.{schema_name}.{table_name}
        """
        
        try:
            data = session.sql(pull_data_sql).collect()
            
            if data:
                # Convert to a list of dictionaries for easier handling
                columns = ["Check Network Permission", "Procteto AI Secret", "Active Subscription", "Registered Function", "Helper Function"]
                data_dict = [dict(zip(columns, row)) for row in data]
                
                st.write("Data from the table:")
                st.write(data_dict)
                return data_dict
            else:
                st.write("The table is empty.")
                return []
        except Exception as e:
            st.write(f"Error pulling data: {str(e)}")
            return None
    else:
        st.write(f"Table '{table_name}' does not exist.")
        return None


def update_network_permission(session, database_name, schema_name, table_name, permission_value):
    # Create or replace the table if it doesn't exist
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {database_name}.{schema_name}.{table_name} (
        "Check Network Permission" STRING,
        "Procteto AI Secret" STRING,
        "Active Subscription" STRING,
        "Registered Function" STRING,
        "Helper Function" STRING
    )
    """
    
    try:
        session.sql(create_table_sql).collect()
        st.info(f"Table {database_name}.{schema_name}.{table_name} created if it didn't exist.")
    except Exception as e:
        st.info(f"Error creating table: {str(e)}")
        return

    # Perform the MERGE operation
    merge_sql = f"""
    MERGE INTO {database_name}.{schema_name}.{table_name} t
    USING (SELECT '{permission_value}' as new_permission) s
    ON (1=1)
    WHEN MATCHED THEN
        UPDATE SET "Check Network Permission" = s.new_permission
    WHEN NOT MATCHED THEN
        INSERT ("Check Network Permission", "Procteto AI Secret", "Active Subscription", "Registered Function", "Helper Function")
        VALUES (s.new_permission, NULL, NULL, NULL, NULL)
    """
    
    try:
        result = session.sql(merge_sql).collect()
        st.info(f"Network Permission updated to {permission_value} in the table.")
        st.info(f"Rows affected: {result[0]['number of rows updated']}")
        return True
    except Exception as e:
        st.error(f"Error updating Network Permission in the table: {str(e)}")
        
        # Additional error information
        if "syntax error" in str(e):
            st.error("There might be an issue with the SQL syntax. Please double-check the table and column names.")
            return False
        else:
            st.error("An unexpected error occurred. Please check your permissions and table structure.")
            return False

def create_network_rule(db_and_schema):

    # Check the DB
    # Usage
    if db_and_schema:
        table_data = check_table_and_pull_data(session, db_and_schema[0], db_and_schema[1], "permission_check")
        
        if table_data is not None:
            # Process the data as needed
            for row in table_data:
                st.write(f"Network Permission: {row['Check Network Permission']}")
                st.write(f"AI Secret: {row['Procteto AI Secret']}")
                st.write(f"Active Subscription: {row['Active Subscription']}")
                st.write(f"Registered Function: {row['Registered Function']}")
                st.write(f"Helper Function: {row['Helper Function']}")
                st.write("---")
        
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
                st.success(f"Network rule '{NETWORK_RULE_NAME}' has been successfully created or replaced. {verify_result}")
                st.toast('Network rule is created successful!', icon='🤖')
                st.write(f"Network rule '{NETWORK_RULE_NAME}' has been successfully created or replaced.")
                status_update_network_permission = update_network_permission(session, db_and_schema[0], db_and_schema[1], "permission_check", True)
                if status_update_network_permission:
                    st.toast('Network Permission Updation is Successful!', icon='😍')
                    return True
            else:
                st.warning("Network rule creation was executed, but verification failed. Please check manually.")
                return False
            
        except SnowparkSQLException as e:
            st.error(f"An error occurred while creating the network rule: {str(e)}")
            return False
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            return False

def store_protecto_auth_key(selected_db_schema):
    if selected_db_schema:
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
            success = session.sql(create_integration_sql).collect()

            query = f"""
            MERGE INTO {selected_db_schema[0]}.{selected_db_schema[1]}.permission_check t
            USING (SELECT '{auth_key}' as new_secret) s
            ON (1=1)
            WHEN MATCHED THEN
                UPDATE SET "Procteto AI Secret" = s.new_secret
            WHEN NOT MATCHED THEN
                INSERT ("Check Network Permission", "Procteto AI Secret", "Active Subscription", "Registered Function", "Helper Function")
                VALUES (NULL, s.new_secret, NULL, NULL, NULL)
            """
            stored_protecto = session.sql(query).collect()

            if stored_protecto:
                st.toast('Protecto Secret Key Stored')
            else:
                st.error("Error in storing Protecto")
            
            if success:
                st.session_state.store_protecto_api_key = True
            
            st.success("Authentication key stored securely and external access integration created successfully.")
            st.toast('Authentication key stored securely and external access integration created successfully.', icon='😍')
    
            # Store in the Data base Here
            

        
        
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




def home_page():
    # st.markdown(page_bg_color, unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>Protecto</h1>", unsafe_allow_html=True)
    st.markdown("<p class='info-text'>Protecto identifies and masks sensitive data while maintaining context and semantic meaning, ensuring accuracy in your LLMs/Gen AI apps.</p>", unsafe_allow_html=True)
    
    demo = execute_file_from_stage()
    
    # Get all functions from the demo module
    functions = [func for func in dir(demo) if callable(getattr(demo, func)) and not func.startswith("__")]
    create_status()
    # Create buttons for each function
    for i, func_name in enumerate(functions):
        if st.button(f"Run {func_name}", key=f"button_{func_name}_{i}"):
            result = getattr(demo, func_name)()
            st.write(f"Result of {func_name}: {result}")

def engage_help_page():
    st.markdown("<p class='section-title'>Engagement Helper Function</p>", unsafe_allow_html=True)
    st.markdown("<p>Mask Function - To Mask Your Data </p>", unsafe_allow_html=True)
    code = '''CREATE OR REPLACE FUNCTION protecto_mask(
    mask_values ARRAY,
    token_type STRING,
    format_type STRING,
    return_type STRING
    )
    RETURNS ARRAY
    LANGUAGE PYTHON
    RUNTIME_VERSION = '3.8'
    PACKAGES = ('snowflake-snowpark-python', 'protecto_ai')
    IMPORTS = ('@my_stage/protecto_ai.zip')
    HANDLER = 'mask'
    EXTERNAL_ACCESS_INTEGRATIONS = ('protecto_access_integration')
    SECRETS = ('cred' = 'protecto_secret')
    AS
    $$'''
    st.code(code, language='python')
    st.button('Run')
    st.button('See Docs')

def docsSection():
    st.markdown("<p>To Docs</p>", unsafe_allow_html=True)



def handle_button_click(selected_db_schema):
    if not st.session_state.network_rule_created:
        # Attempt to create the network rule
        success = create_network_rule(selected_db_schema)
        if success:
            st.session_state.network_rule_created = True
            st.success("Network rule created successfully!")
        else:
            st.error("You don't have permission to create the network rule.")
    else:
        # Here you would implement the logic to remove the permission
        # For this example, we'll just toggle the state back
        st.session_state.network_rule_created = False
        st.info("Network rule removed.")

def register_all_function():
    return True


def check_all_registered_udf(selected_db_schema):
    # Get all the UDFs
    if selected_db_schema:
        # Get All the UDFs
        return True
        


# The Setup Page
def setup_page():
    st.markdown("<h1 class='main-title'>Setup Page</h1>", unsafe_allow_html=True)
    st.markdown("<p>Before setting up the could you specify in which Database Schema that you need to configure it.</p>", unsafe_allow_html=True)
    selected_db_schema = get_databases_and_schemas()
    if selected_db_schema:
        st.write(f"Selected DB & Schema : {selected_db_schema}")
        st.button('Configure')
    st.markdown("<h2 class='section-title'>1. Check Network Permission</h2>", unsafe_allow_html=True)
    if st.session_state.network_rule_created:
        st.write('✅')
    # Get the DB and Schema Detail 
    # Store the DB and Schema in Temporary
    # Create DB Schema To Store 

    
    
    # st.button('Create Network Rule', on_click=lambda: create_network_rule(selected_db_schema))
    # button_text = "Remove Network Rule" if st.session_state.network_rule_created else "Create Network Rule"
    
    # Create the button with the appropriate text and click handler
    # st.button(button_text, on_click=create_network_rule(selected_db_schema))
    # st.button('Create Network Rule', on_click=create_network_rule(selected_db_schema))
    button_text = "Remove Network Rule" if st.session_state.network_rule_created else "Create Network Rule"

    # Create the button with the appropriate text and click handler
    st.button(button_text, on_click=lambda:  handle_button_click(selected_db_schema))
    # st.button('Create Network Rule', on_click=lambda: create_network_rule(selected_db_schema))
    st.markdown("<h2 class='section-title'>2. Store Protecto AI's API Key</h2>", unsafe_allow_html=True)
    store_protecto_auth_key(selected_db_schema)
    if st.session_state.store_protecto_api_key:
        st.write('✅')

    
    st.markdown("<h2 class='section-title'>3. Check Active Subscription</h2>", unsafe_allow_html=True)
    st.button('Check Subscription', on_click=check_active_subscription)
    
    st.markdown("<h2 class='section-title'>4. Select Database and Schema</h2>", unsafe_allow_html=True)
    get_databases_and_schemas_for_register()
    st.markdown("<h2 class='section-title'>5. All Function Calling</h2>", unsafe_allow_html=True)
    # Check if registered 
    # Tell them who it will work
    
    check_all_registered_udf(selected_db_schema)
    st.button('Register', on_click= register_all_function)
    engage_help_page()
    # if session:
    #     get_databases_and_schemas()
    # else:
    #     st.error("No active Snowflake session found. Please ensure you're connected to Snowflake.")

    st.button('Go back to Home', on_click=lambda: navigate_to('home'))
    st.button('Do Docs', on_click=lambda: docsSection)


def document_page():
    st.markdown("<h1>Documentation</h1>", unsafe_allow_html=True)
    st.button('Go back to Home', on_click=lambda: navigate_to('home'))


def main():
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'setup':
        setup_page()
    elif st.session_state.page == 'document':
        document_page()

if __name__ == "__main__":
    main()