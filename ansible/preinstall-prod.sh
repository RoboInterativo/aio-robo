#!/bin/bash
ansible-playbook  -b -v -i  inventories/prod/hosts  pre-install.yml
