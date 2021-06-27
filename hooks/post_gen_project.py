import json
import os
import shutil
# ------------------------------------------------------------------------------


def main():
    src = 'cookiecutter-config.json'
    with open(src) as f:
        config = json.load(f)

    repo = config['repo']
    rtype = config['repo_type']

    if rtype == 'package':
        shutil.rmtree('helm')
        shutil.rmtree('python/' + repo + '/server')
        os.remove('sphinx/server.rst')

    if rtype == 'flask':
        os.remove('python/' + repo + '/server/app.py')

    if rtype != 'dash':
        shutil.rmtree('artifacts')
        shutil.rmtree('templates')
        os.remove('python/conftest.py')

    os.remove(src)

main()
