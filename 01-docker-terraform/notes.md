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

How to preserve state in docker

### UV

```bash
    pip install uv
    uv init
    uv add
    uv run   
```