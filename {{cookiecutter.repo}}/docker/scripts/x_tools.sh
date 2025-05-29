{%- set cc = cookiecutter -%}
{%- if cc.include_mkdocs == 'yes' -%}
{%- set sphinx_dir = "$DOCS_DIR/python" -%}
{%- else -%}
{%- set sphinx_dir = "$DOCS_DIR" -%}
{%- endif -%}
# VARIABLES---------------------------------------------------------------------
export HOME="/home/ubuntu"
export PATH=":$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$HOME/.local/lib"
export JUPYTER_PLATFORM_DIRS=0
export JUPYTER_CONFIG_PATH=/home/ubuntu/.jupyter
export REPO="{{cc.repo}}"
export REPO_DIR="$HOME/$REPO"
export REPO_SNAKE_CASE=`echo $REPO | sed 's/-/_/g'`
export REPO_SUBPACKAGE="$REPO_DIR/python/$REPO_SNAKE_CASE"
export REPO_COMMAND_FILE="$REPO_SUBPACKAGE/command.py"
export BUILD_DIR="$HOME/build"
export CONFIG_DIR="$REPO_DIR/docker/config"
{%- if cc.git_host == 'gitlab' %}
export DOCS_DIR="$REPO_DIR/public"
{%- else %}
export DOCS_DIR="$REPO_DIR/docs"
{%- endif %}
export MIN_PYTHON_VERSION="3.{{ cc.python_min_version }}"
export MAX_PYTHON_VERSION="3.{{ cc.python_max_version }}"
export MKDOCS_DIR="$REPO_DIR/mkdocs"
export PDM_DIR="$HOME/pdm"
{%- if cc.package_registry == 'gitlab' %}
export GIT_PROJECT_ID="ENTER GITLAB PROJECT ID HERE"
export GIT_PROJECT_URL="https://gitlab.com/api/v4/projects/$GIT_PROJECT_ID"
export PYPI_URL="$GIT_PROJECT_URL/packages/pypi"
export PYPI_TEST_URL="$PYPI_URL"
{%- else %}
export PYPI_URL="pypi"
export PYPI_TEST_URL="testpypi"
{%- endif %}
export PYTHONPATH="$REPO_DIR/python:$HOME/.local/lib"
export SCRIPT_DIR="$REPO_DIR/docker/scripts"
export TEST_MAX_PROCS=16
export TEST_PROCS="auto"
export TEST_VERBOSITY=0
export VSCODE_SERVER="$HOME/.vscode-server/bin/*/bin/code-server"
alias cp=cp  # "cp -i" default alias asks you if you want to clobber files
alias rolling-pin="/home/ubuntu/.local/bin/rolling-pin"

{% raw -%}
# COLORS------------------------------------------------------------------------
export BLUE1='\033[0;34m'
export BLUE2='\033[0;94m'
export CYAN1='\033[0;36m'
export CYAN2='\033[0;96m'
export GREEN1='\033[0;32m'
export GREEN2='\033[0;92m'
export GREY1='\033[0;90m'
export GREY2='\033[0;37m'
export PURPLE1='\033[0;35m'
export PURPLE2='\033[0;95m'
export RED1='\033[0;31m'
export RED2='\033[0;91m'
export WHITE='\033[0;97m'
export YELLOW1='\033[0;33m'
export YELLOW2='\033[0;93m'
export CLEAR='\033[0m'

# GENERATE-FUNCTIONS------------------------------------------------------------
_x_repeat () {
    # Echo a given character until it reaches the width of the current terminal
    # args: character
    local width=`tput cols -T xterm`;
    for i in {1..$width}; do
        if [ "$SHELL" = "/usr/bin/zsh" ]; then
            echo -n - $1;
        else
            echo -n $1;
        fi;
    done;
}
export SPACER=`_x_repeat -`

_x_resolve_exit_code () {
    # Returns error code if either code is not 0
    # args: exit code 1, exit code 2
    if [ "$1" -ne "0" ]; then
        echo $1;
        return;
    elif [ "$2" -ne "0" ]; then
        echo $2;
        return;
    fi;
    echo 0;
}

