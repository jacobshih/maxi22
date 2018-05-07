#!/bin/sh
# json_output, it specifies the output for json stream, either stdout or a file.
json_output=

# set_json_output {out}
# set the output for json stream, either stdout or a file.
# {out}, stdout if {out} is not specified, or a file specified explicitly.
set_json_output() {
    [ -z $1 ] && json_output=""
    [ -z $1 ] || json_output=">>$1" && echo "" > $1
}

# clear_json_output
# remove the json output file.
clear_json_output() {
    [ -f $json_output ] && rm $json_output
    json_output=
}

# json_o
# start of a json object.
json_o() {
    eval "$json_output echo {"
}

# json_x
# end of a json object.
json_x() {
    eval "$json_output echo '\"\"':'\"\"'"
    eval "$json_output echo }"
}

# json_add_var {key} {value}
# add a key value pair to json object in which the value is any type other than string.
json_add_var() {
    key=$1; value=$2;
    [ -z $value ] && value="\"\""
    eval "$json_output echo '\"$key\"':$value,"
}

# json_add_str {key} {value}
# add a key value pair to json object in which the value is a string.
json_add_str() {
    key=$1; value=$2;
    eval "$json_output echo '\"$key\"':'\"$value\"',"
}
