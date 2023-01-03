import imp
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/employed/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('colleges/', include("colleges.urls")),
    path("students/", include("students.urls")),
    path('corporates/', include("corporates.urls")),
    path('tests/', include("tests.urls")),
    path('notifications/', include("notify.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)