# basic example of using bcrypt
import bcrypt

# Hash a password
password = "my_secure_password".encode('utf-8')
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

# Check a password against a hash
entered_password = "entered_password".encode('utf-8')
if bcrypt.checkpw(entered_password, hashed_password):
    print("Password is correct!")
else:
    print("Password is incorrect.")
