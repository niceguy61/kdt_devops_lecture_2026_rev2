terraform { required_version = ">= 1.5.0, < 2.0.0" }
module "service" {
  source      = "../../modules/service"
  environment = "dev"
  replicas    = 1
  owner       = "platform-lab"
}
output "service" { value = module.service.summary }
