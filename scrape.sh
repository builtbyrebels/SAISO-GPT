#!/bin/bash

mkdir -p websites
cat sites.txt | xargs -n10 -P4 wget -P specific_folder
