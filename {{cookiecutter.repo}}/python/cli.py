{%- set cc = cookiecutter -%}
#!/usr/bin/env python

try:
    # python2.7 doesn't have typing module
    from typing import Any, List, Tuple  # noqa F401
except ImportError:
    pass

import argparse
import os
import re

# python2.7 doesn't have pathlib module
REPO_PATH = os.path.join(os.sep, *os.path.realpath(__file__).split(os.sep)[:-2])
REPO = os.path.split(REPO_PATH)[-1]
GIT_USER = '{{cc.git_user}}'
{%- if cc.docker_registry == 'gitlab' %}
DOCKER_REGISTRY = 'registry.gitlab.com/{{ cc.git_organization | lower }}/' + REPO
{%- else %}
DOCKER_REGISTRY = '{{ cc.git_user | lower }}/' + REPO
{%- endif %}
USER = 'ubuntu:ubuntu'
PORT = 8080
# --------------------------------------------------------------------------------------------------

'''
A CLI for developing and deploying an app deeply integrated with this
repository's structure. Written to be python version agnostic.
'''


COLORS = {
    'B': '\033[0;94m',  # blue
    'C': '\033[0;96m',  # cyan
    'G': '\033[0;92m',  # green
    'K': '\033[0;37m',  # grey
    'P': '\033[0;95m',  # purple
    'R': '\033[0;91m',  # red
    'W': '\033[0;97m',  # white
    'Y': '\033[0;93m',  # yellow
    'X': '\033[0m',     # clear
}
SEP = '{P}' + '-' * 27 + '|' + '-' * 60 + '{X}'
SEP = SEP.format(**COLORS)
VSEP = '{P}|{X}'.format(**COLORS)
COLORS['SEP'] = SEP
COLORS['VSEP'] = VSEP


class BetterHelpFormatter(argparse.RawTextHelpFormatter):
    '''
    HelpFormatter with better indentation.
    '''
    def __init__(
        self, prog, indent_increment=4, max_help_position=24, width=None
    ):
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_action(self, action):
        output = super()._format_action(action)
        output = re.sub(' {28}', '    ', output)
        return output


