from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from sentry_sdk import capture_exception

from .services.provider.google import GooglePlatform
from .services.provider.microsoft import MicrosoftPlatform
from .utils import google_connection, create_doc
from .models import Memo, Template
from .serializers import MemoSerializer, TemplateSerializer
from user.permissions import IsAdmin
from core import settings


provider = {
    'GOOGLE': GooglePlatform,
    'SMS': MicrosoftPlatform
}
default_provider = "GOOGLE"


class MemoViewset(viewsets.ModelViewSet):
    """Card view sets"""
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """Endpoint to create memo"""
        try:
            serializer = self.get_serializer(data=request.data)
            google_folder_id = settings.GOOGLE_DRIVE_ID
            if serializer.is_valid():
                file_title = request.data['title']
                doc_create = provider[default_provider](credential_path=settings.GOOGLE_CREDENTIALS,
                                               title=file_title).create_document(google_folder_id=google_folder_id)
                serializer.save(url=doc_create['url'], document_id=doc_create['document_id'],
                                provider=default_provider, created_by=self.request.user)
                return Response({'success': True, 'message': 'created successfully', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            capture_exception(e)
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
         parameters=[
             OpenApiParameter("template_id", OpenApiTypes.UUID, OpenApiParameter.QUERY, required=True)])
    @action(methods=['POST'], detail=False, serializer_class=MemoSerializer,
            url_path='template', permission_classes=[IsAuthenticated])
    def create_memo_from_template(self, request, pk=None):
        """This endpoint create a memo from an exisiting template"""
        try:
            template_id = self.request.query_params.get('template_id', None)
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request})
            if serializer.is_valid():
                file_title = request.data['title']
                print(settings.GOOGLE_CREDENTIALS)
                doc_create = provider[default_provider](credential_path=settings.GOOGLE_CREDENTIALS,
                                                title=file_title).create_from_template(template_id)
                serializer.save(url=doc_create['url'], document_id=doc_create['document_id'],
                                provider=default_provider, created_by=self.request.user)
                return Response({'success': True, 'message': f'created successfully',
                                 'data': serializer.data}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            capture_exception(e)
            return Response({'success': False, 'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TemplateViewset(viewsets.ModelViewSet):
    """Card view sets"""
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """Endpoint to create template """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                google_folder_id = settings.GOOGLE_DRIVE_ID
                file_name = request.data['title']
                doc_create = provider[default_provider](credential_path='app/google_credentials.json',title=file_name).\
                    create_document(google_folder_id=google_folder_id)
                serializer.save(url=doc_create['url'], document_id=doc_create["document_id"],
                                provider=default_provider, created_by=self.request.user)
                return Response({'success': True, 'message': 'created successfully', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            capture_exception(e)
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


