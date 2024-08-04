# Protecto Snowflake Native App Setup Guide

This document provides step-by-step instructions to set up the Protecto Snowflake Native App, including environment setup, permissions, and integration with Snowflake. 

## Introduction

The Protecto Snowflake Native App is designed to provide data protection and tokenization functionality within your Snowflake environment. This guide will help you set up the app and configure it for optimal use.

## Prerequisites

Before you begin, ensure you have the following:

1. **Snowflake Account with External Offering Terms Enabled**: Ensure that your Snowflake account has external offering terms enabled. For more information, refer to the [Snowflake UDF Python Packages Documentation](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-packages).
2. **ACCOUNTADMIN Access in Snowflake**: You need ACCOUNTADMIN privileges in Snowflake to set up and manage the Protecto UDFs and other associated objects.
3. **Snowflake Availability Region**: To utilize the functionality with Snowflake Cortex, your Snowflake account must be in one of the required availability regions. For details, see the [Snowflake Cortex Availability Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#availability).
4. **Protecto Auth Key**: Acquire your Protecto auth key by following the step-by-step guide available [PROTECTO API SIGNUP](https://developer.protecto.ai/docs/step-by-step-guide-to-obtain-your-auth-token).

## Installation Steps

### Step 1: Clone the Repository

Clone the repository containing the Protecto Snowflake Native App to your local machine.

```sh
git clone <repository-url>
cd <repository-directory>
```

### Step 2: Set Up the Environment
Ensure you have the necessary environment set up by using the environment.yml file provided.

```sh
conda env create -f environment.yml
conda activate protecto-env
```

### Step 3: Deploy the App in Snowflake
Run the setup script to deploy the app in your Snowflake account.

```
snow app run -x --account="<your_account_identifier>" --user="<your_username>" --password="<your_password>" --role="<your_role>" --warehouse="<your_warehouse>"

```

This `setup.md` provides a structured guide for setting up the Protecto Snowflake Native App, ensuring that all necessary steps are covered, including acquiring the Protecto auth key, configuring Snowflake, and running the Streamlit app.
