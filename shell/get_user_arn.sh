ARN=$(aws iam get-user --query "User.Arn" --output text)
echo "${ARN}"
