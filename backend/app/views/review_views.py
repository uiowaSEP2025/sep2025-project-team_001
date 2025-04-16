from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models.review_models import Review
from ..models.order_models import Order
from ..serializers.review_serializer import ReviewSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models.review_models import Review
from ..serializers.review_serializer import ReviewSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request): #Expect the JSON body to have the order, rating, and comment
    order_id = request.data.get("order")
    
    # Prevent multiple reviews for the same order, Can change this later
    if Review.objects.filter(order_id=order_id).exists():
        return Response({"error": "Review already exists for this order."}, status=400)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        review = serializer.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_reviews(request):
    reviews = Review.objects.select_related("order__customer__user", "order__worker").all().order_by("-created_at")
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
