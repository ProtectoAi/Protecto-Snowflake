
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
def auto_detect(mask_values: list, return_type: str = "token_value") -> list:
    from protecto_ai import ProtectoVault
    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(mask_values, list):
        raise ValueError("The 'mask_values' parameter must be a list.")
    
    try:
        result = vault.mask(mask_values)
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
        return result['data']
    else:
        raise ValueError(f"Invalid return_type: {return_type}")


# Register the UDF
def register_auto_detect(session):
    session.udf.register(
        func=auto_detect,
        name="protecto_auto_detect",
        return_type=ArrayType(),
        input_types = [ArrayType(),StringType()],
        is_permanent=True,
        replace = True,
        stage_location=STAGE_LOCATION,
        external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
        secrets=SECRETS,
        packages=PACKAGES,
        imports=IMPORTS
    )
    print("UDF 'protecto_auto_detect' registered successfully.")

register_auto_detect(session)

