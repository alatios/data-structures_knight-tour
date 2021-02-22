#!/bin/bash
## Runs a large number of knight tour evaluations through slurm on softload partition

NARRAY=(6 8 10 12 20 40 60 100 250 500 1000 2000 5000 10000)

echo "This will overwrite all existing output files. Are you sure you want to run this? y/[n]"
read response

case "$response" in
	[yY][eE][sS]|[yY])
		:
		;;
	*)
		echo "Aborting..."
		exit 3
		;;
esac

rm -rf outputs/out*;

for n in ${NARRAY[@]}; do
	sbatch --partition=softload --nodelist=haas --output=./outputs/out_$n.txt --cpus-per-task=1 --mem-per-cpu=1G --time=2-0:0 --wrap="hostname; python3 main.py $n"
done

exit 0
