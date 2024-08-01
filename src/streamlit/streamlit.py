import streamlit as st
import snowflake.connector
import requests
import json
import tempfile
import os
import types
import pandas as pd
import time
from snowflake.snowpark.context import get_active_session
# from snowflake_connection import get_snowflake_session
from snowflake.snowpark.exceptions import SnowparkSQLException


# Constants
NETWORK_RULE_NAME = 'protecto_network_rule'
EXTERNAL_ACCESS_INTEGRATION_NAME = 'protecto_access_integration'
PROTECTO_API_URL = "https://trial.protecto.ai/api/vault/mask"


# Snowflake session
session = get_active_session()


###################################
# All Config Settings Here

    
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
    
if 'network_rule_created' not in st.session_state:
    st.session_state.network_rule_created = False
    
if 'store_protecto_api_key' not in st.session_state:
    st.session_state.store_protecto_api_key = False

    
if 'store_active_subscription_status' not in st.session_state:
    st.session_state.store_active_subscription_status = False

    
if 'store_is_registered_udfs' not in st.session_state:
    st.session_state.store_is_registered_udfs = False
    
if 'store_is_helper_function' not in st.session_state:
    st.session_state.store_is_helper_function = False


# All Other UI Status
if 'store_edit_protecto_api_key' not in st.session_state:
    st.session_state.store_edit_protecto_api_key = False

def allocate_config_secrets(db, schema):
    pull_data_sql = f"""
        SELECT * FROM {db}.{schema}.permission_check
        """
        
    try:
        data = session.sql(pull_data_sql).collect()
        if data:
            # Convert to a list of dictionaries for easier handling
            columns = ["Check Network Permission", "Procteto AI Secret", "Active Subscription", "Registered Function", "Helper Function"]
            data_dict = [dict(zip(columns, row)) for row in data]
            
            # st.write("Data from the table:")
            # st.write(data_dict[0])
            if data_dict[0]["Check Network Permission"] == "True":
                st.session_state.network_rule_created = True
            if data_dict[0]["Procteto AI Secret"]:
                # st.write(f"The Key : {data_dict[0]['Procteto AI Secret']}")
                st.session_state.store_protecto_api_key = data_dict[0]["Procteto AI Secret"]
            elif data_dict[0]["Active Subscription"] != None:
                st.session_state.store_active_subscription_status = True
            elif data_dict[0]["Registered Function"] != None:
                st.session_state.store_is_registered_udfs = True
            elif data_dict[0]["Helper Function"] != None:
                st.session_state.store_is_helper_function = True
        else:
            st.session_state.network_rule_created = False
            st.session_state.store_protecto_api_key = False
            st.session_state.store_active_subscription_status = False
            st.session_state.store_is_registered_udfs = False
            st.session_state.store_is_helper_function = False
            
    except:
        # st.write("Proceed to Setup")
        st.session_state.network_rule_created = False
        st.session_state.store_protecto_api_key = False
        st.session_state.store_active_subscription_status = False
        st.session_state.store_is_registered_udfs = False
        st.session_state.store_is_helper_function = False




data_dict = [
    {
        'Check Network Permission': 'True',
        'Procteto AI Secret': True,
        'Active Subscription': 'True',
        'Registered Function': 'True',
        'Helper Function': 'True'
    }
]

def get_status(value):
    return "✅" if value != None else "🚫"


def get_status_details(session, database_name, schema_name, table_name):
    # Check if table exists
    # st.write(f"See all Status Permissions: {database_name} | {schema_name} | {table_name}")
    # with st.spinner('Wait for it...'):
        # time.sleep(5)
    try: 
        check_table_sql = f"""
        SELECT COUNT(*)
        FROM {database_name}.{schema_name}.{table_name}
        """
        result = session.sql(check_table_sql).collect()
        if result:
            # st.write(result)
            table_exists = result[0][0] > 0
        
            if table_exists:
                # st.write(f"Table '{table_name}' exists.")
                
                # Pull data from the table
                pull_data_sql = f"""
                SELECT * FROM {database_name}.{schema_name}.{table_name}
                """
                css = """
                <style>
                .container {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 10px;
                    margin: 10px;
                    background-color: blue;
                    padding: 10px;
                    border-radius: 5px;
                }
                .item {
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    text-align: center;
                    display: flex;
                    justify-content: center;
                    background-color: #292929;
                    align-items: center;
                    color: white;
                    margin: 3px;
                }
                .icon {
                    margin-left: 5px;
                }
                
                </style>
                """

                
                
                # Add the CSS to Streamlit
                st.markdown(css, unsafe_allow_html=True)
                try:
                    data = session.sql(pull_data_sql).collect()
                    if data:
                        # Convert to a list of dictionaries for easier handling
                        columns = ["Check Network Permission", "Procteto AI Secret", "Active Subscription", "Registered Function", "Helper Function"]
                        data_dict = [dict(zip(columns, row)) for row in data]
                        # st.write(data_dict[0])
                        st.write("**Permissions and Status:**")
                        with st.expander("See All Permissions"):
                            if data_dict[0]:
                                permissions = [
                                "Network Permission",
                                "Procteto AI Secret",
                                "Active Subscription",
                                "Registered Function",
                                "Helper Function"
                                ]
                                
                                statuses = [
                                    get_status(data_dict[0]['Check Network Permission']),
                                    get_status(data_dict[0]['Procteto AI Secret']),
                                    get_status(data_dict[0]['Active Subscription']),
                                    get_status(data_dict[0]['Registered Function']),
                                    get_status(data_dict[0]['Helper Function'])
                                ]
                                control_options = ["Choose an option", "Allow", "Edit", "Remove"]
                             
                                
                                statuses = [
                                get_status(data_dict[0]['Check Network Permission']),
                                get_status(data_dict[0]['Procteto AI Secret']),
                                get_status(data_dict[0]['Active Subscription']),
                                get_status(data_dict[0]['Registered Function']),
                                get_status(data_dict[0]['Helper Function'])
                                ]
                                control_options = ["Choose an option", "Allow", "Edit", "Remove"]
                         
                            
                                df = pd.DataFrame({
                                    "Permissions": permissions,
                                    "Status": statuses                            
                                })
                                
                            # Display the table header
                            # st.write("Permissions and Status:")
                            
                            # Display the table
                            custom_css = """
                            <style>
                            .stDataFrame {
                                background-color: #000000; /* Black background for the outer container */
                                border-radius: 10px;
                                overflow: hidden;
                            }
                            .stDataFrame table {
                                color: white !important;
                                border-collapse: separate;
                                border-spacing: 0;
                            }
                            .stDataFrame th {
                                background-color: black !important; /* Black background for the header */
                                color: white !important;
                                font-weight: normal !important;
                                padding: 10px !important;
                                border-bottom: 1px solid #444 !important;
                            }
                            .stDataFrame td {
                                background-color: #000000 !important; /* Black background for the cells */
                                padding: 10px !important;
                                border-bottom: 1px solid #444 !important;
                            }
                            .stDataFrame tr:last-child td {
                                border-bottom: none !important;
                            }
                            .stDataFrame tbody tr td:last-child {
                                text-align: center !important;
                            }
                        </style>
                            """
                            
                            # Inject custom CSS
                            st.markdown(custom_css, unsafe_allow_html=True)
                            
                            # Style the DataFrame
                            def style_dataframe(df):
                                return df.style.set_properties(**{
                                    'background-color': '#000000',
                                    'color': 'white',
                                    'border': 'none',
                                    'text-align': 'left'
                                }).set_table_styles([
                                    {'selector': 'th', 'props': [('background-color', 'black'), ('color', '#FFFFFF')]},
                                    {'selector': 'td', 'props': [('background-color', '#000000')]},
                                ]).hide(axis='index')
                            
                            styled_df = style_dataframe(df)
                            df = df.reset_index(drop=True)  # Ensure no index column
                            
                            # Display the styled DataFrame
                            st.dataframe(styled_df, use_container_width=True)

                            
                        
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
    except SnowparkSQLException as e:
        # st.error(e)
        st.markdown("""
            <style>
            .custom-info-box {
                background-color: #5560C4;
                border-left: 5px solid #5560C4;
                border-radius: 4px;
                padding: 8px;
                margin: 30px 0;
                display: flex;
                margin-left: 20px;
                margin-right: 20px;
                align-items: center;
                box-shadow: 0 5px 10px rgba(0,0,2,0.1);
            }
            .custom-info-box:hover {
                box-shadow: 0 7px 14px rgba(0, 0, 0, 0.15), 0 2px 6px rgba(0, 0, 0, 0.11);
                transform: translateY(-2px);
                margin-left: 15px;
                margin-right: 15px;
            }
            .info-icon {
                color: #2196F3;
                font-size: 24px;
                margin-right: 15px;
            }
            .info-message {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: 500;
                font-family: 'Arial', sans-serif;
            }
            </style>
            """, unsafe_allow_html=True)
        # st.markdown(f"""
        #     <div class="custom-info-box">
        #         <div class="info-icon">ℹ️</div>
        #         <div class="info-message">For this Database You don't have the configurations</div>
        #     </div>
        #     """, unsafe_allow_html=True)
        
    
    
    


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

