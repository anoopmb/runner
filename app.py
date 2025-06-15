import os
import subprocess
import tempfile
from flask import Flask, render_template_string, redirect, url_for

GITEA_REPO_URL = os.environ.get('GITEA_REPO_URL', 'https://gitea.example.com/user/frontaccounting.git')
BASE_PORT = int(os.environ.get('BASE_PORT', 8000))
CLONE_ROOT = os.environ.get('CLONE_ROOT', '/tmp/branches')

app = Flask(__name__)

LIST_TEMPLATE = """
<!doctype html>
<title>Branch Runner</title>
<h1>Select a Branch</h1>
<ul>
{% for branch in branches %}
  <li><a href="{{ url_for('run_branch', branch=branch) }}">{{ branch }}</a></li>
{% endfor %}
</ul>
"""

RUN_TEMPLATE = """
<!doctype html>
<title>Running {{ branch }}</title>
<p>Branch <b>{{ branch }}</b> launched on port {{ port }}.</p>
<p>Access it via <a href="http://{{ host }}:{{ port }}/">http://{{ host }}:{{ port }}/</a></p>
"""


def list_branches():
    result = subprocess.run([
        'git', 'ls-remote', '--heads', GITEA_REPO_URL
    ], check=True, capture_output=True, text=True)
    branches = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].startswith('refs/heads/'):
            branches.append(parts[1].replace('refs/heads/', ''))
    return branches


def build_and_run(branch):
    clone_dir = tempfile.mkdtemp(prefix=f'{branch}-', dir=CLONE_ROOT)
    subprocess.run(['git', 'clone', '-b', branch, GITEA_REPO_URL, clone_dir], check=True)
    tag = f'fa:{branch}'
    subprocess.run(['docker', 'build', '-t', tag, clone_dir], check=True)
    port = BASE_PORT + int(subprocess.check_output(['sh', '-c', 'ls -1q ' + CLONE_ROOT + ' | wc -l']).strip())
    subprocess.run(['docker', 'run', '-d', '-p', f'{port}:80', tag], check=True)
    return port


@app.route('/')
def index():
    branches = list_branches()
    return render_template_string(LIST_TEMPLATE, branches=branches)


@app.route('/run/<branch>')
def run_branch(branch):
    port = build_and_run(branch)
    host = os.environ.get('HOST', 'localhost')
    return render_template_string(RUN_TEMPLATE, branch=branch, port=port, host=host)


if __name__ == '__main__':
    os.makedirs(CLONE_ROOT, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