_x_for_each_version () {
    # Runs a given command against multiple python versions
    # Expands version variable in command string
    # args: command (string)

    # create version array
    local min=`echo $MIN_PYTHON_VERSION | sed 's/3.//'`;
    local max=`echo $MAX_PYTHON_VERSION | sed 's/3.//'`;
    for i in {$min..$max}; do
        __versions[$i]="3.$i";
    done;

    # run command for each version
    local exit_code=0;
    for VERSION in $__versions; do
        eval "$1";
        exit_code=`_x_resolve_exit_code $exit_code $?`;
    done;
    return $exit_code;
}

_x_gen_pyproject () {
    # Generates pyproject.toml content given a mode
    # args: mode (dev, test or prod)
    if [ "$1" = "dev" ]; then
        # rolling-pin mangles formatting so use sed
        # add -dev to project.name to avoid circular and ambiguous dependencies
        cat $CONFIG_DIR/pyproject.toml \
            |  sed -E "s/name.*$REPO.*/name = \"$REPO-dev\"/";

    elif [ "$1" = "test" ]; then
        rolling-pin toml $CONFIG_DIR/pyproject.toml \
            --edit "project.requires-python=\">=$MIN_PYTHON_VERSION\"" \
            --delete "tool.pdm.dev-dependencies.lab" \
            --delete "tool.pdm.dev-dependencies.dev";

    elif [ "$1" = "prod" ]; then
        rolling-pin toml $CONFIG_DIR/pyproject.toml \
            --edit "project.requires-python=\">=$MIN_PYTHON_VERSION\"" \
            --delete "tool.pdm.dev-dependencies.lab" \
            --delete "tool.pdm.dev-dependencies.dev";

    elif [ "$1" = "package" ]; then
        rolling-pin toml $CONFIG_DIR/pyproject.toml \
            --edit "project.requires-python=\">=$MIN_PYTHON_VERSION\"" \
            --delete "tool.pdm.dev-dependencies" \
            --delete "tool.mypy" \
            --delete "tool.pytest";
    fi;
}

_x_gen_pdm_files () {
    # Generate pyproject.tom, pdm.toml and pdm.lock files
    # args: mode, python version

    # pyproject.toml
    _x_gen_pyproject $1 > $PDM_DIR/pyproject.toml;

    # pdm.lock
    rm -f $PDM_DIR/pdm.lock;
    cp -f $CONFIG_DIR/$1.lock $PDM_DIR/pdm.lock;

    # .pdm-python
    _x_env_get_python $1 $2 > $PDM_DIR/.pdm-python;

    # pdm.toml
    rolling-pin toml $CONFIG_DIR/pdm.toml \
        --edit "venv.prompt=\"$1-{python_version}\"" \
        --target $PDM_DIR/pdm.toml;
}

_x_set_uv_vars () {
    # Set UV environment variables
    # args: mode, python_version
    export UV_PROJECT_ENVIRONMENT=`find $PDM_DIR/envs -maxdepth 1 -type d | grep $1-$2`;
}

# ENV-FUNCTIONS-----------------------------------------------------------------
_x_env_exists () {
    # determines if given env exists
    # args: environment name
    cd $PDM_DIR;
    local temp=`pdm venv list | grep $1`;
    if [ -n "$temp" ]; then
        echo "true";
    else
        echo "false";
    fi;
}

_x_env_get_path () {
    # gets path of given environment
    # args: environment name
    cd $PDM_DIR;
    pdm venv list | grep $1 | awk '{print $3}';
}

_x_env_get_python () {
    # gets python interpreter path of given environment
    # args: mode, python version
    local penv=`_x_env_get_path $1-$2`;
    if [ -n "$penv" ]; then
        echo $penv;
    else
        echo /usr/bin/python$2;
    fi;
}

_x_env_create () {
    # Create a virtual env given a mode and python version
    # args: mode, python_version
    cd $PDM_DIR;
    _x_gen_pdm_files $1 $2;
    pdm venv create -n $1-$2;
}

x_env_activate () {
    # Activate a virtual env given a mode and python version
    # args: mode, python_version
    local CWD=`pwd`;
    cd $PDM_DIR;
    _x_gen_pdm_files $1 $2;
    . `pdm venv activate $1-$2 | awk '{print $2}'`;
    _x_set_uv_vars $1 $2;
    cd $CWD;
}

