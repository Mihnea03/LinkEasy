#! /bin/bash

FILE_NAME="requirements.txt"

python3 -m pip freeze > $FILE_NAME

while read line; do
    python3 -m pip install $line
done < $FILE_NAME

chmod +x run.sh
source link_easy_env/bin/activate

echo -e Project\ is\ ready\ to\ start!\\nExecute\ run.sh\ to\ start\ the\ server!;

rm $FILE_NAME