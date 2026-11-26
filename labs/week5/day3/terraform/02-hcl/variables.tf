variable "region" {
  description = "AWS 리전"
  type        = string
  default     = "ap-northeast-2"
}

variable "owner" {
  description = "내 GitHub ID (소문자) — 버킷 이름과 태그에 쓴다"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.owner))
    error_message = "owner는 소문자 · 숫자 · 하이픈만 쓸 수 있습니다 (S3 버킷 이름 규칙)."
  }
}

variable "buckets" {
  description = "만들 버킷 — 이름 뒤에 붙일 말과 버전 관리 여부"
  type = map(object({
    versioning = bool
  }))
  default = {
    assets = { versioning = true }
    logs   = { versioning = false }
  }
}
