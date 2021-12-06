## [The Concierge](https://the-concierge1.herokuapp.com/)

Link: https://the-concierge1.herokuapp.com/

The Concierge is the app that a user can sign up to create an itinerary for their trip. The user can search hotels or restaurants by putting in the names of the city and the state. Once the user submits the city and the state, a list of hotels/restaurants will show up with names, addresses, websites, phone numbers, and ratings (however, some places may not have all of the information).

The user can create an itinerary by naming the trip, select start date and end date, select the hotels/restaurants they are going to stay/visit. Their created itinerary will also have information about the places they select. The user can also delete the itinerary. On their itinerary page, all the created itineraries are shown with the names of the trips.

## User Flow

![user flow](static/assets/The%20Concierge%20User%20Flow.png)


## Main Features
- A user can sign up/ log in / log out

  Only a signed up user can create an itinerary from the app

- Search hotels/restaurants by city and state

  People are familair with the names of the places so I chose city and state for the search form

- Showing places' info
  
  When people plan a trip, they are likely look at the information of the place so I make sure to include this and if there is a site of that palce available, the user can click the link directly to get more info of that place or can call from the number shown on the place details

- Create itinerary
 
  Once the user selects where they want to stay and eat, they can create an itinerary and print it out or come back to look at their trip plan later on their account.

## Schema

![Schema](Schema/Capstone%20Schema.png).
  

## API used 

[Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview).

## Technologies used
- Python
- JavaScript
- HTML
- CSS
- SQLAlchemy
- Postgres
- Flask
- [Google maps Python library](https://github.com/googlemaps/google-maps-services-python)

## Try the code on your local machine
1. clone the repo
   
        $ git clone  https://github.com/KKTTAAII/capstone_first.git
2. set up environment
   
        $ python3 -m venv venv

3. insall requirements

        $ pip3 install -r requirements.txt

4. install google maps Python Library
   
        $ pip install -U googlemaps

5. activate the environment

        $ source venv/bin/activate

6. you can create your own API Key here

    [Google Places API KEY](https://mapsplatform.google.com/)

7. create database

          $ createdb user_itinerary

8. create tables

          $ ipython
          In [1]: %run app.py

9.  Enjoy the code!


## Run tests

1. Create test database

        $ createdb itinerary_test

2. Run the command with the test file name you would like to test

    2.1 To run user routes test

        $ python -m unittest tests/test_user_route_app.py

    2.2 To run itinerary routes test

        $ python -m unittest tests/test_itinerary_route_app.py

    2.3 To run user model test

        $ python -m unittest tests/test_user_model.py

    2.4 To run itinerary model test

        $ python -m unittest tests/test_itinerary_model.py

## Future features
  - favorite and unfavorite the places and view all favorites

      - adding a star/favorite button in the place box at the corner. The user can click to favorite and click again to unfavorite.
  
  - can email their itinerary to their friends

      - in the trip detail page, add a "share" button and input where the user can type the email of the recipient and click share to send the itinerary. 

  - the places can show range of prices 

    - in the place box where it shows the place details, add another p tag where we can show 1-5 dollar signs to indicate the range of price of this place. The range price can be obtained from google places API
  
  - minimize the space in the database and get the updated place detail by storing the api of the place detail itself instead of storing name, address, phone number, website. However, with financial limiation from using API, the data will be stored as they are for now
  
  

Author: [Boonyawee P.](https://www.linkedin.com/in/boonyawee-prasertsiripond/)