from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User


# Категория теста
class TestCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Вопросы теста
class Question(models.Model):
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text

# Варианты ответа
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)  # правильный ответ выделяется так

    def __str__(self):
        return self.text

# Результаты студента
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

# Create your models here.
