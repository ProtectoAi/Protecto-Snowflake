# Sample Data

This folder contains sample datasets that can be loaded into Snowflake tables and utilized to run the sample files. These datasets are crucial for demonstrating the functionality of Protecto UDFs and other related features. Below is a table describing each dataset, along with its source.

## Datasets

| **Dataset**           | **Description**                                                                 | **Source**                                  |
|-----------------------|---------------------------------------------------------------------------------|---------------------------------------------|
| `PII_DATA.csv`  | This is an LLM-generated external dataset for the.The Learning Agency Lab - PII Data Detection Competition    | [Kaggle](https://www.kaggle.com/datasets/alejopaullier/pii-external-dataset)           |


## Usage


To load `PII_DATA.csv` into a Snowflake table, you can use the following SQL command or you can use the tokenization_sync.ipynb notebook in the samples folder to load.

### Example

```sql
COPY INTO PII_DATA
FROM @protecto.vault.app_stage/PII_DATA.csv
FILE_FORMAT = (TYPE = 'CSV', FIELD_OPTIONALLY_ENCLOSED_BY='"');
