from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings

from . import views

urlpatterns = [
    # Default routes
    path('', views.dashboard, name="dashboard"), # Dashboard
    path('products/', views.products, name="products"), # Products
    path('customers/<str:pk>/', views.customer, name="customers"), # Customers ( i.e localhost:8888/customers/2 )

    # User Routes
    path('user/', views.userPage, name="user-page"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"), 
    path('account/', views.accountSettings, name="account"),

    # CRUD forms
    path('create_order/<str:pk>/', views.createOrder, name="create_order"), # Create a new Order
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"), # Update an existing order ( i.e localhost:8888/update_order/3 )
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"), # Delete an existing Order ( i.e localhost:8888/delete_order/5 )

    # Email routes
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    path('rest_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),


    # favicon.ico route
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
]