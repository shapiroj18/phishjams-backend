#!/usr/bin/env bash

## have it start docker compose

# help menu
Help() {
    echo "Initialize your Phish Bot Environment"
    echo
    echo "Syntax: source start-dev-env.sh [-l|d|p]"
    echo "options:"
    echo "-l|--local       Export local variables."
    echo "-d|--dev         Export development variables."
    echo "-p|--prod        Export production variables."
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
        echo "Local environmental variables loaded from .env file"
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

# set up ngrok 8443 for telegram webhook
echo 'Stopping any existing ngrok instances'
killall ngrok
echo 'Starting ngrok on port 8443 for telegram bot webhook'
ngrok http 8443 -log=stdout &

# set environmental variable of APP_URL from ngrok
URL=$(curl --silent http://localhost:4040/api/tunnels | jq ".tunnels[].public_url" | grep "https:*" | tr -d '"')
export WEB_URL=$URL/

# turn on docker-compose
docker-compose up --remove-orphans