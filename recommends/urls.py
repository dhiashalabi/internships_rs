from django.urls import path

from recommends.views import RecommendsView, save_csv_file, make_recommendation

urlpatterns = [
    path("recommends/", RecommendsView.as_view(), name="recommends"),
    path("save-file/", save_csv_file, name="save-file"),
    path("make-recommendation/", make_recommendation, name="make-recommendation"),
]
