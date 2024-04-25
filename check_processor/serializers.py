from rest_framework import serializers
from .models import Place, TotalAnalytics, Purchase, CategoryAnalytics, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['purchase']


class PurchaseSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, required=False)

    class Meta:
        model = Purchase
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase = Purchase.objects.create(**validated_data)

        for item_data in items_data:
            Item.objects.create(purchase=purchase, **item_data)

        return purchase


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['place_id', 'place_name']


class CategoryAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryAnalytics
        fields = ['category', 'total_spent', 'average_receipt']


class AnalyticsSerializer(serializers.Serializer):
    place_id = serializers.CharField()
    place_name = serializers.CharField()
    total_purchases = serializers.IntegerField()
    average_receipt = serializers.DecimalField(max_digits=10, decimal_places=2)
    taxes_amount = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
    category_analytics = serializers.DictField(
        child=serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2)))
