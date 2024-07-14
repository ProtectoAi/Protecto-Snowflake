from snowflake.snowpark import Session
from protecto_ai import ProtectoVault
import _snowflake

# Define the external access integration for the UDFs
EXTERNAL_ACCESS_INTEGRATIONS = ('protecto_access_integration',)

# Define the secrets used for authentication
SECRETS = {
    'cred': 'protecto_secret'
}

# Fetch the OAuth token from Snowflake secrets
def get_auth_token():
    return _snowflake.get_generic_secret_string('cred')

# Define the Snowflake session
def get_snowflake_session():
    # Make sure to replace these placeholder values with actual configuration
    return Session.builder.configs({
        'account': '<your_account>',
        'user': '<your_user>',
        'password': '<your_password>',
        'role': '<your_role>',
        'warehouse': '<your_warehouse>',
        'database': '<your_database>',
        'schema': '<your_schema>',
    }).create()

# Define the Snowpark UDF to check the status of an asynchronous mask operation
def check_mask_async_status(tracking_id: str) -> str:
    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(tracking_id, str):
        raise ValueError("The 'tracking_id' parameter must be a string.")
    
    status_data = vault.async_status([tracking_id])
    status = status_data["data"][0]["status"]
    return status

# Register the UDF
def register_check_mask_async_status(session: Session):
    session.udf.register(
        func=check_mask_async_status,
        name="protecto_async_check_status",
        return_type="STRING",
        is_permanent=True,
        stage_location="@my_stage/protecto_ai.zip",
        external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
        secrets=SECRETS
    )
    print("UDF 'protecto_async_check_status' registered successfully.")
