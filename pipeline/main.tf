provider "aws" {
  region = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY
  secret_key = var.AWS_SECRET_KEY
}

resource "aws_lambda_function" "pipeline_lambda" {
  architectures                      = ["x86_64"]
  function_name                      = "c12-based-lmnh-pipeline"
  image_uri                          = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-lambda-pipeline:latest"
  layers                             = []
  memory_size                        = 128
  package_type                       = "Image"
  reserved_concurrent_executions     = -1
  role                               = "arn:aws:iam::129033205317:role/service-role/c12-based-lmnh-pipeline-role-j0fvxt7w"
  skip_destroy                       = false
  tags                               = {}
  tags_all                           = {}
  timeout                            = 60
  environment {
    variables = {
      DB_HOST     = var.DB_HOST
      DB_NAME     = var.DB_NAME
      DB_PASSWORD = var.DB_PASSWORD
      DB_PORT     = var.DB_PORT
      DB_USER     = var.DB_USER
    }
  }
  ephemeral_storage {
    size = 512
  }
  logging_config {
    log_format            = "Text"
    log_group             = "/aws/lambda/c12-based-lmnh-pipeline"
  }
  tracing_config {
    mode = "PassThrough"
  }
}



resource "aws_scheduler_schedule" "pipeline_schedule" {
  group_name                   = "default"
  name                         = "c12-based-pipeline"
  schedule_expression          = "cron(* * * * ? *)"
  schedule_expression_timezone = "Europe/London"
  state                        = "ENABLED"
  flexible_time_window {
    maximum_window_in_minutes = 0
    mode                      = "OFF"
  }
  target {
    arn      = "arn:aws:lambda:eu-west-2:129033205317:function:c12-based-lmnh-pipeline"
    input    = "{}"
    role_arn = "arn:aws:iam::129033205317:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_d6692370b3"
    retry_policy {
      maximum_event_age_in_seconds = 86400
      maximum_retry_attempts       = 185
    }
  }
}