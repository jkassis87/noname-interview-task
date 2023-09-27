terraform {
  required_providers {
    vultr = {
      source = "vultr/vultr"
      version = "~> 2.3.0"  
    }
  }
}

provider "vultr" {
  api_key = var.api_key
}

resource "vultr_instance" "ubuntu_server" {
  count = 2

  plan        = "vc2-1c-1gb"  
  region       = "syd"         
  os_id           = "387"         
  enable_ipv6     = true
  label           = "ubuntu-server-${count.index}"
  tag             = "my_servers"
}
