#!/bin/bash
git pull
ansible-playbook -v -i  inventories/dev/hosts  install.yml
