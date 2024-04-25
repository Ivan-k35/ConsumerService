from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Place, TotalAnalytics, CategoryAnalytics
from .serializers import PlaceSerializer, AnalyticsSerializer


class PlaceListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
            Получает список всех мест

            Получает список всех мест и возвращает их в формате JSON.

            Parameters:
                request (Request): Запрос REST Framework.

            Returns:
                Response: Ответ REST Framework с данными о местах в формате JSON.
        """
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)


class TotalAnalyticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
            Получает аналитику по всем местам

            Получает аналитику по всем местам и возвращает ее в формате JSON.

            Parameters:
                request (Request): Запрос REST Framework.

            Returns:
                Response: Ответ REST Framework с данными аналитики в формате JSON.
        """
        places = Place.objects.all()
        analytics_data = []

        for place in places:
            try:
                total_analytics = TotalAnalytics.objects.get(place=place)
            except TotalAnalytics.DoesNotExist:
                total_analytics = TotalAnalytics(place=place)
                total_analytics.save()

            category_analytics = CategoryAnalytics.objects.filter(place=place)

            data = {
                'place_id': place.place_id,
                'place_name': place.place_name,
                'total_purchases': total_analytics.total_purchases,
                'average_receipt': total_analytics.average_receipt,
                'taxes_amount': {
                    'total_nds': total_analytics.total_nds,
                    'total_tips': total_analytics.total_tips
                },
                'category_analytics': {category.category: {
                    'total_spent': category.total_spent,
                    'average_receipt': category.average_receipt
                } for category in category_analytics}
            }
            analytics_data.append(data)

        serializer = AnalyticsSerializer(analytics_data, many=True)
        return Response(serializer.data)
