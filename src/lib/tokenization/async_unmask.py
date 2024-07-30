from protecto_ai import ProtectoVault
import _snowflake

# Fetch the OAuth token from Snowflake secrets
def get_auth_token():
    return _snowflake.get_generic_secret_string('cred')

# Define the Snowpark UDF to mask data
def async_unmask(unmask_values: list) -> str:

    auth_token = get_auth_token()
    vault = ProtectoVault(auth_token)

    if not isinstance(unmask_values, list):
        raise ValueError("The 'unmask_values' parameter must be a list.")
    
    try:
        tracking_data = vault.async_unmask(unmask_values)
        if isinstance(tracking_data, dict) and 'data' in tracking_data:
            tracking_details = [{"tracking_id":tracking_data["data"][0]["tracking_id"],"success":tracking_data["success"],"error":tracking_data["error"]}]
            return tracking_details
    except ConnectionError as e:
        raise RuntimeError(f"Connection error occurred: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

    else:
        raise RuntimeError(f"Unexpected response format: {result}")


