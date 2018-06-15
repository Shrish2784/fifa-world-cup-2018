from tastypie.resources import ModelResource
from api.models import Match



class MatchResource(ModelResource):
    class Meta:
        queryset = Match.objects.all()
        resource_name = 'match'
