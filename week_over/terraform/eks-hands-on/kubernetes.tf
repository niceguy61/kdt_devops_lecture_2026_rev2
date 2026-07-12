resource "kubernetes_namespace_v1" "irsa_demo" {
  metadata {
    name = local.irsa_namespace
  }

  depends_on = [module.eks]
}

resource "kubernetes_service_account_v1" "aws_reader" {
  metadata {
    name      = local.irsa_service_account
    namespace = kubernetes_namespace_v1.irsa_demo.metadata[0].name
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.irsa_reader.arn
    }
  }

  automount_service_account_token = true
}

resource "kubernetes_pod_v1" "irsa_check" {
  metadata {
    name      = "irsa-check"
    namespace = kubernetes_namespace_v1.irsa_demo.metadata[0].name
  }

  spec {
    service_account_name = kubernetes_service_account_v1.aws_reader.metadata[0].name
    restart_policy       = "Never"

    container {
      name    = "aws-cli"
      image   = "public.ecr.aws/aws-cli/aws-cli:2.35.21"
      command = ["sh", "-c", "aws sts get-caller-identity && sleep 3600"]

      resources {
        requests = {
          cpu    = "50m"
          memory = "96Mi"
        }
        limits = {
          cpu    = "200m"
          memory = "256Mi"
        }
      }
    }
  }

  depends_on = [module.eks, aws_iam_role.irsa_reader]

  # EKS IRSA admission injects the AWS_* environment variables and projected
  # token volume after creation. They are server-managed, not configuration
  # drift, so Terraform must not replace the proof Pod on every plan.
  lifecycle {
    ignore_changes = [
      spec[0].container[0].env,
      spec[0].container[0].volume_mount,
      spec[0].volume,
    ]
  }
}
