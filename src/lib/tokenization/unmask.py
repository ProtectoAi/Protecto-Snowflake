from protecto_ai import ProtectoVault
import _snowflake

# Fetch the OAuth token from Snowflake secrets
def get_auth_token():
    return _snowflake.get_generic_secret_string('cred')

# Define the Snowpark UDF to mask data
def unmask(unmask_values: list) -> list:

    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(unmask_values, list):
        raise ValueError("The 'unmask_values' parameter must be a list.")
    
    try:
        result = vault.unmask(unmask_values)
    except ConnectionError as e:
        raise RuntimeError(f"Connection error occurred: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")
    
    if isinstance(result, dict) and 'data' in result:
        return [item['value'] for item in result['data']]
    else:
        raise RuntimeError(f"Unexpected response format: {result}")

