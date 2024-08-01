from snowflake.snowpark import Session
from snowflake_config import *

def get_snowflake_session():
    connection_parameters = {
        "account": SNOWFLAKE_ACCOUNT,
        "user": SNOWFLAKE_USER,
        "password": SNOWFLAKE_PASSWORD,
        "role": SNOWFLAKE_ROLE,
        "warehouse": SNOWFLAKE_WAREHOUSE,
        "database": SNOWFLAKE_DATABASE,
        "schema": SNOWFLAKE_SCHEMA
    }
    return Session.builder.configs(connection_parameters).create()

# Use the session in your app
session = get_snowflake_session()
