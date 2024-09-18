#! /bin/bash

# exit on error + unboud variable error + debug
set -eux
pwd


load_vars()
{
    # https://stackoverflow.com/questions/46483941/source-configuration-file-avoiding-any-execution?rq=3
    while IFS='=' read -r conf_name conf_value
    do
        if test -z "$conf_name"
        then
            continue
        fi
        export "$conf_name"="$conf_value"
    done
}

poetry_init() 
{
    cd /app
    
    pip config set global.index-url $ASCS_PYPI_REGISTRY_URL
    . $VIRTUAL_ENV/bin/activate

    mkdir -p /app/$SOURCES_ROOT_DIRNAME
    touch /app/$SOURCES_ROOT_DIRNAME/__init__.py

    echo setting up poetry config ...
    # !! certificate name should map to pyproject.toml source name correctly
    # ex, with :
    # 
    # [[tool.poetry.source]]
    # name = "artifactory"
    # url = "https://artifactory.ascs.fr/artifactory/api/pypi/proxy-pypi/simple"
    # priority = "default"
    # 
    # the corresponding setup is : poetry config certificates.artifactory.cert /etc/ssl/cert.pem
    poetry config certificates.proxy-pypi.cert /etc/ssl/cert.pem
    poetry config certificates.ASCS_pypi.cert /etc/ssl/cert.pem
    poetry config certificates.artifactory.cert /etc/ssl/cert.pem
    poetry config virtualenvs.create true

    if [ ! -e "poetry.lock" ]
    then
        echo "\"poetry.lock\" file is missing, building a new one (this can take a lot of time) ..."
        poetry lock -vv
    fi

    poetry show -v

}


echo BUILD_TIME_ENV is : \"$BUILD_TIME_ENV\"

# partie templates dynamiques
if test -e /docker-build.env.template
then
    # on build time this file should contains POETRY_HTTP_BASIC_ASCS_PYPI_USERNAME and POETRY_HTTP_BASIC_ASCS_PYPI_PASSWORD
    # for poetry to access artifactory modules
    cp /docker-build.env.template /docker-build.env
    # set -a avoid exporting each variable
    set -a
    . /docker-build.env
    set +a
    # customize files with tags
    for file in "/docker-build.env"
    do
        echo "customizing $file ..."
        perl -pe 's/\$(\w+)/$ENV{$1}/g' -i $file
        cat "$file"
    done
fi

# loads and exports variables defined inside shell
# https://unix.stackexchange.com/questions/581230/why-doesnt-read-command-work-with-echo-and-piping
load_vars < <(echo "$BUILD_TIME_ENV")

# if build stops here you have to define theses two variables inside 
# BUILD_TIME_ENV
test -n "$POETRY_HTTP_BASIC_ASCS_PYPI_USERNAME"
test -n "$POETRY_HTTP_BASIC_ASCS_PYPI_PASSWORD"

case $1 in
    poetry_install)
        poetry_init
        echo executing poetry install ...
        poetry install --no-cache --no-root --no-interaction --no-ansi --only main
        ;;
    poetry_install_dev)
        poetry_init
        echo executing poetry install ...
        # this require the two groups in pyproject.toml:
        # [tool.poetry.group.test.dependencies]
        # pytest = "^7.4.4"
        # [tool.poetry.group.dev.dependencies]
        #
        poetry install --with dev,test
        ;;
    *)
        echo unknown stage $1
        exit 1
esac