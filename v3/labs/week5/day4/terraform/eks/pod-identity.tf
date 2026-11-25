# Pod가 맡을 IAM 역할 — 4주차의 ServiceAccount를 AWS 역할에 잇는다 (EKS Pod Identity)

# EBS CSI 드라이버: PVC를 만들면 EBS 볼륨을 만들고 붙인다
module "ebs_csi_pod_identity" {
  source  = "terraform-aws-modules/eks-pod-identity/aws"
  version = "~> 2.0"

  name                      = "${var.cluster_name}-ebs-csi"
  attach_aws_ebs_csi_policy = true
}

# AWS Load Balancer Controller: Service(LoadBalancer)를 보고 NLB를 만든다
module "lbc_pod_identity" {
  source  = "terraform-aws-modules/eks-pod-identity/aws"
  version = "~> 2.0"

  name                            = "${var.cluster_name}-lbc"
  attach_aws_lb_controller_policy = true

  associations = {
    lbc = {
      cluster_name    = module.eks.cluster_name
      namespace       = "kube-system"
      service_account = "aws-load-balancer-controller"
    }
  }
}
