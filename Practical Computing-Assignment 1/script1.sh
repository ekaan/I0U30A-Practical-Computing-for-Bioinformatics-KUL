for FILE in `find . -name 'stderr*'`; do

echo $FILE;

if ( grep -q 'Error' $FILE ) || ( grep -q 'error' $FILE ) then

echo 'Found!'
echo $FILE | cut -c 20-27  >> error_jobID.txt

fi

done;

ct=($(wc -l error_jobID.txt))
lineN=${ct[0]}

echo "Words(Error, error) found in $lineN files!"
