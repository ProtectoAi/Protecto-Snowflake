from snowflake.snowpark import Session
from snowflake.snowpark.functions import udf

# Initialize Snowpark session
session = Session.builder.configs(your_snowflake_config).create()

# Register the mask function as a UDF
@udf
def mask_udf(mask_values: list, token_type: str = "Text Token", format_type: str = "Person Name", return_type: str = "token_value") -> list:
    return mask(mask_values, token_type, format_type, return_type)

session.udf.register(
    func=mask_udf,
    name="mask_udf",
    return_type="ARRAY",
    input_types=["ARRAY", "STRING", "STRING", "STRING"],
    packages=["protecto_ai"],
    imports=["@my_stage/protecto_vault_methods.py"],
    language="PYTHON"
)

# Register the async_mask function as a UDF
@udf
def async_mask_udf(mask_values: list) -> str:
    return async_mask(mask_values)

session.udf.register(
    func=async_mask_udf,
    name="async_mask_udf",
    return_type="STRING",
    input_types=["ARRAY"],
    packages=["protecto_ai"],
    imports=["@my_stage/protecto_vault_methods.py"],
    language="PYTHON"
)

# Register the check_mask_async_status function as a UDF
@udf
def check_mask_async_status_udf(tracking_ids: list) -> list:
    return check_mask_async_status(tracking_ids)

session.udf.register(
    func=check_mask_async_status_udf,
    name="check_mask_async_status_udf",
    return_type="ARRAY",
    input_types=["ARRAY"],
    packages=["protecto_ai"],
    imports=["@my_stage/protecto_vault_methods.py"],
    language="PYTHON"
)

# Register the get_mask_async_result function as a UDF
@udf
def get_mask_async_result_udf(tracking_ids: list, return_type: str = "token_value") -> list:
    return get_mask_async_result(tracking_ids, return_type)

session.udf.register(
    func=get_mask_async_result_udf,
    name="get_mask_async_result_udf",
    return_type="ARRAY",
    input_types=["ARRAY", "STRING"],
    packages=["protecto_ai"],
    imports=["@my_stage/protecto_vault_methods.py"],
    language="PYTHON"
)
