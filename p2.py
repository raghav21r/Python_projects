import phonenumbers
import folium
from phonenumbers import geocoder#this module helps us in identifying the country using phonenumber
from phonenumbers import carrier
from opencage.geocoder import OpenCageGeocode
ph=str(input())
a=phonenumbers.parse(ph)
location=geocoder.description_for_number(a,"en")
print(location)
print(carrier.name_for_number(a,"en"))#displays the comapny name of which the user is using 
k='891debbcf90c48b684c43e3d33bbe880'
geo=OpenCageGeocode(k)
query=str(location)
outcome=geo.geocode(query)
lat=outcome[0]['geometry']['lat']
lng=outcome[0]['geometry']['lng']
view=folium.Map(location=[lat,lng],zoom_start=9)
folium.Marker([lat,lng],popup=location).add_to(view)
view.save("current_loc.html")
