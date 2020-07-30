#!/bin/bash
#ansible-playbook -v -i  inventories/dev/hosts  install.yml
ansible-playbook -v -i  inventories/dev/hosts  pre-install.yml -t celery

