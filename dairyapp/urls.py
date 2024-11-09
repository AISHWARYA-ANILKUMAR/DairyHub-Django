"""Dairyhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    
    ######### LOGIN AND LOGOUT 3333333333
    path('',views.index),
    path('all_login',views.all_login),
    path('user_registration', views.user_registrationxxx, name='user_register'),
    path('farmer_register', views.farmer_register, name='farmer_register'),
    path('logout/',views.logout),
    
    
    
    ################### ADMIN #####################
    
    
    path('adminn',views.admin),
    path('admin_add_product',views.admin_add_product,name="admin_add_product"),
    path('update_product/<id>',views.update_product),
    path('delete_product/<id>',views.delete_product),
    path('admin_view_one_eartag_request/<str:ek>',views.admin_view_one_eartag_request,name='admin_view_one_eartag_request'),
    path('admin_view_eartag_request',views.admin_view_eartag_request,name='admin_view_eartag_request'),
    path('admin_accept/<id>/<farmer_email>',views.admin_accept),
    path('admin_reject/<id>/<farmer_email>',views.admin_reject),                                                                                                  
    path('admin_miss_accept/<id>',views.admin_miss_accept),
    path('admin_miss_reject/<id>',views.admin_miss_reject),
    path('admin_misseartag_view',views.admin_misseartag_view),
    path('admin_1_misseartag_view/<id>',views.admin_1_misseartag_view,name='admin_1_misseartag_view'),
    path('admin_re_ai_view',views.admin_re_ai_view,name='admin_re_ai_view'),
    path('admin_re_ai_accept/<id>',views.admin_re_ai_accept,name='admin_re_ai_accept'),
    path('admin_re_ai_reject/<id>',views.admin_re_ai_reject),
    path('admin_view_checkups',views.admin_view_checkups),
    path('admin_1_view_checkup/<id>',views.admin_1_view_checkup,name='admin_1_view_checkup'),
    path('admin_checkup_accept/<id>',views.admin_checkup_accept),
    path('admin_checkup_reject/<id>',views.admin_checkup_reject),
    path('admin_view_ai_all',views.admin_view_ai_all,name='admin_view_ai_all'),
    path('admin_ai_accept/<id>',views.admin_ai_accept),
    path('admin_ai_reject/<id>',views.admin_ai_reject),
    path('admin_1_ai_view/<id>',views.admin_1_ai_view,name='admin_1_ai_view'),
    path("admin_view_farmers",views.admin_view_farmers,name="admin_view_farmers"),
    path("admin_view_eartag_report",views.admin_view_eartag_report,name="admin_view_eartag_report"),
    path("admin_misseartag_view_report",views.admin_misseartag_view_report,name="admin_misseartag_view_report"),
    path("admin_view_ai_report",views.admin_view_ai_report,name="admin_view_ai_report"),
    path("admin_re_ai_report",views.admin_re_ai_report,name="admin_re_ai_report"),
    path("admin_view_checkups_report",views.admin_view_checkups_report,name="admin_view_checkups_report"),
    path("admin_view_orders", views.admin_view_orders),
    path("admin_view_order_more/<id>", views.admin_view_order_more),
    path("admin_view_all_products_report",views.admin_view_all_products_report),
    path("admin_view_farmers_cattle/<id>",views.admin_view_farmers_cattle),
    path("admin_update_status",views.admin_update_status),
    path("admin_view_cattles_report",views.admin_view_cattles_report),
    path("admin_view_cattles_report_more/<id>",views.admin_view_cattles_report_more),

    
    
    #################### FARMER #####################################3
    
    
    path('eartag_register',views.eartag_register),
    path('eartag_register',views.eartag_register),
    path('farmer_view_eartag',views.farmer_view_eartag),
    path('farmer_1_eartag_view/<id>',views.farmer_1_eartag_view,name='farmer_1_eartag_view'),
    path('eartag_re_request/<int:id>/<regidate>',views.eartag_re_request),
    path('farmer_view_misseartag',views.farmer_view_misseartag),
    path('farmer_page', views.farmer_page),
    path('AI_request',views.AI_request,name='AI_request'),
    path('farmer_view_ai_all',views.farmer_view_ai_all,name='farmer_view_ai_all'),
    path('AI_re_request/<int:id>/<str:near_veterinary_hospital>/', views.AI_re_request, name='AI_re_request'),
    path('farmer_view_re_ai',views.farmer_view_re_ai,name='farmer_view_re_ai'),
    path('farmer_healthcheckup/<id>',views.farmer_healthcheckup),
    path('farmer_healthcheckup',views.farmer_healthcheckup),
    path('farmer_checkups',views.farmer_checkups),
    path('farmer_view_checkup',views.farmer_view_checkup),
    path('farmer_view_profile',views.farmer_view_profile),
    path('farmer_view_one_product/<pro_id>', views.farmer_view_one_product),
    path("farmer_add_to_cart",views.farmer_add_to_cart),

    path('farmer_cart_details_view', views.farmer_cart_details_view),
    path("farmer_cart/<id>",views.farmer_removecart),
    path("farmer_pay",views.farmer_pay),
    path("farmer_sa_post",views.farmer_sa_post),
    path("farmer_sa",views.farmer_sa),
    path("farmer_pay_post",views.farmer_pay_post),
    path("farmer_fav_view", views.farmer_fav_view),
    path("farmer_fav_product/<id>",views.farmer_fav_product),
    path("farmer_view_own_orders",views.farmer_view_own_orders),
    path("farmer_view_order_more/<id>",views.farmer_view_order_more),
    path("farmer_delete_fav/<id>", views.farmer_delete_fav),
    #path("farmer_vaccine",views.farmer_vaccine),
    #path("farmer_view_vaccine",views.farmer_view_vaccine),

    ##################### USER #################
    
    
    path('user_page',views.user_page),
    path('user_home',views.user_home),
    path('user_page',views.user_page),
    path('user_view_one_product/<pro_id>',views.user_view_one_product),
    path('user_cart_details_view', views.user_cart_details_view),
    path("user_view_profile",views.user_view_profile),
    path("user_add_to_cart",views.user_add_to_cart),
    path("remove_cart/<id>",views.user_removecart),
    path("user_pay",views.user_pay),
    path("user_sa_post", views.user_sa_post),
    path("user_sa", views.user_sa),
    path("user_pay_post",views.user_pay_post),
    path("user_view_own_orders",views.user_view_own_orders),
    path("user_view_order_more/<id>",views.user_view_order_more),
    path("user_fav_view", views.user_fav_view),
    path("user_fav_product/<id>", views.user_fav_product),
    path("user_delete_fav/<id>",views.user_delete_fav),

]
