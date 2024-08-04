
-- REGISTER PROTECTO MASK
CREATE OR REPLACE FUNCTION PROTECTO.VAULT.protecto_mask(mask_values ARRAY, token_type STRING DEFAULT 'None', format_type STRING DEFAULT 'None', return_type STRING DEFAULT 'token_value')
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/dependencies/protecto_ai.zip','@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/tokenization/mask.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_api)
SECRETS = ('cred' = protecto_api_key )
HANDLER = 'mask.mask';

-- REGISTER PROTECTO UNMASK
CREATE OR REPLACE FUNCTION PROTECTO.VAULT.protecto_unmask(mask_values ARRAY)
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/dependencies/protecto_ai.zip','@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/tokenization/unmask.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_api)
SECRETS = ('cred' = protecto_api_key )
HANDLER = 'unmask.unmask';

-- REGISTER PROTECTO ASYNC MASK

CREATE OR REPLACE FUNCTION PROTECTO.VAULT.protecto_async_mask(mask_values ARRAY, token_type STRING DEFAULT 'None', format_type STRING DEFAULT 'None')
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/dependencies/protecto_ai.zip','@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/tokenization/async_mask.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_api)
SECRETS = ('cred' = protecto_api_key )
HANDLER = 'async_mask.async_mask';

-- REGISTER PROTECTO ASYNC MASK RESULTS

CREATE OR REPLACE FUNCTION PROTECTO.VAULT.protecto_async_mask_result(tracking_id STRING,return_type STRING DEFAULT 'status')
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/dependencies/protecto_ai.zip','@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/tokenization/async_mask_result.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_api)
SECRETS = ('cred' = protecto_api_key )
HANDLER = 'async_mask_result.async_mask_result';


-- REGISTER PROTECTO ASYNC UNMASK

CREATE OR REPLACE FUNCTION PROTECTO.VAULT.protecto_async_unmask(mask_values ARRAY)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/dependencies/protecto_ai.zip','@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/tokenization/async_unmask.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_api)
SECRETS = ('cred' = protecto_api_key )
HANDLER = 'async_unmask.async_unmask';


-- REGISTER PROTECTO ASYNC UNMASK RESULTS

CREATE OR REPLACE FUNCTION PROTECTO.VAULT.protecto_async_unmask_result(tracking_id STRING,return_type STRING DEFAULT 'status')
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/dependencies/protecto_ai.zip','@PROTECTO_PACKAGE.VAULT.PACKAGE_STAGE/tokenization/async_unmask_result.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_api)
SECRETS = ('cred' = protecto_api_key )
HANDLER = 'async_unmask_result.async_unmask_result';


-- USAGE ACCESS TO NEW ROLE
CREATE ROLE IF NOT EXISTS Protecto_role;

-- Grant usage access to Protecto_role on the database
GRANT USAGE ON DATABASE PROTECTO TO ROLE Protecto_role;

-- Grant usage access to Protecto_role on the schema
GRANT USAGE ON SCHEMA PROTECTO.VAULT TO ROLE Protecto_role;

-- Grant usage access to Protecto_role on the PACKAGE_STAGE
GRANT READ ON STAGE PROTECTO.VAULT.APP_STAGE TO ROLE Protecto_role;
GRANT WRITE ON STAGE PROTECTO.VAULT.APP_STAGE TO ROLE Protecto_role;

-- Grant execute access to Protecto_role on the specified functions
GRANT USAGE ON FUNCTION PROTECTO.VAULT.protecto_mask(ARRAY, STRING, STRING, STRING) TO ROLE Protecto_role;
GRANT USAGE ON FUNCTION PROTECTO.VAULT.protecto_unmask(ARRAY) TO ROLE Protecto_role;
GRANT USAGE ON FUNCTION PROTECTO.VAULT.protecto_async_mask(ARRAY, STRING, STRING) TO ROLE Protecto_role;
GRANT USAGE ON FUNCTION PROTECTO.VAULT.protecto_async_mask_result(STRING,STRING) TO ROLE Protecto_role;
GRANT USAGE ON FUNCTION PROTECTO.VAULT.protecto_async_unmask(ARRAY) TO ROLE Protecto_role;
GRANT USAGE ON FUNCTION PROTECTO.VAULT.protecto_async_unmask_result(STRING,STRING) TO ROLE Protecto_role;

GRANT CREATE SECRET ON SCHEMA PROTECTO.VAULT TO ROLE Protecto_role;

GRANT USAGE ON INTEGRATION protecto_api TO ROLE Protecto_role;






