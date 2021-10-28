k=$(grep "OpenBabel" $PWD/tmp/output.sdf | wc -l)
babel=$(grep "OpenBabel" $PWD/tmp/output.sdf | head -1)
for counter in $(seq 1 $k); do sed -i "0,/$babel/s/$babel/Conformer $counter/" $PWD/tmp/output.sdf ;done


