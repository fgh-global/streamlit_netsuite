# Fivetran Netsuite Streamlit App
## 📣 Overview

The [Fivetran Netsuite Streamlit app](https://fivetran-netsuite.streamlit.app/) leverages data from the Fivetran Netsuite connector and Fivetran Netsuite data model to produce analytics ready reports. You may find the analytics ready reports within the pages of this Streamlit app (these may be found on the left pane). These dashboards have been constructed using a combination of the [netsuite2__balance_sheet](https://fivetran.github.io/dbt_netsuite/#!/model/model.netsuite2.netsuite2__balance_sheet) and [netsuite2__income_statement](https://fivetran.github.io/dbt_netsuite/#!/model/model.netsuite2.netsuite2__income_statement) models from the Fivetran [Netsuite dbt package](https://github.com/fivetran/dbt_netsuite). These dashboards provide an example of how you may analyze your Netsuite data.

By default this Streamlit app uses sample Dunder Mifflin Netsuite tickets data to generate the dashboards. This sample data is a replica of the `netsuite2__balance_sheet` and `netsuite2__income_statement` data model outputs. If you would like to leverage this app with your own data, you may follow the instructions within the below Installation and Deployment section.

## 📈 Provided reports

| **Page** | **Description** |
|----------|-----------------|
| [Financial Executive Dashboard](https://fivetran-netsuite.streamlit.app/financial_executive_dashboard) | This report is intended to serve as the executive dashboard for your company's financial well being. Based on the date range applied you will be able to view your company's high level balances, ratios, and revenue/expense breakdowns. Use this dashboard to keep track of your financial health and how you are trending. |
| [Balance Sheet Report](https://fivetran-netsuite.streamlit.app/balance_sheet_report) | This is a replica of your balance sheets for the date range applied. Inspect your assets, liabilities, and equity balances for the specified periods. This dashboard is intended to recreate the balance sheet report from Netsuite. | 
| [Income Statement Report](https://fivetran-netsuite.streamlit.app/profit_and_loss_report) | This is a replica of your cumulative income statement for the date range applied. Inspect your revenue and expenses for the specified periods. This dashboard is intended to recreate the income statement report from Netsuite. | 

# 🎯 How do I use this Streamlit app?
As previously mentioned this Streamlit App is publicly deployed using sample Dunder Mifflin Zendesk ticket data. This is to show an example of the types of analysis that may be performed with modeled Netsuite data synced and transformed with Fivetran. However, this Streamlit App has been designed to be also be forked and customize to leverage other data sources. If you wish to leverage this Streamlit App with your own modeled Netsuite data, you may follow the below steps.

## Deployment with GitHub Actions
This repository includes a GitHub Actions workflow that automatically builds and deploys the Streamlit app as a Docker container to Google Cloud Platform's Artifact Registry. To use this workflow:

1. Fork this repository to your GitHub account
2. Set up the following secrets in your GitHub repository:
   - `GCP_PROJECT_ID`: Your Google Cloud Platform project ID
   - `GCP_SA_KEY`: The JSON key of a service account with permissions to push to Artifact Registry

The workflow will trigger automatically when you push to the main branch, or you can manually trigger it from the Actions tab in your GitHub repository.

## Step 1: Prerequisites
To use this Streamlit app, you must have the following:

- At least one Fivetran Netsuite connector syncing data into your destination.
- A **BigQuery** or **Snowflake** destination.

## Step 2: Data models
You will need to have ran the [Fivetran dbt_netsuite data model](https://github.com/fivetran/dbt_netsuite) to transform your raw Zendesk data into analytics ready tables. Please refer to the data model documentation for instructions on how to run the data models. If you would like to have Fivetran run these data models for you, you may also leverage the [Fivetran Netsuite Quickstart Data Model](https://fivetran.com/docs/transformations/quickstart) for an easier and more streamlined experience.

## Step 3: Fork this repository
To leverage this Streamlit App with your own data, you will need to fork this repo. To learn more about forking repos you may refer to the [GitHub docs](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

## Step 4: Run your forked Streamlit app
Once you have forked the repo, you will need to clone the repo locally to run it and make any minor adjustments. To do this you will perform the following:
- Start a virtual environment and install the requirements. You can use the following commands to create a venv and setup the environment with the appropriate dependencies:
```zsh
python3 -m pip install --user virtualenv && 
python3 -m venv env && 
source env/bin/activate && 
python3 -m pip install --upgrade pip && 
pip3 install -r requirements.txt
```
- If using BigQuery: Obtain/Create a BigQuery Service account with `BigQuery Data Editor` and `BigQuery User` permissions and access to the zendesk__ticket_metrics table.
- If using Snowflake: Obtain/Create an account with access permissions to the zendesk__ticket_metrics model generated by the table.
- Store the credential for your account in a `secrets.toml` file stored within the `.streamlit/` folder.
- Run `streamlit run netsuite.py` in your terminal to deploy the app on your local host.
- Change the Destination variable in the app to be either BigQuery or Snowflake
- Modify the Database and Schema variables in the app to be your designated database.schema where the zendesk__ticket_metrics table resides.