# import Register Function
def execite_protecto_mask(mask_values, token_type, format_type, return_type):
    
    file_protecto_path = '@"PROTECTO_SNOWFLAKE"."MY_SCHEMA"."MY_STAGE"/mask.py'
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download the file to the temporary directory
        local_file_path = os.path.join(temp_dir, 'mask.py')
        session.file.get(file_protecto_path, temp_dir)
        
        # Read the content of the downloaded file
        with open(local_file_path, 'r') as file:
            file_content = file.read()
        
        # Create a new module
        demo_module = types.ModuleType('demo')
        
        # Execute the content in the context of the new module
        exec(file_content, demo_module.__dict__)
        
        # Call the mask function from the loaded module
        return demo_module.mask(mask_values, token_type, format_type, return_type)



def execute_protecto_mask(mask_values, token_type, format_type, return_type):
    # Prepare the SQL command
    sql_command = f"""
    SELECT protecto_mask(ARRAY_CONSTRUCT({','.join([f"'{val}'" for val in mask_values])}),
                         '{token_type}', '{format_type}', '{return_type}') AS processed_value
    """
    
    try:
        # Execute the SQL command
        with st.spinner('Masking...'):
            time.sleep(2)
        result = session.sql(sql_command).collect()
        
        if result:
            st.write(f"Result: {result}")
            st.toast("Your data has been masked!", icon="❤️")
            return result[0]
        else:
            st.warning("No results returned from the query.")
            return None
    except Exception as e:
        st.error(f"An error occurred while executing the query: {str(e)}")
        return None



##### All UFDs import Here

def mask_udf():
    if 'mask_values' not in st.session_state:
        st.session_state.mask_values = []
    if 'token_type' not in st.session_state:
        st.session_state.token_type = "Text Token"
    if 'format_type' not in st.session_state:
        st.session_state.format_type = "Person Name"
    if 'return_type' not in st.session_state:
        st.session_state.return_type = "token_value"

    # Input fields
    st.session_state.mask_values = st.text_input("Enter mask values (comma-separated)", value=','.join(st.session_state.mask_values)).split(',')
    st.session_state.token_type = st.selectbox("Token Type", ["Text Token", "Numeric Token"], index=["Text Token", "Numeric Token"].index(st.session_state.token_type))
    st.session_state.format_type = st.selectbox("Format Type", ["Person Name", "Address", "Phone Number"], index=["Person Name", "Address", "Phone Number"].index(st.session_state.format_type))
    st.session_state.return_type = st.selectbox("Return Type", ["token_value", "toxicity_analysis", "toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack", "all"], index=["token_value", "toxicity_analysis", "toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack", "all"].index(st.session_state.return_type))

    # Button to apply mask
    if st.button('Apply Mask'):
        try:
            result = execute_protecto_mask(
                st.session_state.mask_values,
                st.session_state.token_type,
                st.session_state.format_type,
                st.session_state.return_type
            )
            st.write("Result:")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")









