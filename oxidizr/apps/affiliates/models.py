from django.db import models


class Tenant(models.Model):
    """
    This model allows us to enable multiple tenants register on and use Oxidizr.
    Like in other hosted Software as a Service, we store almost all other data per tenant.
    """
    name = models.CharField(max_length=100)