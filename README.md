# runner

This repository provides a small Flask application that lets users select a
branch from a Gitea repository and run that branch in a Docker container.
The container uses PHP 7.3 and nginx for running FrontAccounting or similar
applications.

## Requirements

- Python 3
- Flask (`pip install flask`)
- Docker

## Configuration

Set the `GITEA_REPO_URL` environment variable to point to your Gitea
repository. Optional environment variables:

- `BASE_PORT` - starting port for launched containers (default `8000`).
- `CLONE_ROOT` - directory for temporary clones (default `/tmp/branches`).
- `HOST` - hostname used in links (default `localhost`).

## Usage

1. Install dependencies and start the Flask app:

   ```bash
   pip install flask
   python app.py
   ```

2. Open `http://<server-ip>:5000` in a browser. Choose a branch to build and
   run. The app clones the branch, builds a Docker image using the provided
   `Dockerfile`, and runs the container on the next available port.

3. The page shows the URL to access the running container.

Cleanup old containers manually or extend the app to remove them when no longer
needed.
