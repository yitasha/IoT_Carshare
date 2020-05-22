from passlib.hash import sha256_crypt

password = sha256_crypt.hash("TestPassword")
print(password)