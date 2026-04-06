from utils.auth import register_user, login_user

print(register_user("test", "1234"))  # True first time
print(login_user("test", "1234"))     # True
print(login_user("test", "wrong"))    # False