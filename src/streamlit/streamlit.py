import streamlit as st
from snowflake.snowpark.context import get_active_session


session = get_active_session()

st.title('Hello Snowflake!')

st.title(say_hello())


st.header('UDF Example')


