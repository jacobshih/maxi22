#!/bin/sh
[ -f /bin/send_cmd ] || ipcam=no
[ -f /bin/send_cmd ] && ipcam=yes

. /var/www/bspanel/scripts/http_response_header.sh
. /var/www/bspanel/scripts/parse_name_value.sh
read -n ${CONTENT_LENGTH} POSTDATA
parse_name_value $POSTDATA "&"

set_led() {
    case ${id} in
    power)
        [ ${color} == on    ] && code=602   # CMD_POWER_LED_ON
        [ ${color} == off   ] && code=603   # CMD_POWER_LED_OFF
        [ ${color} == blink ] && code=2001  # CMD_POWER_LED_BLINK
        ;;
    link)
        [ ${color} == on    ] && code=636   # CMD_LINK_UP
        [ ${color} == off   ] && code=637   # CMD_LINK_DOWN
        [ ${color} == blink ] && code=2002  # CMD_LINK_LED_BLINK
        ;;
    wps)
        [ ${color} == on    ] && code=632   # CMD_WPS_LED_ON
        [ ${color} == off   ] && code=633   # CMD_WPS_LED_OFF
        [ ${color} == blink ] && code=2003  # CMD_WPS_LED_BLINK
        ;;
    ir)
        [ ${color} == on    ] && code=650   # CMD_ICR_ON
        [ ${color} == off   ] && code=651   # CMD_ICR_OFF
        ;;
    *) echo "[unknown]"
        code=0
        ;;
    esac

    cmdline="send_cmd watchdog ${code}"
    [ $ipcam == yes ] && eval ${cmdline} > /dev/null 2> /dev/null
    [ $ipcam == no  ] && echo ${cmdline}
}

set_icr() {
    case ${id} in
    ircutr)
        [ ${value} == on    ] && code=662   # CMD_ICR_ON
        [ ${value} == off   ] && code=663   # CMD_ICR_OFF
        ;;
    *) echo "[unknown]"
        code=0
        ;;
    esac

    cmdline="send_cmd watchdog ${code}"
    [ $ipcam == yes ] && eval ${cmdline} > /dev/null 2> /dev/null
    [ $ipcam == no  ] && echo ${cmdline}
}

set_button() {
    case ${id} in
    wps)
        code=611
        ;;
    reset)
        code=672
        ;;
    *) echo "unknown"
        code=0
        ;;
    esac

    cmdline="send_cmd watchdog ${code}"
    [ $ipcam == yes ] && eval ${cmdline} > /dev/null 2> /dev/null
    [ $ipcam == no  ] && echo ${cmdline}
}

restart() {
    cmdline="/etc/rc.d/init.d/watchdog.sh restart"
    [ $ipcam == yes ] && eval ${cmdline} > /dev/null 2> /dev/null
    [ $ipcam == no  ] && echo ${cmdline}
}

[ $what == led     ] && set_led
[ $what == button  ] && set_button
[ $what == icr     ] && set_icr
[ $what == restart ] && restart
