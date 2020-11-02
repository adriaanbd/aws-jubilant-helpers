OUT=$(aws iam create-user --user-name "$1")
echo "${OUT}"
