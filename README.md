
NoName API Security Interview Task using Chinook Database API

Example commands:

**GET All Tracks**  
curl -X GET http://nns.jkassis.net:8000/tracks/all

**GET a Specific Track**  
curl -X GET http://nns.jkassis.net:8000/tracks/1

**GET search the database**  
curl -X GET http://nns.jkassis.net:8000/tracks/search?query=STRING

**POST Create a New Track**  
curl -X POST -H "Content-Type: application/json" -d '{"Name": "New Track", "AlbumId": 2, "MediaTypeId": 1}' http://nns.jkassis.net:8000/tracks

**PUT Update a Track**  
curl -X PUT -H "Content-Type: application/json" -d '{"Name": "RockRock", "AlbumId": 33, "MediaTypeId": 2}' http://nns.jkassis.net:8000/tracks/1

**DELETE Delete a Track**  
curl -X DELETE http://nns.jkassis.net:8000/tracks/1

Infrastructure and App diagrams:

![enter image description here](https://i.ibb.co/YZh9VSw/noname-task-diagram.png)
