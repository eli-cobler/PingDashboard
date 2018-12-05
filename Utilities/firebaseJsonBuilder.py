locationDict = [str(x) for x in input("What locations do you want to add? ").split()]

def run():

    with open('locations.json', 'a') as jsonFile:
        jsonFile.write('{\n  "Locations" : {')
        for location in locationDict:
            locationName = formatDomain(location)
            locationsJson = '    "{}" : [ "{}", "green", "1ms" ],\n'.format(locationName, location)

            jsonFile.write(locationsJson)

        jsonFile.write('  }\n}')
        print("Done.")

def formatDomain(location):
    name = location.replace('.com', '').capitalize()

    return(name)

if __name__ == '__main__':
    run()
