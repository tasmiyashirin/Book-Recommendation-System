from django.conf.urls import url
from mainapp import views

urlpatterns = [
    url('^$',views.BookRecommend.as_view(), name='bookrecommend'),
    url(r'^toptenbooks/',views.TopTenBooks.as_view(), name='toptenbooks'),
    url(r'^toptenwriters',views.TopTenWriters.as_view(), name='toptenwriters'),
    url(r'^mostreviewedbooks',views.MostReviewedBooks.as_view(), name='mostreviewedbooks'),
]
