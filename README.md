# Patodeweloperka

(_pl. patodeweloperka - pathologically small apartments sold for an exorbitant 
price e.g. 16m<sup>2</sup> "flat"_)  

A scraper written in Python that collects flats advertisements and regularly 
checks for their price changes. Even though a threshold for 
"ridiculously small" area of a flat is not agreed on, I am going to say it's
less than 27m<sup>2</sup>.

### What I am looking for

I will check prices for **buying** and **renting** such flats.

- price of the apartment
- location (city and district)
- the size of the apartment (in m<sup>2</sup>)
- number of rooms
- number of bathrooms
- does it have a garage
- description

The rent offers include usually also the following info:
- can people smoke in the apartment
- can people keep pets at teh apartment

I am scraping data for studios and 2-room flats in Poland (both for sale and 
to rent). I am not putting any size constraints yet

### Aim of the project
1. Learn web scraping
2. Do something productive during the pandemic
3. Expose the scale of the problem in Poland. Maybe. (Too ambitious? We'll see)


### Running the project
```
docker-compose -f db/docker-compose.yml up 
```


TODO: 
1. add data from the big scraper
2. set up a scraper for the smallest flats

