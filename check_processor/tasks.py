from decimal import Decimal
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
from loguru import logger
from .models import Purchase, CategoryAnalytics, TotalAnalytics, Place


@shared_task
def calculate_and_save_analytics():
    try:
        places = Place.objects.all()

        for place in places:
            place_id = place.place_id

            total_purchases = Purchase.objects.filter(place_id=place_id).count()

            total_amount_sum = Purchase.objects.filter(place_id=place_id).aggregate(Sum('total_amount'))[
                'total_amount__sum']
            average_receipt = total_amount_sum / total_purchases if total_purchases > 0 else Decimal('0.00')

            total_nds = Purchase.objects.filter(place_id=place_id).aggregate(Sum('nds_amount'))['nds_amount__sum']

            total_tips = Purchase.objects.filter(place_id=place_id).aggregate(Sum('tips_amount'))['tips_amount__sum']

            total_analytics, created = TotalAnalytics.objects.get_or_create(place=place)
            total_analytics.total_purchases = total_purchases
            total_analytics.average_receipt = average_receipt
            total_analytics.total_nds = total_nds
            total_analytics.total_tips = total_tips
            total_analytics.save()

            category_analytics = {}
            for purchase in Purchase.objects.filter(place_id=place_id):
                for item in purchase.items.all():
                    category = item.category
                    total_spent = item.quantity * item.price
                    if category in category_analytics:
                        category_analytics[category]['total_spent'] += total_spent
                        category_analytics[category]['total_items'] += 1
                    else:
                        category_analytics[category] = {'total_spent': total_spent, 'total_items': 1}

            for category, data in category_analytics.items():
                total_spent = data['total_spent']
                total_items = data['total_items']
                average_receipt_category = total_spent / total_items if total_items > 0 else Decimal('0.00')
                category_instance, created = CategoryAnalytics.objects.get_or_create(place=place, category=category)
                category_instance.total_spent = total_spent
                category_instance.average_receipt = average_receipt_category
                category_instance.save()

    except ObjectDoesNotExist as e:
        logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")
