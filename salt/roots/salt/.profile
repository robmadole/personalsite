# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
      . "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

export PATH=./scripts:$PATH

export SECRETENVS="/vagrant/.secretenvs"
export PYTHONDONTWRITEBYTECODE=1
export PERSONALSITE_SETTINGS_FILE="{{ settings_file }}"

if [ -f "$SECRETENVS" ] ; then
    source $SECRETENVS
else
    echo "Missing $SECRETENVS to hold the secret environment" \
         "variables that should not be public. This needs to" \
         "be created manually."
fi

if [ -d "/vagrant" ] ; then
    cd /vagrant
fi
