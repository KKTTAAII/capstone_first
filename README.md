## The Concierge


The Concierge is the app that a user can sign up to create an itinerary for their trip. The user can search hotels or restaurants by putting in the names of the city and the state. Once the user submits the city and the state, a list of hotels/restaurants will show up with names, addresses, websites, phone numbers, and ratings (however, some places may not have all of the information).

The user can create an itinerary by naming the trip, select start date and end date, select the hotels/restaurants they are going to stay/visit. Their created itinerary will also have information about the places they select. The user can also delete the itinerary. On their itinerary page, all the created itineraries are shown with the names of the trips.

## Main Features
- A user can sign up/ log in / log out

  Only a signed up user can create an itinerary from the app

- Search hotels/restaurants by city and state

  People are familair with the names of the places so I chose city and state for the search form

- Showing places' info
  
  When people plan a trip, they are likely look at the information of the place so I make sure to include this and if there is a site of that palce available, the user can click the link directly to get more info of that place or can call from the number shown on the place details

- Create itinerary
 
  Once the user selects where they want to stay and eat, they can create an itinerary and print it out or come back to look at their trip plan later on their account.
  

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

## Try the code on your local machine
1. clone the repo
   
        $ git clone  https://github.com/KKTTAAII/capstone_first.git
2. set up environment
   
        $ python3 -m venv venv

3. insall requirements

        $ pip3 install -r requirements.txt

4. activate the environment

        $ source venv/bin/activate

5. you can create your own API Key here

    [Google Places API KEY](https://mapsplatform.google.com/)

6. create database

          $ createdb user_itinerary

7. create tables

          $ ipython
          In [1]: %run app.py

8. Enjoy the code!


Author: [Boonyawee P.](https://www.linkedin.com/in/boonyawee-prasertsiripond/)