-- Register the `mask` function as a UDF
CREATE OR REPLACE FUNCTION protecto_mask(mask_values ARRAY, token_type STRING DEFAULT 'Text Token', format_type STRING DEFAULT 'Person Name', return_type STRING DEFAULT 'token_value')
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch')
IMPORTS = ('@my_stage/protecto_ai.zip')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_access_integration)
HANDLER = 'mask'
AS $$
from protecto_ai import ProtectoVault
from requests.exceptions import ConnectionError

auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZXIiOiJQcm90ZWN0byIsImV4cGlyYXRpb25fZGF0ZSI6IjIwMjktMDctMDQiLCJwZXJtaXNzaW9ucyI6WyJtYXNrIiwidW5tYXNrIl0sInVzZXJfbmFtZSI6Im1haWwydml2ZWtzc0BnbWFpbC5jb20iLCJkYl9uYW1lIjoicHJvdGVjdG9fZ21haWxfZnZqcGd4a2kiLCJoYXNoZWRfcGFzc3dvcmQiOiIyMmQ2YmNiMDdiOTAxMjNjMGVjNGZiMDk0OGU4NmNiNTY5ZmI0N2MxMTViMWRkMjE1ODA5Y2Q2MjhmZTc1M2RlIn0.70C6lmgPm3507UHt_fQ6tjoNKAj_6FsI5pElX_oSZTE"
vault = ProtectoVault(auth_token)

def mask(mask_values, token_type="Text Token", format_type="Person Name", return_type="token_value"):
    if not isinstance(mask_values, list):
        raise ValueError("The 'mask_values' parameter must be a list.")
    try:
        result = vault.mask(mask_values, token_type, format_type)
    except ConnectionError as e:
        raise RuntimeError(f"Connection error occurred: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")
    
    # Ensure result is a dictionary and contains 'data' key
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
$$;


-- Register the `async_mask` function as a UDF
CREATE OR REPLACE FUNCTION protecto_async_mask(mask_values ARRAY, token_type STRING DEFAULT 'Text Token', format_type STRING DEFAULT 'Person Name')
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch')
IMPORTS = ('@my_stage/protecto_ai.zip')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_access_integration)
HANDLER = 'async_mask'
AS $$
from protecto_ai import ProtectoVault

auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZXIiOiJQcm90ZWN0byIsImV4cGlyYXRpb25fZGF0ZSI6IjIwMjktMDctMDQiLCJwZXJtaXNzaW9ucyI6WyJtYXNrIiwidW5tYXNrIl0sInVzZXJfbmFtZSI6Im1haWwydml2ZWtzc0BnbWFpbC5jb20iLCJkYl9uYW1lIjoicHJvdGVjdG9fZ21haWxfZnZqcGd4a2kiLCJoYXNoZWRfcGFzc3dvcmQiOiIyMmQ2YmNiMDdiOTAxMjNjMGVjNGZiMDk0OGU4NmNiNTY5ZmI0N2MxMTViMWRkMjE1ODA5Y2Q2MjhmZTc1M2RlIn0.70C6lmgPm3507UHt_fQ6tjoNKAj_6FsI5pElX_oSZTE"
vault = ProtectoVault(auth_token)

def async_mask(mask_values, token_type="Text Token", format_type="Person Name",):
    if not isinstance(mask_values, list):
        raise ValueError("The 'mask_values' parameter must be a list.")
    
    payload = {"mask": [{"value": value} for value in mask_values]}
    tracking_data = vault.async_mask(payload)
    tracking_id = tracking_data["data"][0]["tracking_id"]
    return tracking_id

$$;



-- Register the `check_mask_async_status` function as a UDF
CREATE OR REPLACE FUNCTION protecto_async_check_status(tracking_id STRING)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch')
IMPORTS = ('@my_stage/protecto_ai.zip')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_access_integration)
HANDLER = 'check_mask_async_status'
AS $$
from protecto_ai import ProtectoVault

auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZXIiOiJQcm90ZWN0byIsImV4cGlyYXRpb25fZGF0ZSI6IjIwMjktMDctMDQiLCJwZXJtaXNzaW9ucyI6WyJtYXNrIiwidW5tYXNrIl0sInVzZXJfbmFtZSI6Im1haWwydml2ZWtzc0BnbWFpbC5jb20iLCJkYl9uYW1lIjoicHJvdGVjdG9fZ21haWxfZnZqcGd4a2kiLCJoYXNoZWRfcGFzc3dvcmQiOiIyMmQ2YmNiMDdiOTAxMjNjMGVjNGZiMDk0OGU4NmNiNTY5ZmI0N2MxMTViMWRkMjE1ODA5Y2Q2MjhmZTc1M2RlIn0.70C6lmgPm3507UHt_fQ6tjoNKAj_6FsI5pElX_oSZTE"
vault = ProtectoVault(auth_token)

def check_mask_async_status(tracking_id):
    if not isinstance(tracking_id, str):
        raise ValueError("The 'tracking_ids' parameter must be a string.")
    status_data = vault.async_status([tracking_id])
    status = status_data["data"][0]["status"]
    return status
$$;



-- Register the `get_mask_async_result` function as a UDF
CREATE OR REPLACE FUNCTION protecto_async_mask_result(tracking_id STRING, return_type STRING DEFAULT 'token_value')
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('requests','multipledispatch')
IMPORTS = ('@my_stage/protecto_ai.zip')
EXTERNAL_ACCESS_INTEGRATIONS = (protecto_access_integration)
HANDLER = 'get_mask_async_result'
AS $$
from protecto_ai import ProtectoVault

auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZXIiOiJQcm90ZWN0byIsImV4cGlyYXRpb25fZGF0ZSI6IjIwMjktMDctMDQiLCJwZXJtaXNzaW9ucyI6WyJtYXNrIiwidW5tYXNrIl0sInVzZXJfbmFtZSI6Im1haWwydml2ZWtzc0BnbWFpbC5jb20iLCJkYl9uYW1lIjoicHJvdGVjdG9fZ21haWxfZnZqcGd4a2kiLCJoYXNoZWRfcGFzc3dvcmQiOiIyMmQ2YmNiMDdiOTAxMjNjMGVjNGZiMDk0OGU4NmNiNTY5ZmI0N2MxMTViMWRkMjE1ODA5Y2Q2MjhmZTc1M2RlIn0.70C6lmgPm3507UHt_fQ6tjoNKAj_6FsI5pElX_oSZTE"
vault = ProtectoVault(auth_token)

def get_mask_async_result(tracking_id, return_type="token_value"):
    if not isinstance(tracking_id, str):
        raise ValueError("The 'tracking_ids' parameter must be a list.")
    
    result = vault.async_status([tracking_ids])
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
$$;
