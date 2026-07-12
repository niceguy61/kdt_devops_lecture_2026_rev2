variable "region" {
  description = "AWS Region for the hands-on cluster."
  type        = string
  default     = "ap-northeast-2"
}

variable "cluster_name" {
  description = "Unique EKS cluster name."
  type        = string
  default     = "tf-eks-irsa-lab"
}

variable "kubernetes_version" {
  description = "EKS Kubernetes minor version supported in the target Region."
  type        = string
  default     = "1.35"
}

variable "node_instance_type" {
  description = "Small instance type for the single educational managed node."
  type        = string
  default     = "t3.small"
}

variable "vpc_cidr" {
  description = "CIDR block used by the hands-on VPC."
  type        = string
  default     = "10.42.0.0/16"
}

variable "availability_zone_count" {
  description = "Number of Availability Zones. EKS production-style networking requires at least three in this lab."
  type        = number
  default     = 3

  validation {
    condition     = var.availability_zone_count >= 3
    error_message = "availability_zone_count must be at least 3."
  }
}

variable "control_plane_az_count" {
  description = "AZ count for EKS control-plane ENIs. Keep 3 for a new cluster; use the original AZ count when extending an existing cluster."
  type        = number
  default     = 3

  validation {
    condition     = var.control_plane_az_count >= 2 && var.control_plane_az_count <= 3
    error_message = "control_plane_az_count must be 2 or 3."
  }
}

variable "subnet_newbits" {
  description = "Additional CIDR bits used to derive equal-sized public and private subnets from vpc_cidr."
  type        = number
  default     = 8
}

variable "single_nat_gateway" {
  description = "Use one NAT Gateway to reduce short-lived lab cost. Set false for one NAT Gateway per AZ in production."
  type        = bool
  default     = true
}
