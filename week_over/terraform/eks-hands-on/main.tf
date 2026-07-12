data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  azs = slice(data.aws_availability_zones.available.names, 0, var.availability_zone_count)

  public_subnets = [
    for index in range(var.availability_zone_count) :
    cidrsubnet(var.vpc_cidr, var.subnet_newbits, index + 1)
  ]
  private_subnets = [
    for index in range(var.availability_zone_count) :
    cidrsubnet(var.vpc_cidr, var.subnet_newbits, index + 11)
  ]
  tags = {
    Course    = "terraform-eks-hands-on"
    ManagedBy = "terraform"
    Owner     = "kdt-student"
    CleanupBy = "same-day"
  }
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "6.6.1"

  name = "${var.cluster_name}-vpc"
  cidr = var.vpc_cidr

  azs             = local.azs
  public_subnets  = local.public_subnets
  private_subnets = local.private_subnets

  enable_nat_gateway      = true
  single_nat_gateway      = var.single_nat_gateway
  map_public_ip_on_launch = true
  enable_dns_support      = true
  enable_dns_hostnames    = true

  public_subnet_tags = {
    "kubernetes.io/role/elb"                    = 1
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }


  private_subnet_tags = {
    "kubernetes.io/role/internal-elb"           = 1
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "21.14.0"

  name               = var.cluster_name
  kubernetes_version = var.kubernetes_version

  endpoint_private_access                  = true
  endpoint_public_access                   = true
  enable_cluster_creator_admin_permissions = true
  enable_irsa                              = true

  # EKS encrypts secrets at rest by default with an AWS managed key.
  # Do not create a customer managed KMS key for this short-lived lab because
  # KMS keys remain in a mandatory deletion window after terraform destroy.
  encryption_config = null
  create_kms_key    = false

  addons = {
    coredns    = {}
    kube-proxy = {}
    vpc-cni = {
      before_compute = true
    }
  }

  vpc_id = module.vpc.vpc_id
  # The control plane can attach ENIs to both subnet tiers. Workload nodes are
  # explicitly restricted to private subnets below.
  subnet_ids = concat(
    slice(module.vpc.public_subnets, 0, var.control_plane_az_count),
    slice(module.vpc.private_subnets, 0, var.control_plane_az_count)
  )

  eks_managed_node_groups = {
    lab = {
      subnet_ids     = module.vpc.private_subnets
      ami_type       = "AL2023_x86_64_STANDARD"
      instance_types = [var.node_instance_type]
      capacity_type  = "ON_DEMAND"

      min_size     = 1
      max_size     = 1
      desired_size = 1

      disk_size = 20
      labels = {
        workload = "education"
      }
    }
  }

  tags = local.tags
}
