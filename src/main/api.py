from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, generics, mixins

# Serializers define the API representation.
from rest_framework.viewsets import GenericViewSet

from indices.models import ValuesDetail


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


class ValuesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValuesDetail
        fields = ('numerator', 'denominator', 'value')


# ViewSets define the view behavior.
# class ValuesDetailUpdateService(generics.UpdateAPIView):
class ValuesDetailUpdateService(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ValuesDetail.objects.all()
    serializer_class = ValuesDetailSerializer


# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
router.register(r'values-detail', ValuesDetailUpdateService)