_x_env_lock () {
    # Resolve dependencies listed in pyrproject.toml into a pdm.lock file
    # args: mode, python_version
    cd $PDM_DIR;
    x_env_activate $1 $2 && \
    pdm lock -v && \
    cat $PDM_DIR/pdm.lock > $CONFIG_DIR/$1.lock;
}

_x_env_sync () {
    # Install dependencies from a pdm.lock into a virtual env specified by a
    # given mode and python version
    # args: mode, python_version
    cd $PDM_DIR;
    x_env_activate $1 $2 && \
    # run `pdm lock`` if lock file is empty
    if [ `cat pdm.lock | wc -l` = 0 ]; then
        pdm lock -v;
        exit_code=`_x_resolve_exit_code $exit_code $?`;
    fi;
    pdm sync --no-self --dev --clean -v;
    exit_code=`_x_resolve_exit_code $exit_code $?`;
    deactivate;
    return $exit_code;
}

x_env_activate_dev () {
    # Activates dev environment
    x_env_activate dev $MAX_PYTHON_VERSION;
}

x_env_activate_prod () {
    # Activates prod environment
    x_env_activate prod $MAX_PYTHON_VERSION;
}

x_env_init () {
    # Create a virtual env with dependencies given a mode and python version
    # args: mode, python_version
    cd $PDM_DIR;
    _x_env_create $1 $2;
    exit_code=`_x_resolve_exit_code $exit_code $?`;
    _x_env_sync $1 $2;
    exit_code=`_x_resolve_exit_code $exit_code $?`;
    return $exit_code;
}

# BUILD-FUNCTIONS---------------------------------------------------------------
_x_build () {
    # Build repo for testing, packaging and publishing
    # args: type (test or prod)
    x_env_activate_dev;
    rm -rf $BUILD_DIR;
    rolling-pin conform \
        $CONFIG_DIR/build.yaml \
        --groups base,$1;
    exit_code=`_x_resolve_exit_code $exit_code $?`;
    _x_gen_pyproject $1 > $BUILD_DIR/repo/pyproject.toml;
    exit_code=`_x_resolve_exit_code $exit_code $?`;
    touch $BUILD_DIR/repo/$REPO_SNAKE_CASE/py.typed;
    return $exit_code;
}

_x_build_show_dir () {
    # Run tree command on build directory
    exa --tree --all $BUILD_DIR;
    echo;
}

_x_build_show_package () {
    # Run tree command on untarred pip package
    cd $BUILD_DIR/dist;
    mkdir /tmp/dist;
    local package=`ls | grep tar.gz`;
    tar xvf $package -C /tmp/dist;
    echo "\n${CYAN2}$package${CLEAR}";
    exa --tree --all /tmp/dist;
    rm -rf /tmp/dist;
    echo;
}

x_build_package () {
    # Generate pip package of repo in $HOME/build/repo
    x_env_activate_dev;
    x_build_prod;
    cd $BUILD_DIR/repo;
    echo "${CYAN2}BUILDING PIP PACKAGE${CLEAR}\n";
    pdm build --dest $BUILD_DIR/dist -v;
    rm -rf $BUILD_DIR/repo/build;
    _x_build_show_package;
}

x_build_local_package () {
    # Generate local pip package in docker/dist
    x_build_package;
    cd $BUILD_DIR/dist;
    local package=`ls | grep tar.gz`;
    mkdir -p $REPO_DIR/docker/dist;
    cp $package $REPO_DIR/docker/dist/pkg.tar.gz;
}

x_build_edit_prod_dockerfile () {
    # Edit prod.dockefile for local build development
    sed --in-place -E \
        's/ARG VERSION/COPY \--chown=ubuntu:ubuntu dist\/pkg.tar.gz \/home\/ubuntu\/pkg.tar.gz/' \
        $REPO_DIR/docker/prod.dockerfile;
    sed --in-place -E \
        's/--user.*==\$VERSION/--user \/home\/ubuntu\/pkg.tar.gz/' \
        $REPO_DIR/docker/prod.dockerfile;
}

