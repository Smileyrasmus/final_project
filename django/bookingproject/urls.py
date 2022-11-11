from django.urls import include, path
from rest_framework import routers
from bookingapi import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'groups', views.GroupViewSet, basename='group')
router.register(r'bookablelocations', views.BookableLocationViewSet, basename='bookablelocation')
router.register(r'seats', views.SeatViewSet, basename='seat')
router.register(r'locationbookings', views.LocationBookingViewSet, basename='locationbooking')
router.register(r'seatbookings', views.SeatBookingViewSet, basename='seatbooking')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
