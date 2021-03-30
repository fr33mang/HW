# Simple HW (temporary)

## Running:

+ docker-compose build
+ docker-compose run finder_dev python3 app/numbers/finder.py file.txt
+ docker-compose run finder_dev python3 app/numbers/async_finder.py

## Tests:

+ docker-compose run finder_dev pytest
+ docker-compose run finder_dev flake8

## Results:

### 400 urls

+ 0:00:30.471150 (ASYNC + ProcessPoolExecutor)
+ 0:00:35.284306 20 threads (SYNC + TPE)
+ 0:00:44.389640 8 processes (SUNC + PPE)
+ 0:00:46.432488 asyncio 10 workers (ASYNC)
