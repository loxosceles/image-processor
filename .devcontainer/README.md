# Devcontainer Configuration Template

This template provides a blueprint for a development container for Javascript and Python based projects.

This template includes [Chezmoi](https://www.chezmoi.io/) to automatically pull your own dot files.

## How to setup 

**NOTE**: Before starting make sure that you have stored an ssh key inside the `${HOME}/.ssh`
folder on your host machine. The keys in here will be read by the ssh-agent of the
dev container and, hence, will be available there. You will need this for the last
step. In case that you store your keys somewhere else or only want to pass in
specific keys, edit the `devcontainer.json` file, modifying the path in the
`initializeCommand`.

- Clone this repo in the root of your project:

```
git clone https://github.com/loxosceles/devcontainer_config_template .devcontainers
```

- Remove the `.git` folder inside `.devcontainer`.

```
rm -rf .devcontainer/.git
```

- Update the `chezmoi.toml` file at the root of this project with your own email address and name.
- Create or locate your own private dotfiles repository in your personal github account.
- Open the devcontainer.json and replace the placeholder under "containerDev -> CHEZMOI_DOTFILES_REPOSITORY" with your dotfiles repository (ssh link, starting with `git@..`).
