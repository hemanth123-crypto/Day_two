from user_auth import UserAuth

auth = UserAuth()

def test_register_login():
    assert auth.register("user1", "password1") == True
    assert auth.login("user1", "password1") == True

def test_register_existing_user():
    assert auth.register("admin", "newpassword") == False

def test_login_wrong_password():
    auth.register("user2", "password2")
    assert not auth.login("user2", "wrongpassword")