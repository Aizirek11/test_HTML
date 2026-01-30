from rest_framework import serializers
from .models import TestCategory, Question, Answer, Result
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TestCategory



# Сериализатор ответа
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']


# Сериализатор вопроса
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']

from rest_framework import serializers
from .models import TestCategory

class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = '__all__'


# Сериализатор для отправки результатов
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'user', 'category', 'score', 'total', 'date']


# Сериализатор пользователя (профиль)
class UserSerializer(serializers.ModelSerializer):
    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'results']