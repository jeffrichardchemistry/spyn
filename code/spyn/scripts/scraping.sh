grep "TOTAL EN" /home/jefferson/Dropbox/Tutorial/atompy/tmp/energyGA.log | while read -r line ; do
     i=$((i+1))
     echo "Conformer $i: $line"
done