def get_info():
    # type: () -> Tuple[str, list]
    '''
    Parses command line call.

    Returns:
        tuple[str]: Mode and arguments.
    '''
    desc = '{W}A CLI for developing and deploying the {repo} app.{X}'.format(
        repo=REPO, **COLORS
    )
    parser = argparse.ArgumentParser(
        formatter_class=BetterHelpFormatter,
        description=desc,
        usage='  python cli.py COMMAND [-a --args]=ARGS [-h --help] [--dryrun]'
    )

    parser.add_argument(
        'command',
        metavar='{P}COMMAND                    | DESCRIPTION'.format(**COLORS),
        type=str,
        nargs=1,
        action='store',
        help='''
    {SEP}
    {Y}build-edit-prod-dockerfile {VSEP} Edit prod.dockefile to use local package
    {Y}build-local-package        {VSEP} Generate pip package of repo and copy it to docker/dist
    {Y}build-package              {VSEP} Build production version of repo for publishing
    {Y}build-prod                 {VSEP} Publish pip package of repo to PyPi
    {Y}build-publish              {VSEP} Run production tests first then publish pip package of repo to PyPi
    {Y}build-test                 {VSEP} Build test version of repo for prod testing
    {SEP}
    {C}docker-build               {VSEP} Build development image
    {C}docker-build-from-cache    {VSEP} Build development image from registry cache
    {C}docker-build-no-cache      {VSEP} Build development image without cache
    {C}docker-build-prod          {VSEP} Build production image
    {C}docker-build-prod-no-cache {VSEP} Build production image without cache
    {C}docker-container           {VSEP} Display the Docker container id
    {C}docker-destroy             {VSEP} Shutdown container and destroy its image
    {C}docker-destroy-prod        {VSEP} Shutdown production container and destroy its image
    {C}docker-image               {VSEP} Display the Docker image id
    {C}docker-prod                {VSEP} Start production container
    {C}docker-pull-dev            {VSEP} Pull development image from Docker registry
    {C}docker-pull-prod           {VSEP} Pull production image from Docker registry
    {C}docker-push-dev            {VSEP} Push development image to Docker registry
    {C}docker-push-dev-latest     {VSEP} Push development image to Docker registry with dev-latest tag
    {C}docker-push-prod           {VSEP} Push production image to Docker registry
    {C}docker-push-prod-latest    {VSEP} Push production image to Docker registry with prod-latest tag
    {C}docker-remove              {VSEP} Remove Docker image
    {C}docker-restart             {VSEP} Restart container
    {C}docker-start               {VSEP} Start container
    {C}docker-stop                {VSEP} Stop container
    {SEP}
    {Y}docs                       {VSEP} Generate sphinx documentation
    {Y}docs-architecture          {VSEP} Generate architecture.svg diagram from all import statements
    {Y}docs-full                  {VSEP} Generate documentation, coverage report, diagram and code
    {Y}docs-metrics               {VSEP} Generate code metrics report, plots and tables
    {SEP}
    {C}library-add                {VSEP} Add a given package to a given dependency group
    {C}library-graph-dev          {VSEP} Graph dependencies in dev environment
    {C}library-graph-prod         {VSEP} Graph dependencies in prod environment
    {C}library-install-dev        {VSEP} Install all dependencies into dev environment
    {C}library-install-prod       {VSEP} Install all dependencies into prod environment
    {C}library-list-dev           {VSEP} List packages in dev environment
    {C}library-list-prod          {VSEP} List packages in prod environment
    {C}library-lock-dev           {VSEP} Resolve dev.lock file
    {C}library-lock-prod          {VSEP} Resolve prod.lock file
    {C}library-remove             {VSEP} Remove a given package from a given dependency group
    {C}library-search             {VSEP} Search for pip packages
    {C}library-sync-dev           {VSEP} Sync dev environment with packages listed in dev.lock
    {C}library-sync-prod          {VSEP} Sync prod environment with packages listed in prod.lock
    {C}library-update             {VSEP} Update dev dependencies
    {C}library-update-pdm         {VSEP} Update PDM
    {SEP}
    {Y}quickstart                 {VSEP} Display quickstart guide
    {SEP}
    {C}session-lab                {VSEP} Run jupyter lab server
    {C}session-python             {VSEP} Run python session with dev dependencies
{%- if cc.repo_type in ['dash', 'flask'] %}
    {C}session-server             {VSEP} Run application server inside Docker container
{%- endif %}
    {SEP}
    {Y}state                      {VSEP} State of repository and Docker container
    {SEP}
    {C}test-coverage              {VSEP} Generate test coverage report
    {C}test-dev                   {VSEP} Run all tests
    {C}test-fast                  {VSEP} Test all code excepts tests marked with SKIP_SLOWS_TESTS decorator
    {C}test-format                {VSEP} Format all python files
    {C}test-lint                  {VSEP} Run linting and type checking
    {C}test-prod                  {VSEP} Run tests across all support python versions
    {SEP}
    {Y}version                    {VSEP} Full resolution of repo: dependencies, linting, tests, docs, etc
    {Y}version-bump-major         {VSEP} Bump pyproject major version
    {Y}version-bump-minor         {VSEP} Bump pyproject minor version
    {Y}version-bump-patch         {VSEP} Bump pyproject patch version
    {Y}version-commit             {VSEP} Tag with version and commit changes to master
    {SEP}
    {C}zsh                        {VSEP} Run ZSH session inside Docker container
    {C}zsh-complete               {VSEP} Generate oh-my-zsh completions
    {C}zsh-root                   {VSEP} Run ZSH session as root inside Docker container
    {G}
'''[1:-1].format(repo=REPO, **COLORS))  # noqa: E501

    parser.add_argument(
        '-a',
        '--args',
        metavar='args',
        type=str,
        nargs='+',
        action='store',
        help='Additional arguments to be passed. Be sure to include hyphen prefixes.'
    )

    temp = parser.parse_args()
    mode = temp.command[0]
    args = []
    if temp.args is not None:
        args = re.split(' +', temp.args[0])

    return mode, args


