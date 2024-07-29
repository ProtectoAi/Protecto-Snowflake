
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.types import StringType,ArrayType
import _snowflake

# session = get_active_session()

# ## Should be moved To config file
# SECRETS = {'cred': 'protecto_secret'}
# PACKAGES = ['requests', 'multipledispatch']
# EXTERNAL_ACCESS_INTEGRATIONS = ('protecto_access_integration',)
# IMPORTS = ['@my_stage/protecto_ai.zip']
# STAGE_LOCATION = "@protecto_snowflake.my_schema.my_stage"

# Fetch the OAuth token from Snowflake secrets
# def get_auth_token():
#     return _snowflake.get_generic_secret_string('cred')

# Define the Snowpark UDF to mask data
def mask(mask_values: list,token_type: str = "None", format_type: str = "None", return_type: str = "token_value") -> list:
    from protecto_ai import ProtectoVault
    auth_token =  _snowflake.get_generic_secret_string('cred')
    vault = ProtectoVault(auth_token)

    if not isinstance(mask_values, list):
        raise ValueError("The 'mask_values' parameter must be a list.")
    
    try:
        if token_type == "None" and format_type == "None":
            result = vault.mask(mask_values)
        else:
            result = vault.mask(mask_values,token_type,format_type)
    except ConnectionError as e:
        raise RuntimeError(f"Connection error occurred: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")
    
    if not isinstance(result, dict) or 'data' not in result:
        raise RuntimeError(f"Unexpected response format: {result}")

    if return_type == "token_value":
        token_value_dict = {item['value']: item['token_value'] for item in result['data']}
        return [token_value_dict[mask_value] for mask_value in mask_values]
    elif return_type == "raw":
        return result['data']
    elif return_type == "toxicity_analysis":
        toxicity_value_dict = {item['value']: item['toxicity_analysis'] for item in result['data'] if 'toxicity_analysis' in item }
        return [toxicity_value_dict[mask_value] for mask_value in mask_values if toxicity_value_dict]
    elif return_type in ["toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack"]:
        toxicity_value_dict = {item['value']: item['toxicity_analysis'][return_type]  for item in result['data'] if 'toxicity_analysis' in item }    
        return [toxicity_value_dict[mask_value] for mask_value in mask_values if toxicity_value_dict]
    else:
        raise ValueError(f"Invalid return_type: {return_type}")



# Register the UDF
# def register_protecto_mask(session):
#     session.udf.register(
#         func=mask,
#         name="protecto_mask",
#         return_type=ArrayType(),
#         input_types = [ArrayType(),StringType(),StringType(),StringType()],
#         is_permanent=True,
#         replace = True,
#         stage_location=STAGE_LOCATION,
#         external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
#         secrets=SECRETS,
#         packages=PACKAGES,
#         imports=IMPORTS
#     )
#     print("UDF 'protecto_mask' registered successfully.")


