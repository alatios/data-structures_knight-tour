#!/bin/bash
## Script that parses results stored in outputs/ folder in a readable table

OUTPUTFILE="time_results.txt"

echo -e "n\ttime" > ${OUTPUTFILE};

grep "Path found" outputs/out* \
	| awk '{gsub("outputs/out_","");print}' \
	| awk '{gsub(".txt:Path found in","\t");print}' \
	| awk '{gsub(" seconds.","");print}' \
	>> ${OUTPUTFILE};

exit 0
