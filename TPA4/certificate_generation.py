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

# Add the IP addresses and names of the CN in /etc/hosts.
subprocess.call(["sudo", "sed", "-i", "5i 10.0.0.5        " + chat_server_common_name, "/etc/hosts"])
subprocess.call(["sudo", "sed", "-i", "6i 10.0.1.5        " + web_server_common_name, "/etc/hosts"])

# Step 2: Generate private keys for each certificate
# Replaced the key_filename in the subprocess run statement with cakey.pem and matched it with Lab 6A Step 8.
def generate_private_key(key_filename):
    subprocess.run(["sudo", "openssl", "genrsa", "-aes256", "-out", "cakey.pem", "2048"])

chat_server_key_filename = "chatserver-key.pem"
web_server_key_filename = "webserver-key.pem"

generate_private_key(chat_server_key_filename)
generate_private_key(web_server_key_filename)

# Step 3: Generate certificate signing requests using cakey.pem.
# Removed the key_filename argument and instead used cakey.pem.
def generate_certificate_signing_request(csr_filename, common_name):
    subprocess.run(["sudo", "openssl", "req", "-x509", "-new", "-nodes", "-key", "cakey.pem", "-sha256","-days", "1825", "-out", csr_filename, "-subj", f"/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN={common_name}"])

chat_server_csr_filename = "chatserver-cert.csr"
web_server_csr_filename = "webserver-cert.csr"

# Removed the key_filename argument.
generate_certificate_signing_request(chat_server_csr_filename, chat_server_common_name)
generate_certificate_signing_request(web_server_csr_filename, web_server_common_name)
