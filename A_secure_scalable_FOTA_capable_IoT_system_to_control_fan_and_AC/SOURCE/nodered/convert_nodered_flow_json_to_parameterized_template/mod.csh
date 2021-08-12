#!/bin/csh
sed -E 's/([a-z0-9]\.[a-z0-9]*)"/\1 IDENTIFIER"/g' ${1} > 1
sed -E 's/(subflow.*) IDENTIFIER/\1/g' 1 > 2
sed -E 's/(broker.*) IDENTIFIER/\1/g' 2 > 3
set q = '"'
sed -E "s/\\${q}/'/g" 3 > 4
sed -E "s/'/\\'/g" 4 > 5
sed 's/\\n/\\\\n/g' 5 > 6
awk '{print $0"\\"}' 6 > 7
sed -E -e 's/Unit Prototype/Unit IDENTIFIER/g' -e 's/UI Prototype/Node IDENTIFIER/g' -e 's/°/\\u00b0/g' 7 > out