x_build_prod () {
    # Build production version of repo for publishing
    echo "${CYAN2}BUILDING PROD REPO${CLEAR}\n";
    _x_build prod;
    _x_gen_pyproject package > $BUILD_DIR/repo/pyproject.toml;
    _x_build_show_dir;
}

_x_build_publish () {
    # Publish pip package of repo to PyPi
    # args: user, token, comment, url
    x_build_package;
    cd $BUILD_DIR;
    echo "${CYAN2}PUBLISHING PIP PACKAGE TO PYPI${CLEAR}\n";
    pdm publish \
        --no-build \
        --username "$1" \
        --password "$2" \
        --comment "$3" \
        --repository "$4" \
        --verbose;
}

x_build_publish () {
    # Run production tests first then publish pip package of repo to PyPi
    # args: token
    local version=`_x_get_version`;
    _x_build_publish __token__ $1 $version $PYPI_URL;
}

x_build_publish_test () {
    # Run tests and then publish pip package of repo to test PyPi
    # args: token
    local version=`_x_get_version`;
    _x_build_publish __token__ $1 $version $PYPI_TEST_URL;
}

x_build_test () {
    # Build test version of repo for prod testing
    echo "${CYAN2}BUILDING TEST REPO${CLEAR}\n";
    _x_build test;
    _x_build_show_dir;
}
{%- endraw %}
{% if cc.package_registry == 'gitlab' %}
x_build_unpublish () {
    # Remove current version pip package from package registry
    # args: token
    local version=`_x_get_version`;
    echo "${CYAN2}DELETING PIP PACKAGE VERSION: $version${CLEAR}\n";
    local package_id=` \
        curl \
            --silent \
            --request GET \
            --data "sort=desc" \
            --url "$GIT_PROJECT_URL/packages" \
            --header "PRIVATE-TOKEN: $1" \
        | jq ".[] | select(.version == \"$version\") | .id" \
    `;
    curl \
        --silent \
        --request DELETE \
        --url "$GIT_PROJECT_URL/packages/$package_id" \
        --header "PRIVATE-TOKEN: $1";
    echo "${GREEN2}PIP PACKAGE DELETED${CLEAR}";
}
{% endif %}
{%- raw %}
# DOCS-FUNCTIONS----------------------------------------------------------------
x_docs () {
    # Generate documentation
    x_env_activate_dev;
    local exit_code=$?;
    cd $REPO_DIR;
    echo "${CYAN2}GENERATING DOCS${CLEAR}\n";
    rm -rf $DOCS_DIR;
{%- endraw -%}
{%- if cc.include_mkdocs == 'yes' %}
    mkdocs build --config-file mkdocs/mkdocs.yml;
    exit_code=`_x_resolve_exit_code $exit_code $?`;
{%- endif %}
    mkdir -p {{sphinx_dir}};
    cp $REPO_DIR/README.md $REPO_DIR/sphinx/readme.md;
    sed --in-place -E 's/sphinx\/images/_images/g' $REPO_DIR/sphinx/readme.md;
    sphinx-build sphinx {{sphinx_dir}};
    exit_code=`_x_resolve_exit_code $exit_code $?`;
    rm -f $REPO_DIR/sphinx/readme.md;
    cp -f sphinx/style.css {{sphinx_dir}}/_static/style.css;
    touch {{sphinx_dir}}/.nojekyll;
{%- raw %}
    # mkdir -p $DOCS_DIR/resources;
    # cp resources/* $DOCS_DIR/resources/;
    # mkdir -p $DOCS_DIR/_images/;
    # cp sphinx/images/logo.png $DOCS_DIR/_images/;
    exit_code=`_x_resolve_exit_code $exit_code $?`;
    return $exit_code;
}

x_docs_architecture () {
    # Generate architecture.svg diagram from all import statements
    echo "${CYAN2}GENERATING ARCHITECTURE DIAGRAM${CLEAR}\n";
    x_env_activate_dev;
    rolling-pin graph \
{%- endraw -%}
{%- if cc.include_mkdocs == 'yes' %}
        $REPO_DIR/python $DOCS_DIR/python/architecture.svg \
{%- else %}
        $REPO_DIR/python $DOCS_DIR/architecture.svg \
{%- endif %}
{%- raw %}
        --exclude 'test|mock|__init__' \
        --orient 'lr';
}

