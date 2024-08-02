-- 1. Create application roles
CREATE APPLICATION ROLE IF NOT EXISTS protecto_app_role;

-- 2. Create a versioned schema to hold those UDFs/Stored Procedures
CREATE OR ALTER VERSIONED SCHEMA protecto_core;

-- 3. Grant usage on the schema to the application role
GRANT USAGE ON SCHEMA protecto_core TO APPLICATION ROLE protecto_app_role;

-- 4. Create a stage in the schema
CREATE OR REPLACE STAGE protecto_core.PROTECTO_STAGE;

-- 5. Grant read and write privileges on the stage to the application role
GRANT READ ON STAGE protecto_core.PROTECTO_STAGE TO APPLICATION ROLE protecto_app_role;
GRANT WRITE ON STAGE protecto_core.PROTECTO_STAGE TO APPLICATION ROLE protecto_app_role;

-- 6. Create a Streamlit object
CREATE OR REPLACE STREAMLIT protecto_core.PROTECTO_VAULT
     FROM '/streamlit/'
     MAIN_FILE = 'streamlit.py';

-- 7. Grant usage on the Streamlit object to the application role
GRANT USAGE ON STREAMLIT protecto_core.PROTECTO_VAULT TO APPLICATION ROLE protecto_app_role;
