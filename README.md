build and run the project:

```bash
docker build -t flask . && docker run -it --env-file .env --network host -v `pwd`:/app flask
```
