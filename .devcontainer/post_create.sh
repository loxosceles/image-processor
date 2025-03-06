#!/bin/sh

sudo mkdir -p "$HOME/.config/chezmoi"
# In the Dockerfile we copied the config file to /usr/src
sudo mv /usr/src/chezmoi.toml "$HOME/.config/chezmoi/chezmoi.toml"
sudo chown -R "${USER}:${USER}" "$HOME/.config/chezmoi"

if [ -z "${CHEZMOI_DOTFILES_REPOSITORY}" ]; then
    echo "Please set the CHEZMOI_DOTFILES_REPOSITORY environment variable."
else
    echo "Setting up dotfiles..."
    chezmoi init --apply "${CHEZMOI_DOTFILES_REPOSITORY}"
fi
