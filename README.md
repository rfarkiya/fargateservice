# fargateservice

# Deploying VPC or services
aws cloudformation deploy --template-file vpc.yaml --stack-name Production --parameter-overrides EnvironmentName=ProductionApp  --capabilities CAPABILITY_NAMED_IAM
aws cloudformation describe-stack-events --stack-name Production

# Display all information
aws cloudformation describe-stacks --stack-name Production
aws cloudformation list-stack-resources --stack-name Production

# To get alrady created template from aws account 
aws cloudformation get-template

# Create change sets
aws cloudformation create-change-set --change-set-name Production54dfd33 --template-body file://$PWD/vpc.yaml --stack-name Production --parameters ParameterKey=EnvironmentName,ParameterValue=ProductionApp --capabilities CAPABILITY_NAMED_IAM

# Describe change set
aws cloudformation describe-change-set --change-set-name Production54dfd33 --stack-name Production

# Execute changes
aws cloudformation execute-change-set --change-set-name Production54dfd33 --stack-name Production

# Directly updating stack
aws cloudformation update-stack --template-body file://$PWD/vpc.yaml --stack-name Production --parameters ParameterKey=EnvironmentName,ParameterValue=ProductionApp  --capabilities CAPABILITY_NAMED_IAM

# How to deploy service
aws cloudformation deploy --template-file service.yaml --stack-name MadisonCDTest --parameter-overrides ServiceName=MadisonCDTest VPC=vpc-0cb7f761d71e405db PrivateSubnets="subnet-0561781351283bbbe,subnet-085d99199b683483b,subnet-04945f9f9db279a86" PublicSubnets="subnet-080b89ee857a2cf78,subnet-0e18e838399d08a2e,subnet-05ff043ff1eba11b7" ECRImageName=".dkr.ecr.us-west-2.amazonaws.com/madison-app" ECSCluster="ProductionApp-ecs-cluster" LoadBalancerCertificateARN="arn:aws:iam:::server-certificate/ViiTest" ECSTaskExecutionRole="arn:aws:iam:::role/ProductionApp-ecs-task-execution-role" ECSTaskRole="arn:aws:iam:::role/ProductionApp-ecs-task-role" BlueGreenDeployRole="arn:aws:iam::601873683251:role/Production-BlueGreenDeployRole-8CWZ3IQWWNA4" LogGroup=ProductionApp --capabilities CAPABILITY_NAMED_IAM
