from rest_framework import viewsets, serializers, routers

from fullcalendar.models import AttachFile, Events


# class AttachFileSerializer(serializers.HyperlinkedModelSerializer):
class AttachFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachFile
        fields = '__all__'


class AttachFileViewSet(viewsets.ModelViewSet):
    queryset = AttachFile.objects.all()
    serializer_class = AttachFileSerializer
    filter_fields = ('event',)


router = routers.DefaultRouter()
router.register(r'attach-file', AttachFileViewSet)


class EventsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


router.register(r'events', EventsViewSet)
