#!/bin/sh
parse_name_value() {
    oldifs=$IFS
    DATA=$(decode_postdata $1)
    IFS=$2
    set -- $DATA
    for i in "$@"; do IFS="="; set -- $i; eval $1=\"$2\"; done
    IFS=$oldifs
}

decode_postdata() {
    local v t h l
    t=$1
    t=`echo $t%% | sed -e 's/+/ /g'`        # replace + with space and append %%
    while [ ${#t} -gt 0 -a "${t}" != "%" ]; do
        v="${v}${t%%\%*}"                   # digest up to the first %
        t="${t#*%}"                         # remove digested part
        # decode if there is anything to decode and if not at end of string
        if [ ${#t} -gt 0 -a "${t}" != "%" ]; then
            h=`expr substr $t 1 2`          # save first two chars
            l=`expr \`expr length $t\` - 2` # length of t except first two chars
            t=`expr substr $t 3 $l`         # remove the first two chars
            v="${v}"`echo -e \\\\x${h}`     # convert hex to special char
        fi
    done
    echo $v
}
