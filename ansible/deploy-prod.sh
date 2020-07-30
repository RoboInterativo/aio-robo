#!/bin/bash
ansible-playbook -b -K -v -i  inventories/prod/hosts  install.yml
#ansible-playbook -i inventories/prod/hosts -b install.yml
