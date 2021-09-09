import requests

def find_city_id(city_name):
    location_url = "https://brn-ybus-pubapi.sa.cz/restapi/consts/locations"
    r = requests.get(url=location_url)
    response = r.json()
    for el in response:
        for city in el["cities"]:
            if city["name"] == city_name:
                return str(city["id"])


def find_data(from_loc, to_loc, date):
    data_output = []
    from_loc_city_id = find_city_id(from_loc)
    to_loc_city_id = find_city_id(to_loc)


    url = fr"https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple?departureDate={date}&fromLocationId={from_loc_city_id}&fromLocationType=CITY&locale=cs&tariffs=REGULAR&toLocationId={to_loc_city_id}&toLocationType=CITY"
    r = requests.get(url=url)
    response = r.json()
    for i in range(len(response["routes"])):

        formatted_output = {
            "departure_datetime": response["routes"][i]["departureTime"][:19],
            "arrival_datetime": response["routes"][i]["arrivalTime"][:19],
            "source": from_loc.lower(),
            "destination": to_loc.lower(),
            "price": response["routes"][i]["creditPriceTo"],
            "type": response["routes"][i]["vehicleTypes"][0],
            "source_id": response["routes"][i]["departureStationId"],
            "destination_id": response["routes"][i]["arrivalStationId"],
            "free_seats": response["routes"][i]["freeSeatsCount"],
            "carrier": "REGIOJET"
        }
        data_output.append(formatted_output)
    return data_output

def format_data(from_loc, to_loc, date):
    data_output = []
    output = find_data(from_loc, to_loc, date)
    for itinerary in output:
        formatted_output = {
            "source": itinerary["source"].capitalize(),
            "destination": itinerary["destination"].capitalize(),
            "departure_time": itinerary["departure_datetime"][-8:-3],
            "arrival_time": itinerary["arrival_datetime"][-8:-3],
            "price": str(itinerary["price"]) + " EUR",
            "free_seats": itinerary["free_seats"]
        }
        data_output.append(formatted_output)
    return(data_output)

def all_regiojet_cities():
    location_url = "https://brn-ybus-pubapi.sa.cz/restapi/consts/locations"
    r = requests.get(url=location_url)
    response = r.json()
    country_city = {}
    city_list = []
    for el in response:
        country = el["country"]
        for city in el["cities"]:
            city_list.append(city["name"])
        country_city[country] = city_list
        city_list = []
    return country_city

#working
#print(find_data("Vienna", "Brno", "2021-09-29"))

#working
#print(find_data("Prague", "Brno", "2021-09-29"))

#worknig
#print(find_data("Prague", "Berlin", "2021-10-15"))