{% raw -%}
def resolve(commands):
    # type: (List[str]) -> str
    '''
    Convenience function for creating single commmand from given commands and
    resolving '{...}' substrings.

    Args:
        commands (list[str]): List of commands.

    Returns:
        str: Resolved command.
    '''
    cmd = ' && '.join(commands)

    all_ = dict(
        black='\033[0;30m',
        blue='\033[0;34m',
        clear='\033[0m',
        cyan='\033[0;36m',
        green='\033[0;32m',
        purple='\033[0;35m',
        red='\033[0;31m',
        white='\033[0;37m',
        yellow='\033[0;33m',
        git_user=GIT_USER,
        registry=DOCKER_REGISTRY,
        port=str(PORT),
        pythonpath='{PYTHONPATH}',
        repo_path=REPO_PATH,
        repo=REPO,
        repo_=re.sub('-', '_', REPO),
        user=USER,
    )
    all_.update(COLORS)
    args = {}
    for k, v in all_.items():
        if '{' + k + '}' in cmd:
            args[k] = v

    cmd = cmd.format(**args)
    return cmd


def line(text, sep=' '):
    # type: (str, str) -> str
    '''
    Convenience function for formatting a given block of text as series of
    commands.

    Args:
        text (text): Block of text.
        sep (str, optional): Line separator. Default: ' '.

    Returns:
        str: Formatted command.
    '''
    output = re.sub('^\n|\n$', '', text)  # type: Any
    output = output.split('\n')
    output = [re.sub('^ +| +$', '', x) for x in output]
    output = sep.join(output) + sep
    return output


# SUBCOMMANDS-------------------------------------------------------------------
def enter_repo():
    # type: () -> str
    '''
    Returns:
        str: Command to enter repo.
    '''
    return 'export CWD=`pwd` && cd {repo_path}'


def exit_repo():
    # type: () -> str
    '''
    Returns:
        str: Command to return to original directory.
    '''
    return 'cd $CWD'


def start():
    # type: () -> str
    '''
    Returns:
        str: Command to start container if it is not yet running.
    '''
    cmds = [
        line('''
            export STATE=`docker ps
                -a
                -f name=^{repo}$
                -f status=running
                --format='{{{{{{{{.Status}}}}}}}}'`
        '''),
        line('''
            if [ -z "$STATE" ];
                then cd docker;
                docker compose
                    -p {repo}
                    -f {repo_path}/docker/docker-compose.yml up
                    --detach;
                cd ..;
            fi
        '''),
    ]
    return resolve(cmds)


def stop():
    # type: () -> str
    '''
    Returns:
        str: Command to shutdown container.
    '''
    cmd = line('''
        cd docker;
        docker compose
            -p {repo}
            -f {repo_path}/docker/docker-compose.yml
            down;
        cd ..
    ''')
    return cmd


def remove_container():
    # type: () -> str
    '''
    Returns:
        str: Command to remove container.
    '''
    return 'docker container rm --force {repo}'


def docker_exec(tty=False):
    # type: (bool) -> str
    '''
    Args:
        tty (bool, optional): Include --tty flag. Default: False.

    Returns:
        str: Partial command to call 'docker exec'.
    '''
    if tty:
        cmd = line('''
            docker exec
                --interactive
                --tty
                --user {user}
        ''')
    else:
        cmd = line('''
            docker exec
                --interactive
                --user {user}
        ''')
    return cmd


def version_variable():
    # type: () -> str
    '''
    Returns:
        str: Command to set version variable from pyproject.toml.
    '''
    return line('''
        export VERSION=`cat docker/config/pyproject.toml
            | grep -E '^version *='
            | awk '{{print $3}}'
            | sed 's/\"//g'`
    ''')


def zshrc_tools(command, args=[]):
    # type: (str, list[str]) -> str
    '''
    Creates a tools command string that sources zshrc first.

    Args:
        command (str): command
        args (list, optional): List of arguments to be passed to the command.
            Default: []

    Returns:
        str: command.
    '''
    cmd = 'source /home/ubuntu/.zshrc && {cmd}'.format(cmd=command)
    if args != []:
        cmd = cmd + ' ' + ' '.join(args)
    cmd = '"{cmd}"'.format(cmd=cmd)
    return cmd


