
from main.models import User
import os
import random


def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        registered_user = filtered_user_by_email[0]

        return {
            'username': registered_user.username,
            'email': registered_user.email}

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': os.environ.get('SOCIAL_SECRET', "")}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        authenticated_user = user
        print(authenticated_user)
        return {
            'email': authenticated_user.email,
            'username': authenticated_user.username
        }