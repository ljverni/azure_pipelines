#!/bin/bash

if [ -d "venv" ]; then
    export DW_USER_PROD=`venv/main/bin/python3 src/utilities/azure_vault.py CaratacoDwUid`
    export DW_PASSWORD_PROD=`venv/main/bin/python3 src/utilities/azure_vault.py CaratacoDwPwd`
    source venv/dbt/bin/activate
    cd src/dbt_transform && dbt run
else
    cd dbt_transform && dbt run
fi
