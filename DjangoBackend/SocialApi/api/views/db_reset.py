from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.management import call_command
from django.conf import settings



class ResetViewSet(viewsets.ViewSet):

    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def reset_db(self, request):
        if not settings.DEBUG:
            return Response({'detail': 'This command can only be run in DEBUG mode'}, status=403)

        try:
            call_command('reset_db')
            return Response({'detail': 'Database has been reset successfully'}, status=200)
        except Exception as e:
            return Response({'detail': str(e)}, status=500)
