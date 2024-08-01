-- A general guideline to building this script looks like:
-- 1. Create application roles
CREATE APPLICATION ROLE IF NOT EXISTS protecto_app_role;

-- 2. Create a versioned schema to hold those UDFs/Stored Procedures
CREATE OR ALTER VERSIONED SCHEMA protecto_core;
GRANT USAGE ON SCHEMA protecto_core TO APPLICATION ROLE protecto_app_role;

-- 3. Create a streamlit object using the code you wrote in src/module-ui, as shown below. 
-- The `from` value is derived from the stage path described in snowflake.yml
CREATE STREAMLIT protecto_core.ui
     FROM '/streamlit/'
     MAIN_FILE = 'streamlit.py';

-- 4. Grant appropriate privileges over these objects to your application roles. 
-- GRANT USAGE ON STREAMLIT protecto_core.ui TO APPLICATION ROLE protecto_app_role;

-- Additional steps to allow the app to register UDFs:
-- Grant USAGE on the database (assuming 'protecto_core' schema is part of 'protecto_database')
-- GRANT USAGE ON DATABASE protecto_database TO APPLICATION ROLE protecto_app_role;

-- Grant CREATE FUNCTION on the schema to allow UDF creation
-- GRANT CREATE FUNCTION ON SCHEMA protecto_core TO APPLICATION ROLE protecto_app_role;

-- Optionally, if you want to allow the app to create other objects (e.g., tables, views, etc.), you can add those grants too:
-- GRANT CREATE TABLE ON SCHEMA protecto_core TO APPLICATION ROLE protecto_app_role;
-- GRANT CREATE VIEW ON SCHEMA protecto_core TO APPLICATION ROLE protecto_app_role;


-- Needed at the customer end
-- To extend the Streamlit app's ability to register UDFs in a different database and schema

-- 1. Grant USAGE on the new database to the application role
-- GRANT USAGE ON DATABASE new_database TO APPLICATION ROLE protecto_app_role;

-- 2. Grant USAGE on the new schema to the application role
-- GRANT USAGE ON SCHEMA new_database.new_schema TO APPLICATION ROLE protecto_app_role;

-- 3. Grant CREATE FUNCTION on the new schema to the application role to allow UDF creation
-- GRANT CREATE FUNCTION ON SCHEMA new_database.new_schema TO APPLICATION ROLE protecto_app_role;

-- 4. Optionally, if you want to allow the app to create other objects (e.g., tables, views, etc.) in the new schema, you can add those grants too:
-- GRANT CREATE TABLE ON SCHEMA new_database.new_schema TO APPLICATION ROLE protecto_app_role;
-- GRANT CREATE VIEW ON SCHEMA new_database.new_schema TO APPLICATION ROLE protecto_app_role;

