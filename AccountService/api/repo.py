from api import models


def user_exists(username: str) -> bool:
    return models.User.objects.filter(username=username).exists()


def save_token(user, access_token: str, refresh_token: str):
    models.IssuedToken.objects.create(user=user,
                                      token=access_token,
                                      refresh_token=refresh_token)


def invalidate_all_tokens_for_user(user):
    for token in models.IssuedToken.objects.filter(user=user).all():
        token.is_invalidated = True
        token.save()


def is_refresh_token_valid(refresh_token: str) -> bool:
    return not models.IssuedToken.objects.filter(
        refresh_token=refresh_token,
        is_invalidated=True
    ).exists()


def all_users(*args, **kwargs):
    return models.User.objects.filter(*args, deleted=False, **kwargs)
