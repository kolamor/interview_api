from rest_framework import generics
from .models import *
from .api.serializers import QuestionSerializer, InterviewSerializer, InterviewSerializer, QuestionSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import mixins


def wrapper_serializer(serializer):
    def _serializer(func):
        def wrapper(*args, **kwargs):
            args[0].serializer_class = serializer
            return func(*args, **kwargs)
        return wrapper
    return _serializer


def block_while_null(model, field='ended_at',):
    def block(func):
        def wrapper(*args, **kwargs):
            self, request, *_ = args
            data = request.data
            if not data.get(field, None):
                obj = model.objects.all()
                if not getattr(obj, field, None):
                    return Response({"error": f'field {field }is Null in db or does not sent.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            return func(*args, **kwargs)
        return wrapper
    return block


class UserAuthenticatorPermissionView:
    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        if self.request.method != ['GET', 'POST']:
            permission_classes = [SessionAuthentication, TokenAuthentication]
            return [permission() for permission in permission_classes]
        return super().get_authenticators()


class AdminAuthenticatorPermissionView:
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        if self.request.method != 'GET':
            permission_classes = [SessionAuthentication, TokenAuthentication]
            return [permission() for permission in permission_classes]
        return super().get_authenticators()


class InterviewListView(generics.ListAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                        AdminAuthenticatorPermissionView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class InterviewDetailView(mixins.CreateModelMixin,
                          generics.RetrieveAPIView,
                          mixins.UpdateModelMixin,
                          AdminAuthenticatorPermissionView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def post(self, request, pk, *args, **kwargs):
        return self.create(request, pk, *args, **kwargs)

    @block_while_null(Interview, field='ended_at')
    def put(self, request, pk, format=None):
        return self.update(request, pk, format=None)

    def delete(self, request, pk, format=None):
        interview = self.get_object()
        if interview.ended_at is None:
            return Response({"error": 'field ended_at is Null in db.'},
                            status=status.HTTP_400_BAD_REQUEST)
        interview.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context_key = getattr(self.serializer_class.Meta, ('exist_key_in_context'), None)
        if context_key and 'pk' in self.kwargs:
            context.update({context_key: self.kwargs['pk']})
        return context


class QuestionListView(generics.ListAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                       AdminAuthenticatorPermissionView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                         AdminAuthenticatorPermissionView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @block_while_null(Interview, field='ended_at')
    def put(self, request, pk, format=None):
        return self.update(request, pk, format=None)

    def delete(self, request, pk, format=None):
        interview = self.get_object()
        interview.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            Token.objects.get_or_create(user=user)
            return Response({"token": user.auth_token.key},)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ActiveInterviewListView(generics.ListAPIView, UserAuthenticatorPermissionView):
    queryset = Interview.objects.all().filter(ended_at__isnull=True).filter(started_at__isnull=False)
    serializer_class = InterviewSerializer

#
# class PassingInterview(generics.ListAPIView,
#                        mixins.CreateModelMixin,
#                        mixins.UpdateModelMixin,
#                        UserAuthenticatorPermissionView):
#
#     queryset = UserAnswer.objects.all()
#     serializer_class = UserAnswerSerializer
#
#     def post(self, request, *args, **kwargs):
#         """ id answer, user_id, text( no required) """
#
#         return self.create(request, *args, **kwargs)







