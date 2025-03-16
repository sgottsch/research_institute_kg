from django.urls import path

from . import views

urlpatterns = [
    path("", views.KGView.as_view(), name="kgview"),
    path("people", views.KGPeopleView.as_view(), name="kgpeopleview"),
    path("location", views.KGLocationView.as_view(), name="kglocationview"),
    path("language", views.KGLanguageView.as_view(), name="kglanguageview"),
    path("workplace", views.KGWorkplaceView.as_view(), name="kgworkplaceview"),
    path(
        "researchfield", views.KGResearchFieldView.as_view(), name="kgresearchfieldview"
    ),
    path("papers", views.KGPaperView.as_view(), name="kgpaperview"),
    path(
        "conferenceauthor",
        views.KGConferenceAuthorView.as_view(),
        name="kgconferenceauthorview",
    ),
    path(
        "journalauthor", views.KGJournalAuthorView.as_view(), name="kgjournalauthorview"
    ),
]
