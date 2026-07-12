terraform { required_version = ">= 1.5.0, < 2.0.0" }

resource "terraform_data" "this" {
  input = {
    environment = var.environment
    replicas    = var.replicas
    owner       = var.owner
  }
}
