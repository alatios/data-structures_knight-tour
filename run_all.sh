#!/bin/bash
## Runs a large number of knight tour evaluations through slurm on softload partition

NARRAY=(6 8 10 12 20 40 60 80 100 126 150 176 200 224 250 276 300 324 350 376 400 450 500 550 600 624 650 676 700 726 750 776 800 824 850 876 900 924 950 976 1000)

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
