# aquarium-opil
Python interface for using OPIL with Aquarium

workflow -> opil.Protocol(workflow.name)

## keeping stuff up-to-date

1. uncomment the pip install commands in `.devcontainer/Dockerfile`
2. comment the pip install command in `.devcontainer/devcontainer.json`
3. rebuild the container in vscode
4. update base-requirements.txt to use the new versions  of opil and pydent from `pip freeze`
5. restore comment state
6. rebuild the container


