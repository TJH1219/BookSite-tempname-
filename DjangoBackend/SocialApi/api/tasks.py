from celery import shared_task
from .token_management import cleanup_expired_tokens

@shared_task
def cleanup_tokens_task():
    return cleanup_expired_tokens()