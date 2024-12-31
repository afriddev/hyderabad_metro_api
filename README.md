


# Hyderabad Metro API
The Hyderabad Metro API provides real-time data on metro schedules, routes, and station locations, ensuring seamless travel planning. It allows developers to integrate live updates and connectivity information into apps and services.

#### Base url
```
https://hyderabadmetroapi1-gn8j6tzm.b4a.run/
```

#### Example

⭐ **Get all station details**
```ts
const  url = https://hyderabadmetroapi1-gn8j6tzm.b4a.run/api/allstations
method = "GET"
``` 


####  methods

⭐ **Get all stations details**
```ts
const  url = https://hyderabadmetroapi1-gn8j6tzm.b4a.run/api/allstations
method = "GET"

```
⭐ **Get Route**

```ts
const  url = https://hyderabadmetroapi1-gn8j6tzm.b4a.run/api/route/stations
method = "post"

```
```json
{
    "fromStation":{
        "stationName":"raidurg",
        "_comment": "StationNo nad lineNo are optional if you know you can pass",
    },
    "toStation":{
        "stationName":"miyapur",
        "_comment": "StationNo nad lineNo are optional if you know you can pass",
    }
}
```

⭐ **Get All Line details**

```ts
const  url = https://hyderabadmetroapi1-gn8j6tzm.b4a.run/api/all
method = "GET"
```
#### ⭐ Due to free hosting inital latency may be high due to docker container sleep 😴
#### ⭐ To change any station details OR to solve BUG feel free to contact to my Gmail, You need Secret Key 😁



#### Authors

- [Afrid Shaik](https://www.github.com/afriddev)
- [Portfolio](https://afriddev.vercel.app/)
- [Gmail](mailto:afridayan01@gmail.com)

