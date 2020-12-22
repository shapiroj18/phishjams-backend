#!/usr/bin/env bash

# pull environmental variables for config. -s denotes as shell format. will require login if you aren't logged in to cli.
# sed replaces "'" with nothing
export `heroku config -s --app=phish-telegram-bot | sed 's/'"'"'//g'`

# export other required variables
export FLASK_APP=phish_bot.py

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

# flags (this is useful: https://pretzelhands.com/posts/command-line-flags)

for arg in "$@"
do
    case "$arg" in
        -p|--phish)
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
        shift
        ;;
    esac
done