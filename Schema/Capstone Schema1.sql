CREATE TABLE "hotel" (
    "id" PRIMARY KEY,
    "api_info" TEXT   NOT NULL
);

CREATE TABLE "restaurant" (
    "id" PRIMARY KEY,
    "api_info" TEXT   NOT NULL
);

CREATE TABLE "user" (
    "id" PRIMARY KEY,
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "email" TEXT   NOT NULL  
);

CREATE TABLE "itinerary" (
    "id" PRIMARY KEY,
    "user_id" INT NOT NULL,
    "start_date" DATE,
    "end_date" DATE 
);

CREATE TABLE "itinerary_hotel" (
    "itinerary_id" PRIMARY  KEY,
    "hotel_id" PRIMARY KEY
);

CREATE TABLE "itinerary_rest" (
    "itinerary_id" PRIMARY  KEY,
    "rest_id" PRIMARY  KEY
);

CREATE TABLE "fav_hotel" (
    "fav_id" PRIMARY  KEY,
    "hotel_id" PRIMARY  KEY
);

CREATE TABLE "fav_rest" (
    "fav_id" PRIMARY  KEY,
    "rest_id" PRIMARY  KEY
);

