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
    return Session.builder.configs({
        'account': '<your_account>',
        'user': '<your_user>',
        'password': '<your_password>',
        'role': '<your_role>',
        'warehouse': '<your_warehouse>',
        'database': '<your_database>',
        'schema': '<your_schema>',
    }).create()

# Define the Snowpark UDF to mask data
def mask(mask_values: list, token_type: str = "Text Token", format_type: str = "Person Name", return_type: str = "token_value") -> list:
    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(mask_values, list):
        raise ValueError("The 'mask_values' parameter must be a list.")
    
    try:
        result = vault.mask(mask_values, token_type, format_type)
    except ConnectionError as e:
        raise RuntimeError(f"Connection error occurred: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")
    
    if not isinstance(result, dict) or 'data' not in result:
        raise RuntimeError(f"Unexpected response format: {result}")

    if return_type == "token_value":
        return [item['token_value'] for item in result['data']]
    elif return_type == "toxicity_analysis":
        return [item['toxicity_analysis'] for item in result['data']]
    elif return_type in ["toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack"]:
        return [item['toxicity_analysis'].get(return_type, None) for item in result['data']]
    elif return_type == "all":
        return result
    else:
        raise ValueError(f"Invalid return_type: {return_type}")


# Register the UDF
def register_mask(session: Session):
    session.udf.register(
        func=mask,
        name="protecto_mask",
        return_type="ARRAY",
        is_permanent=True,
        stage_location="@my_stage/protecto_ai.zip",
        external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
        secrets=SECRETS
    )
    print("UDF 'protecto_mask' registered successfully.")
