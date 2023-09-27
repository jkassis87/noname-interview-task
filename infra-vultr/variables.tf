variable "api_key" {
  description = "API key for Vultr"
  type        = string
  sensitive   = true  # This will hide the variable value in CLI outputs
}