# All Helper Function
def get_databases_and_schemas():
    st.markdown("""
    <style>
    .stSelectbox {
        
        min-width: 200px;
    }
    .horizontal-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        
    }
    .selector-container {
        flex: 1;
        margin-right: 20px;
        margin-left: 20px;
        text-align: center;
        color: white;
    }
    .button-container {
        display: flex;
        gap: 10px;
    }
    .stButton>button {
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton.primary>button {
        background-color: #5E5CEC;
        color: white;
    }
    .stButton.secondary>button {
        background-color: white;
        color: #5E5CEC;
        border: 2px solid #5E5CEC;
    }
    
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown("<div class='selector-container'>", unsafe_allow_html=True)
        databases_query = "SHOW DATABASES"
        databases_result = session.sql(databases_query).collect()
        databases = [row['name'] for row in databases_result]
        selected_db = st.selectbox("Select Database", databases, key='db_select-onere')
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='selector-container'>", unsafe_allow_html=True)
        schemas_query = f"SHOW SCHEMAS IN DATABASE {selected_db}"
        schemas_result = session.sql(schemas_query).collect()
        schemas = [row['name'] for row in schemas_result]
        selected_schema = st.selectbox("Select Schema", schemas, key='schema_select')
        st.markdown("</div>", unsafe_allow_html=True)




    
    return selected_db, selected_schema

st.markdown("""
    <style>
    /* Target the label of the selectbox */
    div[data-testid="stSelectbox"] > label {
        color: #FFFFFF !important; /* Change this to any color you want */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def get_databases_and_schemas_for_register():
    databases_query = "SHOW DATABASES"
    databases_result = session.sql(databases_query).collect()
    databases = [row['name'] for row in databases_result]

    selected_db = st.selectbox("Select Database", databases, key="selectbox_5")

    schemas_query = f"SHOW SCHEMAS IN DATABASE {selected_db}"
    schemas_result = session.sql(schemas_query).collect()
    schemas = [row['name'] for row in schemas_result]

    selected_schema = st.selectbox("Select Schema", schemas, key="selectbox_6")

    st.write(f"Selected Database: {selected_db}")
    st.write(f"Selected Schema: {selected_schema}")

    return selected_db, selected_schema


def register_udfs():
    st.write("yet to register")
    execite_protecto_mask()
    return None
    


def check_registered_udf(selected_db_schema):
    # st.write("Registered Permission!!!")
    # st.write(f"Selected DB: {selected_db_schema[0]}, Schema: {selected_db_schema[1]}")
    with st.spinner('Checking for Registered UDFs'):
        time.sleep(4)
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
    # st.write(result_udf[0][0].split("Function Name: "))
    if len(result_udf[0][0].split("Function Name: ")) <= 0:
        st.info("UDFs Not Registered")
    elif len(result_udf[0][0].split("Function Name: ")) > 0:
        if result_udf and len(result_udf) > 0:
            udf_string = result_udf[0][0]
            # st.write(f"Raw result: {udf_string}")
            
            # Parse the string to extract function names
            function_info_list = udf_string.split("Function Name: ")
            function_names = []
            
            for info in function_info_list[1:]:  # Skip the first empty element
                name = info.split(",")[0].strip()
                function_names.append(name)
            
            # st.write("Found UDFs:")
            if len(function_names) <=0 :
                st.markdown("""
                <style>
                .custom-info-box {
                    background-color: #5560C4;
                    border-left: 5px solid #5560C4;
                    border-radius: 4px;
                    padding: 8px;
                    margin: 8px 0;
                    display: flex;
                    align-items: center;
                    box-shadow: 0 5px 10px rgba(0,0,2,0.1);
                }
                .custom-info-box:hover {
                    box-shadow: 0 7px 14px rgba(0, 0, 0, 0.15), 0 2px 6px rgba(0, 0, 0, 0.11);
                    transform: translateY(-2px);
                }
                .info-icon {
                    color: #2196F3;
                    font-size: 24px;
                    margin-right: 15px;
                }
                .info-message {
                    color: #FFFFFF;
                    font-size: 16px;
                    font-weight: 500;
                    font-family: 'Arial', sans-serif;
                }
                </style>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="custom-info-box">
                        <div class="info-icon">ℹ️</div>
                        <div class="info-message">UDFs Not Registered</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:

                css = """
                <style>
            .my-container {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
                gap: 10px;
                margin: 10px;
                padding: 20px;
                background-color: darkblue;
                border-radius: 5px;
            }
            .my-item {
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                text-align: center;
                color: white;
                background-color: #333;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
                </style>
                """
                
                # Add the CSS to Streamlit
                # st.markdown(css, unsafe_allow_html=True)
                on = len(function_names) > 0
                
                if on:
                    udfs = [
                        "EXECUTE_GET_UDFS",
                        "GET_ALL_UDFS",
                        "PROTECTO_ASYNC_MASK",
                        "PROTECTO_ASYNC_MASK_RESULT",
                        "PROTECTO_ASYNC_UNMASK_RESULT",
                        "PROTECTO_MASK",
                        "PROTECTO_UNMASK"
                    ]
                    
                    def format_name(name):
                        return " ".join(word.capitalize() for word in name.split("_"))
                    
                    # Create an expander
                    # with st.expander("UDF Functions"):
                    #     # Initialize session state for inputs and results if not exist
                    #     if 'inputs' not in st.session_state:
                    #         st.session_state.inputs = {udf: "" for udf in udfs}
                    #     if 'results' not in st.session_state:
                    #         st.session_state.results = {udf: "" for udf in udfs}
                    
                    #     # Create the table
                    #     for udf in udfs:
                    #         col1, col2, col3 = st.columns([2, 3, 3])
                    #         with col1:
                    #             st.write(format_name(udf))
                    #         with col2:
                    #             input_key = f"input_{udf}"
                    #             st.session_state.inputs[udf] = st.text_input("Input", key=input_key, value=st.session_state.inputs[udf])
                    #         with col3:
                    #             st.write(st.session_state.results[udf])
                    
                    #     # Process button
                    #     if st.button("Process Functions"):
                    #         for udf in udfs:
                    #             # Here you would typically call your actual UDF functions
                    #             # For this example, we'll just simulate results
                    #             if st.session_state.inputs[udf]:
                    #                 st.session_state.results[udf] = f"Processed: {st.session_state.inputs[udf]}"
                    
                    #     # Display the results in a static table
                    #     df = pd.DataFrame({
                    #         "Function Name": [format_name(udf) for udf in udfs],
                    #         "Input": [st.session_state.inputs[udf] for udf in udfs],
                    #         "Result": [st.session_state.results[udf] for udf in udfs]
                    #     })
                    #     st.table(df)
                    
                else:
                    return None
                # st.write(f"""All Functions: {function_names}""")
                
                # CSS for the card and chips
                style = """
                <style>
                .card {
                    background-color: #ffffff;
                    border-radius: 10px;
                    padding: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    margin-bottom: 10px;
                }
                .chip {
                    display: inline-block;
                    padding: 4px 8px;
                    margin: 5px;
                    background-color: #f1f1f1;
                    border-radius: 25px;
                    font-size: 12px;
                    cursor: pointer;
                }
                .chip:hover {
                    background-color: #e0e0e0;
                }
                </style>
                """
                
                # Start the page with the style
                st.markdown(style, unsafe_allow_html=True)
                st.markdown("""<h4 style='color: black; text-align: center;'>All Registered Functions</h4>""", unsafe_allow_html=True)
                # Add the card with chips
                card_html = '<div class="card">'
                
                for function in function_names:
                    card_html += f'<div class="chip">{function}</div>'
                
                card_html += '</div>'
                
                st.markdown(card_html, unsafe_allow_html=True)
            
            # Function to check if a specific UDF exists
            def udf_exists(udf_name):
                return udf_name in function_names

            st.markdown("""
            <style>
                .protecto-gradient-button {
                    background: linear-gradient(90deg, #A9A5D0 0%, #FFFF99 100%);
                    border: none;
                    color: #1E1E2E;  /* Dark text color for contrast */
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    font-weight: bold;
                    margin: 6px 4px;
                    cursor: pointer;
                    border-radius: 4px;
                    transition: 0.3s;
                }
                .protecto-gradient-button:hover {
                    opacity: 0.8;
                }
                .protecto-gradient-button:active {
                    opacity: 0.6;
                }
                .protecto-gradient-button:focus {
                    outline: none;
                    box-shadow: 0 0 0 3px rgba(169, 165, 208, 0.5);
                }
                .center-content {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
            </style>
            """, unsafe_allow_html=True)

            custom_css = """
            <style>
            .stButton > button {
                background: linear-gradient(to right, #707CED, #FFFF99);
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 5px;
                font-size: 16px;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                background: linear-gradient(to right, #45a049, #1e88e5);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .stButton > button:active {
                transform: translateY(2px);
            }
            </style>
            """

            st.markdown(custom_css, unsafe_allow_html=True)

            def on_click_handler():
                st.session_state.navigate_to = "setup"
            
            

            
            udf_to_check = "PROTECTO_UNMASK"  # Replace with the function you want to check
            if udf_exists(udf_to_check):
                st.toast(f"The function {udf_to_check} exists.")
                # check for all UDFs
                button_placeholder = st.empty()

                # Use markdown to create a custom HTML button
                # Create the button
                if 'page' not in st.session_state:
                    st.session_state.page = 'home'
                
                # Function to handle navigation
                def navigate_to(page):
                    st.session_state.page = page
                
                # Create the button
                # st.button("Setup", on_click=navigate_to, args=('setup',), key="setup_button")
                
                # Navigation logic
                if st.session_state.page == 'home':
                    # st.write("This is the home page. Click the 'Setup' button to navigate.")
                    pass
                elif st.session_state.page == 'setup':
                    # st.write("You've navigated to the setup page!")
                    # Add your setup page content here
                    st.session_state.current_page = 'Setup'
                    # setup_page()
                    # Optional: Button to go back to home
                    # if st.button("Go back to Home"):
                    #     navigate_to('home')
                # st.divider()
                # Check if the button is clicked using a st.button with the same key
                # if st.button('Protecto Vault', key='protecto-button-pep', style='display: none;'):
                #     on_button_click()
                
                # Check if the button is clicked using a st.button with the same key
                # if st.button('Setup', key='setup-button-peopr', style='display: none;'):
                #     navigate_to('setup')
                # st.markdown("<p class='section-title'>Helper Function</p>", unsafe_allow_html=True)
                # st.markdown("<h6 class='white-text'>1. Mask Function - To Mask Your Data </h6>", unsafe_allow_html=True)
                # st.markdown("<h6 style='color: white;' class='mask-function-expansion'>1. Mask Function - To Mask Your Data</h6>", unsafe_allow_html=True)
                # st.markdown("<div style='color: black;'>")

                # custom_css = """
                # <style>
                # /* Custom style for the expander label */
                # div[role='button'][aria-expanded='false'] > div:first-child,
                # div[role='button'][aria-expanded='true'] > div:first-child {
                #     color: black !important;
                # }
                # .css-1y0tads {
                #     background-color: black !important;
                #     color: white !important;
                # }
                # </style>
                # """
                # st.markdown(custom_css, unsafe_allow_html=True)
                
                # with st.expander("See explanation"):
                #     # code = '''select protecto_mask(ARRAY_CONSTRUCT('your_first_data','your_second_data'),'Text Token','Person Name','token_value') AS processed_value;
                #     # '''
                #     # st.code(code, language='python')
                #     # st.button('Run', on_click=lambda:  mask_udf())
                #     if 'mask_values' not in st.session_state:
                #         st.session_state.mask_values = []
                #     if 'token_type' not in st.session_state:
                #         st.session_state.token_type = "Text Token"
                #     if 'format_type' not in st.session_state:
                #         st.session_state.format_type = "Person Name"
                #     if 'return_type' not in st.session_state:
                #         st.session_state.return_type = "token_value"
                
                #     st.markdown("""
                #         <style>
                #         /* Style for text inputs */
                #         .stTextInput input {
                #             color: white !important;
                #             background-color: #0e1117 !important;
                #         }
                #         .stTextInput input::placeholder {
                #             color: #4a4a4a !important;
                #         }
                        
                #         /* Style for selectboxes */
                #         .stSelectbox > div > div > div {
                #             color: white !important;
                #             background-color: #0e1117 !important;
                #         }
                #         /* Style for selectbox options */
                #         .stSelectbox ul {
                #             background-color: #262730 !important;
                #         }
                #         .stSelectbox ul li {
                #             color: white !important;
                #         }
                #         /* Style for the selectbox arrow */
                #         .stSelectbox svg {
                #             color: white !important;
                #         }
                #         </style>
                #     """, unsafe_allow_html=True)
                    
                    # Create the inputs with white text
                    # st.session_state.mask_values = st.text_input(
                    #     "Enter mask values (comma-separated)",
                    #     value=','.join(st.session_state.mask_values)
                    # ).split(',')
                    
                    # st.session_state.token_type = st.selectbox(
                    #     "Token Type",
                    #     ["Text Token", "Numeric Token"],
                    #     index=["Text Token", "Numeric Token"].index(st.session_state.token_type)
                    # )
                    
                    # st.session_state.format_type = st.selectbox(
                    #     "Format Type",
                    #     ["Person Name", "Address", "Phone Number"],
                    #     index=["Person Name", "Address", "Phone Number"].index(st.session_state.format_type)
                    # )
                    
                    # st.session_state.return_type = st.selectbox(
                    #     "Return Type",
                    #     ["token_value", "toxicity_analysis", "toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack", "all"],
                    #     index=["token_value", "toxicity_analysis", "toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack", "all"].index(st.session_state.return_type)
                    # )
                    
                    # Display the current values (this will be in default color for visibility)
                    # st.write("Current values:")
                    # st.write(f"Mask values: {st.session_state.mask_values}")
                    # st.write(f"Token Type: {st.session_state.token_type}")
                    # st.write(f"Format Type: {st.session_state.format_type}")
                    # st.write(f"Return Type: {st.session_state.return_type}")
                    # Button to apply mask
                    if st.button('Apply Mask'):
                        try:
                            result = execute_protecto_mask(
                                st.session_state.mask_values,
                                st.session_state.token_type,
                                st.session_state.format_type,
                                st.session_state.return_type
                            )
                            
                            st.write("Result:")
                            st.write(result)
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                        st.button('See Docs')
                    st.markdown("</div>")
                # st.markdown("<h6 style='color: white;' class='mask-function-expansion'>2. Unmask Function - To Unmask Your Data </h6>", unsafe_allow_html=True)
                # with st.expander("See explanation"):
                #     code = '''SELECT protecto_unmask(ARRAY_CONSTRUCT('uZBT4QPIeY c6Uqu8wb1j','Z6DSssr7Av','SXveExLhyM')) AS UNMASKED_VALUES;'''
                #     st.code(code, language='python')
                #     # st.button('Run', on_click=lambda:  mask_udf(), key="see_docs_zero")
                #     if 'masked_values' not in st.session_state:
                #         st.session_state.masked_values = []
       

                #     st.markdown("""
                #         <style>
                #         /* Target the label of the text input */
                #         div[data-testid="stTextInput"] > label {
                #             color: #FFFFFF !important; /* Change this to any color you want */
                #             font-weight: bold;
                #         }
                #         </style>
                #     """, unsafe_allow_html=True)
                #     # Input fields
                #     st.session_state.masked_values = st.text_input("Enter masked values (comma-separated)", value=','.join(st.session_state.masked_values), key="see_docs_3").split(',')
                    
                #     # Button to apply mask
                #     if st.button('Unmask'):
                #         try:
                #             result = execute_protecto_unmask(
                #                 st.session_state.masked_values
                #             )
                            
                #             st.write("Result:")
                #             st.write(result)
                #         except Exception as e:
                #             st.error(f"An error occurred: {str(e)}")
                #         st.button('See Docs')

                # st.button('To Document', on_click=lambda: navigate_to('Docs'), key="doc-ids")
                st.markdown(custom_css, unsafe_allow_html=True)

                # Display the code snippet using st.code with the updated CSS
                st.markdown("""<h5 style='color: black; text-align: center;'>Grant Permission To Other Role</h5>""", unsafe_allow_html=True)
                
                # st.markdown("""<div style='color: white;'>""", unsafe_allow_html=True)
                # st.code("GRANT MODIFY ON SECRET `protecto_secret` TO ROLE `Protecto_role;`", language='python')
                # st.markdown("""</div>""", unsafe_allow_html=True)

                custom_css = """
                <style>
                .stCodeBlock {
                    background-color: #2E2E2E;  /* Dark background color */
                    color: #FFFFFF;  /* White text color */
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                </style>
                """
                
                # Inject the custom CSS
                st.markdown(custom_css, unsafe_allow_html=True)
                
     
                
                code = """

                GRANT MODIFY ON SECRET `protecto_secret` TO ROLE `Protecto_role;"""
                # st.markdown( f'<pre style="color:white; background-color:black; text-weight: 700;">{code}</pre>', unsafe_allow_html=True )
                code_content = "GRANT MODIFY ON SECRET `protecto_secret` TO ROLE `Protecto_role;`"

                # Placeholder for the animated text
                placeholder = st.empty()
                typed_text = ""
                for char in code_content:
                    typed_text += char
                    placeholder.markdown(f'<pre style="color:white; background-color:black; font-weight: 700; padding:10px; border-radius: 5px;">{typed_text}</pre>', unsafe_allow_html=True)
                    time.sleep(0.1)
                if st.button('Grant Role', key="grant-access-role"):
                    st.session_state.current_page = "Docs"
                

                # st.code("GRANT MODIFY ON SECRET protecto_secret TO ROLE Protecto_role;")
                if st.button('To Document', key="setup-btn"):
                    st.session_state.current_page = "Docs"
                
            else:
                st.toast(f"The function {udf_to_check} does not exist.")
                st.markdown("""
                <style>
                .styled-button {
                    background-color: #5E5CEC;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.3s, box-shadow 0.3s;
                    display: inline-block;
                    text-align: center;
                    text-decoration: none;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                }
                .styled-button:hover {
                    background-color: #4A48D4;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                }
                .styled-button:active {
                    background-color: #3634A8;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
                }
                </style>
                """, unsafe_allow_html=True)

                button_style_btn = f"""
                <style>
                div.stButton > button:first-child {{
                background-color: {'#5560C4' if True else 'white'};
                color: {'white' if True else '#5560C4'};
                border: {'none' if True else '2px solid #5560C4'};
                border-radius: 20px;
                padding: 10px 24px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 60%;
                display: block;
                margin: 0 auto;
            }}
            div.stButton > button:hover {{
                background-color: {'#5A52D5' if True else '#F0F0FF'};
            }}
            .button-container {{
                display: flex;
                justify-content: center;
                width: 100%;
            }}
                </style>
                """

                st.markdown(button_style_btn, unsafe_allow_html=True)
                
                # Create the button
                button_placeholder = st.empty()

                # Use markdown to create a custom HTML button
                # Create the button
                if 'page' not in st.session_state:
                    st.session_state.page = 'home'
                
                # Function to handle navigation
                def navigate_to(page):
                    st.session_state.page = page
                
            
                # st.button("Setup", on_click=lambda: navigate_to('setup'), key="setup_button")
                # st.button("Configure Now", on_click=lambda: navigate_to("setup"), key="setup_button-one")
                # st.button('Go back to Home', on_click=lambda: navigate_to('setup'))
                    # navigate_to(setup_page)
                # st.button('Register Now', on_click=register_udfs)
            
            # st.write("Have Registered UDPs")
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
            # st.write(f"The function {udf_to_check} does not exist.") 
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
    .section-title { color: white; font-size: 1.5em; font-weight: bold; margin-top: 20px; margin-bottom: 10px; }
     .mask-function-expansion ( color: white; )
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
        # st.write(f"Table '{table_name}' exists.")
        
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
                # st.write(data_dict)
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

st.session_state.edit_api_auth_key = False

def edit_api_auth_key():
    st.session_state.edit_api_auth_key = True
    

def store_protecto_auth_key(selected_db_schema):

    
    
    if st.session_state.store_protecto_api_key:
        #st.write('✅')
        st.text_input("Enter your Protecto API authentication key:", type="password", disabled=True, value=st.session_state.store_protecto_api_key)
        edit_yes_btn = st.button("Edit API authentication Key")
        # st.markdown(
        #             """
        #             <button class="custom-disabled-button" disabled>
        #                 <span class="tick-mark">✓</span>
        #                 Edit API authentication Key
        #             </button>
        #             """,
        #             unsafe_allow_html=True
        #         )
        if edit_yes_btn:
            auth_key = st.text_input("Enter your Protecto API authentication key:", type="password", key="edit-protector-key-input")
            save_edit_protecto_key = st.button("Save API authentication Key", key="edit-protector-key-save")
            if save_edit_protecto_key:
                try:
                    # ### 
                    create_secret_sql = f"""
                    CREATE OR REPLACE SECRET protecto_secret
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
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
    else:
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



def store_protecto_auth_key_home_page(selected_db_schema):
    button_style_btn = f"""
                <style>
                div.stButton > button:first-child {{
                background-color: {'#5560C4' if True else 'white'};
                color: {'white' if True else '#5560C4'};
                border: {'none' if True else '2px solid #5560C4'};
                border-radius: 20px;
                padding: 10px 24px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 70%;
                display: block;
                margin: 0 auto;
            }}
            div.stButton > button:hover {{
                background-color: {'#5A52D5' if True else '#F0F0FF'};
            }}
            .button-container {{
                display: flex;
                justify-content: center;
                width: 100%;
            }}
                </style>
                """

    st.markdown(button_style_btn, unsafe_allow_html=True)
    if st.session_state.store_protecto_api_key:
        #st.write('✅')
        st.text_input("Enter your Protecto API authentication key:", type="password", disabled=True, value=st.session_state.store_protecto_api_key)
        edit_yes_btn = st.button("Edit API authentication Key")
        # st.markdown(
        #             """
        #             <button class="custom-disabled-button" disabled>
        #                 <span class="tick-mark">✓</span>
        #                 Edit API authentication Key
        #             </button>
        #             """,
        #             unsafe_allow_html=True
        #         )
        if edit_yes_btn:
            auth_key = st.text_input("Enter your Protecto API authentication key:", type="password", key="edit-protector-key-input")
            save_edit_protecto_key = st.button("Save API authentication Key", key="edit-protector-key-save")
            if save_edit_protecto_key:
                try:
                    # ### 
                    create_secret_sql = f"""
                        CREATE OR REPLACE SECRET protecto_vault.vault_schema.protecto_secret
                        TYPE = GENERIC_STRING
                        SECRET_STRING = '{auth_key}';
                    """
                    res = session.sql(create_secret_sql).collect()
            
                  

        
                    if res:
                        st.toast('Protecto Secret Key Stored')
                    else:
                        st.error("Error in storing Protecto")
                    
                    if res:
                        st.session_state.store_protecto_api_key = True
                    
                    st.success("Authentication key stored securely and external access integration created successfully.")
                    st.toast('Authentication key stored securely and external access integration created successfully.', icon='😍')
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
    else:
        if selected_db_schema:
            auth_key = st.text_input("Enter your Protecto API authentication key:", type="password")
            
            if not auth_key:
                st.warning("Please enter an authentication key.")
                return
        
            try:
                create_secret_sql = f"""
                        CREATE OR REPLACE SECRET protecto_vault.vault_schema.protecto_secret
                        TYPE = GENERIC_STRING
                        SECRET_STRING = '{auth_key}';
                """
                session.sql(create_secret_sql).collect()
        
                
                success = session.sql(create_secret_sql).collect()
    
            
                if success:
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
    
    # Need to Change Change and Unchange Here
    # XXXX
    # Save to the DB



    # 1. Hit API 
    # 2. Store the Status in DB
    # 3. Session Store To Session
    # 4. Change the Button and Do the Toast

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

    
    # st.session_state.store_active_subscription_status = True


    except Exception as error:
        st.error(f"An unexpected error occurred: {error}")
    
    
    

    # try:
    #     headers = {
    #         "Content-Type": "application/json; charset=utf-8",
    #         "Authorization": "Bearer <YOUR_BEARER_TOKEN>"
    #     }

    #     body = {
    #         "auth_key": "<Protecto_API_AUTH_KEY>"
    #     }

    #     response = requests.put(PROTECTO_API_URL, json=body, headers=headers)
    #     response.raise_for_status()

    #     masked_result = response.json()
    #     st.json(masked_result)
    #     st.success("Subscription is active and API is working correctly.")
    # except requests.exceptions.RequestException as error:
    #     st.error(f"API request failed: {error}")
    # except json.JSONDecodeError as error:
    #     st.error(f"JSON decoding error: {error}")
    # except Exception as error:
    #     st.error(f"An unexpected error occurred: {error}")

def remove_active_subscription():
    return True


def protecto_app_role_screen():


    st.markdown("""
    <style>
        .section-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 20px;
            background-color: #2E2E3E;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .section-title {
            color: #707CED;
            font-size: 20px;
            font-weight: bold;
            margin: 0;
            text-align: center;
        }
        .custom-button {
            background-image: linear-gradient(to right, #707CED, #FFD700);
            color: #1E1E2E;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.3s;
        }
        .custom-button:hover {
            opacity: 0.8;
        }
        .custom-disabled-button {
            background-color: #4A4A4A;
            color: #FFFFFF;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-weight: bold;
            cursor: not-allowed;
        }
        .tick-mark {
            margin-right: 8px;
            font-size: 18px;
        }
    </style>
    """, unsafe_allow_html=True)

    
    st.markdown("""

    We have created and configured all the UDFs in `protecto_vault` DB and Schema `vault_schema` 
    

    """)
    
    st.markdown("<h2 class='section-title'>Store Protecto AI's API Key</h2>", unsafe_allow_html=True)
    selected_db_schema = True
    store_protecto_auth_key_home_page(selected_db_schema)

def create_landing_page():
    # Set page config
    # st.set_page_config(layout="wide", page_title="Build vs. Buy")

    # Custom CSS for styling
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(180deg, #f7f7ff, #e0e7ff);
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
     .protecto-vault {
        font-family: Arial, sans-serif;
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        background-color: #F0F0F5;
        border-radius: 10px;
        margin-bottom: 0px;
        background-image: linear-gradient(to right, #707CED, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
    }
    .stButton>button {
        color: white;
        border-radius: 20px;
        height: 3em;
        width: 10em;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main content
    col1, col2, col3 = st.columns([1,6,1])
    
    with col2:
        st.markdown("""<div class="protecto-vault">Protecto Vault</div>""", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey; font-size: 2.0em;'>Secure approach to data security and privacy</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: black;'>Unlock the full potential of your data while effortlessly ensuring data privacy and security - all with the simplicity of an API.</p>", unsafe_allow_html=True)
        # create_status()
        # Buttons

        protecto_app_role_screen()
    
    # Background effect (simplified)
    st.markdown("""
    <div style='position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -3;'>
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <circle cx="10%" cy="10%" r="5" fill="#FFA500" />
            <circle cx="90%" cy="20%" r="3" fill="#FFD700" />
            <circle cx="30%" cy="80%" r="4" fill="#40E0D0" />
            <circle cx="70%" cy="90%" r="6" fill="#40E0D0" />
        </svg>
    </div>
    """, unsafe_allow_html=True)

def check_active_edit_key():
    st.session_state.store_active_subscription_status = False



    try:
        # Execute the SQL command
        with st.spinner('Masking...'):
            time.sleep(2)
        result = session.sql(sql_command).collect()
        
        if result:
            st.write(f"Result: {result}")
            st.toast("Your data has been masked!", icon="❤️")
            return result[0]
        else:
            st.warning("No results returned from the query.")
            return None
    except Exception as e:
        st.error(f"An error occurred while executing the query: {str(e)}")
        return None

def execute_protecto_unmask(masked_values):
    # Convert the list of masked values to a string for SQL
    masked_values_str = ','.join(f"'{value}'" for value in masked_values)
    
    # Prepare the SQL command
    sql_command = f"""
    SELECT protecto_unmask(ARRAY_CONSTRUCT({masked_values_str})) AS UNMASKED_VALUES
    """
    
    # Execute the SQL command
    result = session.sql(sql_command).collect()
    with st.spinner('Unmasking...'):
        time.sleep(2)
    if result:
        unmasked_values = result[0]["UNMASKED_VALUES"]
        st.write(f"Unmasked Values: {unmasked_values}")
        st.toast("Your data has been unmasked!", icon="❤️")
        return unmasked_values
    else:
        st.write("No results returned.")
        return None



def home_page():
    # st.markdown(page_bg_color, unsafe_allow_html=True)
    custom_css = """
    <style>
        .protecto-vault {
        font-family: Arial, sans-serif;
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        background: linear-gradient(180deg, #f7f7ff, #e0e7ff);
        background-repeat: no-repeat;
        background-attachment: fixed;
        border-radius: 10px;
        margin-bottom: 0px;
        background-image: linear-gradient(to right, #707CED, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
    }
     .main-title {
        font-family: Arial, sans-serif;
        font-size: 24px;
        font-weight: bold;
        color: #1E2A3B;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        font-family: Arial, sans-serif;
        font-size: 16px;
        color: #4A5568;
        text-align: center;
        margin-left: 20px;
        margin-right: 20px;
    }
    </style>
    """

    
    
    create_landing_page()
    # html_content = """
    # <div class="protecto-vault">Protecto Vault</div>
    # """
    # # st.write(session.sql("SELECT CURRENT_ROLE(), CURRENT_ACCOUNT(), CURRENT_USER(), CURRENT_DATABASE(), CURRENT_SCHEMA()").collect())
    # html_content_des = """
    # <div class="title-container">
    #     <div class="main-title">Secure approach to data security and privacy</div>
    #     <div class="subtitle">Unlock the full potential of your data while effortlessly ensuring data privacy and security - all with the simplicity of an API.</div>
    # </div>
    # """
    # full_html = custom_css + html_content
    # # st.markdown("<h1 class='main-title'>Protecto</h1>", unsafe_allow_html=True)
    # st.markdown(full_html, unsafe_allow_html=True)
    # st.markdown(html_content_des, unsafe_allow_html=True)

    # st.markdown("<p class='info-text'>Protecto identifies and masks sensitive data while maintaining context and semantic meaning, ensuring accuracy in your LLMs/Gen AI apps.</p>", unsafe_allow_html=True)
    
    # demo = execute_file_from_stage()
    
    # Get all functions from the demo module
    # functions = [func for func in dir(demo) if callable(getattr(demo, func)) and not func.startswith("__")]
    # create_status()
    # Create buttons for each function
    # for i, func_name in enumerate(functions):
    #     if st.button(f"Run {func_name}", key=f"button_{func_name}_{i}"):
    #         result = getattr(demo, func_name)()
    #         st.write(f"Result of {func_name}: {result}")

def engage_help_page():
    st.markdown("<h4 class='section-title'>Try out - Helper Function</h4>", unsafe_allow_html=True)
    col_a, col_b = st.columns([2,2])
    col_a.markdown("<h6>1. Mask Function - To Mask Your Data </h6>", unsafe_allow_html=True)
    with col_a.expander("See explanation"):
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
        col_a.code(code, language='python')
        col_a.button('Run', on_click=lambda:  mask_udf())
        if 'mask_values' not in st.session_state:
            st.session_state.mask_values = []
        if 'token_type' not in st.session_state:
            st.session_state.token_type = "Text Token"
        if 'format_type' not in st.session_state:
            st.session_state.format_type = "Person Name"
        if 'return_type' not in st.session_state:
            st.session_state.return_type = "token_value"

        col_a.markdown(
   """
    <style>
 .main {
        background: linear-gradient(180deg, #f7f7ff, #e0e7ff);
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }

    /* Protecto Vault title */
    .protecto-vault {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        margin-bottom: 0px;
        background-image: linear-gradient(to right, #707CED, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
    }

    /* Main title */
    .main-title {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 16px;
        color: #A0AEC0;
        text-align: center;
        margin-left: 20px;
        margin-right: 20px;
    }

    /* Section title */
    .section-title {
        text-align: center;
        color: #707CED;
        font-size: 40px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Configuration button */
    .config-btn {
        text-align: center;
    }

    

    /* Input fields and select boxes */
    input, select {
        background-color: #2E2E3E;
        color: #FFFFFF;
        border: 1px solid #707CED;
        border-radius: 5px;
        padding: 5px 10px;
    }

  
    </style>
    """, unsafe_allow_html=True)
        en_one, en_two, en_three = st.columns([1,2,1])

        st.session_state.mask_values = st.text_input("Enter mask values (comma-separated)", value=','.join(st.session_state.mask_values)).split(',')
        
        st.session_state.token_type = st.selectbox("Token Type", ["Text Token", "Numeric Token"], index=["Text Token", "Numeric Token"].index(st.session_state.token_type))
        st.session_state.format_type = st.selectbox("Format Type", ["Person Name", "Address", "Phone Number"], index=["Person Name", "Address", "Phone Number"].index(st.session_state.format_type))
        st.session_state.return_type = st.selectbox("Return Type", ["token_value", "toxicity_analysis", "toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack", "all"], index=["token_value", "toxicity_analysis", "toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack", "all"].index(st.session_state.return_type))
        
        # Button to apply mask
        if en_two.button('Apply Mask'):
            try:
                result = execute_protecto_mask(
                    st.session_state.mask_values,
                    st.session_state.token_type,
                    st.session_state.format_type,
                    st.session_state.return_type
                )
                st.write("Result:")
                st.write(result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            st.button('See Docs')
    col_b.markdown("<h6>2. Unmask Function - To Unmask Your Data </h6>", unsafe_allow_html=True)
    with col_b.expander("See explanation"):
        code = '''SELECT protecto_unmask(ARRAY_CONSTRUCT('uZBT4QPIeY c6Uqu8wb1j','Z6DSssr7Av','SXveExLhyM')) AS UNMASKED_VALUES;
        '''
        col_b.code(code, language='python')
        if 'masked_values' not in st.session_state:
            st.session_state.masked_values = []
        # Input fields
        st.session_state.masked_values = st.text_input("Enter mask values (comma-separated)", value=','.join(st.session_state.masked_values), key="see_docs_3").split(',')
        
        # Button to apply mask
        if col_b.button('Unmask', key="see_docs_8"):
            try:
                result = execute_protecto_unmask(
                    st.session_state.masked_values
                )
                col_b.write("Result:")
                col_b.write(result)
            except Exception as e:
                col_b.error(f"An error occurred: {str(e)}")
            col_b.button('See Docs', key="see_docs_one")

def docsSection():
    st.markdown("<p>To Docs</p>", unsafe_allow_html=True)
    


def handle_button_click(selected_db_schema):
    if not st.session_state.network_rule_created:
        # Attempt to create the network rule
        st.toast("Create a New Protecto API Key")
    else:
        st.session_state.store_edit_protecto_api_key = True




def register_all_function():

    # Call the Register Function and Register all UDFs
    # And Store the status in DB status 
    # Update local session info too

    
    
    return True


def check_all_registered_udf(selected_db_schema):
    # Get all the UDFs
    if selected_db_schema:
        # Get All the UDFs
        return True
        

def show_selected_db_and_schema(selected_db_schema):
    st.write(f"Selected DB: {selected_db_schema[0]} | Schema: {selected_db_schema[1]}")


# The Setup Page
def setup_page():

    st.markdown(
   """
    <style>
    .main {
      
        background: linear-gradient(180deg, #f7f7ff, #e0e7ff);
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    
    /* Protecto Vault title */
    .protecto-vault {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        margin-bottom: 0px;
        background-image: linear-gradient(to right, #707CED, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
    }

    /* Main title */
    .main-title {
        font-size: 24px;
        font-weight: bold;
        color: #171D45;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 16px;
        color: #171D45;
        text-align: center;
        margin-left: 20px;
        margin-right: 20px;
    }

    /* Section title */
    .section-title {
        text-align: center;
        color: #707CED;
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Configuration button */
    .config-btn {
        text-align: center;
    }

  

    /* Input fields and select boxes */
    input, select {
        background-color: #2E2E3E;
        color: #FFFFFF;
        border: 1px solid #707CED;
        border-radius: 5px;
        padding: 5px 10px;
    }

    /* Code blocks */
    pre, code {
        background-color: #2E2E3E;
        color: #FFFFFF;
        border-radius: 5px;
        padding: 10px;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)
    
    html_content = """
    <div class="protecto-vault">Setup Page</div>
    """
    
    html_content_des = """
    <div class="title-container">
        <div class="main-title">Secure approach to data security and privacy</div>
        <div class="subtitle">Unlock the full potential of your data while effortlessly ensuring data privacy and security - all with the simplicity of an API.</div>
    </div>
    """
    full_html = html_content
    # st.markdown("<h1 class='main-title'>Protecto</h1>", unsafe_allow_html=True)
    st.markdown(full_html, unsafe_allow_html=True)
    st.markdown(html_content_des, unsafe_allow_html=True)
    st.markdown("""
    <style>
        .section-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 20px;
            background-color: #2E2E3E;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .section-title {
            color: #707CED;
            font-size: 20px;
            font-weight: bold;
            margin: 0;
        }
        .custom-button {
            background-image: linear-gradient(to right, #707CED, #FFD700);
            color: #1E1E2E;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.3s;
        }
        .custom-button:hover {
            opacity: 0.8;
        }
        .custom-disabled-button {
            background-color: #4A4A4A;
            color: #FFFFFF;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-weight: bold;
            cursor: not-allowed;
        }
        .tick-mark {
            margin-right: 8px;
            font-size: 18px;
        }
    </style>
    """, unsafe_allow_html=True)

    selected_db_schema = get_databases_and_schemas()
    if selected_db_schema:
        allocate_config_secrets(selected_db_schema[0], selected_db_schema[1])
    
    # Network Permission Check Section
    # st.markdown(
    #     """
    #     <div class="section-container">
    #         <h2 class="section-title">1. Check Network Permission</h2>
    #         <div>
    #     """,
    #     unsafe_allow_html=True
    # )
    
    check_registered_udf(selected_db_schema)
    
    # if st.session_state.network_rule_created:
    #     st.markdown(
    #         """
    #         <button class="custom-disabled-button" disabled>
    #             <span class="tick-mark">✓</span>
    #             Network Established
    #         </button>
    #         """,
    #         unsafe_allow_html=True
    #     )
    # else:
    #     if st.button('Create Network Rule', key='create_network_rule'):
    #         create_network_rule(selected_db_schema)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    .button-container {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    .custom-disabled-button {
        display: inline-flex;
        align-items: center;button
        justify-content: center;
        padding: 10px 20px;
        background-color: #000000;
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        font-size: 16px;
        cursor: not-allowed;
        transition: background-color 0.3s;
        border-radius: 50px;
    }
    .tick-mark {
        margin-right: 8px;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # if st.session_state.network_rule_created:
    #     button_html = f"""
    #     <div class="button-container">
    #     <button class="custom-disabled-button" disabled>
    #         <span class="tick-mark">✓</span>
    #         Network Established
    #     </button>
    #     </div>
    #     """

        # Render the button
        # st.markdown(button_html, unsafe_allow_html=True)
    # else:
        # st.button('Create Network Rule', on_click=lambda: create_network_rule(selected_db_schema))
    # button_text = "Remove Network Rule" if st.session_state.network_rule_created else "Create Network Rule"
    col1, col2, col3 = st.columns([1, 2, 1])
    
    st.markdown("""
    <style>
    .network-rule-button {
    padding: 15px 32px;
    text-align: center;
    background-color: #4CAF50;
    border: none;
    color: white;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 5px;
    }
    
    .network-rule-button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    
    .network-rule-button.remove {
        background-color: #f44336;
    }
    
    .network-rule-button.remove:hover {
        background-color: #d32f2f;
    }

    .section-title { 
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

    button_style_btn = f"""
                <style>
                div.stButton > button:first-child {{
                background-color: {'#5560C4' if True else 'white'};
                color: {'white' if True else '#5560C4'};
                border: {'none' if True else '2px solid #5560C4'};
                border-radius: 20px;
                padding: 10px 24px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 60%;
                display: block;
                margin: 0 auto;
            }}
            div.stButton > button:hover {{
                background-color: {'#5A52D5' if True else '#F0F0FF'};
            }}
            .button-container {{
                display: flex;
                justify-content: center;
                width: 100%;
            }}
                </style>
                """

    st.markdown(button_style_btn, unsafe_allow_html=True)
                
                # Create the button
    #if st.session_state.network_rule_created:
        # st.button("Setup", on_click=lambda: navigate_to('setup'), key="network_rule_button", help="Click to create or remove network rule")
    #else:
        # st.button("Remove Network Rule", on_click=lambda: navigate_to('setup'), key="setup_button")
    #button_text = "Remove Network Rule" if st.session_state.network_rule_created else "Create Network Rule"
    #button_class = "network-rule-button remove" if st.session_state.network_rule_created else "network-rule-button"

    #if st.button("Setup", on_click=lambda: navigate_to('setup'), key="network_rule_button", help="Click to create or remove network rule"):
    # Your button click logic here
     #   create_network_rule(selected_db_schema)
      #  pass    

    # Create the button with the appropriate text and click handler
    # st.button(button_text, on_click=create_network_rule(selected_db_schema))
    # st.button('Create Network Rule', on_click=create_network_rule(selected_db_schema))
    #with col2:
    #    if st.button(button_text):
    #        # Toggle the network_rule_created state
    #        st.session_state.network_rule_created = not st.session_state.network_rule_created
    #        # Rerun the app to reflect the changes
    #        st.experimental_rerun()
    
    # Create the button with the appropriate text and click handler
    # st.button(button_text, on_click=lambda:  handle_button_click(selected_db_schema))
    # st.button('Create Network Rule', on_click=lambda: create_network_rule(selected_db_schema))
    # st.markdown("<h2 class='section-title'>2. Store Protecto AI's API Key</h2>", unsafe_allow_html=True)
    # selected_db_schema = get_databases_and_schemas()
    # store_protecto_auth_key(selected_db_schema)
    # if st.session_state.store_protecto_api_key:
    #     st.write('✅')
        

    
    # st.markdown("<h2 class='section-title'>3. Check Active Subscription</h2>", unsafe_allow_html=True)
    # st.button('Check Subscription', on_click=check_active_subscription, key="One")
    # st.button('Remove Subscription', on_click=remove_active_subscription, key="Two")
    
    # st.markdown("<h2 class='section-title'>4. Select Database and Schema</h2>", unsafe_allow_html=True)
    # get_databases_and_schemas_for_register()
    # show_selected_db_and_schema(selected_db_schema)
    # st.markdown("<h2 class='section-title'>3. Register All Function</h2>", unsafe_allow_html=True)
    # register_All_function()
    # Check if registered 
    # Tell them who it will work
    
    # check_all_registered_udf(selected_db_schema)
    # st.button('Register', on_click= register_all_function)
    # engage_help_page()
    # if session:
    #     get_databases_and_schemas()
    # else:
    #     st.error("No active Snowflake session found. Please ensure you're connected to Snowflake.")

    st.button('Go back to Home', on_click=lambda: navigate_to('home'))
    

    # JavaScript to handle button click
    st.markdown("""
    <script>
    function docsSection() {
        // Call your Python function here
        console.log("Do Docs clicked");
    }
    </script>
    """, unsafe_allow_html=True)



def document_page():
    st.markdown("<h1 style='text-align: center;'>Documentation</h1>", unsafe_allow_html=True)
    st.markdown("""
        <style>
      .main {
        background: linear-gradient(180deg, #f7f7ff, #e0e7ff);
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
        .docs-container {
            background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
            border-radius: 10px;
            padding: 30px;
            backdrop-filter: blur(10px);
            margin: 20px 0;
        }
                
        .main-title-docs {
            color: white;        
            font-weight: bold;
            font-size: 24px;
            text-align: center;
        }

        .subtitle-docs {
            color: white;  
            text-align: center;  
            margin-bottom: 20px;
        }
                
      .github-button {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #24292e;
        color: white;
        padding: 10px 10px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        transition: background-color 0.3s;
        text-align: center;
        margin: 0 auto;  /* This centers the button horizontally */
    }
    .github-button:hover {
        background-color: #5c5c5c;
    }
    .github-icon {
        margin-right: 10px;
    }
    .btn-github {
        margin: 0;
        padding: 0;
    }

        </style>
        """, unsafe_allow_html=True)

    # HTML content for the docs section
    html_content = """
    <div class="docs-container">
        <div class="main-title-docs">Refer the Documentation</div>
        <div class="subtitle-docs">Unlock the full potential of your data while effortlessly ensuring data privacy and security - all with the simplicity of an API.</div>
           <a href="https://github.com/viveksrinivasanss/Protecto-Snowflake" class="github-button" target="_blank">
            <svg class="github-icon" height="32" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="32" data-view-component="true">
                <path fill="white" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
            <p class="btn-github">Do Docs</p>
        </a>
    </div>
    """
        
    st.markdown(html_content, unsafe_allow_html=True)
    # st.button('Go back to Home', on_click=lambda: navigate_to('home'))
    # st.markdown("""
    # <style>
    # .main {
    #     background-color: #1E1E2E;
    #     color: #c9d1d9;
    #     font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji;
    #     font-size: 16px;
    #     line-height: 1.5;
    # }
    # h1, h2, h3 {
    #     border-bottom: 1px solid #21262d;
    #     padding-bottom: 0.3em;
    #     color: #c9d1d9;
    # }
    # .code-block {
    #     background-color: #2E2E3E;
    #     border-radius: 6px;
    #     padding: 16px;
    #     font-family: monospace;
    #     font-size: 85%;
    #     line-height: 1.45;
    #     overflow-x: auto;
    #     white-space: pre-wrap;
    #     word-wrap: break-word;
    # }
    # .function-name {
    #     color: #707CED;
    #     font-weight: bold;
    # }
    # .parameter {
    #     color: #FFD700;
    # }
    # </style>
    # """, unsafe_allow_html=True)
    
    # # Documentation content
    # st.markdown("""
    # # Protecto Vault Documentation
    
    # ## 1. Mask Function - To Mask Your Data
    
    # The `protecto_mask` function is used to encrypt sensitive data.
    
    # ### Syntax
    
    # <div class="code-block">
    # SELECT <span class="function-name">protecto_mask</span>(
    #     ARRAY_CONSTRUCT(<span class="parameter">'your_data_here'</span>),
    #     <span class="parameter">token_type</span>,
    #     <span class="parameter">format_type</span>,
    #     <span class="parameter">return_type</span>
    # )
    # </div>
    
    # ### Parameters
    
    # - `your_data_here`: The data you want to mask (string or array of strings)
    # - `token_type`: Type of token to use for masking (e.g., 'Text Token', 'Numeric Token')
    # - `format_type`: Format of the input data (e.g., 'Person Name', 'Address', 'Phone Number')
    # - `return_type`: Type of return value (e.g., 'token_value', 'toxicity_analysis', 'all')
    
    # ### Example
    
    # <div class="code-block">
    # SELECT <span class="function-name">protecto_mask</span>(
    #     ARRAY_CONSTRUCT('John Doe'),
    #     'Text Token',
    #     'Person Name',
    #     'token_value'
    # )
    # </div>
    
    # ## 2. Unmask Function - To Unmask Your Data
    
    # The `protecto_unmask` function is used to decrypt previously masked data.
    
    # ### Syntax
    
    # <div class="code-block">
    # SELECT <span class="function-name">protecto_unmask</span>(
    #     ARRAY_CONSTRUCT(<span class="parameter">'your_masked_data_here'</span>),
    #     <span class="parameter">other_parameters</span>
    # )
    # </div>
    
    # ### Parameters
    
    # - `your_masked_data_here`: The masked data you want to unmask (string or array of strings)
    # - `other_parameters`: Additional parameters required for unmasking (specific to your implementation)
    
    # ### Example
    
    # <div class="code-block">
    # SELECT <span class="function-name">protecto_unmask</span>(
    #     ARRAY_CONSTRUCT('4KTxXX9xZ4'),
    #     'additional_param1',
    #     'additional_param2'
    # )
    # </div>
    
    # ## Usage Notes
    
    # - Ensure you have the necessary permissions to use these functions.
    # - Always handle sensitive data with care and in compliance with data protection regulations.
    # - The mask function encrypts data, while the unmask function decrypts it.
    # - Be cautious when using the unmask function, as it reveals sensitive information.
    # - Regularly review and update your data masking policies to maintain security.
    
    # For more detailed information, please refer to the full Protecto Vault documentation.
    # """, unsafe_allow_html=True)

def main():
    st.markdown("""
    <style>
        /* Custom background for sidebar */
        [data-testid=stSidebar] {
            background-color: #000221;
            background-attachment: fixed;
            background-size: cover;
        }
        
        /* Ensure content in sidebar is visible */
        [data-testid=stSidebar] > div:first-child {
            background-color: #000221;
            padding: 2rem 1rem;
            height: 100vh;
        }

        /* Logo image styling */
        .sidebar-logo {
            display: flex;
            justify-content: center;
            padding-bottom: 1rem;
        }
        .sidebar-logo img {
            width: 130px;
            height: 80px;
            object-fit: contain;
        }

       .stButton > button {
            text-align: center;
            background: linear-gradient(to right, #707CED, #FFFF99);
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 5px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(to right, #45a049, #1e88e5);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .stButton > button:active {
            transform: translateY(2px);
        }
        
        /* Style for buttons */
        .stButton-one > button {
            width: 100%;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 10px 15px;
            transition: all 0.3s;
            background-color: rgba(255, 255, 255, 0.7);
            color: #4B68FF;
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 10px;
        }
        .stButton-one > button:hover {
            background-color: rgba(75, 104, 255, 0.1);
        }
        .stButton-one > button:active {
            background-color: #4B68FF;
            color: white;
        }
        
    
    </style>
    """, unsafe_allow_html=True)
   
    custom_sidebar_css = """
    <style>
        .sidebar .stButton > button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom: 10px;
            transition: background-color 0.3s;
        }
        .sidebar .stButton > button:hover {
            background-color: #45a049;
        }
        .sidebar-logo {
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
    """
    
    # Inject custom CSS
    st.markdown(custom_sidebar_css, unsafe_allow_html=True)
    


    
    # Initialize session state for current page
    def change_page(page):
        st.session_state.current_page = page

    # Sidebar content
    with st.sidebar:
        # Add logo
        st.markdown('<div class="sidebar-logo"><img src="https://i.postimg.cc/NyJc67wq/oie-DBP9i-CBL61-C8.png" alt="Logo" width="190" height="140"></div>', unsafe_allow_html=True)
        
        # Create buttons for navigation
        st.markdown('<div class="sidebar-nav-sidebar-here">', unsafe_allow_html=True)
        
        pages = ['Home', 'Setup', 'Try Now', 'Docs']
        for page in pages:
            
            active_class = 'active' if st.session_state.current_page == page else ''
            
            if st.button(page, key=f"nav-{page}", help=f"Navigate to {page}", 
                         use_container_width=True, 
                         type="secondary" if st.session_state.current_page != page else "primary"):
                st.session_state.current_page = page
                change_page(page)
                # st.toast(f"""Selected Page: {page}""", icon = "⚡️")
                # st.toast(f"""Page: {st.session_state.current_page} -> {active_class}""", icon = "⚡️")
        
        st.markdown('</div>', unsafe_allow_html=True)
    

    # JavaScript for handling button clicks
    st.markdown("""
    <script>
    function handleClick(page) {
        // Update session state
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            name: 'current_page',
            value: page
        }, '*');
        
        // Trigger re-run
        window.parent.postMessage({type: 'streamlit:forceRerun'}, '*');
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Main content area
    # st.write(f"Current page: {st.session_state.current_page}")

    # Display the selected page
    if st.session_state.current_page == 'Home':
        home_page()
    elif st.session_state.current_page == 'Setup':
        setup_page()
    elif st.session_state.current_page == 'Try Now':
        engage_help_page()
    elif st.session_state.current_page == 'Docs':
        document_page()



if __name__ == "__main__":
    main()