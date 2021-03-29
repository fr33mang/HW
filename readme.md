# Simple HW (temporary)

## Running:

+ docker-compose build
+ docker-compose run finder_dev python3 app/numbers/finder.py file.txt

## Tests:

+ docker-compose run finder_dev pytest
+ docker-compose run finder_dev flake8

## Results:

+ 0:00:37.735341 10 threads (TPE)
+ 0:00:35.284306 20 threads 
+ 0:00:46.067926 10 processes
+ 0:00:44.389640 8 processes (PPE)
+ 0:00:46.432488 asyncio 10 workers (ASYNC)
