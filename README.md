AWS_POC
CRUD using AWS Lambda(Python 3.9), Dynamodb,API Gateway(for restfull API)
Terraform(Automate Dynamodb table)

Dynamodb table name  'users'
Api endpoint (resourse)- user
hashable id- 'userId'

testing module- pytest

###################################################################

1. creating dynamodb Table(users) using Terraform via AWS CLI
	(Downloading and configure Terraform and AWS CLI on Machine)

	open cmd and path upto root directory where terraform .tf file present
	
	- commands 
		- terraform init
		- terraform plan    (*optional for checking resourse in tf file)
		- terraform apply    

		