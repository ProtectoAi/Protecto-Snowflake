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
  SECRET_STRING = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZXIiOiJQcm90ZWN0byIsImV4cGlyYXRpb25fZGF0ZSI6IjIwMjktMDctMDQiLCJwZXJtaXNzaW9ucyI6WyJtYXNrIiwidW5tYXNrIl0sInVzZXJfbmFtZSI6Im1haWwydml2ZWtzc0BnbWFpbC5jb20iLCJkYl9uYW1lIjoicHJvdGVjdG9fZ21haWxfZnZqcGd4a2kiLCJoYXNoZWRfcGFzc3dvcmQiOiIyMmQ2YmNiMDdiOTAxMjNjMGVjNGZiMDk0OGU4NmNiNTY5ZmI0N2MxMTViMWRkMjE1ODA5Y2Q2MjhmZTc1M2RlIn0.70C6lmgPm3507UHt_fQ6tjoNKAj_6FsI5pElX_oSZTE';

--- external access integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION protecto_external_access_integration
ALLOWED_NETWORK_RULES = (protecto_network_rule)
ALLOWED_AUTHENTICATION_SECRETS = (protecto_secret)
ENABLED = true;








