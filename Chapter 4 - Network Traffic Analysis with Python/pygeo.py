import pygeoip

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

def print_record(target):
    rec = gi.record_by_name(target)
    city = rec['city']
    region = rec['region_code']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']

    print("[*] Target: " + target + " Geo-located")
    print("[+] " + str(city) + ", " + str(region) + ", " + str(country))
    print("[+] Latitude: " + str(lat) + ", Longitude: " + str(long))

target = '173.255.226.98'

print_record(target)