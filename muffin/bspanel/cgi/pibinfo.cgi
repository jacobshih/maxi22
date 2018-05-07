#!/bin/sh
[ -f /bin/send_cmd ] || ipcam=no
[ -f /bin/send_cmd ] && ipcam=yes

. /var/www/bspanel/scripts/http_response_header.sh
. /var/www/bspanel/scripts/parse_name_value.sh
. /var/www/bspanel/scripts/json_utils.sh
read -n ${CONTENT_LENGTH} POSTDATA
parse_name_value $POSTDATA "&"

# POSTDATA:
# {
#   "cmd": command,
#   "key": key,
#   "value": value
# }
#

case ${cmd} in
all )
    ;;
HWBoard |  Sensor | SensorCaps | HWVersion | ModelName |  MacAddress | MacAddress2 )
    ;;
Region | RegionABand | KTKey | FactoryPassword | BootMode | EfuseBufferMode)
    ;;
ApSecurityMode | PowerFrequency | DewarpOffset | ApKey | DevUid )
    ;;
set )
    ;;
*)
    cmd=""
    ;;
esac

pibinfo_set() {
    key=$1
    value=$2
    echo "$key=$value" > $out
    cmdline="pibinfo set < $out; rm $out;"
    if [ $ipcam == yes ]; then
        eval ${cmdline}
        pibinfo_get $key
    else
        echo ${cmdline}
    fi
}

pibinfo_get() {
    key=$1
    cmdline="pibinfo ${key} > $out; cat $out; rm $out;"
    if [ $ipcam == yes ]; then
        value=`eval ${cmdline}`
        set_json_output
        json_o
        json_add_str "$key" "$value"
        json_x
    else
        echo ${cmdline}
    fi
}

pibinfo_all() {
    cmdline="pibinfo all > $out; cat $out;"
    if [ $ipcam == yes ]; then
        value=`eval ${cmdline}`
        IFS=$(echo -en "\n\b")
        set -- $value
        for i in "$@"; do IFS="="; set -- $i; eval $1=$2; done
        set_json_output
        json_o
        json_add_str "HWBoard" $HWBoard
        json_add_str "Sensor" $Sensor
        json_add_str "SensorCaps" $SensorCaps
        json_add_str "HWVersion" $HWVersion
        json_add_str "ModelName" $ModelName
        json_add_str "MacAddress" $MacAddress
        json_add_str "MacAddress2" $MacAddress2
        json_add_str "Region" $Region
        json_add_str "RegionABand" $RegionABand
        json_add_str "KTKey" $KTKey
        json_add_str "FactoryPassword" $FactoryPassword
        json_add_str "BootMode" $BootMode
        json_add_str "EfuseBufferMode" $EfuseBufferMode
        json_add_str "ApSecurityMode" $ApSecurityMode
        json_add_str "PowerFrequency" $PowerFrequency
        json_add_str "DewarpOffset" $DewarpOffset
        json_add_str "ApKey" $ApKey
        json_add_str "DevUid" $DevUid
        json_x
        clear_json_output
    else
        echo ${cmdline}
    fi
}

if [ ! -z $cmd ]; then
    out=/tmp/cgi_pibinfo
    if [ $cmd == set ]; then
        pibinfo_set "$key" "$value"
    elif [ $cmd == all ]; then
        pibinfo_all
    else
        pibinfo_get &cmd
    fi
fi
