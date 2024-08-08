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
  region  = "eu-west-2"
}

resource "aws_ecs_task_definition" "pipeline" {
  family = "c12-based-pipeline"
  cpu = 1024
  memory = 1024
  execution_role_arn = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"
  task_role_arn = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"
  requires_compatibilities = [ "EC2" ]
  network_mode = "awsvpc"
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
  container_definitions = jsonencode([
  {
    name: "c12-based-pipeline"
    image: "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-dashboard:latest"
    portMappings: [
      {
      containerPort = 1433
      hostPort      = 1433
      },
      {
      containerPort = 80
      hostPort      = 80
      }
    ]
    essential: true
    environment: [
      {name: "SECRET_KEY"
        value: tostring(var.secret_key)
      },
      {   name: "ACCESS_KEY"
        value: tostring(var.access_key)
      },
      {   name: "DB_HOST"
        value: tostring(var.db_host)
      },
      {   name: "DB_PORT"
        value: tostring(var.db_port)
      },
      {   name: "DB_PASSWORD"
        value: tostring(var.db_password)
      },
      {   name: "DB_USER"
        value: tostring(var.db_user)
      },
      {   name: "DB_NAME"
        value: tostring(var.db_name)
      }
    ]
    logConfiguration: {
      logDriver: "awslogs"
      options: {
        awslogs-group: "ecs/c12-based-pipeline"
        awslogs-create-group: "true"
        awslogs-region: "eu-west-2"
        awslogs-stream-prefix: "ecs"
      }}
  }])
        
}
