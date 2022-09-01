from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    '''override django default to call
    modified signals for line item'''

    name = 'checkout'

    def ready(self):
        import checkout.signals
