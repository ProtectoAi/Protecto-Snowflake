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

# Define the Snowpark UDF to perform asynchronous masking
def async_mask(mask_values: list, token_type: str = "None", format_type: str = "None") -> str:
    from protecto_ai import ProtectoVault
    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(mask_values, list):
        raise ValueError("The 'mask_values' parameter must be a list.")
    
    try:
        if token_type == "None" and format_type == "None":
            payload = {"mask": [{"value": value} for value in mask_values]}
            tracking_data = vault.async_mask(payload)
        else:
            payload = {"mask": [{"value": value,"token_name": token_type, "format": format_type } for value in mask_values]}
            tracking_data = vault.async_mask(payload)
    except ConnectionError as e:
        raise RuntimeError(f"Connection error occurred: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

    if not isinstance(tracking_data, dict) or 'data' not in tracking_data:
        raise RuntimeError(f"Unexpected response format: {tracking_data}")
    
    tracking_id = tracking_data["data"][0]["tracking_id"]
    return tracking_id


# Register the UDF
def register_async_mask(session: session):
    session.udf.register(
        func=async_mask,
        name="protecto_async_mask",
        return_type=StringType(),
        input_types = [ArrayType(),StringType(),StringType()],
        is_permanent=True,
        replace = True,
        stage_location=STAGE_LOCATION,
        external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
        secrets=SECRETS,
        packages=PACKAGES,
        imports=IMPORTS
    )
    print("UDF 'protecto_async_mask' registered successfully.")

