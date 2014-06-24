import json
import requests
import sys
from datetime import datetime
import pytz


from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from apps.meetup.models import Keyword, Event
from apps.common import helpers


class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get('http://stream.meetup.com/2/open_events?since_count=100', stream=True)
        for line in r.iter_lines():
            if line:
                event = json.loads(line)
                if event['status'] != 'cancelled' or event['status'] != 'deleted':
                    kwargs = dict(
                        event_id=event['id'],
                        name=event['name'],
                        event_url=event['event_url'],
                    )
                    if 'description' in event:
                        # print 'Description', event['description'][:100]
                        kwargs['description'] = helpers.strip_tags(event['description'])
                    print 'URL', event['event_url']
                    print 'Name', event['name']

                    if 'time' in event:
                        event['time'] = datetime.utcfromtimestamp(int(event['time']) / 1000).replace(tzinfo=pytz.utc)
                        print 'Time', event['time']
                        kwargs['when'] = event['time']

                    if 'venue' in event:
                        if 'city' in event['venue']:
                            print 'City', event['venue']['city']
                            kwargs['venue_city'] = event['venue']['city']
                        if 'country' in event['venue']:
                            print 'Country', str(event['venue']['country']).upper()
                            kwargs['venue_country'] = str(event['venue']['country']).upper()

                    print event['group']['urlname']
                    kwargs['group_url'] = 'http://www.meetup.com/%s' % event['group']['urlname']
                    print

                    try:
                        model = Event.objects.create(**kwargs)
                        model.save()
                    except IntegrityError:
                        pass
                    sys.stdout.flush()