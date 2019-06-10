from tools import access_pointsPackage as access
import sys 
import requests

def main():
    # [skyHook API Key, deviceId, optional xmlFile]
    args = sys.argv
    points = scanAccessPoints()
    xmlFile = accessPointsToXmlForSkyHook(points, args[1], args[2])
    xmlString = readIn(xmlFile)
    api_location_endPoint = 'https://global.skyhookwireless.com/wps2/location'
    request = postRequestXML(api_location_endPoint, xmlString)
    print(request.text)
    return request 

def scanAccessPoints():
    # Get all access points for any wifi adapter. 

    wifi_scanner = access.get_scanner()
    points = wifi_scanner.get_access_points()

    return points

def accessPointsToXmlForSkyHook(accessPoints, apiKey, deviceId, xmlFile = 'xmlRequest.xml'):
    import xml.etree.ElementTree as ElementTree

    # Location RQ values:
    LocationRQ = ElementTree.Element('LocationRQ')

    LocationRQ.set('xlms', "http://skyhookwireless.com/wps/2005")
    LocationRQ.set('version', "2.25")
    LocationRQ.set('street-address-lookup', "full")
    LocationRQ.set('timezone-lookup', "true")

    authentication = ElementTree.SubElement(LocationRQ, 'authentication')
    authentication.set('key', apiKey)
    authentication.set('username', deviceId)

    for point in accessPoints:
        accessPoint = ElementTree.SubElement(LocationRQ, 'access-point')
        
        bssid = point.bssid.replace(':','')
        quality = point.quality

        accessPoint.set('mac', bssid)
        accessPoint.set('signal-strength', quality)
    
    mydata = ElementTree.tostring(LocationRQ, encoding="unicode") 
    myfile = open(xmlFile, "w")
    myfile.write(mydata)
    return xmlFile 

def readIn(fileName):
	in_file = open(fileName, 'r')
	string = in_file.read()
	return string 

def postRequestXML(location_api_endPoint, xml_string):
    header = {'Content-Type': 'text/xml'}

    postRequest = requests.post(location_api_endPoint, data = xml_string, headers = header)
    return postRequest

if __name__ == '__main__':
    main()