# 3일차 VPC와 같은 설계 + NAT 하나 + 로드 밸런서가 서브넷을 찾을 표시
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 6.0"

  name = "${var.cluster_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}c"]
  public_subnets  = ["10.0.0.0/20", "10.0.16.0/20"]
  private_subnets = ["10.0.128.0/20", "10.0.144.0/20"]

  enable_nat_gateway   = true # 노드(private)가 이미지를 받으려면 밖으로 나가야 한다
  single_nat_gateway   = true # 실습: 하나만 (운영: AZ마다 하나)
  enable_dns_hostnames = true
  enable_dns_support   = true

  # AWS Load Balancer Controller가 '어느 서브넷에 로드 밸런서를 둘지' 찾는 표시
  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}
