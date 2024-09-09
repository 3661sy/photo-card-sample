from rest_framework import serializers

from photocard.models import Sale


class SaleSerializer(serializers.ModelSerializer):
    photo_card_id = serializers.IntegerField(help_text='포토카드 id')
    create_date = serializers.DateTimeField(read_only=True, help_text='생성일시')
    renewal_date = serializers.DateTimeField(read_only=True, help_text='수정일시')
    
    class Meta:
        model = Sale
        fields = [
            'id',
            'photo_card_id',
            'price',
            'create_date',
            'renewal_date',
        ]

    def validate(self, attrs):
        attrs['fee'] = attrs['price'] * 0.2  # 판매가의 20%를 수수료로 한다
        attrs['seller'] = self.context['request'].user
        return attrs


class RecentPriceSerializer(serializers.Serializer):
    sold_date = serializers.DateTimeField(read_only=True, help_text='판매일시')
    price = serializers.IntegerField(read_only=True, help_text='판매가')


class SaleDetailSerializer(SaleSerializer):
    photo_card_id = serializers.IntegerField(read_only=True, help_text='포토카드 id')
    total_price = serializers.SerializerMethodField(read_only=True, help_text='총 금액(판매가 + 수수료)')
    recent_sold_prices = serializers.SerializerMethodField(read_only=True, help_text='최근 거래가')

    class Meta:
        model = Sale
        fields = SaleSerializer.Meta.fields + [
            'fee',
            'total_price',
            'recent_sold_prices',
        ]

    def get_total_price(self, obj):
        return obj.price + obj.fee

    def get_recent_sold_prices(self, obj):
        photo_card_id = obj.photo_card_id
        # 해당 포토카드의 최근 5개 거래가
        recent_sold_prices = Sale.objects.filter(
            photo_card_id=photo_card_id, state='END'
        ).order_by('-sold_date')[:5]
        return RecentPriceSerializer(recent_sold_prices, many=True).data
