# Using Environment Variables with Streamlit Netsuite App

This app has been updated to support using environment variables for Snowflake connection settings when the `.streamlit/secrets.toml` file is not available.

## How It Works

1. The app first checks if `.streamlit/secrets.toml` exists
2. If it exists, the app uses the settings from that file (local development)
3. If it doesn't exist, the app uses environment variables (deployed environment)

## Required Environment Variables

When deploying the app without a secrets.toml file, you need to set the following environment variables:

```
SNOWFLAKE_ACCOUNT=your-account-id
SNOWFLAKE_USER=your-username
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_ROLE=your-role
SNOWFLAKE_WAREHOUSE=your-warehouse
SNOWFLAKE_DATABASE=your-database
SNOWFLAKE_SCHEMA=your-schema
SNOWFLAKE_CLIENT_SESSION_KEEP_ALIVE=true

# Authentication
STREAMLIT_AUTH_PASSWORD=your-password
```
## Setting Environment Variables in Cloud Environments

Most cloud platforms provide ways to set environment variables for your application:

- **GCP Cloud Run**: Set environment variables in the Cloud Run service configuration
- **AWS ECS**: Set environment variables in the task definition
- **Heroku**: Set environment variables using the Heroku CLI or dashboard
- **Azure App Service**: Set environment variables in the application settings

## Testing Locally

To test your app locally with environment variables:

1. Temporarily rename or remove your `.streamlit/secrets.toml` file
2. Set the environment variables in your terminal:

```bash
export SNOWFLAKE_ACCOUNT=your-account-id
export SNOWFLAKE_USER=your-username
export SNOWFLAKE_PASSWORD=your-password
export SNOWFLAKE_ROLE=your-role
export SNOWFLAKE_WAREHOUSE=your-warehouse
export SNOWFLAKE_DATABASE=your-database
export SNOWFLAKE_SCHEMA=your-schema
export SNOWFLAKE_CLIENT_SESSION_KEEP_ALIVE=true
export STREAMLIT_AUTH_PASSWORD=your-password
```

3. Run your Streamlit app:

```bash
streamlit run netsuite.py
