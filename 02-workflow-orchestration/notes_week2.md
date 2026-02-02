## Workflow Orchestration


```
cd /mnt/c/Users/Carlos/Desktop/projects/data-engineering-zoomcamp-2026/02-workflow-orchestration
```

```
cd /data-engineering-zoomcamp-2026/02-workflow-orchestration

```

### Workflow orchestration

Orchestrator ties multiple tools together, provies also logging info, Complex Orchetration Logic to run things in parallel, workflows can be run automatically 

* module goal: build ETL pipeline

### Kestra 
open source, infinitely scalabel orchestration platform. 
worksflow can be build as code, no-code, ai with a humongous plug in library and language agnostisc, with full visibility, scheduled and event-driven trigger 

#### Kestra Concepts

* `id` and `namespace` identify the flow, cannot be change

* `task` can be change. also have `id` and `type`, each `task` has defined properties. Robust documentation

* `input` the ideal way to pass data to the workflow at the start of an execution. `type` defines the type of input jiji

* `variable` similar to an input, but withe the nature of being key:value pairs to define things that you will use multiple times in a workflow, vars.<variable_name> really useful trick. `render` renders the value of the variable an avoids returning strings literal with the name of the variable.

Note: inputs are variable are great ways of defining data before the workflow starts or as It is about to starts

`pluginDefaults` similar tu variables, define customization troughout a same type of task

`trigger` similar to task, initiates the workflow

`concurrency` limit the times a workflow multiple times at the same time

#### Orchestrate python code in Kestra

`commands task` allows kestra to execute external files(.py files?) we can upload them as namespace files. 

Note: kestra starts a docker container to run the python code


#### Load Data into Postgres


#### Loggin into the postgres service 
servers -> register -> server 

name: db
host name/address: pgdatabase
port: 5432
maintenance database:ny_taxi
Username: root
Password: Root

04_postgres_taxi.yaml is a manual-triggered workflow
05_postgres_taxi_scheduled.yaml to create a scheduled workflow, automated execution also with backfills

echo "SECRET_GCP_SERVICE_ACCOUNT=$(cat cred.json | base64 -w 0)" >> .env_encoded