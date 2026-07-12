output "region" {
  value = var.region
}

output "cluster_name" {
  value = module.eks.cluster_name
}

output "cluster_endpoint" {
  value     = module.eks.cluster_endpoint
  sensitive = true
}

output "oidc_issuer_url" {
  value = module.eks.cluster_oidc_issuer_url
}

output "irsa_role_arn" {
  value = aws_iam_role.irsa_reader.arn
}

output "kubeconfig_command" {
  value = "aws eks update-kubeconfig --region ${var.region} --name ${module.eks.cluster_name}"
}
