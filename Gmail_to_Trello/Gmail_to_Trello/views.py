from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MailSerializer

from .models import Mail

@api_view(['GET'])      #@api_view(['GET', 'POST'])
def apiOverview(request):
    api_urls = {
        'List':'/mail-list/',



    }
    return Response(api_urls)

@api_view(['GET'])
def mailList(request):
    mails = Mail.objects.all()
    serializer = MailSerializer(mails, many=True)
    return Response(serializer.data)