from django.urls import path
from .views import Signup
from .views import Login 
from .views import Signup1
from .views import Login1 
from . import views
from django.contrib.auth import views as auth_views  

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('profile/', views.profile, name="profile"),

	path('update_item/', views.updateItem, name="update_item"),

	path('process_order/', views.processOrder, name="process_order"),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
	path('logout', views.logout , name='logout'),
	path('signup1/', Signup1.as_view(), name='signup1'),
    path('login1/', Login1.as_view(), name='login1'),
	path('password_reset/',auth_views.PasswordResetView.as_view(template_name = "store/password_reset_form.html"),name='password_reset'),
	path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = "store/password_reset_done.html"),name='password_reset_done'),
	path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "store/password_reset_confirm.html"),name='password_reset_confirm'),
	path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name = "store/password_reset_complete.html"),name='password_reset_complete'),
]
