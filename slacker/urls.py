from django.contrib import admin
from django.urls import path

from django.conf.urls import url
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include(('slacker.core.urls', 'core'), namespace='core')),
    url(r'^slack/', include(('slacker.slack.urls', 'slack'), namespace='slack')),
]
