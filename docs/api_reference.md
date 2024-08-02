# Protecto Vault UDF Functions

## Overview
This document provides detailed information about the UDF functions created in the Protecto Vault for masking and unmasking data.

## 1. Tokenization

### 1. protecto_mask
- **Purpose**: Masks the provided data values.
- **Parameters**:
  - `mask_values` (ARRAY): The data values to be masked.
  - `token_type` (STRING, default 'None'): The type of tokenization to use. When it is "None" the token type is automatically applied.[Reference for Token Type](https://developer.protecto.ai/docs/supported-phi/)
  - `format_type` (STRING, default 'None'): The format of the tokenization. When it is "None" the format type is automatically detected.[Reference for Format Type](https://developer.protecto.ai/docs/supported-phi/)
  - `return_type` (STRING, default 'token_value'): The type of value to return. Possible return types are "raw_json", "toxicity_analysis", and each toxicity type as an individual return type: "toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack".
- **Returns**: An array of masked values.
- **Usage**:
  ```sql
  SELECT protecto_vault.vault_schema.protecto_mask(ARRAY_CONSTRUCT('value_1','value_1 Reagon'),'token_type','format_type','return_type') AS masked_value;
```

### 2. protecto_unmask
- **Purpose**: Unmasks the provided masked token.
- **Parameters**:
  - `mask_values` (ARRAY): The data values to be unmasked.
- **Returns**: An array of unmasked values.
- **Usage**:
  ```sql
  SELECT protecto_vault.vault_schema.protecto_unmask(ARRAY_CONSTRUCT('masked_value_1','masked_value_')) AS unmasked_values;
```

### 3.protecto_async_mask
- **Purpose**: Asynchronously masks the provided data values.
- **Parameters**:
  - `mask_values` (ARRAY): The data values to be masked.
  - `token_type` (STRING, default 'None'): The type of tokenization to use. When it is "None" the token type is automatically applied.[Reference for Token Type](https://developer.protecto.ai/docs/supported-phi/)
  - `format_type` (STRING, default 'None'): The format of the tokenization. When it is "None" the format type is automatically detected.[Reference for Format Type](https://developer.protecto.ai/docs/supported-phi/)
- **Returns**: A string tracking ID.
- **Usage**:
  ```sql
  SELECT protecto_vault.vault_schema.protecto_async_mask(ARRAY_CONSTRUCT('value_1','value_1 Reagon'),'token_type','format_type') AS tracking_id;;
```

  

### 4. protecto_async_mask_result
- **Purpose**: Retrieves the result of an asynchronous mask operation.
- **Parameters**:
  - `tracking_id` (STRING): The tracking ID for the async operation.
  - `return_type` (STRING, default 'status'): The type of value to return. Possible return types are "raw_json", "token_value","toxicity_analysis", and each toxicity type as an individual return type: "toxicity", "severe_toxicity", "obscene", "threat", "insult", "identity_attack".
- **Returns**: An array of masked values.
- **Usage**:
  ```sql
  SELECT protecto_vault.vault_schema.protecto_async_mask_result('tracking_id','status') AS masked_result;
```



### 5. protecto_async_unmask
- **Purpose**: Asynchronously unmasks the provided data values.
- **Parameters**:
  - `mask_values` (ARRAY): The data values to be unmasked.
- **Returns**: A string tracking ID.
- **Usage**:
  ```sql
  SELECT protecto_vault.vault_schema.protecto_async_unmask((ARRAY_CONSTRUCT('masked_value_1','masked_value_2'))) AS tracking_id;
```
  
### 6. protecto_async_unmask_result
- **Purpose**: Retrieves the result of an asynchronous unmask operation.
- **Parameters**:
  - `tracking_id` (STRING): The tracking ID for the async operation.
  - `return_type` (STRING, default 'status'): The type of value to return. Other return type is "value" to get the unmasked values
- **Returns**: An array of unmasked values.
- **Usage**:
  ```sql
  SELECT protecto_vault.vault_schema.protecto_async_unmask_result('tracking_id','status') AS unmasked_result;
```

For more detailed code samples refer to  [Samples](https://github.com/viveksrinivasanss/Protecto-Snowflake/tree/main/samples)






