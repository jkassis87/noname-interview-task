# AWS Provider
provider "aws" {
  region = "ap-southeast-2"
}

# Create ECS cluster
resource "aws_ecs_cluster" "my_cluster" {
  name = "my-cluster"
}

# Create VPC, subnets, and security groups for ECS
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "subnet_a" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-southeast-2a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "subnet_b" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "ap-southeast-2b"
  map_public_ip_on_launch = true
}

resource "aws_security_group" "ecs_security_group" {
  name        = "ecs-security-group"
  description = "ECS Security Group"
  vpc_id      = aws_vpc.my_vpc.id
}


resource "aws_security_group_rule" "ingress_http" {
  type        = "ingress"
  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]  # Allow incoming HTTP traffic from anywhere
  security_group_id = aws_security_group.ecs_security_group.id
}

resource "aws_security_group_rule" "egress_all" {
  type        = "egress"
  from_port   = 0
  to_port     = 0
  protocol    = "-1"  # Allow all outbound traffic
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = aws_security_group.ecs_security_group.id
}

# Create an ECS task definition and service

resource "aws_ecs_task_definition" "my_task" {
  family                   = "my-flask-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"

  container_definitions = jsonencode([
    {
      name      = "first"
      image     = "service-first"
      cpu       = 512
      memory    = 1024
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    },
    # {
    #   name      = "second"
    #   image     = "service-second"
    #   cpu       = 256
    #   memory    = 512
    #   essential = true
    #   portMappings = [
    #     {
    #       containerPort = 443
    #       hostPort      = 443
    #     }
    #   ]
    # }
  ])
}



resource "aws_ecs_service" "my_service" {
  name            = "my-flask-service"
  cluster         = aws_ecs_cluster.my_cluster.id
  task_definition = aws_ecs_task_definition.my_task.arn
  launch_type     = "FARGATE"
  desired_count   = 2  # Redundancy across 2 AZs

  network_configuration {
    subnets = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]
    security_groups = [aws_security_group.ecs_security_group.id]
  }
}

# Create an API Gateway
resource "aws_api_gateway_rest_api" "my_api" {
  name = "my-flask-api"
}

# # Output the URL of the API Gateway
# output "api_gateway_url" {
#   value = aws_api_gateway_rest_api.my_api.invoke_url
# }