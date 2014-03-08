#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR
while read p; do
    echo "installing ${p}"
    sudo apt-get install $p -y
done < $DIR/apt-get_list.txt

pip install -r $DIR/base-python.txt