x_docs_full () {
    # Generate documentation, coverage report, architecture diagram and code
    # metrics
    x_docs && x_docs_metrics && x_docs_architecture && x_test_coverage;
}

x_docs_metrics () {
    # Generate code metrics report, plots and tables
    echo "${CYAN2}GENERATING METRICS${CLEAR}\n";
    x_env_activate_dev;
    cd $REPO_DIR;
{%- endraw -%}
{%- if cc.include_mkdocs == 'yes' %}
    rolling-pin plot \
        $REPO_DIR/python $DOCS_DIR/python/plots.html;
    rolling-pin table \
        $REPO_DIR/python $DOCS_DIR/python;
{%- else %}
    rolling-pin plot \
        $REPO_DIR/python $DOCS_DIR/plots.html;
    rolling-pin table \
        $REPO_DIR/python $DOCS_DIR;
{%- endif %}
{%- raw %}
}

# LIBRARY-FUNCTIONS-------------------------------------------------------------
_x_library_pdm_to_repo_dev () {
    # Copies pdm/pyproject.toml and pdm/pdm.lock to repo's pyproject.toml and
    # dev.lock files
    cp -f $PDM_DIR/pdm.lock $CONFIG_DIR/dev.lock;
    cat $PDM_DIR/pyproject.toml \
        | sed -E "s/name.*$REPO-dev.*/name = \"$REPO\"/" \
        > $CONFIG_DIR/pyproject.toml;
}

_x_library_pdm_to_repo_prod () {
    # Copies pdm/pdm.lock to repo's prod.lock
    cp -f $PDM_DIR/pdm.lock $CONFIG_DIR/prod.lock;
}

_x_library_sync () {
    # Sync lock with given environment
    # args: mode, python_version
    x_env_activate $1 $2;
    echo "${CYAN2}DEPENDENCY SYNC $1-$2${CLEAR}\n";
    cd $PDM_DIR;
    pdm sync --no-self --dev --clean -v;
    deactivate;
    x_env_activate_dev;
}

x_library_add () {
    # Add a given package to a given dependency group
    # args: package, group
    x_env_activate_dev;
    echo "${CYAN2}ADDING PACKAGE TO DEV DEPENDENCIES${CLEAR}\n";
    cd $PDM_DIR;
    if [ "$2" = '' ] || [ "$2" = 'default' ]; then
        pdm add --no-self $1 -v;
    else
        pdm add --no-self -dG $2 $1 -v;
    fi;
    _x_library_pdm_to_repo_dev;
    echo "${GREEN2}LIBRARY ADD COMPLETE${CLEAR}";
}

x_library_graph_dev () {
    # Graph dependencies in dev environment
    x_env_activate_dev;
    echo "${CYAN2}DEV DEPENDENCY GRAPH${CLEAR}\n";
    cd $PDM_DIR;
    pdm list --graph;
}

x_library_graph_prod () {
    # Graph dependencies in prod environment
    x_env_activate_prod;
    echo "${CYAN2}PROD DEPENDENCY GRAPH${CLEAR}\n";
    cd $PDM_DIR;
    pdm list --graph;
    deactivate;
    x_env_activate_dev;
}

x_library_install_dev () {
    # Install all dependencies into dev environment
    x_library_lock_dev;
    x_library_sync_dev;
    echo "${GREEN2}LIBRARY INSTALL DEV COMPLETE${CLEAR}";
}

x_library_install_prod () {
    # Install all dependencies into prod environment
    x_library_lock_prod;
    x_library_sync_prod;
    echo "${GREEN2}LIBRARY INSTALL PROD COMPLETE${CLEAR}";
}

x_library_list_dev () {
    # List packages in dev environment
    x_env_activate_dev;
    echo "${CYAN2}DEV DEPENDENCIES${CLEAR}\n";
    cd $PDM_DIR;
    pdm list --sort name --fields name,version,groups;
}

