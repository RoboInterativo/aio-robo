#!/bin/bash
ansible-playbook -b -K -v -i  inventories/prod/hosts  it.yml
