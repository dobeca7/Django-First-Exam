from django.urls import path

from academies.views import AcademyCreateView, AcademyDeleteView, AcademyDetailView, AcademyEditView, AcademyListView

urlpatterns = [
    path("", AcademyListView.as_view(), name="academy-list"),
    path("create/", AcademyCreateView.as_view(), name="academy-create"),
    path("slug/<slug:slug>/", AcademyDetailView.as_view(), name="academy-detail-slug"),
    path("<int:pk>/", AcademyDetailView.as_view(), name="academy-detail"),
    path("<int:pk>/edit/", AcademyEditView.as_view(), name="academy-edit"),
    path("<int:pk>/delete/", AcademyDeleteView.as_view(), name="academy-delete"),
]
