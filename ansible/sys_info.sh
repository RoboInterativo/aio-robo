#!/bin/bash
ansible-playbook -v  -b -K  -i inventories/prod/hosts  it.yml
