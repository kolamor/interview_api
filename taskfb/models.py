from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


__all__ = ('Interview', 'Question', 'Answer', )

USER = get_user_model()


class Interview(models.Model):
    title = models.CharField(max_length=255)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    question_options = settings.QUESTION_OPTIONS

    text = models.TextField()
    type_question = models.CharField(choices=question_options, max_length=255)
    interview = models.ForeignKey(Interview, related_name='questions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return str(self.text)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    user_id = models.IntegerField()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return str(self.text)


# class UserAnswer(models.Model):
#     user_id = models.IntegerField()
#     answer = models.ManyToManyField(Answer, related_name='user_answers')
#     text = models.TextField(blank=True)
#
#     def __str__(self):
#         return str(f'{self.answer}')
