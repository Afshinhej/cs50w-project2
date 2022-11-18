from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("category", views.categoryindex, name="categoryindex"),
    path("category/<int:category_pk>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listings/<int:auction_pk>", views.auction, name="auction"),
    path("comment/<int:auction_pk>", views.comment, name="comment")
]
