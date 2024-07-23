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

# Define the Snowpark UDF to mask data
def async_unmask(unmask_values: list) -> str:
    from protecto_ai import ProtectoVault
    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(unmask_values, list):
        raise ValueError("The 'unmask_values' parameter must be a list.")
    
    try:
        tracking_data = vault.async_unmask(unmask_values)
        if isinstance(tracking_data, dict) and 'data' in tracking_data:
            tracking_details = [{"tracking_id":tracking_data["data"][0]["tracking_id"],"success":tracking_data["success"],"error":tracking_data["error"]}]
            return tracking_details
    except ConnectionError as e:
        raise RuntimeError(f"Connection error occurred: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

    else:
        raise RuntimeError(f"Unexpected response format: {result}")


# Register the UDF
def register_async_unmask(session):
    session.udf.register(
        func=async_unmask,
        name="protecto_async_unmask",
        return_type=ArrayType(),
        input_types = [ArrayType()],
        is_permanent=True,
        replace = True,
        stage_location=STAGE_LOCATION,
        external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
        secrets=SECRETS,
        packages=PACKAGES,
        imports=IMPORTS
    )
    print("UDF 'protecto_async_unmask' registered successfully.")
