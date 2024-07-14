-- ==========================================
-- This script runs when the app is installed 
-- ==========================================

-- Create Application Role and Schema
create application role if not exists app_instance_role;
create or alter versioned schema app_instance_schema;


-- Create Streamlit app
create or replace streamlit app_instance_schema.streamlit from '/app' main_file='streamlit.py';



-- Grant usage and permissions on objects
grant usage on schema app_instance_schema to application role app_instance_role;
grant usage on streamlit app_instance_schema.streamlit to application role app_instance_role;





