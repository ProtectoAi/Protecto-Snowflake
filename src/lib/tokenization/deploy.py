from snowflake.snowpark import Session
from mask import register_mask


def register_tokenization_helpers():
    from mask import register_protecto_mask
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
    
    # Register all UDFs
    register_protecto_mask(session)
    register_async_mask(session)
    register_get_mask_async_result(session)
    
    print("All UDFs have been registered successfully.")

