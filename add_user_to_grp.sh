OUT=$(aws iam add-user-to-group --group-name "$1" --user-name "$2")
echo "${OUT}"

