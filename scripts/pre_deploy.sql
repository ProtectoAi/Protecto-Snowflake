CREATE DATABASE IF NOT EXISTS protecto_vault;

USE DATABASE protecto_vault;

-- Step 2: Create a schema called vault_schema
CREATE SCHEMA IF NOT EXISTS vault_schema;

USE SCHEMA vault_schema;

-- Step 3: Create a stage called vault_stage
CREATE STAGE IF NOT EXISTS protecto_vault.vault_schema.vault_stage;

-- Step 4: Create network rule, secret, and external access integration


---- network rule
CREATE OR REPLACE NETWORK RULE protecto_network_rule
MODE = EGRESS
TYPE = HOST_PORT
VALUE_LIST = ('trial.protecto.ai');

--- Secret
CREATE OR REPLACE SECRET protecto_secret
  TYPE = GENERIC_STRING
  SECRET_STRING = '';

--- external access integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION protecto_external_access_integration
ALLOWED_NETWORK_RULES = (protecto_network_rule)
ALLOWED_AUTHENTICATION_SECRETS = (protecto_secret)
ENABLED = true;












