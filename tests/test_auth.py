from security.auth import hash_password, verify_password

def test_password_hashing():
    password = "StrongPassword123!"
    hashed = hash_password(password)
    assert password not in hashed
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)
