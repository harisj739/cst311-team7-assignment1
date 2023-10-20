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
# Running the chat server on h4 and the web server on h2.
subprocess.call(["sudo", "sed", "-i", "5i 10.0.1.2        "  + chat_server_common_name, "/etc/hosts"])
subprocess.call(["sudo", "sed", "-i", "6i 10.0.0.2        " + web_server_common_name, "/etc/hosts"])

# Step 2: Generate private keys for each certificate
# Replaced the key_filename in the subprocess run statement with cakey.pem and matched it with Lab 6A Step 20.
def generate_private_key(key_filename):
    subprocess.run(["sudo", "openssl", "genrsa", "-out", key_filename, "2048"])

chat_server_key_filename = "chatserver-key.pem"
web_server_key_filename = "webserver-key.pem"

generate_private_key(chat_server_key_filename)
generate_private_key(web_server_key_filename)

# Step 3: Generate certificate signing requests using cakey.pem.
# Using Lab6A Step 21.
def generate_certificate_signing_request(key_filename, csr_filename, common_name):
    subprocess.run(["sudo", "openssl", "req", "-nodes", "-new", "-config", "/etc/ssl/openssl.cnf","-key", key_filename, "-out", csr_filename, "-subj", f"/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN={common_name}"])

chat_server_csr_filename = "chatserver-cert.csr"
web_server_csr_filename = "webserver-cert.csr"

generate_certificate_signing_request(chat_server_key_filename, chat_server_csr_filename, chat_server_common_name)
generate_certificate_signing_request(web_server_key_filename, web_server_csr_filename, web_server_common_name)


# Using Lab 6A Step 23 to generate certificate.
# Update: Changed the key_filename argument to cert_filename which is the name of the server certificate.
def generate_certificate(cert_filename, csr_filename, common_name):
    subprocess.run(["sudo", "openssl", "x509", "-req", "-days", "365", "-in", csr_filename, "-CA","/etc/ssl/demoCA/cacert.pem", "-CAkey", "/etc/ssl/demoCA/private/cakey.pem", "-CAcreateserial", "-out", cert_filename])

chat_server_cert_filename = "chatserver-cert.pem"
web_server_cert_filename = "webserver-cert.pem"

generate_certificate(chat_server_cert_filename, chat_server_csr_filename, chat_server_common_name)
generate_certificate(web_server_cert_filename, web_server_csr_filename, web_server_common_name)
