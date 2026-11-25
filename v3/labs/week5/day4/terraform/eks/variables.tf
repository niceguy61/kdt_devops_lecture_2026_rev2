variable "region" {
  type    = string
  default = "ap-northeast-2"
}

variable "owner" {
  description = "내 GitHub ID (소문자)"
  type        = string
}

variable "cluster_name" {
  type    = string
  default = "devmart"
}

variable "kubernetes_version" {
  description = "EKS가 지원하는 최신 — aws eks describe-cluster-versions 로 확인"
  type        = string
  default     = "1.36"
}

variable "node_instance_type" {
  type    = string
  default = "t3.medium" # 2 vCPU · 4 GiB — DevMart + Argo CD + 입구가 들어간다
}

variable "node_count" {
  type    = number
  default = 2
}
