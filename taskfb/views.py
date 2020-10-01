from rest_framework import generics
from .models import *
from .api.serializers import  InterviewSerializer, QuestionSerializer, \
    UserAnswerSerializer, UserAnswerViewSerializer
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
    """Отдает статус 400 если у модели нет поля в db"""
    def block(func):
        def wrapper(*args, **kwargs):
            self, request, *_ = args
            data = request.data
            if not data.get(field, None):
                obj = model.objects.filter(pk=request.parser_context['kwargs']['pk'])
                if not getattr(obj, field, None):
                    return Response({"error": f'field {field }is Null in db or does not sent.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            return func(*args, **kwargs)
        return wrapper
    return block


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
        """передаем ключ к контекс"""
        context = super().get_serializer_context()
        context_key = getattr(self.serializer_class.Meta, ('exist_key_in_context'), None)
        if context_key and 'pk' in self.kwargs:
            context.update({context_key: self.kwargs['pk']})
        return context


class QuestionListView(generics.ListAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                       AdminAuthenticatorPermissionView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetailView(generics.RetrieveAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                         AdminAuthenticatorPermissionView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'interview' not in data:
            return Response({"error": "interview field required"}, status=status.HTTP_201_CREATED)
        data['id'] = kwargs['pk']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def put(self, request, pk, format=None):
        self.get_interview()
        return self.update(request, pk, format=None)

    def delete(self, request, pk, format=None):
        question = self.get_interview()
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_interview(self):
        question = self.get_object()
        interview = Interview.objects.get(pk=question.interview.pk)
        if not interview.ended_at:
            return Response({"error": f'field ended_at is Null in db or does not sent.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return question


class ActiveInterviewListView(generics.ListAPIView, UserAuthenticatorPermissionView):
    queryset = Interview.objects.all().filter(ended_at__isnull=True).filter(started_at__isnull=False)
    serializer_class = InterviewSerializer


class UserAnswerListView(generics.ListAPIView,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         ):

    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerViewSerializer

    permission_classes = ()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qw = UserAnswer.objects.all().filter(user_id=self.kwargs['pk'])
        return qw


class UserAnswerDetailView(mixins.CreateModelMixin,
                           generics.RetrieveAPIView,
                           mixins.UpdateModelMixin,
                           ):
    permission_classes = ()
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def post(self, request, pk, *args, **kwargs):
        return self.create(request, pk, *args, **kwargs)






