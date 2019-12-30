from app.models import Contractor, Station

def contractor_list(request):
    contractors = Contractor.objects.all()
    return {"contractors_list" : contractors}


def station_list(request):
    stations = Station.objects.all()
    return {"stations_list" : stations}