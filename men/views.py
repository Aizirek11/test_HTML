from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TestCategory, Question, Answer, Result
from .serializers import TestCategorySerializer, QuestionSerializer, AnswerSerializer, ResultSerializer, UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

# ---------------------------
# DRF: Профиль пользователя
# ---------------------------
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# ---------------------------
# HTML: Профиль пользователя
# ---------------------------
def profile_page(request):
    user = request.user
    results = user.results.all().order_by('-date') if user.is_authenticated else []
    return render(request, 'men/profile.html', {'user': user, 'results': results})

# ---------------------------
# DRF: Список категорий тестов
# ---------------------------
class TestCategoryListView(generics.ListAPIView):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer

class CreateCategoryView(generics.CreateAPIView):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer

# ---------------------------
# HTML: Список категорий тестов
# ---------------------------
def categories_page(request):
    categories = TestCategory.objects.all()
    return render(request, 'men/categories.html', {'categories': categories})


# ---------------------------
# DRF: Список вопросов по категории
# ---------------------------
class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Question.objects.filter(category_id=category_id)

# ---------------------------
# HTML: Вопросы по категории
# ---------------------------
def questions_page(request, category_id):
    category = get_object_or_404(TestCategory, id=category_id)
    questions = category.questions.all()

    if request.method == "POST":
        score = 0
        total = questions.count()

        for question in questions:
            selected_answer_id = request.POST.get(f"question_{question.id}")
            if selected_answer_id:
                selected_answer = Answer.objects.get(id=int(selected_answer_id))
                if selected_answer.is_correct:
                    score += 1

        if request.user.is_authenticated:
            Result.objects.create(user=request.user, category=category, score=score, total=total)

        return redirect('history_page')

    return render(request, 'men/questions.html', {'category': category, 'questions': questions})

# ---------------------------
# HTML: Создание вопроса через форму
# ---------------------------
def create_question_page(request):
    categories = TestCategory.objects.all()
    message = ""

    if request.method == "POST":
        category_id = request.POST.get("category")  # <- здесь должно прийти значение
        text = request.POST.get("text")
        correct = request.POST.get("correct_answer")

        if not category_id:  # защита от пустого значения
            message = "Выберите категорию!"
        else:
            question = Question.objects.create(category_id=category_id, text=text)

            for i in range(1, 5):
                answer_text = request.POST.get(f"answer_text_{i}")
                is_correct = (str(i) == correct)
                Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)

            message = "Вопрос успешно добавлен!"

    return render(request, "men/create_question.html", {"categories": categories, "message": message})

# ---------------------------
# DRF: Создание вопроса через API
# ---------------------------
class CreateQuestionView(APIView):
    def post(self, request):
        category_id = request.data.get("category")
        text =request.data.get("text")
        answers_data = request.data.get("answers")

        question = Question.objects.create(category_id=category_id, text=text)

        for ans in answers_data:
            Answer.objects.create(
                question=question,
                text=ans["text"],
                is_correct=ans.get("is_correct", False)
            )
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ---------------------------
# DRF: Отправка результатов теста
# ---------------------------
class SubmitTestView(APIView):
    def post(self, request):
        user = request.user
        category_id = request.data.get("category")
        answers = request.data.get("answers")

        score = 0
        total = len(answers)

        for ans in answers:
            question = Question.objects.get(id=ans["question"])
            selected_answer = Answer.objects.get(id=ans["answer"])
            if selected_answer.is_correct:
                score += 1

        result = Result.objects.create(user=user, category_id=category_id, score=score, total=total)
        serializer = ResultSerializer(result)
        return Response(serializer.data)

# ---------------------------
# HTML: История тестов
# ---------------------------
def history_page(request):
    results = request.user.results.all().order_by('-date') if request.user.is_authenticated else []
    return render(request, 'men/history.html', {'results': results})

# ---------------------------
# HTML: Рейтинг студентов
# ---------------------------
def rating_page(request):
    users = User.objects.annotate(total_score=Sum('results__score')).order_by('-total_score')
    return render(request, 'men/rating.html', {'users': users})