x_library_list_prod () {
    # List packages in prod environment
    x_env_activate_prod;
    echo "${CYAN2}PROD DEPENDENCIES${CLEAR}\n";
    cd $PDM_DIR;
    pdm list --sort name --fields name,version,groups;
    deactivate;
    x_env_activate_dev;
}

x_library_lock_dev () {
    # Resolve dev.lock file
    x_env_activate_dev;
    echo "${CYAN2}DEV DEPENDENCY LOCK${CLEAR}\n";
    cd $PDM_DIR;
    pdm lock -v;
    _x_library_pdm_to_repo_dev;
    echo "${GREEN2}LIBRARY LOCK COMPLETE${CLEAR}";
}

x_library_lock_prod () {
    # Resolve prod.lock file
    x_env_activate_prod;
    echo "${CYAN2}PROD DEPENDENCY LOCK${CLEAR}\n";
    cd $PDM_DIR;
    pdm lock -v;
    _x_library_pdm_to_repo_prod;
    echo "${GREEN2}LIBRARY LOCK COMPLETE${CLEAR}";
    deactivate;
    x_env_activate_dev;
}

x_library_remove () {
    # Remove a given package from a given dependency group
    # args: package, group
    x_env_activate_dev;
    echo "${CYAN2}REMOVING PACKAGE FROM DEV DEPENDENCIES${CLEAR}\n";
    cd $PDM_DIR;
    if [ "$2" = '' ] || [ "$2" = 'default' ]; then
        pdm remove --no-self $1 -v;
    else
        pdm remove --no-self -dG $2 $1 -v;
    fi;
    _x_library_pdm_to_repo_dev;
    echo "${GREEN2}LIBRARY REMOVE COMPLETE${CLEAR}";
}

x_library_search () {
    # Search for pip packages
    # args: package name
    x_env_activate_dev;
    cd $PDM_DIR;
    pdm search $1;
}

x_library_sync_dev () {
    # Sync dev environment with packages listed in dev.lock
    echo "${CYAN2}SYNC DEV DEPENDENCIES${CLEAR}\n";
    _x_library_sync dev $MAX_PYTHON_VERSION;
    echo "${GREEN2}LIBRARY SYNC DEV COMPLETE${CLEAR}";
}

x_library_sync_prod () {
    # Sync prod environment with packages listed in prod.lock
    echo "${CYAN2}SYNC PROD DEPENDENCIES${CLEAR}\n";
    _x_for_each_version '_x_library_sync prod $VERSION';
    echo "${GREEN2}LIBRARY SYNC PROD COMPLETE${CLEAR}";
}

x_library_update () {
    # Update a given package, or all packages, from a given dependency group
    # args: package, group
    x_env_activate_dev;
    echo "${CYAN2}UPDATING DEV DEPENDENCIES${CLEAR}\n";
    cd $PDM_DIR;
    if [ "$2" = '' ] || [ "$2" = 'default' ]; then
        pdm update --no-self $1 -v;
    else
        pdm update --no-self -dG $2 $1 -v;
    fi;
    _x_library_pdm_to_repo_dev;
    echo "${GREEN2}LIBRARY UPDATE COMPLETE${CLEAR}";
}

x_library_update_pdm () {
    # Update PDM in all environments
    echo "${CYAN2}UPDATE PDM${CLEAR}\n";
{%- endraw %}
    pip3.{{ cc.python_max_version }} install --user --upgrade pdm;
{%- raw %}
    echo "${GREEN2}LIBRARY UPDATE COMPLETE${CLEAR}";
}

# QUICKSTART-FUNCTIONS----------------------------------------------------------
x_quickstart () {
    # Display quickstart guide
    echo "${CYAN2}QUICKSTART GUIDE${CLEAR}\n";
    cat $REPO_DIR/README.md \
    | grep -A 10000 '# Quickstart' \
    | grep -B 10000 '# Development CLI' \
    | grep -B 10000 -E '^---$' \
    | grep -vE '^---$' \
    | grep -v '# Quickstart';
}

# SESSION-FUNCTIONS-------------------------------------------------------------
x_session_lab () {
    # Run jupyter lab server
    x_env_activate_dev;
    echo "${CYAN2}JUPYTER LAB${CLEAR}\n";
    jupyter lab \
        --allow-root \
        --ip=0.0.0.0 \
        --no-browser;
}

