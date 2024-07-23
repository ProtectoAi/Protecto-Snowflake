def run_streamlit():
   # Import python packages
   # Streamlit app testing framework requires imports to reside here
   # Streamlit app testing documentation: https://docs.streamlit.io/library/api-reference/app-testing
   import pandas as pd
   import streamlit as st
   from snowflake.snowpark.functions import call_udf, col
   from snowflake.snowpark import Session

   st.title('Hello Snowflake!')


   st.header('UDF Example')

   st.write(
      """The sum of the two numbers is calculated by the Python add_fn() function
         which is called from core.add() UDF defined in your setup_script.sql.
      """)


if __name__ == '__main__':
   run_streamlit()
