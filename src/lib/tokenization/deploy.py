from snowflake.snowpark import Session
from src.lib.tokenization.mask.mask import register_mask
from src.lib.tokenization.mask.async_mask import register_async_mask
from src.lib.tokenization.mask.async_mask_result import register_get_mask_async_result

def register_tokenization_helpers():
    from src.lib.tokenization.mask.mask import get_snowflake_session
    session = get_snowflake_session()

    # For Streamlit 
    #from snowflake.snowpark.context import get_active_session
    #session = get_active_session()
    
    # Register all UDFs
    register_mask(session)
    register_async_mask(session)
    register_get_mask_async_result(session)
    
    print("All UDFs have been registered successfully.")

