from protecto_ai import ProtectoVault
import _snowflake

# Fetch the OAuth token from Snowflake secrets
def get_auth_token():
    return _snowflake.get_generic_secret_string('cred')

# Define the Snowpark UDF to get the result of an asynchronous mask operation
def async_unmask_result(tracking_id: str, return_type: str = "status") -> list:

    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(tracking_id, str):
        raise ValueError("The 'tracking_id' parameter must be a string.")
    
    result = vault.async_status([tracking_id])
    
    for item in result['data']:
        if return_type == "status":
            final_result = [{"status": item["status"],"error":item["error_msg"]}]
        elif return_type == "value":
            final_result = [res['value'] for res in item['result']]
        else:
            raise ValueError(f"Invalid return_type: {return_type}")
    
    return final_result



