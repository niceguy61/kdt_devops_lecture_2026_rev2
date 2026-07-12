terraform { required_version = ">= 1.5.0, < 2.0.0" }
module "service" {
  source      = "../../modules/service"
  environment = "prod"
  replicas    = 3
  owner       = "platform-team"
}
output "service" { value = module.service.summary }
