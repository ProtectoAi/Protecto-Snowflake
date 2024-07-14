# src/udfs/protecto_udfs.py

from snowflake.snowpark import Session
from protecto_ai import ProtectoVault
from requests.exceptions import ConnectionError
import _snowflake

# Define the external access integration for the UDFs
EXTERNAL_ACCESS_INTEGRATIONS = ('protecto_access_integration',)

# Define the secrets used for authentication
SECRETS = {
    'cred': 'protecto_oauth_token'
}

# Fetch the OAuth token from Snowflake secrets
auth_token = _snowflake.get_oauth_access_token('cred')
vault = ProtectoVault(auth_token)

# Define the Snowflake session
session = Session.builder.configs({
    'account': '<your_account>',
    'user': '<your_user>',
    'password': '<your_password>',
    'role': '<your_role>',
    'warehouse': '<your_warehouse>',
    'database': '<your_database>',
    'schema': '<your_schema>',
}).create()

# Define and register the UDFs

# Snowpark UDF to mask data
def mask(mask_values: list, token_type: str = "Text Token", format_type: str = "Person Name", return_type: str = "token_value") -> list:
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
session.udf.register(
    func=mask,
    name="protecto_mask",
    return_type="ARRAY",
    is_permanent=True,
    stage_location="@my_stage/protecto_ai.zip",
    external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
    secrets=SECRETS
)

# Snowpark UDF to perform asynchronous masking
def async_mask(mask_values: list, token_type: str = "Text Token", format_type: str = "Person Name") -> str:
    if not isinstance(mask_values, list):
        raise ValueError("The 'mask_values' parameter must be a list.")
    
    payload = {"mask": [{"value": value} for value in mask_values]}
    tracking_data = vault.async_mask(payload)
    tracking_id = tracking_data["data"][0]["tracking_id"]
    return tracking_id

# Register the UDF
session.udf.register(
    func=async_mask,
    name="protecto_async_mask",
    return_type="STRING",
    is_permanent=True,
    stage_location="@my_stage/protecto_ai.zip",
    external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
    secrets=SECRETS
)

# Snowpark UDF to check the status of an asynchronous mask operation
def check_mask_async_status(tracking_id: str) -> str:
    if not isinstance(tracking_id, str):
        raise ValueError("The 'tracking_id' parameter must be a string.")
    
    status_data = vault.async_status([tracking_id])
    status = status_data["data"][0]["status"]
    return status

# Register the UDF
session.udf.register(
    func=check_mask_async_status,
    name="protecto_async_check_status",
    return_type="STRING",
    is_permanent=True,
    stage_location="@my_stage/protecto_ai.zip",
    external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
    secrets=SECRETS
)

# Snowpark UDF to get the result of an asynchronous mask operation
def get_mask_async_result(tracking_id: str, return_type: str = "token_value") -> list:
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
session.udf.register(
    func=get_mask_async_result,
    name="protecto_async_mask_result",
    return_type="ARRAY",
    is_permanent=True,
    stage_location="@my_stage/protecto_ai.zip",
    external_access_integrations=EXTERNAL_ACCESS_INTEGRATIONS,
    secrets=SECRETS
)
