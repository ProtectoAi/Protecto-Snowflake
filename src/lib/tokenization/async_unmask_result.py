from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.types import StringType,ArrayType
import _snowflake

session = get_active_session()

## Should be moved To config file
SECRETS = {'cred': 'protecto_secret'}
PACKAGES = ['requests', 'multipledispatch']
EXTERNAL_ACCESS_INTEGRATIONS = ('protecto_access_integration',)
IMPORTS = ['@my_stage/protecto_ai.zip']
STAGE_LOCATION = "@protecto_snowflake.my_schema.my_stage"

# Fetch the OAuth token from Snowflake secrets
def get_auth_token():
    return _snowflake.get_generic_secret_string('cred')

# Define the Snowpark UDF to get the result of an asynchronous mask operation
def get_unmask_async_result(tracking_id: str, return_type: str = "status") -> list:
    from protecto_ai import ProtectoVault
    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(tracking_id, str):
        raise ValueError("The 'tracking_id' parameter must be a string.")
    
    result = vault.async_status([tracking_id])
    
    for item in result['data']:
        if return_type == "status":
            final_result = [{"status": item["status"],"error":item["error_msg"]}]
        elif return_type == "value":
            final_result = [res['value'] for res in item['result']]
        else:
            raise ValueError(f"Invalid return_type: {return_type}")
    
    return final_result

# Register the UDF
def register_async_unmask_result(session: session):
    session.udf.register(
        func=get_unmask_async_result,
        name="protecto_async_unmask_result",
        return_type=ArrayType(),
        input_types = [StringType(),StringType()],
        is_permanent=True,
        replace = True,
        stage_location=STAGE_LOCATION,
        external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
        secrets=SECRETS,
        packages=PACKAGES,
        imports=IMPORTS
    )
    print("UDF 'protecto_async_unmask_result' registered successfully.")
