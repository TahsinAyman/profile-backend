import hashlib
import json

from models import Authentication, db

try:
    user = input("Enter User: ")
    password = input("Enter Password: ")

    print(f"User: {user}")
    print(f"Password: {hashlib.md5(password.encode()).hexdigest()}")

    encrypted_password = hashlib.md5(password.encode()).hexdigest()

    auth = Authentication(user=user, password=encrypted_password)
    db.session.add(auth)
    db.session.commit()
except Exception as e:
    print(e)


# print([json.loads(i.__str__()) for i in Authentication.query.all()])
# print(f"User: {input('User: ')}")
# print(f"Password: {hashlib.md5(input('Password: ').encode()).hexdigest()}")
# 0bcc0dd770173491c51453c1eb2b8486
# 0bcc0dd770173491c51453c1eb2b8486

