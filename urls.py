from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('admin/', views.admin, name="admin"),

    #path('pageindex', views.pageindex, name="pageindex"),

    path('searchpage', views.multiplesearch, name="searchpage"),

    path('page1', views.invdisplay, name="invdisplay"),
    path('Create', views.invinsert, name="invinsert"),
    path('Create1', views.invinsert1, name="invinsert1"),
    path('Edit1/<int:id>', views.invedit, name="invedit"),
    path('Update1/<int:id>', views.invupdate, name="invupdate"),
    path('Delete1/<int:id>', views.invdel, name="invdel"),

    path('page2', views.mbdisplay, name="mbdisplay"),
    path('Create2', views.mbinsert,name="mbinsert"),
    path('Edit2/<int:id>', views.mbedit, name="mbedit"),
    path('Edit2/<int:id>', views.mbedit, name="mbedit"),
    path('Update2/<int:id>', views.mbupdate, name="mbupdate"),
    path('Delete2/<int:id>', views.mbdel, name="mbdel"),

    path('page3', views.webpage3, name="webpage3"),
    path('testp', views.webtestp, name="webtestp"),
    path('testrms1', views.webtestrms1, name="webtestrms1"),
    path('testrms2', views.webtestrms2, name="webtestrms2"),
    path('page4', views.testrms1, name="testrms1"),

    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('customer1/<str:pk_test1>/', views.customer1, name="customer1"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),


]