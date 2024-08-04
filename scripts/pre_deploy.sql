-- Define variables
SET DBNAME = 'PROTECTO';
SET SCHEMA = 'VAULT';
SET STAGE = 'APP_STAGE';
SET NETWORK_RULE = 'PROTECTO_NETWORK';
SET API_SECRET = 'PROTECTO_API_KEY';
SET EXTERNAL_ACCESS_INTEGRATION = 'PROTECTO_API';

-- Step 1: Create database if it does not exist
CREATE DATABASE IF NOT EXISTS IDENTIFIER($DBNAME);

-- Use the database
USE DATABASE IDENTIFIER($DBNAME);

-- Step 2: Create schema if it does not exist
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($SCHEMA);

-- Use the schema
USE SCHEMA IDENTIFIER($SCHEMA);

-- Step 3: Create stage if it does not exist
SET SQL_STATEMENT = 
    'CREATE STAGE IF NOT EXISTS ' || $DBNAME || '.' || $SCHEMA || '.' || $STAGE;

-- Execute the SQL statement
EXECUTE IMMEDIATE $SQL_STATEMENT;

-- Step 4: Create network rule, secret, and external access integration

-- Create network rule
CREATE OR REPLACE NETWORK RULE IDENTIFIER($NETWORK_RULE)
MODE = EGRESS
TYPE = HOST_PORT
VALUE_LIST = ('trial.protecto.ai');

-- Create secret
CREATE OR REPLACE SECRET IDENTIFIER($API_SECRET)
TYPE = GENERIC_STRING
SECRET_STRING = '';

-- Create external access integration
SET SQL_STATEMENT = 
    'CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION ' || $EXTERNAL_ACCESS_INTEGRATION || 
    ' ALLOWED_NETWORK_RULES = (' || $NETWORK_RULE || ')' ||
    ' ALLOWED_AUTHENTICATION_SECRETS = (' || $API_SECRET || ')' ||
    ' ENABLED = true;';

-- Execute the SQL statement
EXECUTE IMMEDIATE $SQL_STATEMENT;
