*Start service/only changed code
docker-compose up -d

*Check logs
docker logs -f carousell-crawler-analyzer-carousell-crawler-1

*Update those requirements, dockerfile, need to --build and run again
docker-compose up -d --build

