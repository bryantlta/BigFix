from tools import access_pointsPackage
from tools import accessPointsMethods
from tools import postRequests
from tools import readArgs
from tools import accessPointsToXmlForSkyhook
import sys 

def main():
    # [skyHook API Key, deviceId, optional xmlFile]
    args = sys.argv

    points = accessPointsMethods.scanAccessPoints()

    xmlFile = accessPointsToXmlForSkyhook.accessPointsToXmlForSkyHook(points, args[1], args[2])

    in_file = open(xmlFile, 'r')
	xmlString = xmlFile.read()

	api_location_endPoint = 'https://global.skyhookwireless.com/wps2/location'
    postRequests.postRequestXML(api_location_endPoint, xmlString)
    print(postRequest.text)
    return postRequest



if __name__ == "__main__":
    main()