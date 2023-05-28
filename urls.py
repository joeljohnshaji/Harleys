"""HarleysTravelogue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from Travelogue import views
  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('SignUp/',views.Customer_Registration,name='Sign Up'),
    path('SignIn/',views.SignIn,name='Sign In'),
    path('AboutUs/',views.About_Us,name='About Us'),
    path('ContactUs/',views.Contact,name='Contact Us'),
    path('Gallery/',views.Gallery,name='Gallery'),
    path('ClubSignUp/',views.Club_Registration,name='Club Sign Up'),
    path('ShopSignUp/',views.Shop_Registration,name='Shop Sign Up'),
    path('AdminHome/',views.Admin_Home,name='Admin Home'),
    path('ClubHome/',views.Club_Home,name='Club Home'),
    path('ShopHome/',views.Shop_Home,name='Shop Home'),
    path('CustomerHome/',views.Customer_Home,name='Customer Home'),
    path('',views.Common_Home,name='Common Home'),
    path('index/',views.Common_Home,name='Common Home'),
    path('ClubHome/',views.Club_Home,name='Club Home'),
    path('ShopHome/',views.Shop_Home,name='Shop Home'),
    path('AdminAddHospital/',views.Admin_Add_Hospital,name='Admin Add Hospital'),
    path('AdminRemoveHospital/',views.AdminRemoveHospital,name='AdminRemoveHospital'),
    path('AdminAddHotel/',views.Admin_Add_Hotel,name='Admin Add Hotel'),
    path('AdminRemoveHotel/',views.AdminRemoveHotel,name='AdminRemoveHotel'),
    path('AdminAddWorkshop/',views.Admin_Add_Workshop,name='Admin Add Workshop'),
    path('AdminRemoveWorkshop/',views.AdminRemoveWorkshop,name='AdminRemoveWorkshop'),
    path('AdminAddCategory/',views.Admin_Add_Category,name='Admin Add Category'),
    path('AdminRemoveCategory/',views.AdminRemoveCategory,name='AdminRemoveCategory'),
    path('AdminAddBrand/',views.Admin_Add_Brand,name='Admin Add Brand'),
    path('AdminRemoveBrand/',views.AdminRemoveBrand,name='AdminRemoveBrand'),
    path('AdminViewCustomers/',views.Admin_View_Customers,name='Admin View Customers'),
    path('AdminViewFeedback/',views.Admin_View_Feedback,name='Admin View Feedback'),
    path('AdminViewClub/',views.Admin_View_Club,name='Admin View Club'),
    path('AdminViewShop/',views.Admin_View_Shop,name='Admin View Shop'),
    path('ClubAddNotification/',views.Club_Add_Notification,name='Club Add Notification'),
    path('ClubRemoveNotification/',views.ClubRemoveNotification,name='ClubRemoveNotification'),
    path('ClubViewRequest/',views.Club_View_Request,name='Club View Request'),
    path('ClubViewRiders/',views.Club_View_Riders,name='Club View Riders'),
    path('ClubAddVehicle/',views.Club_Add_Vehicle,name='Club Add Vehicle'),
    path('ClubRemoveVehicle/',views.ClubRemoveVehicle,name='ClubRemoveVehicle'),
    path('ClubViewBooking/',views.Club_View_Booking,name='Club View Booking'),
    path('ShopViewMyProduct/',views.Shop_View_My_Product,name='Shop View My Product'),
    path('ShopRemoveProduct/',views.ShopRemoveProduct,name='ShopRemoveProduct'),
    path('ShopUpdateProduct/',views.ShopUpdateProduct,name='ShopUpdateProduct'),
    path('ShopAddProduct/',views.Shop_Add_Product,name='Shop Add Product'),
    path('ShopViewOrders/',views.Shop_View_Orders,name='Shop View Orders'),
    path('CustomerViewProfile/',views.Customer_View_Profile,name='Customer View Profile'),
    path('CustomerViewBuyProduct/',views.Customer_View_Buy_Product,name='Customer View Buy Product'),
    path('CustomerViewNotification/',views.Customer_View_Notification,name='Customer View Notification'),
    path('CustomerSearchClub/',views.Customer_Search_Club,name='Customer Search Club'),
    path('CustomerShopping/',views.CustomerShopping,name='CustomerShopping'),
    path('CustomerViewProDetails/',views.CustomerViewProDetails,name='CustomerViewProDetails'),
    path('CustomerViewProCategory/',views.CustomerViewProCategory,name="CustomerViewProCategory"),
    path('CustomerViewProSubCategory/',views.CustomerViewProSubCategory,name="CustomerViewProSubCategory"),
    path('CustomerOrderProduct/',views.CustomerOrderProduct,name="CustomerOrderProduct"),
    path('CustomerViewCart/',views.CustomerViewCart,name="CustomerViewCart"),
    path('CustomerViewMyBooking/',views.CustomerViewMyBooking,name="CustomerViewMyBooking"),
    path('CustomerViewOrders/',views.CustomerViewOrders,name="CustomerViewOrders"),
    path('subcat/',views.subcat,name="subcat"),
    path('payment1/',views.payment1,name='payment1'),
    path('payment2/',views.payment2,name='payment2'),
    path('payment3/',views.payment3,name='payment3'),
    path('payment4/',views.payment4,name='payment4'),
    path('payment5/',views.payment5,name='payment5'),
    path('subcat/',views.subcat,name="subcat"),
    path('CustomerSearchRentBike/',views.CustomerSearchRentBike,name='CustomerSearchRentBike'),
    path('CustomerRentBikeRequest/',views.CustomerRentBikeRequest,name='CustomerRentBikeRequest'),
    path('subcatforbike/',views.subcatforbike,name="subsubcatforbikecat"),
    path('Map/',views.Map,name="Map"),
    path('customer_View_workshop/',views.customer_View_workshop,name="customer_View_workshop"),
    path('customer_View_hotel/',views.customer_View_hotel,name="customer_View_hotel"),
    path('customer_View_hospital/',views.customer_View_hospital,name="customer_View_hospital"),

    path('guestviewproduct/',views.guestviewproduct,name="guestviewproduct"),
    path('guestviewshop/',views.guestviewshop,name="guestviewshop"),
    path('guestviewclub/',views.guestviewclub,name="guestviewclub"),
    path('RentStatus/',views.RentStatus,name="RentStatus"),
    path('RentDelete/<int:id>/', views.RentDelete, name="RentDelete"),
    path('RentPay/<int:id>/',views.RentPay,name="RentPay"),
    path('RentPaySuccess/<int:id>/',views.RentPaySuccess,name="RentPaySuccess"),

]
