from ..models import *
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.exceptions import ErrorDetail, ValidationError
from django.db import transaction


class UnknownFieldsSerializerMixin:
    def is_valid(self, raise_exception=False):
        super().is_valid(False)

        if hasattr(self.Meta, 'optional_fields'):
            fields_keys = self.Meta.optional_fields.copy()
            fields_keys = set(list(fields_keys) + list(self.fields.keys()))
        else:
            fields_keys = set(self.fields.keys())

        input_keys = set(self.initial_data.keys())
        additional_fields = input_keys - fields_keys

        if bool(additional_fields):
            self._errors['fields'] = ['Additional fields not allowed: {}.'.format(list(additional_fields))]
        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)


class AtomicCreateUpdate:

    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ExistForCreateMixin:

    def create(self, validated_data):
        exist_key_in_context = getattr(self.Meta, 'exist_key_in_context', None)
        if exist_key_in_context and self.context.get(exist_key_in_context):
            validated_data.update({'pk': self.context[exist_key_in_context]})
            exist = self.Meta.model.objects.filter(pk=self.context[exist_key_in_context]).count()
            if exist:
                raise ValidationError(f'error already exists {validated_data}')
        return super().create(validated_data)
    
    class Meta:
        exist_key_in_context = ''


class AnswerSerializer(UnknownFieldsSerializerMixin, AtomicCreateUpdate,
                       ExistForCreateMixin, serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'user_id']
        optional_fields = ['question']
        exist_key_in_context = 'answer_pk'

    def create(self, validated_data):
        """Варианты Question settings.QUESTION_OPTIONS"""
        if isinstance(validated_data['question'], Question):
            question = validated_data['question']
        elif isinstance(validated_data['question'], int):
            question = Question.objects.get(pk=validated_data['question'])
        type_question = question.type_question

        if type_question == 'text' or 'choice':
            data = self.Meta.model.objects.filter(user_id=validated_data['user_id'],
                                                  question=validated_data['question']).count()
            if data:
                raise ValidationError("The answer does not create. ")

        return super().create(validated_data=validated_data)


class QuestionSerializer(UnknownFieldsSerializerMixin, AtomicCreateUpdate,
                         ExistForCreateMixin, WritableNestedModelSerializer):
    answers = AnswerSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type_question', 'answers']
        optional_fields = ['interview']
        exist_key_in_context = 'question_pk'


class InterviewSerializer(UnknownFieldsSerializerMixin, ExistForCreateMixin,
                          AtomicCreateUpdate, WritableNestedModelSerializer):
    questions = QuestionSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Interview
        fields = ['id', 'title', 'started_at', 'ended_at', 'description', 'questions']
        optional_fields = []
        exist_key_in_context = 'interview_pk'


# class UserAnswerSerializer(WritableNestedModelSerializer):
#     answer = AnswerSerializer(many=True, read_only=False, required=True)
#
#     class Meta:
#         model = UserAnswer
#         fields = ['id',  'answer', 'text', 'user_id', ]
#         optional_fields = ['text', ]
#
#     # def create(self, validated_data):


