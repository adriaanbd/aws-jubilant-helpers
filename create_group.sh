OUTPUT=$(aws iam create-group --group-name "$1")
echo "${OUTPUT}"
