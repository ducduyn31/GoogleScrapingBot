#!/bin/bash

declare -a EXTS=("txt" "pdf" "xml" "odt" "rtf" "ods" "odp" "doc" "docx" "ppt" "pptx" "xls" "xlsx" "html" "csv" "epub" "gz" "zip" "gif" "jar")

for val in ${EXTS[@]}; do
  python searchndownload.py -i corona -e $val -o $val
done
