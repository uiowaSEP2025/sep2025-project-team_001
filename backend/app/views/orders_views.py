from rest_framework import generics
from app.models import CurrentItem
from app.serializers.current_item_serializer import CurrentItemSerializer

class CurrentItemsList(generics.ListAPIView):
    queryset = CurrentItem.objects.filter(status="active")
    serializer_class = CurrentItemSerializer