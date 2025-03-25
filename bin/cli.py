#!/usr/bin/env python3

from pathlib import Path
import argparse
import re
import os
import json
import shutil
import subprocess
import sys
# ------------------------------------------------------------------------------


class PrettyHelpFormatter(argparse.RawTextHelpFormatter):
    '''
    Argparse formatters suck at text wrapping.
    So, I created this.
    '''
    def _format_action(self, action):
        if isinstance(action, argparse._SubParsersAction):
            lines = []
            for item in set(action._choices_actions):
                line = '    {:<25} - {}'.format(item.dest, item.help.strip())
                lines.append(line)
            output = '\n'.join(lines)
            output = '\n' + output + '\n'
            return output
        return super()._format_action(action)


def main():
    # main parser
    cmd_parser = argparse.ArgumentParser(
        description='Datalus command line interface', usage='',
        formatter_class=PrettyHelpFormatter
    )
    cmd_parser.add_argument('command', help='Command to run')
    # commands = cmd_parser.add_subparsers(metavar='', title='commands')
    commands = cmd_parser.add_subparsers(metavar='')

    # build_test_repo
    build = commands.add_parser('build-test-repo', help='Build datalus test repo')
    build.add_argument('--target', type=str, help='parent directory of test repo', required=True)

    # patch_cruft_json
    patch = commands.add_parser(
        'patch-cruft-json', help='Patch .cruft.json file with skip patterns'
    )
    patch.add_argument('--target', type=str, help='cruft.json file', required=True)

    # cruft_update_repo
    cruft = commands.add_parser(
        'cruft-update-repo', help='Apply silent cruft update to target repo'
    )
    cruft.add_argument('--target', type=str, help='cruft.json file', required=True)
    cruft.add_argument('--branch', type=str, help='datalus branch or commmit', default='HEAD')

    # extract_cookiecutter_yaml
    extract = commands.add_parser(
        'extract-cookiecutter-yaml',
        help='Extract cookiecutter yaml file from given .cruft.json file',
    )
    extract.add_argument('--source', type=str, help='cruft.json file', required=True)
    extract.add_argument('--target', type=str, help='cookiecutter yaml file', required=True)

    # command lookup table
    lut = {
        'build-test-repo': (build, build_test_repo),
        'patch-cruft-json': (patch, patch_cruft_json),
        'cruft-update-repo': (cruft, cruft_update_repo),
        'extract-cookiecutter-yaml': (extract, extract_cookiecutter_yaml),
    }

    # parse command
    if len(sys.argv) < 2:
        cmd_parser.print_help()
        return
    command = cmd_parser.parse_args([sys.argv[1]]).command
    if command not in lut:
        print('{} is not a command'.format(command))
        return

    # run command
    parser, func = lut[command]
    kwargs = dict(parser.parse_args(sys.argv[2:])._get_kwargs())
    func(**kwargs)
# ------------------------------------------------------------------------------


def build_test_repo(target):
    # type: (str) -> None
    '''
    Build datalus test repo.

    Args:
        target (str): Parent directory of test repo.
    '''
    tgt_ = Path(target, 'datalus-test')
    tgt = tgt_.as_posix()
    if tgt_.is_dir():
        shutil.rmtree(tgt)
    os.makedirs(tgt)
    cmd = 'cookiecutter . --no-input --config-file test_config.yml --output-dir {}'.format(tgt)
    subprocess.Popen(cmd, shell=True).wait()


def patch_cruft_json(target):
    # type: (str) -> None
    '''
    Patch .cruft.json file with skip patterns.

    Args:
        target (str): .cruft.json file.
    '''
    repo = re.sub('-', '_', Path(target).parent.name)
    with open(target) as f:
        data = json.load(f)

    data['skip'] = [
        '__init__\\.py$',
        '\\.gitignore$',
        '\\.gitkeep$',
        'docker/config/.*\\.lock$',
        'docker/config/build\\.yaml',
        'docs/.*',
        'LICENSE',
        'mkdocs/md/(?!index\\.md|style\\.css)',
        'public/.*',
        'python/{}/.*(?!command\\.py$)'.format(repo),
        'resources/.*',
        'sphinx/.*rst$',
    ]
    with open(target, 'w') as f:
        json.dump(data, f, indent=2)


def cruft_update_repo(target, branch='HEAD'):
    # type: (str, str) -> None
    '''
    Applies a silent cruft update to target repo, such that when `cruft update`
    is later called, all the changes .rej files can be ignored.

    Args:
        target (str): Repo directory.
        branch (str, optional): Cruft template branch. Default: master.
    '''
    # get cruft.json data
    target = Path(target, '.cruft.json').as_posix()
    with open(target) as f:
        raw_data = f.read()
        data = json.loads(raw_data)

    # set cruft.json template field to local repo
    data['template'] = Path(os.getcwd()).absolute().as_posix()
    with open(target, 'w') as f:
        json.dump(data, f, indent=2)

    # run cruft diff
    cmd = 'cruft diff --checkout {} > /tmp/cruft.diff'.format(branch)
    subprocess.Popen(cmd, shell=True, cwd=target).wait()

    # revert cruft.json to orginal form
    with open(target, 'w') as f:
        f.write(raw_data)

    # apply git diff
    cmd = 'git apply /tmp/cruft.diff'
    subprocess.Popen(cmd, shell=True, cwd=target).wait()

    # delete temp file
    os.remove('/tmp/cruft.diff')

    # if cruft.json skip field has patterns
    skip = data.get('skip', [])
    if skip != []:
        # find git diff filepaths
        cmd = 'git --no-pager diff --name-only'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd=target)
        proc.wait()

        # filter by skip patterns
        diff = proc.stdout.read().decode('utf-8').split('\n')
        revert = filter(lambda x: re.search('|'.join(skip), x), diff)
        revert = ' '.join(list(revert))

        # revert matching files
        cmd = 'git checkout HEAD -- {}'.format(revert)
        subprocess.Popen(cmd, shell=True, cwd=target).wait()


def extract_cookiecutter_yaml(source, target):
    # type: (str, str) -> None
    '''
    Extract cookiecutter yaml file from given .cruft.json file.

    Args:
        source (str): Cruft.json file.
        target (str): Target yaml file.
    '''
    with open(source) as f:
        data = json.load(f)
    data = dict(default_context=data['context']['cookiecutter'])
    with open(target, 'w') as f:
        json.dump(data, f, indent=4)
# ------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
