from django.urls import include, path
from rest_framework import routers
from alternativebookingapi import views as alternativebookingapi_views
from accounts import views as accounts_views
from django.contrib import admin
from rest_framework.authtoken import views as token_views

router = routers.DefaultRouter()
router.register(r"users", accounts_views.UserViewSet, basename="user")
router.register(r"groups", accounts_views.GroupViewSet, basename="group")
router.register(r"orders", alternativebookingapi_views.OrderViewSet, basename="order")
router.register(
    r"bookings", alternativebookingapi_views.BookingViewSet, basename="booking"
)
router.register(
    r"locations", alternativebookingapi_views.LocationViewSet, basename="location"
)
router.register(
    r"bookableitems",
    alternativebookingapi_views.BookableItemViewSet,
    basename="bookableitem",
)
router.register(r"events", alternativebookingapi_views.EventViewSet, basename="event")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", token_views.obtain_auth_token),
]
