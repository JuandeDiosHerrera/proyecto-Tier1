import httplib
import urllib

conn = httplib.HTTPConnection('10.10.0.10')
imagewidth = 640
imageheight = 360
imagerotation = 180
x_coord = 320
y_coord = 180
zoom = 500
areazoom = str(x_coord) + "," + str(y_coord) + "," + str(zoom)
params = {'areazoom':areazoom, 'imagewidth':imagewidth, 'imageheight':imageheight, 'imagerotation':imagerotation}
url = "/axis-cgi/com/ptz.cgi?camera=1&%s" %  urllib.urlencode(params)

print(url)
conn.request("GET",url)
if conn.getresponse().status != 204:
    print("Error getting response")
