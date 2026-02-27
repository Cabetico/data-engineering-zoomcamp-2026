# 5.6 - My Own Notes

## ASSETS

```
"""@bruin
 DEFINITIONS

@bruin""" 

CONTEXT
```

* Definitions = Configurations
* Context = Code
* Yaml could be use as seeds

## PIPELINE 

* CONTAINS CONNECTIONS A CONFIGURATIONS

## VARIABLES

* built-in (initialized and provided in every new pipeline run)
    * variables are injected via jinja(like dbt) in sql
    * python inject variables through env variables

* custom 
    * they are set a pipeline level
    * General
        * environment, start date, end date 
        * full-Refresh (creates thje table again the opose to insert only)
        * Imterval-Modifiers, Exclusive-EndDate, Push-Metada

## COMMANDS
```
 bruin run <pipeline_name/pipeline.yaml>
```

```
 bruin validate 
```
* circulars dependency?

### `.py` example

How it works
A few key things to notice:
The `"""@bruin ... @bruin"""`  block at the top is Bruin's way of embedding asset config inside a `.py` file. Everything outside it is just regular Python.
The `materialize()` function is the magic — when Bruin runs a Python asset, it looks for this function and expects it to return a `pandas.DataFrame`. Bruin then uses ingestr under the hood to load that DataFrame into the destination (DuckDB in this case).
`strategy: append` means each run adds new rows rather than replacing the table — ideal for time-series data like taxi trips where you'd change the URL month by month or parameterize it.
`requirements.txt` is picked up automatically by Bruin — it searches up the directory tree from the asset file to find the nearest one and creates an isolated virtual environment for it.