provider "aws" {
  region = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY
  secret_key = var.AWS_SECRET_KEY
}


resource "aws_lambda_function" "based_historic_lambda" {
  architectures                      = ["x86_64"]
  code_signing_config_arn            = null
  description                        = null
  filename                           = null
  function_name                      = "c12-based-update-historic-data"
  handler                            = null
  image_uri                          = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-lambda:latest"
  kms_key_arn                        = null
  layers                             = []
  memory_size                        = 128
  package_type                       = "Image"
  publish                            = null
  replace_security_groups_on_destroy = null
  replacement_security_group_ids     = null
  reserved_concurrent_executions     = -1
  role                               = "arn:aws:iam::129033205317:role/service-role/based-update-historic-data-role-nh0kc4vk"
  runtime                            = null
  s3_bucket                          = null
  s3_key                             = null
  s3_object_version                  = null
  skip_destroy                       = false
  source_code_hash                   = null
  tags                               = {}
  tags_all                           = {}
  timeout                            = 3
  ephemeral_storage {
    size = 512
  }
  logging_config {
    application_log_level = null
    log_format            = "Text"
    log_group             = "/aws/lambda/based-update-historic-data"
    system_log_level      = null
  }
  tracing_config {
    mode = "PassThrough"
  }
}

resource "aws_scheduler_schedule" "lambda_schedule" {
  description                  = null
  end_date                     = null
  group_name                   = "default"
  kms_key_arn                  = null
  name                         = "c12-based-historic-data-upload"
  name_prefix                  = null
  schedule_expression          = "cron(0 0 * * ? *)"
  schedule_expression_timezone = "UTC"
  start_date                   = null
  state                        = "ENABLED"
  flexible_time_window {
    maximum_window_in_minutes = 15
    mode                      = "FLEXIBLE"
  }
  target {
    arn      = "arn:aws:lambda:eu-west-2:129033205317:function:c12-based-update-historic-data"
    input    = null
    role_arn = "arn:aws:iam::129033205317:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_0af6e2ce3c"
    retry_policy {
      maximum_event_age_in_seconds = 86400
      maximum_retry_attempts       = 185
    }
  }
}