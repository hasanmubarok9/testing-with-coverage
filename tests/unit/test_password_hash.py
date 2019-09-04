from app.users.views import make_password_hash

def test_password_hash():
    test_user_password = 'password-tria'
    test_user_password_hash = make_password_hash(test_user_password)
    assert test_user_password_hash != test_user_password