#!/bin/sh

# variables
aws_region="ap-northeast-1"
aws_account_id="346416576166"
aws_ecr_name="test"



# pre-build
echo "authenticating the docker cli to use the ECR registry..."
aws ecr get-login-password --region $aws_region | docker login --username AWS --password-stdin $aws_account_id.dkr.ecr.$aws_region.amazonaws.com

# build
echo "building image..."
docker build -f project/Dockerfile.prod --platform=linux/amd64 -t $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$aws_ecr_name:dev ./project/

# post-build
echo "pushing image to AWS ECR..."
docker push $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$aws_ecr_name:dev

echo "updating ECS service..."
aws ecs update-service --cluster $aws_cluster_name --service $aws_service_name --force-new-deployment

echo "done!"