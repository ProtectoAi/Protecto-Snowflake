# App Folder

This folder contains the necessary files and directories for your Snowflake Native App, including a Streamlit app for setting up the environment by updating the required authorization and role permissions.


## Files and Directories

| **File/Directory**      | **Description**                                                                                                         | **Link**                                                 |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| `/streamlit`            | Contains the Streamlit app for customers to set up the environment by updating required authorization and role permissions. | [streamlit](./streamlit)                                 |
| `manifest.yml`          | Defines properties required by the application package. Find more details at the Manifest Documentation.                | [manifest.yml](./manifest.yml)                           |
| `setup_script.sql`      | Contains SQL statements that are run when a consumer installs or upgrades a Snowflake Native App in their account.       | [setup_script.sql](./setup_script.sql)                   |
| `environment.yml`       | Specifies the environment dependencies required for the Streamlit app.                                                  | [environment.yml](./environment.yml)                     |


