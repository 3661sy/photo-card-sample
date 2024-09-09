from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Window, F, Sum
from django.db.models.functions.window import FirstValue
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cash.models import Cash
from photocard.models import Sale
from photocard.serializers import SaleSerializer, SaleDetailSerializer


class PhotoCardSaleListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Sale.objects.filter(state='ING').annotate(
        lowest_sale_id=Window(
            expression=FirstValue('id'),
            partition_by=[F('photo_card_id')],
            order_by=['price', 'renewal_date']

        )
    ).filter(id=F('lowest_sale_id'))
    serializer_class = SaleSerializer


class PhotoCardSaleDetailView(RetrieveAPIView, PhotoCardSaleListCreateView):
    serializer_class = SaleDetailSerializer
    lookup_url_kwarg = 'photo_card_id'
    lookup_field = 'photo_card_id'


class PhotoCardBuyView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Sale.objects.all()
    lookup_url_kwarg = 'sale_id'
    lookup_field = 'id'

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        buyer = request.user
        buyer_total_cash = Cash.objects.filter(user=buyer).aggregate(total_cash=Sum('amount'))['total_cash']
        seller = instance.seller
        total_price = instance.price + instance.fee

        if buyer_total_cash < total_price:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"price": "소지금이 부족하여 구매할 수 없습니다."}
            )

        instance.buyer = buyer
        instance.state = 'END'
        instance.sold_date = timezone.now()

        Cash.objects.create(user=buyer, amount=-total_price)
        Cash.objects.create(user=seller, amount=instance.price)

        instance.save()
        return Response(status=status.HTTP_200_OK, data=SaleSerializer(instance).data)
