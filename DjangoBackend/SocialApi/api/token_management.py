import logging
from datetime import timedelta
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status

logger = logging.getLogger(__name__)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            if self._detect_suspicious_activity(request):
                logger.warning(f"Suspicious activity detected")
                return Response(
                    {
                        "detail" : "Too many refresh attempts"
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            response = super().post(request, *args, **kwargs)
            logger.info(f"Token successfully refreshed")
            return response
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return Response(
                {
                    "detail" : "Error refreshing token"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _detect_suspicious_activity(self, request):
        last_hour = timezone.now() - timedelta(hours=1)
        refresh_count = OutstandingToken.objects.filter(
            user=request.user,
            created_at__gte=last_hour
        ).count()

        THRESHOLD = 10
        return refresh_count > THRESHOLD

def cleanup_expired_tokens():
    try:
        expired_tokens = OutstandingToken.objects.filter(expires_at__lte=timezone.now())
        count = expired_tokens.count()
        expired_tokens.delete()

        logger.info(f"Cleaned up {count} tokens")
        return count
    except Exception as e:
        logger.error(f"Error cleaning up expired tokens: {e}")
        raise
