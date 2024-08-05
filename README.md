## Introduction

Welcome to the Protecto Library for Snowflake, a comprehensive solution designed to provide robust data masking and unmasking functionalities within Snowflake. This project leverages the power of Protecto API to ensure sensitive data is securely masked and unmasked, adhering to the highest standards of data privacy and security within Snowflake.

This Library, built on top of Snowpark for Python can be seamlessly integrated into your Snowflake environment Additionally, a Streamlit Native app that can be installed from the Snowflake Marketplace.

## Tokenization:

Tokenization library allows for customized tokenization and detokenization processes tailored to your specific requirements to mask and unmask data, both synchronously and asynchronously.

## Prerequisites

1. **Snowflake Account with External Offering Terms Enabled**: Ensure that your Snowflake account has external offering terms enabled. For more information, refer to the [Snowflake UDF Python Packages Documentation](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-packages).

2. **ACCOUNT ADMIN Previliges in Snowflake**: You need `ACCOUNTADMIN` privileges in Snowflake to set up and manage the Protecto UDFs and other associated objects.

3. **Snowflake Availability Region**: To utilize the functionality with Snowflake Cortex, your Snowflake account must be in one of the required availability regions. For details, see the [Snowflake Cortex Availability Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#availability).

4. **Protecto Auth Key**: Acquire your Protecto auth key by following the step-by-step guide available here. [Protecto Auth Key](https://developer.protecto.ai/docs/step-by-step-guide-to-obtain-your-auth-token/)


 
# Directory Structure

# Directory Structure

| **Objects**                     | **Description**                                                                                           |
|---------------------------------|-----------------------------------------------------------------------------------------------------------|
| [**`/app`**](./app)             | Holds Snowflake Native App and Streamlit files.                                                           |
| [**`/scripts`**](./scripts)     | Contains `pre_deploy.sql` and `post_deploy.sql` for creating objects and helper UDFs.                     |
| [**`/src`**](./src)             | Contains all library files for registering the Protecto UDFs.                                             |
| [**`/docs`**](./docs)           | Contains the API reference documentation for Protecto UDFs and related functionalities.                    |
| [**`/samples`**](./samples)     | Contains code examples demonstrating how to utilize the Protecto UDFs effectively.                        |
| [**`/data`**](./data)           | Contains sample datasets that can be loaded into Snowflake and used to run sample files.                  |
| [**`snowflake.yml`**](./snowflake.yml) | Used by Snowflake CLI to discover your project's code and interact with Snowflake.                        |







## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES # OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS, PUBLISHERS OR COPYRIGHT HOLDERS BE # LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
