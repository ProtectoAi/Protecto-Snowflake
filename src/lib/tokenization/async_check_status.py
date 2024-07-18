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


# Define the Snowpark UDF to check the status of an asynchronous mask operation
def check_mask_async_status(tracking_id: str) -> str:
    from protecto_ai import ProtectoVault
    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(tracking_id, str):
        raise ValueError("The 'tracking_id' parameter must be a string.")
    
    status_data = vault.async_status([tracking_id])
    status = status_data["data"][0]["status"]
    return status

# Register the UDF
def register_check_mask_async_status(session: session):
    session.udf.register(
        func=check_mask_async_status,
        name="protecto_async_status",
        return_type=StringType(),
        input_types = [StringType()],
        is_permanent=True,
        replace = True,
        stage_location=STAGE_LOCATION,
        external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
        secrets=SECRETS,
        packages=PACKAGES,
        imports=IMPORTS
    )
    print("UDF 'protecto_async_check_status' registered successfully.")