# COMMANDS----------------------------------------------------------------------
def build_dev_command(use_cache=True):
    # type: (bool) -> str
    '''
    Build image for development.

    Args:
        use_cache (bool, optional): Use layer cache. Default: False.

    Returns:
        str: Command to build dev image.
    '''
    cmd = line('''
        cd docker;
        docker build
            --file dev.dockerfile
            --build-arg BUILDKIT_INLINE_CACHE=1
{%- endraw %}
{%- if cc.include_secret_env == 'yes' %}
            --secret id=secret-env,src=config/secret-env
{%- endif %}
{%- raw %}
            --label "repository={repo}"
            --label "docker-registry={registry}"
            --label "git-user={git_user}"
            --label "git-branch=$(git branch --show-current)"
            --label "git-commit=$(git rev-parse HEAD)"
    ''')
    if use_cache:
        cmd += ' --cache-from {registry}:dev-latest'
    else:
        cmd += ' --no-cache'
    cmd += ' --tag {repo}:dev . && cd ..'

    cmds = [
        enter_repo(),
        cmd,
        exit_repo(),
    ]
    return resolve(cmds)


def build_prod_command(use_cache=False):
    # type: (bool) -> str
    '''
    Build image for production.

    Args:
        use_cache (bool, optional): Use layer cache. Default: False.

    Returns:
        str: Command to build prod image.
    '''
    cmd = line('''
{%- endraw %}
{%- if cc.include_secret_env == 'yes' %}
        export DOCKER_BUILDKIT=1;
{%- endif %}
        cd docker;
        docker build
            --force-rm
            --file prod.dockerfile
            --build-arg VERSION="$VERSION"
{%- if cc.include_secret_env == 'yes' %}
            --secret id=secret-env,src=config/secret-env
{%- endif %}
{%- raw %}
            --label "repository={repo}"
            --label "docker-registry={registry}"
            --label "git-user={git_user}"
            --label "git-branch=$(git branch --show-current)"
            --label "git-commit=$(git rev-parse HEAD)"
    ''')
    if not use_cache:
        cmd += ' --no-cache'
    cmd += ' --tag {repo}:prod . && cd ..'
    cmds = [
        enter_repo(),
        version_variable(),
        cmd,
        exit_repo(),
    ]
    return resolve(cmds)


def container_id_command():
    # type: () -> str
    '''
    Returns:
        str: Command to get docker container id.
    '''
    cmds = [
        "docker ps -a --filter name=^{repo}$ --format '{{{{.ID}}}}'"
    ]
    return resolve(cmds)


def destroy_dev_command():
    # type: () -> str
    '''
    Returns:
        str: Command to destroy dev container and image.
    '''
    cmds = [
        enter_repo(),
        stop(),
        remove_container(),
        'docker image rm --force {repo}:dev',
        exit_repo(),
    ]
    return resolve(cmds)


def destroy_prod_command():
    # type: () -> str
    '''
    Returns:
        str: Command to destroy prod image.
    '''
    cmds = [
        'docker container rm --force {repo}-prod:prod',
        'docker image rm {repo}:prod',
    ]
    return resolve(cmds)


def image_id_command():
    # type: () -> str
    '''
    Returns:
        str: Command to get docker image id.
    '''
    cmds = [
        enter_repo(),
        start(),
        "docker images {repo} --format '{{{{.ID}}}}'",
        exit_repo(),
    ]
    return resolve(cmds)


