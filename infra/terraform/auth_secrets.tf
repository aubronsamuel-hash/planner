// Placeholder Terraform configuration for auth secrets storage.
terraform {
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type        = string
  description = "AWS region hosting secret storage"
  default     = "eu-west-3"
}

resource "aws_ssm_parameter" "planner_jwt_secret" {
  name  = "/planner/jwt/secret"
  type  = "SecureString"
  value = "CHANGE_ME"
}
