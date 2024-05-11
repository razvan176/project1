#!/bin/bash
if [ $# -eq 0 ]; then
    CURRENT_DATE=$(date +'%Y-%m-%d')
    # Calculate the date for the previous day
    PREVIOUS_DAY_DATE=$(date -d "$CURRENT_DATE - 1 day" +'%Y-%m-%d')
else
    PREVIOUS_DAY_DATE=$1
fi

# Create the path using the previous day's date
LOG_PATH="/data/pmta/log/acct-${PREVIOUS_DAY_DATE}-0*.csv"

csvtool namedcol type,timeLogged,vmta,dlvSourceIp,jobId ${LOG_PATH} | grep "^d" | grep -v _inbound | awk -F "," '{print $2" "$3 " " $4 " " $5}' | awk -F ":" '{print $1 " " $3}' | awk -F " " '{print $1 " " $2 " " $4 " "$5 " " $6}' | sort | uniq -c > log_${PREVIOUS_DAY_DATE}.txt