x_session_python () {
    # Run python session with dev dependencies
    x_env_activate_dev;
    python3;
}

x_session_server () {
    # Run application server
    x_env_activate_dev;
    echo "${CYAN2}SERVER${CLEAR}\n";
    python3 $REPO_SUBPACKAGE/server/app.py;
}

# TEST-FUNCTIONS----------------------------------------------------------------
x_test_coverage () {
    # Generate test coverage report
    x_env_activate_dev;
    echo "${CYAN2}GENERATING TEST COVERAGE REPORT${CLEAR}\n";
    rm -rf /tmp/coverage;
    mkdir /tmp/coverage;
    cd /tmp/coverage;
    pytest \
        --config-file $CONFIG_DIR/pyproject.toml \
        --maxprocesses $TEST_MAX_PROCS \
        --numprocesses $TEST_PROCS \
        --verbosity $TEST_VERBOSITY \
        --cov=$REPO_DIR/python \
        --cov-config=$CONFIG_DIR/pyproject.toml \
{%- endraw -%}
{%- if cc.include_mkdocs == 'yes' %}
        --cov-report=html:$DOCS_DIR/python/htmlcov \
{%- else %}
        --cov-report=html:$DOCS_DIR/htmlcov \
{%- endif %}
{%- raw %}
        $REPO_SUBPACKAGE;
{%- endraw %}
    exit_code=$?;
{%- if cc.include_mkdocs == 'yes' %}
    rm -f $DOCS_DIR/python/htmlcov/.gitignore;
{%- else %}
    rm -f $DOCS_DIR/htmlcov/.gitignore;
{%- endif %}
    return $exit_code;
{%- raw %}
}

x_test_dev () {
    # Run all tests
    x_env_activate_dev;
    echo "${CYAN2}TESTING DEV${CLEAR}\n";
    cd $REPO_DIR;
    pytest \
        --config-file $CONFIG_DIR/pyproject.toml \
        --maxprocesses $TEST_MAX_PROCS \
        --numprocesses $TEST_PROCS \
        --verbosity $TEST_VERBOSITY \
        --durations 20 \
        $REPO_SUBPACKAGE;
}

x_test_fast () {
    # Test all code excepts tests marked with SKIP_SLOWS_TESTS decorator
    x_env_activate_dev;
    echo "${CYAN2}FAST TESTING DEV${CLEAR}\n";
    cd $REPO_DIR;
    SKIP_SLOW_TESTS=true \
    pytest \
        --config-file $CONFIG_DIR/pyproject.toml \
        --maxprocesses $TEST_MAX_PROCS \
        --numprocesses $TEST_PROCS \
        --verbosity $TEST_VERBOSITY \
        $REPO_SUBPACKAGE;
}

x_test_format () {
    # Run ruff formatting on all python code
    x_env_activate_dev;
    echo "${CYAN2}FORMATTING${CLEAR}\n";
    ruff format --config $CONFIG_DIR/pyproject.toml python;
}

x_test_lint () {
    # Run linting and type checking
    x_env_activate_dev;
    local exit_code=$?;
    cd $REPO_DIR;

    echo "${CYAN2}LINTING${CLEAR}";
    ruff check --config $CONFIG_DIR/pyproject.toml python;
    exit_code=`_x_resolve_exit_code $exit_code $?`;

    echo "\n${CYAN2}TYPE CHECKING${CLEAR}\n";
    mypy python --config-file $CONFIG_DIR/pyproject.toml;
    exit_code=`_x_resolve_exit_code $exit_code $?`;

    return $exit_code;
}

