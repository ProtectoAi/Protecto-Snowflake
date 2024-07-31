-- 1. Create application roles
CREATE APPLICATION ROLE IF NOT EXISTS protecto_app_role;

-- 2. Create a versioned schema to hold those UDFs/Stored Procedures
CREATE OR ALTER VERSIONED SCHEMA protecto_core;
GRANT USAGE ON SCHEMA protecto_core TO APPLICATION ROLE protecto_app_role;

CREATE OR REPLACE STAGE protecto_core.PROTECTO_STAGE;
GRANT READ ON STAGE protecto_core.PROTECTO_STAGE TO APPLICATION ROLE protecto_app_role;
GRANT WRITE ON STAGE protecto_core.PROTECTO_STAGE TO APPLICATION ROLE protecto_app_role;

-- 3. Create a streamlit object 
CREATE OR REPLACE STREAMLIT protecto_core.PROTECTO_VAULT
     FROM '/streamlit/'
     MAIN_FILE = 'streamlit.py';

-- 4. Grant appropriate privileges over these objects to your application roles. 
GRANT USAGE ON STREAMLIT protecto_core.PROTECTO_VAULT TO APPLICATION ROLE protecto_app_role;


-- Grant execute access to Protecto_role on the specified functions
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_mask(ARRAY, STRING, STRING, STRING) TO ROLE protecto_app_role;
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_unmask(ARRAY) TO ROLE protecto_app_role;
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_async_mask(ARRAY, STRING, STRING) TO ROLE protecto_app_role;
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_async_mask_result(STRING,STRING) TO ROLE protecto_app_role;
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_async_unmask(ARRAY) TO ROLE protecto_app_role;
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_async_unmask_result(STRING,STRING) TO ROLE protecto_app_role;

-- Grant usage on the secret to Protecto_role
GRANT USAGE ON SECRET protecto_secret TO ROLE Protecto_role;

-- Grant modify on the secret to Protecto_role
GRANT MODIFY ON SECRET protecto_secret TO ROLE Protecto_role;




