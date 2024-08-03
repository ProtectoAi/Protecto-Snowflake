## Introduction

Welcome to the Protecto Vault project, a comprehensive solution designed to provide robust data masking and unmasking functionalities within Snowflake. This project leverages the power of Protecto API to ensure sensitive data is securely masked and unmasked, adhering to the highest standards of data privacy and security.

The Protecto Vault offers a suite of UDFs that can be seamlessly integrated into your Snowflake environment, allowing for customized tokenization and detokenization processes tailored to your specific requirements.
Protecto Vault's core functionalities include a range of UDFs for masking and unmasking data, both synchronously and asynchronously. These functions are built using Python and are designed to handle various data formats and tokenization types. 

Additionally, the project features a Streamlit app that provides an interactive UI to set up and manage authorization and roles within Snowflake. For more information on supported languages, visit [Protecto Snowflake Markeplace]().

## Prerequisites

1. **Snowflake Account with External Offering Terms Enabled**: Ensure that your Snowflake account has external offering terms enabled. For more information, refer to the [Snowflake UDF Python Packages Documentation](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-packages).

2. **ACCOUNTADMIN Access in Snowflake**: You need ACCOUNTADMIN privileges in Snowflake to set up and manage the Protecto UDFs and other associated objects.

3. **Snowflake Availability Region**: To utilize the functionality with Snowflake Cortex, your Snowflake account must be in one of the required availability regions. For details, see the [Snowflake Cortex Availability Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#availability).


 
# Directory Structure
## `/app`
This directory holds your Snowflake Native App files.

### `/app/README.md`
Exposed to the account installing the application with details on what it does and how to use it.

### `/app/manifest.yml`
Defines properties required by the application package. Find more details at the [Manifest Documentation.](https://docs.snowflake.com/en/developer-guide/native-apps/creating-manifest)

### `/app/setup_script.sql`
Contains SQL statements that are run when a consumer installs or upgrades a Snowflake Native App in their account.

## `/scripts`
Contains `pre_deploy.sql` and `post_deploy.sql` which creates necessary objects and helper UDFS to utilize protecto's functionality

## `/src`
The src folder contains all the necessary Streamlit code and libraries for registering the Protecto UDFs (User-Defined Functions) in Snowflake.

## `/docs`
The docs folder contains the api_reference.md file, which provides detailed API references and documentation for the Protecto UDFs and related functionalities.

## `/samples`
The samples folder contains detailed code examples demonstrating how to utilize the Protecto UDFs effectively.

## `/data`
Contains sample datasets that can be loaded as Snowflake table and utilzied to run the sample files.

## `snowflake.yml`
Snowflake CLI uses the `snowflake.yml` file  to discover your project's code and interact with Snowflake using all relevant privileges and grants. 


## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES # OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS, PUBLISHERS OR COPYRIGHT HOLDERS BE # LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
