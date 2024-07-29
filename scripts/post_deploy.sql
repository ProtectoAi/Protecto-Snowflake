CREATE OR REPLACE FUNCTION protecto_vault.vault_schema.protecto_mask(mask_values ARRAY, token_type STRING DEFAULT 'Text Token', format_type STRING DEFAULT 'Person Name', return_type STRING DEFAULT 'token_value')
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch','snowflake-snowpark-python')
IMPORTS = ('@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/dependencies/protecto_ai.zip','@PROTECTO_VAULT_PACKAGE.MY_SCHEMA.stage/streamlit/tokenization/mask.py')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_external_access_integration)
SECRETS = ('cred' = protecto_secret )
HANDLER = 'mask.mask'