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

# Define the Snowpark UDF to get the result of an asynchronous mask operation
def get_mask_async_result(tracking_id: str, return_type: str = "token_value") -> list:
    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(tracking_id, str):
        raise ValueError("The 'tracking_id' parameter must be a string.")
    
    result = vault.async_status([tracking_id])
    final_result = []
    
    for item in result['data']:
        if return_type == "token_value":
            final_result.append([res['token_value'] for res in item['result']])
        elif return_type == "toxicity_analysis":
            final_result.append([res['toxicity_analysis'] for res in item['result']])
        elif return_type in ["toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack"]:
            final_result.append([res['toxicity_analysis'][return_type] for res in item['result']])
        elif return_type == "all":
            final_result.append(item['result'])
        else:
            raise ValueError(f"Invalid return_type: {return_type}")
    
    return final_result

# Register the UDF
def register_get_mask_async_result(session: Session):
    session.udf.register(
        func=get_mask_async_result,
        name="protecto_async_mask_result",
        return_type="ARRAY",
        is_permanent=True,
        stage_location="@my_stage/protecto_ai.zip",
        external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
        secrets=SECRETS
    )
    print("UDF 'protecto_async_mask_result' registered successfully.")