def prod_command(args):
    # type: (list) -> str
    '''
    Returns:
        str: Command to start prod container.
    '''
    cmd = 'docker run'
    if args != ['']:
        cmd += ' --volume {}:/mnt/storage'.format(args[0])
    cmds = [
        enter_repo(),
        version_variable(),
        line(cmd + '''
            --rm
            --interactive
            --tty
            --publish {port}:{port}
            --name {repo}-prod
            {repo}:prod
            bash
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def pull_command(tag='dev-latest'):
    # type: (str) -> str
    '''
    Args:
        tag (str, optional): Tag prefix. Default: 'dev-latest'.

    Returns:
        str: Command to pull Docker image from registry.
    '''
    cmds = [
        'docker pull {registry}:' + tag,
    ]
    return resolve(cmds)


def push_command(mode='dev', suffix='$VERSION'):
    # type: (str, str) -> str
    '''
    Args:
        mode (str, optional): Mode. Default: 'dev'.
        suffix (str, optional): Tag suffix. Default: '$VERSION'.

    Returns:
        str: Command to push Docker image to registry.
    '''
    tag = mode + '-' + suffix
    target = ' {registry}:' + tag
    cmds = [
        enter_repo(),
        version_variable(),
        start(),
        version_variable(),
        'docker tag {repo}:' + mode + target,
        'docker push' + target,
        'docker rmi' + target,
        exit_repo(),
    ]
    return resolve(cmds)


def remove_command():
    # type: () -> str
    '''
    Returns:
        str: Command to remove container.
    '''
    cmds = [
        enter_repo(),
        remove_container(),
        exit_repo(),
    ]
    return resolve(cmds)


def restart_command():
    # type: () -> str
    '''
    Returns:
        str: Command to restart container.
    '''
    cmds = [
        enter_repo(),
        line('''
            cd docker;
            docker compose
                -p {repo}
                -f {repo_path}/docker/docker-compose.yml
                restart;
            cd ..
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def start_command():
    # type: () -> str
    '''
    Returns:
        str: Command to start container.
    '''
    cmds = [
        enter_repo(),
        start(),
    ]
    return resolve(cmds)


def state_command():
    # type: () -> str
    '''
    Returns:
        str: Command to get state of app.
    '''
    cmds = [
        enter_repo(),
        version_variable(),
        'export IMAGE_EXISTS=`docker images {repo} | grep -v REPOSITORY`',
        'export CONTAINER_EXISTS=`docker ps -a -f name=^{repo}$ | grep -v CONTAINER`',
        'export RUNNING=`docker ps -a -f name=^{repo}$ -f status=running | grep -v CONTAINER`',
        line(r'''
            export PORTS=`
                cat docker/docker-compose.yml |
                grep -E ' - "....:...."' |
                sed s'/.* - "//g' |
                sed 's/"//g' |
                sed 's/^/{blue}/g' |
                sed 's/:/{purple}|{CLEAR}->/g' |
                awk 1 ORS=' '
            `
        '''),
        line('''
            if [ -z "$IMAGE_EXISTS" ];
                then export IMAGE_STATE="{red}absent{clear}";
            else
                export IMAGE_STATE="{green}present{clear}";
            fi;
            if [ -z "$CONTAINER_EXISTS" ];
                then export CONTAINER_STATE="{red}absent{clear}";
            elif [ -z "$RUNNING" ];
                then export CONTAINER_STATE="{red}stopped{clear}";
            else
                export CONTAINER_STATE="{green}running{clear}";
            fi
        '''),
        line('''echo
            "app: {cyan}{repo}{clear} -
            version: {yellow}$VERSION{clear} -
            image: $IMAGE_STATE -
            container: $CONTAINER_STATE -
            ports: {blue}$PORTS{clear}"
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def stop_command():
    # type: () -> str
    '''
    Returns:
        str: Command to stop container.
    '''
    cmds = [
        enter_repo(),
        stop(),
        exit_repo(),
    ]
    return resolve(cmds)


def x_tools_command(command, args=[], tty=False):
    # type: (str, list[str], bool) -> str
    '''
    Runs a x_tools command.

    Args:
        command (str): x_tools command
        args (list, optional): List of arguments to be passed to the command.
            Default: []
        tty (bool, optional): Include docker --tty flag. Default: False.

    Returns:
        str: x_tools command.
    '''
    cmds = [
        enter_repo(),
        start(),
        docker_exec(tty=tty) + ' {repo} zsh -c ' + zshrc_tools(command, args),
        exit_repo(),
    ]
    return resolve(cmds)


def quickstart_command():
    # type: () -> str
    '''
    Returns a command which prints the quickstart guide.

    Returns:
        str: quickstart command.
    '''
    return line('''
        cat README.md
        | grep -A 10000 '# Quickstart'
        | grep -B 10000 '# Development CLI'
        | grep -B 10000 -E '^---$'
        | grep -vE '^---$'
    ''')


def version_commit_command(args=[]):
    # type: (List[str]) -> str
    '''
    Args:
        args (list[str], optional): List containing a target branch.
          Default: ['master'].

    Returns:
        str: Git tag and commit command.
    '''
    args = list(filter(lambda x: x != '', args))
    branch = 'master'
    if args != []:
        branch = args[0]
    cmds = [
        enter_repo(),
        version_variable(),
        'git add --all',
        'git commit --message $VERSION',
        'git tag --annotate $VERSION --message "version: $VERSION"',
        'git push --follow-tags origin HEAD:' + branch + ' --push-option ci.skip',
        exit_repo(),
    ]
    return resolve(cmds)


def zsh_command():
    # type: () -> str
    '''
    Returns:
        str: Command to run a zsh session inside container.
    '''
    cmds = [
        enter_repo(),
        start(),
        docker_exec(tty=True) + ' {repo} zsh',
        exit_repo(),
    ]
    return resolve(cmds)


def zsh_complete_command():
    # type: () -> str
    '''
    Returns:
        str: Command to generate and install zsh completions.
    '''
    cmds = [
        'mkdir -p ~/.oh-my-zsh/custom/completions',
        'export _COMP=~/.oh-my-zsh/custom/completions/_{repo}',
        'touch $_COMP',
        "echo 'fpath=(~/.oh-my-zsh/custom/completions $fpath)' >> ~/.zshrc",
        'echo "#compdef {repo} rec" > $_COMP',
        'echo "" >> $_COMP',
        'echo "local -a _subcommands" >> $_COMP',
        'echo "_subcommands=(" >> $_COMP',
        line('''
            bin/{repo} --help
                | grep '    - '
                | sed -E 's/ +- /:/g'
                | sed -E 's/^ +//g'
                | sed -E "s/(.*)/    '\\1'/g"
                | parallel "echo {{}} >> $_COMP"
        '''),
        'echo ")" >> $_COMP',
        'echo "" >> $_COMP',
        'echo "local expl" >> $_COMP',
        'echo "" >> $_COMP',
        'echo "_arguments \\\\" >> $_COMP',
        'echo "    \'(-h --help)\'{{-h,--help}}\'[show help message]\' \\\\" >> $_COMP',
        'echo "    \'(-d --dryrun)\'{{-d,--dryrun}}\'[print command]\' \\\\" >> $_COMP',
        'echo "    \'*:: :->subcmds\' && return 0" >> $_COMP',
        'echo "\n" >> $_COMP',
        'echo "if (( CURRENT == 1 )); then" >> $_COMP',
        'echo "    _describe -t commands \\"{repo} subcommand\\" _subcommands\" >> $_COMP',
        'echo "    return" >> $_COMP',
        'echo "fi" >> $_COMP',
    ]
    return resolve(cmds)


def zsh_root_command():
    # type: () -> str
    '''
    Returns:
        str: Command to run a zsh session as root inside container.
    '''
    return re.sub('ubuntu:ubuntu', 'root:root', zsh_command())


def get_illegal_mode_command():
    # type: () -> str
    '''
    Returns:
        str: Command to report that the mode given is illegal.
    '''
    cmds = [
        line('''
            echo "That is not a legal command.
            Please call {cyan}{repo} --help{clear} to see a list of legal
            commands."
        ''')
    ]
    return resolve(cmds)
{%- endraw %}


# MAIN--------------------------------------------------------------------------
def main():
    # type: () -> None
    '''
    Print different commands to stdout depending on mode provided to command.
    '''
    mode, args = get_info()
    lut = {
        'build-edit-prod-dockerfile': x_tools_command('x_build_edit_prod_dockerfile', args),
        'build-local-package': x_tools_command('x_build_local_package', args),
        'build-package': x_tools_command('x_build_package', args),
        'build-prod': x_tools_command('x_build_prod', args),
        'build-publish': x_tools_command('x_build_publish', args),
        'build-test': x_tools_command('x_build_test', args),
        'docker-build': build_dev_command(),
        'docker-build-from-cache': build_dev_command(use_cache=True),
        'docker-build-no-cache': build_dev_command(use_cache=False),
        'docker-build-prod': build_prod_command(use_cache=True),
        'docker-build-prod-no-cache': build_prod_command(use_cache=False),
        'docker-container': container_id_command(),
        'docker-destroy': destroy_dev_command(),
        'docker-destroy-prod': destroy_prod_command(),
        'docker-image': image_id_command(),
        'docker-prod': prod_command(args),
        'docker-pull-dev': pull_command('dev-latest'),
        'docker-pull-prod': pull_command('prod-latest'),
        'docker-push-dev': push_command('dev'),
        'docker-push-dev-latest': push_command('dev', 'latest'),
        'docker-push-prod': push_command('prod'),
        'docker-push-prod-latest': push_command('prod', 'latest'),
        'docker-remove': remove_command(),
        'docker-restart': restart_command(),
        'docker-start': start_command(),
        'docker-stop': stop_command(),
        'docs': x_tools_command('x_docs', args),
        'docs-architecture': x_tools_command('x_docs_architecture', args),
        'docs-full': x_tools_command('x_docs_full', args),
        'docs-metrics': x_tools_command('x_docs_metrics', args),
        'library-add': x_tools_command('x_library_add', args),
        'library-graph-dev': x_tools_command('x_library_graph_dev', args),
        'library-graph-prod': x_tools_command('x_library_graph_prod', args),
        'library-install-dev': x_tools_command('x_library_install_dev', args),
        'library-install-prod': x_tools_command('x_library_install_prod', args),
        'library-list-dev': x_tools_command('x_library_list_dev', args),
        'library-list-prod': x_tools_command('x_library_list_prod', args),
        'library-lock-dev': x_tools_command('x_library_lock_dev', args),
        'library-lock-prod': x_tools_command('x_library_lock_prod', args),
        'library-remove': x_tools_command('x_library_remove', args),
        'library-search': x_tools_command('x_library_search', args),
        'library-sync-dev': x_tools_command('x_library_sync_dev', args),
        'library-sync-prod': x_tools_command('x_library_sync_prod', args),
        'library-update': x_tools_command('x_library_update', args),
        'library-update-pdm': x_tools_command('x_library_update_pdm', args),
        'quickstart': quickstart_command(),
        'session-lab': x_tools_command('x_session_lab', args, tty=True),
        'session-python': x_tools_command('x_session_python', args, tty=True),
{%- if cc.repo_type in ['dash', 'flask'] %}
        'session-server': x_tools_command('x_session_server', args),
{%- endif %}
        'state': state_command(),
        'test-coverage': x_tools_command('x_test_coverage', args),
        'test-dev': x_tools_command('x_test_dev', args),
        'test-fast': x_tools_command('x_test_fast', args),
        'test-format': x_tools_command('x_test_format', args),
        'test-lint': x_tools_command('x_test_lint', args),
        'test-prod': x_tools_command('x_test_prod', args),
        'version': x_tools_command('x_version', args),
        'version-bump-major': x_tools_command('x_version_bump_major', args),
        'version-bump-minor': x_tools_command('x_version_bump_minor', args),
        'version-bump-patch': x_tools_command('x_version_bump_patch', args),
        'version-commit': version_commit_command(args),
        'zsh': zsh_command(),
        'zsh-complete': zsh_complete_command(),
        'zsh-root': zsh_root_command(),
    }
    cmd = lut.get(mode, get_illegal_mode_command())

    # print is used instead of execute because REPO_PATH and USER do not
    # resolve in a subprocess and subprocesses do not give real time stdout.
    # So, running `command up` will give you nothing until the process ends.
    # `eval "[generated command] $@"` resolves all these issues.
    print(cmd)


if __name__ == '__main__':
    main()
