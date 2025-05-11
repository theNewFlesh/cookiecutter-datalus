#!/usr/bin/env python3

from enum import Enum
from pathlib import Path
import argparse
import re
import os
import json
import shutil
import subprocess
import sys
# ------------------------------------------------------------------------------


class TerminalColorscheme(Enum):
    '''
    Terminal color scheme.
    '''
    BLUE1 = '\033[0;34m'
    BLUE2 = '\033[0;94m'
    CYAN1 = '\033[1;96m'
    CYAN2 = '\033[0;96m'
    GREEN1 = '\033[1;92m'
    GREEN2 = '\033[0;92m'
    GREY1 = '\033[0;90m'
    GREY2 = '\033[0;37m'
    PURPLE1 = '\033[0;35m'
    PURPLE2 = '\033[0;95m'
    RED1 = '\033[0;31m'
    RED2 = '\033[0;91m'
    WHITE = '\033[1;97m'
    YELLOW1 = '\033[0;33m'
    YELLOW2 = '\033[0;93m'
    CLEAR = '\033[0m'


class PrettyHelpFormatter(argparse.RawTextHelpFormatter):
    '''
    Argparse formatters suck at text wrapping. So, I created this.
    '''
    def __init__(
        self, prog, indent_increment=4, max_help_position=24, width=None
    ):
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_usage(self, *args):
        pass

    def _format_action(self, action):
        cyan2 = TerminalColorscheme.CYAN2.value
        green1 = TerminalColorscheme.GREEN1.value
        clear = TerminalColorscheme.CLEAR.value
        if isinstance(action, argparse._SubParsersAction):
            lines = []
            for item in set(action._choices_actions):
                line = '    {a}{b:<25}{c} - {d}'
                line = line.format(
                    a=cyan2,
                    b=item.dest,
                    c=clear,
                    d=item.help.strip(),
                )
                lines.append(line)
            output = '\n'.join(lines)
            output = output + green1 + '\n'
            return output
        return super()._format_action(action)

    def _add_item(self, func, args):
        cyan1 = TerminalColorscheme.CYAN1.value
        green2 = TerminalColorscheme.GREEN2.value
        white = TerminalColorscheme.WHITE.value
        clear = TerminalColorscheme.CLEAR.value

        if func.__name__ == '_format_action':
            if args[0].dest == 'command':
                args[0].dest = clear
                args[0].help = ''

            elif args[0].__class__.__name__ == '_HelpAction':
                args[0].option_strings[0] = green2 + args[0].option_strings[0]
                args[0].help = ' ' * 6 + clear + args[0].help

        elif func.__name__ == '_format_text':
            args = args[0]
            args = '{}{}{}{}'.format(white, args, clear, cyan1)
            args = [args]

        super()._add_item(func, args)

