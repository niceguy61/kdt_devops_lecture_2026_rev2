terraform {
  required_version = ">= 1.15"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  # 5교시 · 원격 state — bucket의 YOUR_ID를 바꾼다
  backend "s3" {
    bucket       = "devmart-tfstate-YOUR_ID"
    key          = "w5d3/vpc/terraform.tfstate"
    region       = "ap-northeast-2"
    use_lockfile = true # S3 자체 잠금 (DynamoDB 없이)
    encrypt      = true
  }
}

provider "aws" {
  region = "ap-northeast-2"
  default_tags {
    tags = { Project = "devmart", ManagedBy = "terraform" }
  }
}
