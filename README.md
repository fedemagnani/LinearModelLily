# LinearModelLily

# Requirements
Install docker for ubuntu here https://docs.docker.com/engine/install/ubuntu/


# Steps - Run locally via docker

- Create `src` app in the parent folder

- in the parent folder, create the `Dockerfile`

- in the `src` folder, create the `app.py` file

- in the parent folder build the docker image using a reusable tag_name: `sudo docker build --tag <tag_name> .`. Here we are using `linear_lily`, so the command is 
```
sudo docker build --no-cache --tag linear_lily .
``` 
- we create local input and output directoris.  . 
```
mkdir /tmp/output_linear_lily
mkdir /tmp/input_linear_lily
```
The output directory for example is accessible via `computer/tmp/output_linear_lily`

- in order to run locally the application, we run 
```
sudo docker run --rm -v /tmp/output_linear_lily:/outputs -v /tmp/input_linear_lily:/inputs  linear_lily --cid-source QmaW9TL7ACBK4VFLxg7tbSnePjDnxd4R1upu4yb5xLBuy1 --target-column "Car Purchase Amount" --ignore-columns "Customer Name" "Customer e-mail" "Country" 
``` 
Some insights about docker flags:
- `--rm` automatically removes the container when it exits
- `-v` creates a mapping between the local folder and the docker container. In our case, we are mapping the local folder `/tmp/output_linear_lily` to the docker container `/outputs`. The same for the input folder
- `-e` sets the environment variable 

# Steps - Push to dockerhub and run via lilypad

- Now we are about to push the image to dockerhub, so we run 
```
sudo docker login
```
- Once that the login is perfomed, we associate the tag initially defined via `docker tag <tag_name> <docker-hub-user>/<tag_name>:1.0.0`. In our case is
```
sudo docker tag linear_lily drunnn/linear_lily:1.0.0
```
- Now we are ready to push the image to dockerhub
```
sudo docker push drunnn/linear_lily:1.0.0
```
- In order to recover the sha256 digest of the pushed image, one can run (notice that we are replacing `sha256:` with `0x`)
`docker pull <docker-hub-user>/<tag_name>:1.0.0 | grep "Digest: sha256:" | sed 's/.*sha256:/0x/'` i.e.
```
sudo docker pull drunnn/linear_lily:1.0.0 | grep "Digest: sha256:" | sed 's/.*sha256:/0x/'
```
- Now we need to create the `lilypad_module.json.tmpl` file (check example file). Make sure it is called in this way

- We are ready to push the repo on github!

- Once that we have pushed our repo, you need to create a tag for the code on github. We are calling it `v1.2`. NOw we are ready to run our job task. Notice that `--module-hash` refers to the commit hash of the update
```
lilypad run github.com/fedemagnani/LinearModelLily:v1.2 -i X=5 -i Y=3 --module-repo https://github.com/fedemagnani/LinearModelLily --module-hash 5e477712394cb29cebf68aa2ac1b8b63f9e9cf01 --module-path ./lilypad_module.json.tmpl
```

If you want more verbose logs, tyoe `export LOG_LEVEL=debug`