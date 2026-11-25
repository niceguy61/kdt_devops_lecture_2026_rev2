module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"

  name               = var.cluster_name
  kubernetes_version = var.kubernetes_version

  # 실습: 내 노트북에서 kubectl로 닿게 (운영: 사설 + VPN · 허용 IP)
  endpoint_public_access = true

  # 이 Terraform을 실행한 사람(devops-admin)에게 클러스터 관리자 — Access Entry로
  enable_cluster_creator_admin_permissions = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets # 노드는 private에

  addons = {
    vpc-cni = {
      before_compute = true # 노드보다 먼저 — Pod IP를 VPC에서 받는 네트워크 플러그인
    }
    eks-pod-identity-agent = {
      before_compute = true # Pod가 IAM 역할을 맡게 해 주는 에이전트
    }
    kube-proxy     = {}
    coredns        = {}
    metrics-server = {}
    aws-ebs-csi-driver = {
      pod_identity_association = [{
        role_arn        = module.ebs_csi_pod_identity.iam_role_arn
        service_account = "ebs-csi-controller-sa"
      }]
    }
  }

  eks_managed_node_groups = {
    default = {
      ami_type       = "AL2023_x86_64_STANDARD"
      instance_types = [var.node_instance_type]
      min_size       = 1
      max_size       = 3
      desired_size   = var.node_count
    }
  }
}
