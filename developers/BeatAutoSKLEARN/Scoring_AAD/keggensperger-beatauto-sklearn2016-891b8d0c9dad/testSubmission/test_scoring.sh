#! /bin/bash

if [ ! -e $1 ]
then
    echo $1 is not a file
fi

rm program -rf
mkdir program
cp $1 program

cd program
unzip Beat*.zip > /dev/null
cd ..

for JSON in $2/hp*.json.zip
do
    echo "HANDLING $JSON"
    rm res -rf
    rm output -rf
    rm hp.json *.zip

    echo "make dir"
    mkdir res
    mkdir output

    cp $JSON res/

    cd res/
    unzip *.zip
    cd ..

    export PATH=/mhome/aad/automl_2015/anaconda2/bin:$PATH
    echo "Starting new configuration at $(date "+%Y.%m.%d-%H.%M.%S")"
    time python program/score.py ./ output/ 3>&1 1>output/log.txt 2>&1
    echo "Finished configuration at $(date "+%Y.%m.%d-%H.%M.%S")"

    if ! grep -q "set1_score: 0." output/scores.txt
    then
        echo "No Score calculated. Keep output!"
        current_time=$(date "+%Y.%m.%d-%H.%M.%S")
        mv res output/
        mv output output_${current_time}
    
    elif grep -q "Unexpected exception" output/scores.txt
    then
        echo "Unexpected exception. Keep output!"
        current_time=$(date "+%Y.%m.%d-%H.%M.%S")
        mv res output/
        mv output output_${current_time}
    
    elif grep -q "timeout" output/scores.txt
    then
        echo "Timeout. Keep output!"
        current_time=$(date "+%Y.%m.%d-%H.%M.%S")
        mv res output/
        mv output output_${current_time}
    
    elif grep -q "memory limit" output/scores.txt
    then
        echo "Memory limit. Keep output!"
        current_time=$(date "+%Y.%m.%d-%H.%M.%S")
        mv res output/
        mv output output_${current_time}
    fi
done
