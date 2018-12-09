#!/usr/bin/env bash

# Pull latest changes in the repositories
echo "...updating repository wiseml..."
pwd
git reset --hard HEAD
git clean -f
git pull

echo "...updating repository baselines..."
cd ../baselines/
pwd
git reset --hard HEAD
git clean -f
git pull

echo "...launching wiseml launch_script..."
cd ../wiseml/
pwd

if [ $# -eq 0 ]
  then
    source launch_script.sh
else
    source launch_script.sh "$@"
fi

