# 1교시 · 첫 Terraform — S3 버킷 하나
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
}

resource "aws_s3_bucket" "first" {
  bucket = "devmart-tf-first-YOUR_ID" # 전 세계에서 유일한 이름 — YOUR_ID를 바꾼다

  tags = {
    Project   = "devmart"
    ManagedBy = "terraform"
  }
}
