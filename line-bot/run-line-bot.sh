#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYFILE=line-bot.py

#python $DIR/$PYFILE > $DIR/$PYFILE.`date +%F`.log 2>&1
python $DIR/$PYFILE 2>&1

exit
#ps auxw | grep line-bot.py | grep -v grep
if [ ! "`ps auxw | grep $PYFILE | grep -v grep`" ] ; then
  #cd $DIR
  nohup python $DIR/$PYFILE > $DIR/$PYFILE.`date +%F`.log 2>&1 &
  #pwd
fi
