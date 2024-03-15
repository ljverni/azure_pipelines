# Azure Data Pipeline

#### Overview
Data is extracted in batches from the News API using the Python requests library. The data collected from the News API is loaded into an Azure Blob container, and then moved to an Azure SQL landing table. ETL jobs are written using Python and DBT and scheduled in Cron.  

![resource_group](https://github.com/ljverni/azure_pipelines/blob/main/azure_resource_group.jpg)

### Resources/Infrastructure
All resources utilized are within the Microsoft Azure ecosystem.
 - Virtual Machine (Ubuntu 20.04).
 - SQL Server database.
 - Storage Account (Blob).
 - Key Vault.
 - Container Registry.
 - Container Instances.
 - Virtual Networks.
 - Network Security Groups.

### ELT Flow

 - **Extract**: Data Collected (JSON) from the API is moved to Landing Zone 1 (Azure blob containers), manipulation object name prefix to simulate filesystem.
 - **Load**: JSON files are collected from Blob and loaded into Landing Zone 2 (SQL Server target tables - "src" schema).
 - **Transform**: DBT models are used for transformation. Data is passed from landing tables to staging tables ("stg" schema), and finally to live tables ("prod" schema).

## Virtual Environments
Two main environments were created, one for main packages and a another one for DBT packages.

## Secrets
All secrets are managed by Azure Vault. Authentication to Azure resources from Dev VM is done via Managed Identity.

## Scheduler
Python and DBT jobs are run by bash scripts, scheduled in Crontab.

## CI/CD:
The CI step runs tests (PyTest) and lint checks. CD was initially condigured to push changes to Prod VM via GitHub Actions. This has been deprecated and replaced by an Azure DevOps pipeline that creates Docker images and pushes them to a Container Registry. 

## Next steps:
Orchestrate ETL via Kubernetes and Apache Airflow.
