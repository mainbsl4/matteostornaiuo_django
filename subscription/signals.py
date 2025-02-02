from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings

from .models import Packages, Subscription

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@receiver(post_save, sender=Packages)
def create_stripe_product(sender, instance, created, **kwargs):
    if not instance.stripe_product_id:
        stripe_product = stripe.Product.create(
            name=instance.name,
            description=instance.description
            # images=[settings.MEDIA_URL + instance.image.url],
        )
        instance.stripe_product_id = stripe_product.id
        instance.save()
    if not instance.stripe_price_id:
        stripe_price = stripe.Price.create(
            product=instance.stripe_product_id,
            currency= 'NOK',
            unit_amount= int(instance.price * 100),
            recurring={
                'interval':'month',
                
            }
        )
        instance.stripe_price_id = stripe_price.id
        instance.save()

@receiver(post_save, sender=Packages)
def update_stripe_product(sender, instance, created, **kwargs):
    if instance.stripe_product_id and instance.stripe_price_id:
        stripe_product = stripe.Product.retrieve(instance.stripe_product_id)
        stripe_price = stripe.Price.retrieve(instance.stripe_price_id)
        
        if stripe_product['name'] != instance.name:
            stripe.Product.modify(
                stripe_product.id,
                name=instance.name,
                description=instance.description
                
            )

        if stripe_price['unit_amount'] != int(instance.price * 100):
            # remove previous price 
            stripe.Price.modify(instance.stripe_price_id, active=False)
            # create new price
            new_price = stripe.Price.create(
                product=instance.stripe_product_id,
                currency= 'NOK',
                unit_amount= int(instance.price * 100),
                recurring={
                    'interval':'month',
                    
                }
            )
            instance.stripe_price_id = new_price.id
            instance.save()

@receiver(pre_delete, sender=Packages)
def delete_stripe_product(sender, instance, **kwargs):
    if instance.stripe_product_id:
        # delete product
        stripe.Product.modify(
            instance.stripe_product_id,
            active=False,
        )
        # delete stripe price 
        stripe.Price.modify(
            instance.stripe_price_id,
            active=False,
        )