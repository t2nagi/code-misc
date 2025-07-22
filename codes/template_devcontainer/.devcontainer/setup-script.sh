#!/bin/bash

# Update packages
sudo apt-get -y update && sudo apt-get -y upgrade

# Check if alias settings already exist
if ! grep -q 'alias g="git"' ~/.bashrc; then
    echo 'alias g="git"' >> ~/.bashrc
    echo 'alias gs="git status"' >> ~/.bashrc
    echo 'alias gc="git commit"' >> ~/.bashrc
    echo 'alias gp="git push"' >> ~/.bashrc
    echo 'alias gl="git log"' >> ~/.bashrc
    echo 'alias gd="git diff"' >> ~/.bashrc
    echo 'alias gco="git checkout"' >> ~/.bashrc
    echo 'alias gb="git branch"' >> ~/.bashrc
    echo 'alias ga="git add"' >> ~/.bashrc

    # Docker aliases
    echo 'alias d="docker"' >> ~/.bashrc
    echo 'alias dc="docker-compose"' >> ~/.bashrc
    echo 'alias dps="docker ps"' >> ~/.bashrc
    echo 'alias dex="docker exec"' >> ~/.bashrc

    # Other useful aliases
    echo 'alias ll="ls -la"' >> ~/.bashrc
    echo 'alias ..="cd .."' >> ~/.bashrc
    echo 'alias ...="cd ../.."' >> ~/.bashrc
    echo 'alias h="history"' >> ~/.bashrc

    # Apply aliases immediately
    source ~/.bashrc
    
    echo "Aliases have been configured"
else
    echo "Aliases are already configured"
fi

