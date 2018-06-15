#! /bin/bash --


## Verify if we need sudo
[ "$(id -u)" -eq "0" ] && SUDO= || SUDO=sudo


printf '\n## Uninstalling old docker versions\n'
$SUDO apt-get remove docker docker-engine


printf '\n## Installing packages needed for apt to use repository over HTTPS\n'
$SUDO apt-get update && $SUDO apt-get install\
 curl\
 gnupg2\
 ca-certificates\
 apt-transport-https\
 software-properties-common


printf "\n## Adding Docker's official GPG key\n"
$SUDO curl -fsSL https://download.docker.com/linux/debian/gpg | $SUDO apt-key add -
$SUDO apt-key fingerprint 0EBFCD88


printf '\n## Setting up the stable repository\n'
$SUDO add-apt-repository\
 "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"


printf '\n## Installing docker-ce\n'
$SUDO apt-get update && $SUDO apt-get install docker-ce


printf '\n## Installing docker-compose\n'
$SUDO curl -o /usr/local/bin/docker-compose\
 -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-$(uname -s)-$(uname -m) &&\
$SUDO chmod +x /usr/local/bin/docker-compose


printf '\n## Installing command completion\n'
$SUDO curl -o /etc/bash_completion.d/docker-compose\
 -L https://raw.githubusercontent.com/docker/compose/1.16.1/contrib/completion/bash/docker-compose


self=$(whoami)
printf "\n## Added $self to the docker group:\n"
$SUDO usermod -aG docker $self
#newgrp - docker


printf '\n## Installed versions:\n'
docker --version
docker-compose --version
