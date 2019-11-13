from django.shortcuts import render

from ...utils.helpers import get_network_for_user_or_404

# Create your views here.


def index(request):
    return render(request, "neural/index.html")


def view_network(request, network_id):
    network = get_network_for_user_or_404(request.user, id=network_id)

    return render(request, "neural/view.html", {"network": network})


def edit_network(request, network_id):
    network = get_network_for_user_or_404(request.user, id=network_id)

    return render(request, "neural/edit.html", {"network": network})
