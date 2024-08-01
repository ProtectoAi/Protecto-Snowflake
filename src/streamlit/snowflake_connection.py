from snowflake.snowpark import Session
from snowflake_config import *

def get_snowflake_session():
    connection_parameters = {
        "account": "nq71637.west-us-2.azure",
        "user": "Vivek",
        "password": "Vivekshankar@123",
        "role": "VIVEK_ROLE",
        "warehouse": "VIVEK_WAREHOUSE",
        "database": "PROTECTO_SNOWFLAKE",
        "schema": "MY_SCHEMA"
    }
    return Session.builder.configs(connection_parameters).create()

# Use the session in your app
session = get_snowflake_session()
