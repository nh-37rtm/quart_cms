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


echo "activating venv ($VIRTUAL_ENV)" ...
. $VIRTUAL_ENV/bin/activate
echo "loading vars for build environment ..."

# loads and exports variables defined inside shell
# https://unix.stackexchange.com/questions/581230/why-doesnt-read-command-work-with-echo-and-piping
# in the dev container the build environement should be available
load_vars < <(echo "$ASCS_BUILD_TIME_ENV")
# these should be available from build layer