x_test_run () {
    # Run test in given environment
    # args: mode, python_version
    x_env_activate $1 $2;
    local exit_code=$?;

    cd $BUILD_DIR/repo;
    echo "${CYAN2}LINTING $1-$2${CLEAR}\n";
    ruff check --config $CONFIG_DIR/pyproject.toml $REPO_SUBPACKAGE;
    exit_code=`_x_resolve_exit_code $exit_code $?`;

    echo "${CYAN2}TYPE CHECKING $1-$2${CLEAR}\n";
    mypy --config-file pyproject.toml $REPO_SUBPACKAGE;
    exit_code=`_x_resolve_exit_code $exit_code $?`;

    echo "${CYAN2}TESTING $1-$2${CLEAR}\n";
    pytest \
        --config-file pyproject.toml \
        --maxprocesses $TEST_MAX_PROCS \
        --numprocesses $TEST_PROCS \
        --verbosity $TEST_VERBOSITY \
        $REPO_SUBPACKAGE;
    exit_code=`_x_resolve_exit_code $exit_code $?`;

    deactivate;
    x_env_activate_dev;
    return $exit_code;
}

x_test_prod () {
    # Run tests across all support python versions
    x_env_activate_dev;
    x_build_test;
    _x_for_each_version 'x_test_run prod $VERSION';
}

# VERSION-FUNCTIONS-------------------------------------------------------------
_x_get_version () {
    # get current pyproject version
    cat $CONFIG_DIR/pyproject.toml \
        | grep -E '^version *=' \
        | awk '{print $3}' \
        | sed 's/\"//g';
}
{% endraw -%}

{%- if cc.include_mkdocs == 'yes' %}
_x_version_file_update () {
    # update non-pyproject files with new pyproject version
    # args: old_version, new_version
    sed --in-place -E "s/$1/$2/g" $MKDOCS_DIR/mkdocs.yml;
}
{% endif %}

{%- raw %}
x_version () {
    # Full resolution of repo: dependencies, linting, tests, docs, etc
    x_library_install_dev;
    x_test_lint;
    x_docs_full;
}

_x_version_bump () {
    # Bump repo's version
    # args: type
    x_env_activate_dev;
    local title=`echo $1 | tr '[a-z]' '[A-Z]'`;
    echo "${CYAN2}BUMPING $title VERSION${CLEAR}\n";
{%- endraw -%}
{%- if cc.include_mkdocs == 'yes' %}
    local old_version=`_x_get_version`;
{%- endif %}
    cd $PDM_DIR
    pdm bump $1;
    _x_library_pdm_to_repo_dev;
{%- if cc.include_mkdocs == 'yes' %}
    local new_version=`_x_get_version`;
    sed --in-place -E \
        "s/verbdg-.+-x/verbdg-$new_version-x/" \
        $REPO_DIR/README.md;
    _x_version_file_update $old_version $new_version;
{%- endif %}
{%- raw %}
}

x_version_bump_major () {
    # Bump repo's major version
    _x_version_bump major;
}

x_version_bump_minor () {
    # Bump repo's minor version
    x_env_activate_dev;
    _x_version_bump minor;
}

x_version_bump_patch () {
    # Bump repo's patch version
    _x_version_bump patch;
}

x_version_bump () {
    # Bump repo's patch version up to x.x.20, then bump minor version
    local minor=`python3 -c \
        "v = '$(_x_get_version)'.split('.')[-1]; print(int(v) >= 20)"
    `;
    if [ "$minor" = "True" ]; then
        x_version_bump_minor;
    else
        x_version_bump_patch;
    fi;
}

x_version_commit () {
    # Tag with version and commit changes to master with given message
    # args: message
    local version=`_x_get_version`;
{%- endraw %}
{%- if cc.git_host == 'github' %}
    git commit --message "$version <no ci>";
    git tag --annotate $version --message "$1";
    git push --follow-tags origin HEAD:master;
{%- else %}
    git commit --message "$version";
    git tag --annotate $version --message "$1";
    git push --follow-tags origin HEAD:master --push-option ci.skip;
{%- endif %}
{%- raw %}
}

# VSCODE-FUNCTIONS--------------------------------------------------------------
x_vscode_reinstall_extensions () {
    # Reinstall all VSCode extensions
    echo "${CYAN2}REINSTALLING VSCODE EXTENSIONS${CLEAR}\n";
    cat $REPO_DIR/.devcontainer.json \
        | jq '.customizations.vscode.extensions[]' \
        | sed 's/"//g' \
        | parallel "$VSCODE_SERVER --install-extension {}";
}
{%- endraw %}
