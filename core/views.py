from django.shortcuts import render
from tkinter import E
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
# Create your views here.

class HandleFileUpload(APIView):

    def home(request):
        return render(request,'index.html')

    def post(self,request):
        try:
            data= request.data
            serializer = FileListSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' :200,
                    'message': 'Files uploaded Successfully...'
                })
            return Response({
                'status': 400,
                'message' : 'Something went Wrongg...',
                'data' : serializer.errors
            })
        except Exception as e:
            return Response({
                'status': 500,
                'message': 'Internal Server Error',
                'error': str(e)
            })
