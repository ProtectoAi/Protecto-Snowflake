-- REGISTER PROTECTO MASK

CREATE OR REPLACE FUNCTION protecto_vault.vault_schema.protecto_mask(mask_values ARRAY, token_type STRING DEFAULT 'None', format_type STRING DEFAULT 'None', return_type STRING DEFAULT 'token_value')
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/dependencies/protecto_ai.zip','@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/tokenization/mask.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_external_access_integration)
SECRETS = ('cred' = protecto_secret )
HANDLER = 'mask.mask';

-- REGISTER PROTECTO UNMASK
CREATE OR REPLACE FUNCTION protecto_vault.vault_schema.protecto_unmask(mask_values ARRAY)
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/dependencies/protecto_ai.zip','@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/tokenization/unmask.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_external_access_integration)
SECRETS = ('cred' = protecto_secret )
HANDLER = 'unmask.unmask';

-- REGISTER PROTECTO ASYNC MASK

CREATE OR REPLACE FUNCTION protecto_vault.vault_schema.protecto_async_mask(mask_values ARRAY, token_type STRING DEFAULT 'None', format_type STRING DEFAULT 'None')
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/dependencies/protecto_ai.zip','@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/tokenization/async_mask.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_external_access_integration)
SECRETS = ('cred' = protecto_secret )
HANDLER = 'async_mask.async_mask';

-- REGISTER PROTECTO ASYNC MASK RESULTS

CREATE OR REPLACE FUNCTION protecto_vault.vault_schema.protecto_async_mask_result(tracking_id STRING,return_type STRING DEFAULT 'status')
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/dependencies/protecto_ai.zip','@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/tokenization/async_mask_result.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_external_access_integration)
SECRETS = ('cred' = protecto_secret )
HANDLER = 'async_mask_result.async_mask_result';


-- REGISTER PROTECTO ASYNC UNMASK

CREATE OR REPLACE FUNCTION protecto_vault.vault_schema.protecto_async_unmask(mask_values ARRAY)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/dependencies/protecto_ai.zip','@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/tokenization/async_unmask.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_external_access_integration)
SECRETS = ('cred' = protecto_secret )
HANDLER = 'async_unmask.async_unmask';


-- REGISTER PROTECTO ASYNC UNMASK RESULTS

CREATE OR REPLACE FUNCTION protecto_vault.vault_schema.protecto_async_unmask_result(tracking_id STRING,return_type STRING DEFAULT 'status')
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/dependencies/protecto_ai.zip','@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/tokenization/async_unmask_result.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_external_access_integration)
SECRETS = ('cred' = protecto_secret )
HANDLER = 'async_unmask_result.async_unmask_result';


-- USAGE ACCESS TO NEW ROLE
CREATE ROLE IF NOT EXISTS Protecto_role;

-- Grant usage access to Protecto_role on the database
GRANT USAGE ON DATABASE protecto_vault TO ROLE Protecto_role;

-- Grant usage access to Protecto_role on the schema
GRANT USAGE ON SCHEMA protecto_vault.vault_schema TO ROLE Protecto_role;

-- Grant usage access to Protecto_role on the stage
GRANT READ ON STAGE protecto_vault.vault_schema.vault_stage TO ROLE Protecto_role;
GRANT WRITE ON STAGE protecto_vault.vault_schema.vault_stage TO ROLE Protecto_role;

-- Grant execute access to Protecto_role on the specified functions
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_mask(ARRAY, STRING, STRING, STRING) TO ROLE Protecto_role;
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_unmask(ARRAY) TO ROLE Protecto_role;
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_async_mask(ARRAY, STRING, STRING) TO ROLE Protecto_role;
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_async_mask_result(STRING,STRING) TO ROLE Protecto_role;
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_async_unmask(ARRAY) TO ROLE Protecto_role;
GRANT USAGE ON FUNCTION protecto_vault.vault_schema.protecto_async_unmask_result(STRING,STRING) TO ROLE Protecto_role;




