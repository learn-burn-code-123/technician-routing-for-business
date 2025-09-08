import hashlib
import os
import binascii

def hash_password(password):
    """Hash a password for storing"""
    # Generate a random salt
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    # Hash the password with the salt
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    # Return the salt and hash
    return (salt + pwdhash).decode('ascii')

def verify_password(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    # Extract the salt
    salt = stored_password[:64]
    # Extract the hash
    stored_hash = stored_password[64:]
    # Hash the provided password with the salt
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                provided_password.encode('utf-8'), 
                                salt.encode('ascii'), 
                                100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    # Compare the hashes
    return pwdhash == stored_hash
