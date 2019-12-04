from django.urls import path
from app.views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
     path('', Dashboard.as_view(), name='app_url'),
     path('ajax/load_posts/', load_posts, name='load_posts_url'),
     path('ajax/load_cards/', load_cards, name='load_cards_url'),


     path('start-wash', StartWash.as_view(), name='start_wash_url'),

     path('partners/', PartnerList.as_view(), name='partner_list_url'),
     path('partners/detail/', partnerDetailRequest, name='partner_detail_url'),

     path('contractors/', ContractorList.as_view(), name='contractor_list_url'),
     path('contractors/detail/', contractorDetailRequest,
          name='contractor_detail_url'),

     path('cards/', CardList.as_view(), name='card_list_url'),
     path('cards/detail', cardDetailRequest, name='card_detail_url'),

     path('stations/', StationList.as_view(), name='station_list_url'),
     path('stations/detail', stationDetailRequest, name='station_detail_url'),


     path('posts/', PostList.as_view(), name='post_list_url'),
     path('posts/detail', postDetailRequest, name='post_detail_url'),
     path('posts/unavailable', UnavailablePostListRequest.as_view(),
          name='unavailable_post_list_request_url'),

     path('payments/', PaymentList.as_view(), name='payment_list_url'),
     path('transactions/', TransactionList.as_view(), name='transaction_list_url'),


     path('partner/create/', PartnerCreate.as_view(), name='partner_create_url'),
     path('contractor/create/', ContractorCreate.as_view(),
          name='contractor_create_url'),
     path('station/create/', StationCreate.as_view(), name='station_create_url'),
     path('card/create/', CardActive.as_view(), name='card_create_url'),
     path('payment/create/', PaymentCreate.as_view(), name='payment_create_url'),



     path('partner/<int:id>/update/',
          PartnerUpdate.as_view(), name='partner_update_url'),
     path('contractor/<int:id>/update/',
          ContractorUpdate.as_view(), name='contractor_update_url'),
     path('station/<int:id>/update/',
          StationUpdate.as_view(), name='station_update_url'),
     path('card/<int:id>/update/', CardUpdate.as_view(), name='card_update_url'),

     path('contractor/<int:id>/delete/',
          ContractorDelete.as_view(), name='contractor_delete_url'),
     path('partner/<int:id>/delete/',
          PartnerDelete.as_view(), name='partner_delete_url'),
     # path('station/<int:id>/delete/', StationDelete.as_view(), name='station_delete_url'),
     path('card/<int:id>/delete/', CardDelete.as_view(), name='card_delete_url'),




     path('partner/<int:id>/add-coins/',
          PartnerAddCoins.as_view(), name='partner_add_coins_url'),
     path('partner/ajax/add-coins/', partnerAddCoinsRequest,
          name='partner_ajax_add_coins_url'),

     path('user-transactions/', UserTransactionList.as_view(),
          name='user_transaction_list_url'),



     path('login/', LoginView.as_view(template_name='sign_in.html'), name='login_url'),
     path('logout/', LogoutView.as_view(next_page='/'), name='logout_url'),

     path('transactions/ajax/', TransactionListJson.as_view(),
          name="transactions_ajax_request"),
     path('user_profile/update/', UserProfileUpdate.as_view(), name='user_profile_update_url'),
     path('epos-payment/', eposPaymentRequest, name='epos_payment_request_url')

]
