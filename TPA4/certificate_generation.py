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
subprocess.call(["sudo", "sed", "-i", "5i 127.0.0.1       " + chat_server_common_name, "/etc/hosts"])
subprocess.call(["sudo", "sed", "-i", "6i 10.0.0.3        " + web_server_common_name, "/etc/hosts"])

#Lab 6A Step 8 - Generate a private key for the root certificate.
subprocess.run(["sudo", "openssl", "genrsa", "-aes256", "-out", "cakey.pem", "2048"])

#Lab 6A Step 11 - Generate a signed root certificate.
subprocess.run(["sudo", "openssl", "req", "-x509", "-new", "-nodes", "-key", "cakey.pem", "-sha256","-days", "1825", "-out", "cacert.pem", "-subj", f"/C=US/ST=CA/L=Seaside/O=SCD/OU=CST311/CN=ca.csumb.test"])

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
def generate_certificate(key_filename, csr_filename, common_name):
    subprocess.run(["sudo", "openssl", "x509", "-req", "-days", "365", "-in", csr_filename, "-CA","cacert.pem", "-CAkey", "cakey.pem", "-CAcreateserial", "-out", key_filename])

generate_certificate(chat_server_key_filename, chat_server_csr_filename, chat_server_common_name)
generate_certificate(web_server_key_filename, web_server_csr_filename, web_server_common_name)
