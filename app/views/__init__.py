from app.views.dashboard import Dashboard, StartWash, load_cards, load_posts
from app.views.transactions import TransactionList, TransactionListJson
from app.views.partners import PartnerList, PartnerCreate, PartnerUpdate, PartnerDelete, PartnerAddCoins, partnerAddCoinsRequest, partnerDetailRequest, PartnerDetail
from app.views.contractors import ContractorList, ContractorUpdate, ContractorCreate, ContractorDelete, contractorDetailRequest, ContractorDetail
from app.views.cards import CardCreate, CardList, CardUpdate, CardDelete, CardActive, cardDetailRequest, CardDetail
from app.views.stations import StationCreate, StationList, StationUpdate, stationDetailRequest, StationDetail
from app.views.posts import PostList, postDetailRequest, UnavailablePostListRequest, PostUpdateEripId, PostDetail
from app.views.payments import PaymentCreate, PaymentList
from app.views.user_transactions import UserTransactionList
from app.views.user_profile import UserProfileUpdate
from app.views.epos_payments import eposPaymentRequest, EposPaymentList