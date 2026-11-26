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
  region = var.region

  # 이 프로바이더로 만드는 모든 자원에 붙는 태그 (2일차 7교시)
  default_tags {
    tags = {
      Project   = "devmart"
      Owner     = var.owner
      ManagedBy = "terraform"
    }
  }
}
