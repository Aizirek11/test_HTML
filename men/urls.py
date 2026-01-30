from django.urls import path
from .views import profile_page,CreateCategoryView, create_question_page,categories_page, questions_page, history_page, rating_page

urlpatterns = [
    path('profile/', profile_page, name='profile_page'),
    path('categories/', categories_page, name='categories_page'),
    path('categories/<int:category_id>/', questions_page, name='questions_page'),
    path('history/', history_page, name='history_page'),
    path('rating/', rating_page, name='rating_page'),
    path('create-question/html/', create_question_page, name='create_question_page'),
    path('categories/create/', CreateCategoryView.as_view(), name='create_category_api'),
]