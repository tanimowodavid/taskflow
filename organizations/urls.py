from django.urls import path
from .views import OrganizationListCreateView, InviteCreateView, AcceptInviteView

urlpatterns = [
    path("", OrganizationListCreateView.as_view(), name="org-list-create"),
    path("invite/", InviteCreateView.as_view()),
    path("invite/accept/<uuid:token>/", AcceptInviteView.as_view()),
]

