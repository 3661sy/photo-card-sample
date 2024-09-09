from rest_framework import serializers

from photocard.models import Sale


class SaleSerializer(serializers.ModelSerializer):
    photo_card_id = serializers.IntegerField()
    create_date = serializers.DateTimeField(read_only=True)
    renewal_date = serializers.DateTimeField(read_only=True)
    
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
        attrs['fee'] = attrs['price'] * 0.2
        attrs['seller'] = self.context['request'].user
        return attrs


class RecentPriceSerializer(serializers.Serializer):
    sold_date = serializers.DateTimeField(read_only=True)
    price = serializers.IntegerField(read_only=True)


class SaleDetailSerializer(SaleSerializer):
    photo_card_id = serializers.IntegerField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    recent_sold_prices = serializers.SerializerMethodField(read_only=True)

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
        recent_sold_prices = Sale.objects.filter(
            photo_card_id=photo_card_id, state='END'
        ).order_by('-sold_date')[:5]
        return RecentPriceSerializer(recent_sold_prices, many=True).data
