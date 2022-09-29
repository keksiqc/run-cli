# Run

## Install

```bash
pip install -U run-scripts
```

## Basic Usage

```bash
run init [--short]
# Creates either a runfile.yml or run.yml file in the current directory

run [script]
# Runs the script defined in the runfile.yml or run.yml file
```

## Examples

### runfile.yml

```yaml
scripts:
    lint: "poetry run black ."
    build: 
        - "run lint"
        - "docker build -t image ."
```