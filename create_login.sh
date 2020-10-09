OUT=$(aws iam create-login-profile --user-name "$1" --password "$2")
echo "${OUT}"
