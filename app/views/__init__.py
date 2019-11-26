from app.views.dashboard import Dashboard, StartWash, load_cards, load_posts
from app.views.transactions import TransactionList, TransactionListJson
from app.views.partners import PartnerList, PartnerCreate, PartnerUpdate, PartnerDelete, PartnerAddCoins, partnerAddCoinsRequest, partnerDetailRequest
from app.views.contractors import ContractorList, ContractorUpdate, ContractorCreate, ContractorDelete, contractorDetailRequest
from app.views.cards import CardCreate, CardList, CardUpdate, CardDelete, CardActive, cardDetailRequest
from app.views.stations import StationCreate, StationList, StationUpdate, stationDetailRequest
from app.views.posts import PostList, postDetailRequest
from app.views.payments import PaymentCreate, PaymentList
from app.views.user_transactions import UserTransactionList