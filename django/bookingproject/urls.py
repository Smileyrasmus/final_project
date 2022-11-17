from django.urls import include, path
from rest_framework import routers
from alternativebookingapi import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"groups", views.GroupViewSet, basename="group")
router.register(r"orders", views.OrderViewSet, basename="order")
router.register(r"locations", views.LocationViewSet, basename="location")
router.register(r"bookableitems", views.BookableItemViewSet, basename="bookableitem")
router.register(r"events", views.EventViewSet, basename="event")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
