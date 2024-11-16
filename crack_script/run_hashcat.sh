#!/bin/bash
set -e

SOURCE=`basename $0 .sh`

work_path=/media/chenny/share/wifi_crack

LOG_PATH=${work_path}/log
LOG=${LOG_PATH}/${SOURCE}_`date +"%Y%m%d"`.log

mkdir -p ${LOG_PATH}
exec > ${LOG} 2>&1

printf "$0 started at `date`\n" 

cd ${work_path}

dict_path=${work_path}/phone.dict
cap_path=${work_path}/caps
cap=48:7D:2E:1C:05:EA.cap-01.cap

echo "Work path: ${work_path}"
echo "Dictionary file: ${dict_path}"

cap_name=$(basename ${cap} .cap)

hc22000_file=${cap_path}/${cap_name}.hc22000
if [ -f ${hc22000_file} ]; then
    echo "Generate hc22000 hash file"
    hcxpcapngtool -o ${hc22000_file} ${cap_path}/${cap_name}.cap 
    echo "Generated: "
    ls -l ${hc22000_file}
else
    echo "hc22000 hash file found, skip generating"
fi

echo "Show phone dictionary"
ls -l ${dict_path}

if [ -f ${work_path}/${cap_name}.restore ]; then
    echo "Restore file exists..."
    hashcat --session ${cap_name} \
     -w 4 \
    --restore \
    --restore-file-path=${work_path}/${cap_name}.restore
else
    echo "Kicking off hashcat..."
    hashcat -m 22000 -w 3 --hwmon-disable \
    --session ${cap_name} --status --status-timer 10 \
    --restore-file-path=${work_path}/${cap_name}.restore \
    ${hc22000_file} \
    ${dict_path} \
    -o ${work_path}/${cap_name}_key.txt --potfile-path ${work_path}/${cap_name}.potfile
fi

printf "$0 finished at `date`\n"