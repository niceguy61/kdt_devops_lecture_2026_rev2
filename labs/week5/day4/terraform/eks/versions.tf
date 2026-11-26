terraform {
  required_version = ">= 1.15"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket       = "devmart-tfstate-YOUR_ID"
    key          = "w5d4/eks/terraform.tfstate"
    region       = "ap-northeast-2"
    use_lockfile = true
    encrypt      = true
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Project   = "devmart"
      Owner     = var.owner
      ManagedBy = "terraform"
    }
  }
}
