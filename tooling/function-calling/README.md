## For local run

```bash
docker build -t ml-infra-app .
docker run -it --rm -p 3000:3000 --name running-app ml-infra-app  
```