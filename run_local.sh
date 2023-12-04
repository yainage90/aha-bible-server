docker run\
  --name aha-bible-server\
  --rm -d\
  -p 8000:8000\
  --network host\
  --env-file ./.env\
  aha-bible-server