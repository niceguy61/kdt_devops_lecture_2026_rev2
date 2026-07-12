locals {
  irsa_namespace       = "irsa-demo"
  irsa_service_account = "aws-reader"
  oidc_provider        = replace(module.eks.cluster_oidc_issuer_url, "https://", "")
}

data "aws_iam_policy_document" "irsa_assume" {
  statement {
    sid     = "AssumeRoleFromExactServiceAccount"
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [module.eks.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${local.oidc_provider}:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "${local.oidc_provider}:sub"
      values   = ["system:serviceaccount:${local.irsa_namespace}:${local.irsa_service_account}"]
    }
  }
}

resource "aws_iam_role" "irsa_reader" {
  name               = "${var.cluster_name}-irsa-reader"
  assume_role_policy = data.aws_iam_policy_document.irsa_assume.json

  tags = local.tags
}

# This role intentionally has no application permission policy attached.
# sts:GetCallerIdentity is sufficient to prove which role the Pod assumed.
# Add only the exact AWS actions/resources required by a real workload.
