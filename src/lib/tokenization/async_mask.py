from protecto_ai import ProtectoVault
import _snowflake

# Fetch the OAuth token from Snowflake secrets
def get_auth_token():
    return _snowflake.get_generic_secret_string('cred')

# Define the Snowpark UDF to perform asynchronous masking
def async_mask(mask_values: list, token_type: str = "None", format_type: str = "None") -> str:

    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(mask_values, list):
        raise ValueError("The 'mask_values' parameter must be a list.")
    
    try:
        if token_type == "None" and format_type == "None":
            payload = {"mask": [{"value": value} for value in mask_values]}
            tracking_data = vault.async_mask(payload)
        else:
            payload = {"mask": [{"value": value,"token_name": token_type, "format": format_type } for value in mask_values]}
            tracking_data = vault.async_mask(payload)
    except ConnectionError as e:
        raise RuntimeError(f"Connection error occurred: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

    if not isinstance(tracking_data, dict) or 'data' not in tracking_data:
        raise RuntimeError(f"Unexpected response format: {tracking_data}")
    
    tracking_id = tracking_data["data"][0]["tracking_id"]
    return tracking_id


