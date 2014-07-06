from django.core.management.base import BaseCommand

from apps.twitter.models import Keyword, Tweet, Account, get_weight


class Command(BaseCommand):
    def handle(self, *args, **options):
        for handle in Account.objects.all():
            handle.weight = get_weight(handle.follower_count, handle.following_count, handle.status_count,
                                       handle.listed_in_count, handle.is_verified)
            handle.save()