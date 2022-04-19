"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Base import views as b_views
from LoginLogout import views as l_views

urlpatterns = [path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path('accounts/HomePage/', b_views.HomePage, name="HomePage"),
    path('admin/', admin.site.urls),
    path('', l_views.LoginOrInscription, name='LoginOrInscription'),
    path('inscription/', l_views.Inscription, name='Inscription'),
    path('logout', l_views.logout_request, name='logout', ),
    path('ticket_creation/', b_views.ticket_upload, name='ticket_creation'),
    path('review_and_ticket_creation/', b_views.review_and_ticket_upload, name='review_and_ticket_creation'),
    path('subscribers_page/', b_views.subscribers_page, name='subscribers_page'),
    path('review_creation/', b_views.review_upload, name='review_creation'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
