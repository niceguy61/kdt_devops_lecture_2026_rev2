variable "environment" { type = string }
variable "replicas" {
  type = number
  validation {
    condition     = var.replicas > 0
    error_message = "Replicas must be greater than zero."
  }
}
variable "owner" { type = string }
