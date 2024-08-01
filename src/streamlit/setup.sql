-- setup.sql for Snowflake Native App with Python Functions

-- Create a schema for the application
CREATE SCHEMA IF NOT EXISTS tokenization_app;

-- Create a stage to store Python files
CREATE OR REPLACE STAGE tokenization_app.python_files;

-- Upload Python files to the stage (you'll need to do this separately)
-- PUT file://path/to/your/python/files/@tokenization_app.python_files;

-- Create Python UDFs for each function
CREATE OR REPLACE FUNCTION tokenization_app.async_check_status(job_id STRING)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'async_check_status_udf'
AS $$
import_dir = sys._xoptions.get("snowflake_import_directory")
import sys
import os
sys.path.append(import_dir)
from async_check_status import async_check_status

def async_check_status_udf(job_id):
    return async_check_status(job_id)
$$;

CREATE OR REPLACE FUNCTION tokenization_app.async_mask_result(job_id STRING)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'async_mask_result_udf'
AS $$
import_dir = sys._xoptions.get("snowflake_import_directory")
import sys
import os
sys.path.append(import_dir)
from async_mask_result import async_mask_result

def async_mask_result_udf(job_id):
    return async_mask_result(job_id)
$$;

CREATE OR REPLACE FUNCTION tokenization_app.async_mask(input_data VARIANT)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'async_mask_udf'
AS $$
import_dir = sys._xoptions.get("snowflake_import_directory")
import sys
import os
sys.path.append(import_dir)
from async_mask import async_mask

def async_mask_udf(input_data):
    return async_mask(input_data)
$$;

CREATE OR REPLACE FUNCTION tokenization_app.mask(input_data VARIANT)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'mask_udf'
AS $$
import_dir = sys._xoptions.get("snowflake_import_directory")
import sys
import os
sys.path.append(import_dir)
from mask import mask

def mask_udf(input_data):
    return mask(input_data)
$$;

-- Create a procedure for demo
CREATE OR REPLACE PROCEDURE tokenization_app.run_demo()
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'run_demo'
AS $$
import_dir = sys._xoptions.get("snowflake_import_directory")
import sys
import os
sys.path.append(import_dir)
from demo import main as run_demo

def run_demo():
    return run_demo()
$$;

-- Grant usage on the schema to the application role
GRANT USAGE ON SCHEMA tokenization_app TO APPLICATION ROLE app_public;

-- Grant usage on functions and procedures to the application role
GRANT USAGE ON FUNCTION tokenization_app.async_check_status(STRING) TO APPLICATION ROLE app_public;
GRANT USAGE ON FUNCTION tokenization_app.async_mask_result(STRING) TO APPLICATION ROLE app_public;
GRANT USAGE ON FUNCTION tokenization_app.async_mask(VARIANT) TO APPLICATION ROLE app_public;
GRANT USAGE ON FUNCTION tokenization_app.mask(VARIANT) TO APPLICATION ROLE app_public;
GRANT USAGE ON PROCEDURE tokenization_app.run_demo() TO APPLICATION ROLE app_public;

-- Create a version function (optional, but recommended for versioning)
CREATE OR REPLACE FUNCTION tokenization_app.get_version()
RETURNS STRING
AS
$$
    '1.0.0'
$$;