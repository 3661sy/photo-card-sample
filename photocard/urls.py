from django.urls import path

from photocard.views import PhotoCardSaleListCreateView, PhotoCardSaleDetailView, PhotoCardBuyView

urlpatterns = [
    path('photo-card', PhotoCardSaleListCreateView.as_view(), name='photo-card-sale-list-create'),
    path('photo-card/<int:photo_card_id>', PhotoCardSaleDetailView.as_view(), name='photo-card-sale-detail'),
    path('sales/<int:sale_id>/buy', PhotoCardBuyView.as_view(), name='photo-card-buy'),
]
