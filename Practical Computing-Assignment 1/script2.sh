longest="00:00:00"
longestjname="" 

for FILE in `find . -name 'stdout*'`; do
 
       if [ $# -eq 0 ] ; then

                var=` grep 'cput' $FILE `
                btime=$(echo $var | cut -c22-29)
                echo $btime

                var2=` grep 'Job Name' $FILE `
                bjname=$(echo $var2 | cut -c11-)
                echo $bjname

                if [[ "$btime" > "$longest" ]]; then
                        longest=$btime
                        longestjname=$bjname
                fi

        else

            	var=` grep 'cput' $FILE `
                btime=$(echo $var | cut -c22-29)
                echo $btime

                var2=` grep 'Job Name' $FILE `
                bjname=$(echo $var2 | cut -c11-)
                echo $bjname

                if [ "$bjname" = "$1" ]; then

                        if [[ "$btime" > "$longest" ]]; then
                                longest="$btime"
                                longestjname="$bjname"
                        fi
                fi
        fi
done

if [ "$#" -eq "0" ]; then

echo "Maximum CPU time of $longest for job $longestjname "

else

echo "CPU time of $longest for job $longestjname "
fi

