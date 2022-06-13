from django.shortcuts import render
from community.models import Community
import folium
import branca

def maps(request):
    counter = 0
    size = Community.objects.all().count()
    map = folium.Map(location=[34.700559, 135.495734], zoom_start=15)
    if Community.objects.first() is None:
        x = 135.495734
        y = 34.700559
        url = "http://127.0.0.1:8000/community/community_create/"
        html = '<a href ='+url+' target="_blank" rel="noopener noreferrer">あああ</a>'
        iframe = branca.element.IFrame(html=html, width=300, height=500)
        popup = folium.Popup(iframe, max_width=300)
        map = folium.Map(location=[y, x], zoom_start=15)
        folium.Marker(
        location=[y, x],
        popup = popup,
        icon=folium.Icon(color='red', icon='home')
        ).add_to(map)
    else:
        for counter in range(size):
            counter = counter + 1
            l = Community.objects.filter(id = counter).first()
            num = l.id
            name =  Community.objects.get(id =num)
            x = l.lat
            y = l.lon
            url = "http://127.0.0.1:8000/community/community_top/" + str(name) + '/'
            html = '<a href ='+url+' target="_blank" rel="noopener noreferrer">' + str(name) + '</a>'
            iframe = branca.element.IFrame(html=html, width=300, height=500)
            popup = folium.Popup(iframe, max_width=300)
            folium.Marker(
            location=[y, x],
            popup = popup,
            icon=folium.Icon(color='red', icon='home')
            ).add_to(map)
    map = map._repr_html_()
    context = {
        'map': map,
    }
    return render(request, 'maps/maps.html', context)