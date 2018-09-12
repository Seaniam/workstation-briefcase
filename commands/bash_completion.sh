MY_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Break out the bash versions
bashver=${BASH_VERSION%.*}
bmajor=${bashver%.*}
bminor=${bashver#*.}

# Check for interactive shell.
if [ $bmajor -eq 2  ]; then
    echo "bash-completion not supported!" >&2
    return 1
elif [ $bmajor -eq 3 ]; then
    if [ $IS_OSX == "true" ]; then
        # BASH_COMPLETION_DIR contains a subset of completions that are relevant to OS X
        BASH_COMPLETION="${MY_PATH}/bash_3.x/bash_completion"
        BASH_COMPLETION_DIR="${MY_PATH}/bash_3.x/completions"
        BASH_COMPLETION_COMPAT_DIR="/usr/local/etc/bash_completion.d"
        . $BASH_COMPLETION
    fi
else
    if [ $IS_OSX == "true" ]; then
        # maybe they have something installed here?
        BASH_COMPLETION_COMPAT_DIR="/usr/local/etc/bash_completion.d"
        . $MY_PATH/bash_4.x/darwin/bash_completion
    else
        . $MY_PATH/bash_4.x/linux/bash_completion
    fi
fi

#Include git flow completion if it exists
if [ -f /usr/local/etc/bash_completion.d/git-flow-completion.bash ]; then
    . /usr/local/etc/bash_completion.d/git-flow-completion.bash
fi

#Includ maven bash completion
if [ "${MAVEN_BASH_AUTOCOMPLETE:-true}" == "true" ] ; then
    source $MY_PATH/../maven_bash_completion.bash
fi

unset bashver bminor bmajor MY_PATH