def main():
    # main parser
    cmd_parser = argparse.ArgumentParser(
        description='Datalus command line interface', usage='',
        formatter_class=PrettyHelpFormatter
    )
    cmd_parser.add_argument('command')
    commands = cmd_parser.add_subparsers(metavar='')
    cmd_parser._action_groups[0]._group_actions.pop(0)

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

    # cruft_check_files
    check = commands.add_parser(
        'cruft-check-files', help='Check for extra and missing template files'
    )
    check.add_argument('--source', type=str, help='repository', required=True)
    check.add_argument('--branch', type=str, help='datalus branch or commmit', default='HEAD')

    # command lookup table
    lut = {
        'build-test-repo': (build, build_test_repo),
        'patch-cruft-json': (patch, patch_cruft_json),
        'cruft-update-repo': (cruft, cruft_update_repo),
        'extract-cookiecutter-yaml': (extract, extract_cookiecutter_yaml),
        'cruft-check-files': (check, cruft_check_files),
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
        "secret-env",
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
    target = Path(target, '.cruft.json')
    assert target.is_file(), '{} is not a file'.format(target)
    cwd = target.parent

    with open(target) as f:
        raw_data = f.read()
        data = json.loads(raw_data)

    # set cruft.json template field to local repo
    data['template'] = Path(os.getcwd()).absolute().as_posix()
    with open(target, 'w') as f:
        json.dump(data, f, indent=2)

    # run cruft diff
    cmd = 'cruft diff --checkout {} > /tmp/cruft.diff'.format(branch)
    subprocess.Popen(cmd, shell=True, cwd=cwd).wait()

    # revert cruft.json to orginal form
    with open(target, 'w') as f:
        f.write(raw_data)

    # apply git diff
    cmd = 'git apply /tmp/cruft.diff'
    subprocess.Popen(cmd, shell=True, cwd=cwd).wait()

    # delete temp file
    os.remove('/tmp/cruft.diff')

    # if cruft.json skip field has patterns
    skip = data.get('skip', [])
    if skip != []:
        # find git diff filepaths
        cmd = 'git --no-pager diff --name-only'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd=cwd)
        proc.wait()

        # filter by skip patterns
        diff = proc.stdout.read().decode('utf-8').split('\n')
        revert = filter(lambda x: re.search('|'.join(skip), x), diff)
        revert = ' '.join(list(revert))

        # revert matching files
        cmd = 'git checkout HEAD -- {}'.format(revert)
        subprocess.Popen(cmd, shell=True, cwd=cwd).wait()


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


def cruft_check_files(
    source,
    branch='HEAD',
    template='https://github.com/theNewFlesh/cookiecutter-datalus',
):
    # type: (str, str, str) -> None
    '''
    Compares source repo to a cruft generated version.

    Args:
        source (str): Source repository.
        branch (str, optional): Cruft template branch. Default: HEAD.
        template (str, optional): Cruft template repo.
            Default: https://github.com/theNewFlesh/cookiecutter-datalus
    '''
    # create /tmp/datalus
    root = '/tmp/datalus'
    shutil.rmtree(root)
    os.makedirs(root)
    target = Path(root, 'config.yaml').as_posix()

    # extract config
    cruft = Path(source, '.cruft.json').as_posix()
    extract_cookiecutter_yaml(cruft, target)

    # create example repo
    cmd = 'cruft create {template} --checkout {branch} --output-dir {root} '
    cmd += '--config-file {target} -y'
    cmd = cmd.format(template=template, branch=branch, root=root, target=target)
    subprocess.Popen(cmd, shell=True).wait()

    # establish ignore file pattern
    ignore_re = r'\.git/|docs|drawio|DS_Store|jpeg|jpg|mypy|node_modules'
    ignore_re += '|notebooks|png|public|pytest|python|resources|ruff'
    ignore_re += '|sphinx/images|user-settings'

    # get expected filepaths
    demo = Path(root, Path(source).name).as_posix()
    expected = []
    for root, _, files in os.walk(demo):
        for file_ in files:
            f = Path(root, file_).as_posix()
            f = re.sub(demo + os.sep, '', f)
            if not re.search(ignore_re, f):
                expected.append(f)

    # get found filepaths
    found = []
    for root, _, files in os.walk(source):
        for file_ in files:
            f = Path(root, file_).as_posix()
            f = re.sub(source + os.sep, '', f)
            if not re.search(ignore_re, f):
                found.append(f)

    kwargs = dict(
        green1=TerminalColorscheme.GREEN1.value,
        red1=TerminalColorscheme.RED1.value,
        clear=TerminalColorscheme.CLEAR.value,
    )

    # print extra files
    for item in set(found).difference(expected):
        msg = '{green1}EXTRA   {item}{clear}'.format(item=item, **kwargs)
        print(msg)

    # print missing files
    for item in set(expected).difference(found):
        msg = '{red1}MISSING {item}{clear}'.format(item=item, **kwargs)
        print(msg)

    # clean up temp repo
    shutil.rmtree(root)
# ------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
