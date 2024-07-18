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

# Define the Snowpark UDF to perform asynchronous masking
def async_mask(mask_values: list, token_type: str = "Text Token", format_type: str = "Person Name") -> str:
    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(mask_values, list):
        raise ValueError("The 'mask_values' parameter must be a list.")
    
    payload = {"mask": [{"value": value} for value in mask_values]}
    tracking_data = vault.async_mask(payload)
    tracking_id = tracking_data["data"][0]["tracking_id"]
    return tracking_id

# Register the UDF
def register_async_mask(session: Session):
    session.udf.register(
        func=async_mask,
        name="protecto_async_mask",
        return_type="STRING",
        is_permanent=True,
        stage_location="@my_stage/protecto_ai.zip",
        external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
        secrets=SECRETS
    )
    print("UDF 'protecto_async_mask' registered successfully.")
