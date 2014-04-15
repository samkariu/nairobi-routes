Nairobi Routes is a Google Appengine hosted app that display all of the bus and rail routes in the Nairobi Metropolitan area.

Check it out at http://nairobi-routes.appspot.com

##**API**
It also has a rudimentary read-only API:

1.GET /routes/road - list all road routes.

2.GET /routes/rail - list all rail routes.

3.GET /route/road/<route-name> - return a road route

4.GET /route/rail/<route-name> - return a rail route.

5.GET /stops/road/<route-name> - return all stops along a road route.

6.GET /stops/rail/<route-name> - return all stops along a rail route.

##**Credits**
Based on GTFS data collected by the Digital Matatus project (http://www.digitalmatatus.com/)

#**Pull Requests**
Pull requests are welcome! 

#**License**
Released under the MIT license.
