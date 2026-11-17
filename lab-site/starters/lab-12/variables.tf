variable "location" {
  type    = string
  default = "centralindia"
}

variable "vm_size" {
  type    = string
  default = "Standard_B2s_v2"
}

variable "lab_prefix" {
  type = string
}

variable "storage_account_name" {
  type = string
}

variable "ssh_source_cidr" {
  type = string
  validation {
    condition     = can(cidrnetmask(var.ssh_source_cidr)) && endswith(var.ssh_source_cidr, "/32")
    error_message = "Enter your public IPv4 address in /32 CIDR notation."
  }
}

variable "ssh_public_key_path" {
  type    = string
  default = "lab-key.pub"
}
