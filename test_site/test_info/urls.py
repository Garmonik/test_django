from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.admin_settings_view, name='home'),
    path('tests/', views.tests, name='tests'),
    path('result/', views.results, name='result'),
    path('result/<int:id>/', views.get_results, name='get_result'),

    path('start/tests/<int:id>/', views.start_test, name='start_test'),
    path('tests/<int:id>/', views.test_get, name='test_get'),

    path('testing/<int:id>/', views.testing, name='testing'),

    path('testing/<int:id>/save/', views.testing_save, name='testing_save'),

    path('testing/<int:id>/result/', views.testing_finish_test, name='finish_test'),

    # path('products/<int:id>/', views.get_product, name='get_product'),
    # path('products/<int:id>/delete/', views.delete_product, name='delete_product'),
    # path('products/add/', views.add_product, name='add_product'),

    # path('market/<int:id>/sell/', views.sell_from_market, name='sell_from_market'),
    # path('market/history/', views.market_history, name='market_history'),
    # path('market/<int:id>/return/', views.return_from_market, name='return_from_market'),
    # path('market/<int:id>/return_all/', views.return_from_market_all, name='return_from_market_all'),
    # path('market/<int:id>/write_off_all/', views.write_off_from_market_all, name='write_off_all'),
    # path('market/add/', views.add_to_market, name='add_to_market'),
    # path('market/<int:pk>/', views.update_to_market, name='update_to_market'),
    # path('market/update/<int:pk>/', views.update_to_market_new, name='update_to_market_new'),
    # path('market/update/amount/<int:pk>/', views.update_amount_to_market, name='update_to_market_amount'),

    # path('storage/add/', views.add_to_storage, name='add_to_storage'),
    # path('storage/<int:id>/write-off/', views.write_off_from_storage, name='write_off_from_storage'),
    #
    # path('places/', views.places, name='places'),
    # path('places/<int:id>/', views.get_place, name='get_place'),
    # path('places/<int:id>/delete/', views.delete_place, name='delete_place'),
    # path('places/add/', views.add_place, name='add_place'),


    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]