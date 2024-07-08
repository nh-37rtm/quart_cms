#! /bin/bash

set -ex
pwd
ls -altr

PATH=$PATH:$VIRTUAL_ENV/bin

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

echo ASCS_RUN_TIME_ENV is : \"$ASCS_RUN_TIME_ENV\"

# partie templates dynamiques
if test -e /app/.env.template
then
    cp /app/.env.template /app/.env
    set -a
    . /app/.env
    set +a
fi

# loads and exports variables defined inside shell
# https://unix.stackexchange.com/questions/581230/why-doesnt-read-command-work-with-echo-and-piping
load_vars < <(echo "$ASCS_RUN_TIME_ENV")

. $VIRTUAL_ENV/bin/activate

echo dumping environement variables ...
env

echo running application ...

if [ "$1" = "wait_forever" ]
then
    echo keeping container up until kill ...
    while true
    do 
        /bin/sleep 10
    done
fi

echo running command "$@" in container environment ...

$@