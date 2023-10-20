"""Certificate Generation for CST311 Programming Assignment 4"""
__author__ = "Team 7 - SSS"
__credits__ = [
  "Andrew Grant",
  "Anthony Matricia",
  "Haris Jilani"
]

import subprocess

# Step 1: Ask for common names
chat_server_common_name = input("Enter common name for the chat server: ")
web_server_common_name = input("Enter common name for the web server: ")

# Step 2: Generate private keys
def generate_private_key(key_filename):
    subprocess.run(["sudo", "openssl", "genrsa", "-out", key_filename, "2048"])

chat_server_key_filename = "chatserver-key.pem"
web_server_key_filename = "webserver-key.pem"

generate_private_key(chat_server_key_filename)
generate_private_key(web_server_key_filename)

# Step 3: Generate certificate signing requests
def generate_certificate_signing_request(key_filename, csr_filename, common_name):
    subprocess.run(["sudo", "openssl", "req", "-new", "-config", "/etc/ssl/openssl.cnf", "-key", key_filename, "-out", csr_filename, "-subj", f"/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN={common_name}"])

chat_server_csr_filename = "chatserver-cert.csr"
web_server_csr_filename = "webserver-cert.csr"

generate_certificate_signing_request(chat_server_key_filename, chat_server_csr_filename, chat_server_common_name)
generate_certificate_signing_request(web_server_key_filename, web_server_csr_filename, web_server_common_name)

