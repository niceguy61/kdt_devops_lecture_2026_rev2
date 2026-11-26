# 5교시 · 원격 state를 담을 버킷 — 이 프로젝트만은 state를 로컬에 둔다 (닭과 달걀)
terraform {
  required_version = ">= 1.15"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-2"
  default_tags {
    tags = { Project = "devmart", ManagedBy = "terraform", Purpose = "tfstate" }
  }
}

variable "owner" {
  type = string
}

resource "aws_s3_bucket" "tfstate" {
  bucket = "devmart-tfstate-${var.owner}"

  lifecycle {
    prevent_destroy = true # 실수로 지우면 모든 프로젝트의 state가 사라진다
  }
}

resource "aws_s3_bucket_versioning" "tfstate" {
  bucket = aws_s3_bucket.tfstate.id
  versioning_configuration {
    status = "Enabled" # state를 되돌릴 수 있게
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tfstate" {
  bucket = aws_s3_bucket.tfstate.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "tfstate" {
  bucket                  = aws_s3_bucket.tfstate.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "bucket" {
  value = aws_s3_bucket.tfstate.bucket
}
