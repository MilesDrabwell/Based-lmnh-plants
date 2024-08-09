terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.55.0"
    }
  }
  required_version = ">= 1.2.0"
}
provider "aws" {
  region  = var.AWS_REGION
}

resource "aws_security_group" "dashboard_sg" {
  name        = "c12-based-dashboard"
  description = "Allow inbound psql traffic"
  vpc_id      = "vpc-061c17c21b97427d8"
}
resource "aws_vpc_security_group_ingress_rule" "ipv4_sl_in" {
  security_group_id = aws_security_group.dashboard_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 8501
  ip_protocol       = "tcp"
  to_port           = 8501
}
resource "aws_vpc_security_group_ingress_rule" "ipv4_db_in" {
  security_group_id = aws_security_group.dashboard_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 1433
  ip_protocol       = "tcp"
  to_port           = 1433
}
resource "aws_vpc_security_group_egress_rule" "ipv4_all_out" {
  security_group_id = aws_security_group.dashboard_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_ecs_task_definition" "dashboard" {
  family = "c12-based-dashboard"
  cpu = 1024
  memory = 6144
  execution_role_arn = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"
  task_role_arn = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
  container_definitions = jsonencode([
  {
    name: "c12-based-dashboard"
    image: "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-dashboard:latest"
    cpu: 0
    portMappings: [
      {
      containerPort = 1433
      hostPort      = 1433
      },
      {
      containerPort = 8501
      hostPort      = 8501
      }
    ]
    essential: true
    environment: [
      {name: "SECRET_KEY"
        value: tostring(var.AWS_SECRET_KEY)
      },
      {   name: "ACCESS_KEY"
        value: tostring(var.AWS_ACCESS_KEY)
      },
      {   name: "DB_HOST"
        value: tostring(var.DB_HOST)
      },
      {   name: "DB_PORT"
        value: tostring(var.DB_PORT)
      },
      {   name: "DB_PASSWORD"
        value: tostring(var.DB_PASSWORD)
      },
      {   name: "DB_USER"
        value: tostring(var.DB_USER)
      },
      {   name: "DB_NAME"
        value: tostring(var.DB_NAME)
      }
    ]
    logConfiguration: {
      logDriver: "awslogs"
      options: {
        awslogs-group: "/ecs/c12-based-dashboard"
        awslogs-create-group: "true"
        awslogs-region: "eu-west-2"
        awslogs-stream-prefix: "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "dashboard" {
    name                    = "c12-based-dashboard"
    cluster                 = "arn:aws:ecs:eu-west-2:129033205317:cluster/c12-ecs-cluster"
    desired_count           = 1
    task_definition         = aws_ecs_task_definition.dashboard.arn
    capacity_provider_strategy {
      capacity_provider = "FARGATE"
      base = 1
      weight = 100

    }
    
    network_configuration {
        security_groups = [aws_security_group.dashboard_sg.id]
        subnets         = ["subnet-058f02e41ee6a5439", "subnet-0c459ebb007081668", "subnet-0ff947058bbc1165d"]
        assign_public_ip = true
  }
}