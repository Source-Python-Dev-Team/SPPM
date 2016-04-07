from django.conf.urls import url

from .views import UserListView, UserView

urlpatterns = [
    url(
        regex=r'^$',
        view=UserListView.as_view(),
        name='user-list'
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=UserView.as_view(),
        name='user-detail',
    ),
]
