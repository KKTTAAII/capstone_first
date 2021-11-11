CREATE TABLE "hotel" (
    "id" PRIMARY KEY,
    "name" TEXT   NOT NULL,
    "address" TEXT   NOT NULL,
    "website" TEXT   NOT NULL,
    "number" TEXT   NOT NULL,
);

CREATE TABLE "restaurant" (
    "id" PRIMARY KEY,
    "name" TEXT   NOT NULL,
    "address" TEXT   NOT NULL,
    "website" TEXT   NOT NULL,
    "number" TEXT   NOT NULL,
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
    "name" TEXT,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL
);

CREATE TABLE "itinerary_hotel" (
    "id" PRIMARY KEY,
    "itinerary_id" INT NOT NULL,
    "hotel_id" INT NOT NULL
);

CREATE TABLE "itinerary_rest" (
    "id" PRIMARY KEY,
    "itinerary_id" INT NOT NULL,
    "rest_id" INT NOT NULL
);


