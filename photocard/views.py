from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from photocard.models import Sale
from photocard.serializers import SaleSerializer


class SaleListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
