
import pandas as pd
import streamlit as st
from snowflake.snowpark.functions import call_udf, col
from snowflake.snowpark import Session
from hello1 import say_hello,register_protecto_mask


st.title('Hello Snowflake!')


st.header('UDF Example')


st.write(
   """TESTING APP
   """)

