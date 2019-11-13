from django.http import Http404

from ..apps.neural.models import Network


def can_access_network(*, user, network):
    return user == network.owner or user.is_superuser


def get_network_for_user_or_404(user, **kwargs):
    try:
        network = Network.objects.get(**kwargs)
        if can_access_network(user=user, network=network):
            return network
    except Network.DoesNotExist:
        pass

    raise Http404(
        "Either the specified neural network does not exist, or you do not have access to it"
    )
