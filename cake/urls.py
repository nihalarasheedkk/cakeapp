from django.urls import path

from cake.views import RegisterView,SignInView,CategoryCreateView,remove_category,\
    CakeCreateView,CakeListView,remove_cakeview,CakeVarientView,CakeDetailView,CakeUpdateView,CakeVarientUpdateView,remove_varient

urlpatterns=[
    path("signup/",RegisterView.as_view(),name="sign-up"),
    path("",SignInView.as_view(),name="signin"),
    path("category/add",CategoryCreateView.as_view(),name="add-category"),
    path("categories/<int:pk>/remove",remove_category,name="remove-category"),
    path("cakes/add",CakeCreateView.as_view(),name="cake-add"),
    path("cakes/list",CakeListView.as_view(),name="cake-list"),
    path("cakes/<int:pk>/remove",remove_cakeview,name="cake-remove"),
    path("cakes/<int:pk>/varients/add",CakeVarientView.as_view(),name="add-cakevarient"),
    path("cakes/<int:pk>/",CakeDetailView.as_view(),name="cake-detail"),
    path("cakes/<int:pk>/change",CakeUpdateView.as_view(),name="cake-update"),
    path("varients/<int:pk>/change/",CakeVarientUpdateView.as_view(),name="update-varient"),
    path("varients/<int:pk>/remove",remove_varient,name="del-varient")
]