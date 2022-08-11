provider "aws" {
  region = "ap-south-1"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "Users"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "UserId"
  range_key      = "FirstName"
  attribute {
    name = "UserId"
    type = "S"
  }

  attribute {
    name = "FirstName"
    type = "S"
  }

  attribute {
    name = "EmailId"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }

  global_secondary_index {
    name               = "FirstNameIndex"
    hash_key           = "FirstName"
    range_key          = "EmailId"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["UserId"]
  }

  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}