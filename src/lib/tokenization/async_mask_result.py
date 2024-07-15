from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.types import StringType,ArrayType
import _snowflake

session = get_active_session()

## Should be moved To config file
SECRETS = {'cred': 'protecto_secret'}
PACKAGES = ['requests', 'multipledispatch']
EXTERNAL_ACCESS_INTEGRATIONS = ('protecto_access_integration',)
IMPORTS = ['@my_stage/protecto_ai.zip']

# Fetch the OAuth token from Snowflake secrets
def get_auth_token():
    return _snowflake.get_generic_secret_string('cred')

# Define the Snowpark UDF to get the result of an asynchronous mask operation
def get_mask_async_result(tracking_id: str, return_type: str = "token_value") -> list:
    from protecto_ai import ProtectoVault
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
def register_get_mask_async_result(session: session):
    session.udf.register(
        func=get_mask_async_result,
        name="protecto_async_mask_result",
        return_type=ArrayType(),
        input_types = [StringType(),StringType()],
        is_permanent=True,
        replace = True,
        stage_location="@demos.public.MY_STAGE",
        external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
        secrets=SECRETS,
        packages=PACKAGES,
        imports=IMPORTS
    )
    print("UDF 'protecto_async_mask_result' registered successfully.")
