# NOTES

### ABOUT FORK'D REPO

No, a forked repository on GitHub does not automatically update when the original (upstream) repository is updated. You need to manually sync it.
How to update your fork:
Option 1: Using GitHub's web interface (easiest)

Go to your forked repository on GitHub
Click the "Sync fork" button (if available)
Click "Update branch"

Option 2: Using Git commands (more control)
First time setup - add the original repo as a remote:

```bash
    git remote add upstream https://github.com/ORIGINAL_OWNER/REPO_NAME.git
    git remote -v  # verify it was added
```

Then, whenever you want to sync:

# Fetch the latest changes from the original repo
```bash
    git fetch upstream
```

# Make sure you're on your main branch
```bash
    git checkout main  # or master, depending on branch name
```
# Merge the changes from upstream
```bash
    git merge upstream/main
```
# Push the updates to your fork on GitHub
```bash
    git push origin main
```

Alternative - rebase instead of merge:

```bash
    git fetch upstream
    git checkout main
    git rebase upstream/main
    git push origin main --force-with-lease 
```

Key points:

* Your fork is a snapshot at the time you created it
* The connection is one-way: original → fork (not automatic)
* You control when and how to pull updates
* The original repo owner cannot push to your fork (you maintain control)

This design gives you independence to make changes without interference, while still allowing you to pull in updates when you want them.

### About terminal

```bash
    PS1="> "
```

```
    echo 'PS1="> "' > ~/.bashrc
```

### DOCKER

Quick command that remove all the containers/clears env
```bash
    docker rm `docker ps -aq`
```

How to preserve state in docker?

add in docker the `--rm` to erase the state after everything, e.g.

```
docker run -it --entrypoint=bash --rm test:pandas
```

it sbetter to run the entrypoint from the Dockerfile? 
maybe, but remember if you do it don't add `--entrypoint=bash` to the `docker run` command

After creating the ingestion pipeline we need to connect the pg with the container with th ingestion pipeline,
we need to make the containers part of the same network, 

I thing I need to create the network first

```bash
    docker network create pg-network
```

```bash
mkdir ny_taxi_postgres_data

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:16
  
```

```bash
    docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table=yellow_taxi_trips
```

Updated docker run command corresponding to the ingestion file parameters

@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')


```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=localhost \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
```

### UV

```bash
    pip install uv
    uv init
    uv add
    uv run   
```

remember the ```uv add --dev``` for dev dependancies and avoid installing them in the prod env

### ABOUT `pgcli`

```bash
   uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

### ABOUT INGESTION

We are using pandas for data ingestion, everything is int he `notebook.ipynb`