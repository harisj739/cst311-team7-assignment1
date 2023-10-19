# Generate_certificates.py

from OpenSSL import crypto
import subprocess

# Common Names for the servers
web_server_cn = "www.webpa4.test"
chat_server_cn = "chat_server.pa4.test"

# Generate a certificate for the web server
web_cert = crypto.X509()
web_cert.set_serial_number(1)
web_cert.gmtime_adj_notBefore(0)
web_cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # Valid for a year

web_subject = web_cert.get_subject()
web_subject.CN = web_server_cn

key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)
web_cert.set_pubkey(key)
web_cert.sign(key, "sha256")

with open("web_server.crt", "wb") as web_cert_file:
    web_cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, web_cert))
with open("web_server.key", "wb") as web_key_file:
    web_key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

# Generate a certificate for the chat server
chat_cert = crypto.X509()
chat_cert.set_serial_number(2)
chat_cert.gmtime_adj_notBefore(0)
chat_cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # Valid for a year

chat_subject = chat_cert.get_subject()
chat_subject.CN = chat_server_cn

key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)
chat_cert.set_pubkey(key)
chat_cert.sign(key, "sha256")

with open("chat_server.crt", "wb") as chat_cert_file:
    chat_cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, chat_cert))
with open("chat_server.key", "wb") as chat_key_file:
    chat_key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

# Copy the certificates
subprocess.call(["cp", "web_server.crt", "/etc/ssl/certs/"])
subprocess.call(["cp", "web_server.key", "/etc/ssl/private/"])
subprocess.call(["cp", "chat_server.crt", "/etc/ssl/certs/"])
subprocess.call(["cp", "chat_server.key", "/etc/ssl/private/"])
# Add the IP addresses and names of the CN in /etc/hosts.
subprocess.call(["sudo", "sed", "-i", "5i 127.0.0.1       chat_server.pa4.test", "/etc/hosts"])
subprocess.call(["sudo", "sed", "-i", "6i 10.0.0.5        www.webpa4.test", "/etc/hosts"])
