#!/bin/bash
set -e

SOURCE=`basename $0 .sh`

work_path=/media/chenny/share/wifi_crack

LOG_PATH=${work_path}/log
LOG=${LOG_PATH}/${SOURCE}_`date +"%Y%m%d"`.log

mkdir -p ${LOG_PATH}

usage() {
    echo "Usage: $0 --cap <cap_file>, e.g. $0 --cap test.cap"
    exit 1
}

# Parse command-line arguments
if [[ $# -lt 2 ]]; then
    usage
    exit 1
fi

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --cap)
            cap="$2"
            shift # past argument
            shift # past value
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

if [ -z "$cap" ]; then
    echo "Usage: $0 --cap <cap_file>"
    exit 1
fi


exec > ${LOG} 2>&1
printf "$0 started at `date`\n" 

cd ${work_path}

dict_path=${work_path}/dict/8_digits_phone.dict
cap_path=${work_path}/caps

echo "Cap file: ${cap}"
echo "Work path: ${work_path}"
echo "Dictionary file: ${dict_path}"

cap_name=$(basename ${cap} .cap)

hc22000_file=${cap_path}/${cap_name}.hc22000
if [ -f ${hc22000_file} ]; then
    echo "hc22000 hash file found, skip generating"

else
    echo "Generate hc22000 hash file"
    hcxpcapngtool -o ${hc22000_file} ${cap_path}/${cap_name}.cap 
    echo "Generated: "
    ls -l ${hc22000_file}
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
    --potfile-path=${LOG_PATH}/${cap_name}.potfile \
    -o ${LOG_PATH}/${cap_name}_key.txt \
    ${hc22000_file} \
    ${dict_path}
fi

printf "$0 finished at `date`\n"