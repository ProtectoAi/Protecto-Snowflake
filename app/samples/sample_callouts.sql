
-- Example table and data
CREATE OR REPLACE TABLE example_table (id INT, value STRING);
INSERT INTO example_table (id, value) VALUES
    (1, 'George Washington is happy'),
    (2, 'Mark lives in the U.S.A'),
    (3, 'Alice works at ACME Inc.');

-- Call To 
SELECT 
    id,
    processed_value.value::STRING AS masked_value
FROM example_table,
    LATERAL FLATTEN(INPUT => mask_sensitive_info(ARRAY_AGG(value), 'Text Token', 'Person Name', 'token_value')) AS processed_value;

-- Call the vectorized UDF with the entire column
SELECT 
    id,
    async_mask_sensitive_info(ARRAY_AGG(value)) AS tracking_id
FROM example_table;