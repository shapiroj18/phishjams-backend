#!/usr/bin/env bash

# help menu
Help() {
    echo "Initialize your Phish Bot Environment"
    echo
    echo "Syntax: source start-dev-env.sh [-d|p]"
    echo "options:"
    echo "l         Export local variables."
    echo "d         Export development variables."
    echo "p         Export production variables."
}


# flags (this is useful: https://pretzelhands.com/posts/command-line-flags)
for arg in "$@"
do
    case "$arg" in
        -h|--help)
        Help
        return
        ;;
        -l|--local)
        # pull environmental variables for config. -s denotes as shell format. will require login if you aren't logged in to cli.
        # sed replaces "'" with nothing
        export APP_SETTINGS="config.DevelopmentConfig"
        shift
        ;;
        -d|--dev)
        # pull environmental variables for config. -s denotes as shell format. will require login if you aren't logged in to cli.
        # sed replaces "'" with nothing
        export `heroku config -s --app=phishjam-bot-dev | sed 's/'"'"'//g'`
        shift
        ;;
        -p|--prod)
        # pull environmental variables for config. -s denotes as shell format. will require login if you aren't logged in to cli.
        # sed replaces "'" with nothing
        export `heroku config -s --app=phishjam-bot | sed 's/'"'"'//g'`
        shift
        ;;
        \?)
        echo "Error: Invalid Option"
        ;;
    esac
done

# set up venv
{
if [[ "$VIRTUAL_ENV" != "" ]]
then
    deactivate
    python3 -m venv ./venv_phish_bot && . ./venv_phish_bot/bin/activate
    pip install --upgrade pip && pip install -r requirements.txt
else
    python3 -m venv ./venv_phish_bot && . ./venv_phish_bot/bin/activate
    pip install --upgrade pip && pip install -r requirements.txt
fi
} &> /dev/null


# print a cool phish logo
if [[ $(brew help) ]]; then
    if [[ $(brew ls --versions figlet) ]]; then
        figlet -f bulbhead "phish bot"
    else
        echo 'Installing Figlet via Homebrew'
        brew install figlet
        figlet -f bulbhead "phish bot"
    fi
else
    echo 'Install Homebrew if you want fun features at brew.sh'
fi