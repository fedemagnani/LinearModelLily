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
sudo docker run --rm -v /tmp/output_linear_lily:/outputs -v /tmp/input_linear_lily:/inputs  linear_lily --target-column "Car Purchase Amount" --ignore-columns "Customer Name" "Customer e-mail" "Country" 
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
- Once that the login is perfomed, we associate the tag initially defined via `docker tag <tag_name> <docker-hub-user>/<tag_name>:1.0.4`. In our case is
```
sudo docker tag linear_lily drunnn/linear_lily:1.0.4
```
- Now we are ready to push the image to dockerhub
```
sudo docker push drunnn/linear_lily:1.0.4
```
- In order to recover the sha256 digest of the pushed image, one can run (notice that we are replacing `sha256:` with `0x`)
`docker pull <docker-hub-user>/<tag_name>:1.0.4 | grep "Digest: sha256:" | sed 's/.*sha256:/0x/'` i.e.
```
sudo docker pull drunnn/linear_lily:1.0.4 | grep "Digest: sha256:" | sed 's/.*sha256:/0x/'
```
- Now we need to create the `lilypad_module.json.tmpl` file (check example file). Make sure it is called in this way

- We are ready to push the repo on github!

- Once that we have pushed our repo, you need to create a tag for the code on github, we are calling it `v1.8`. 

- we set also our private key via
```
export WEB3_PRIVATE_KEY=<pvtk>
```
- Now we are ready to run our job task. Notice that `--module-hash` refers to the commit hash of the update

```
lilypad run github.com/fedemagnani/LinearModelLily:v1.8 -i URL=https://ipfs.chainsafe.io/ipfs/QmaW9TL7ACBK4VFLxg7tbSnePjDnxd4R1upu4yb5xLBuy1 -i Y="Car Purchase Amount" -i IGNORE1="Customer Name" -i IGNORE2="Customer e-mail" -i IGNORE3="Country" --module-repo https://github.com/fedemagnani/LinearModelLily --module-hash 25fa0f35b8e2daf306accab4ac18b9e44b3d8718 --module-path ./lilypad_module.json.tmpl
```
### IMPORTANT: 
- Notice that by committing the code, a new commit hash is produced and so you need to update the prompt
- If you want more verbose logs, tyoe `export LOG_LEVEL=debug`
- Around 2:00 AM, Lilypad goes to sleep
- Once that the job task is triggered, docker doesn't have access to the internet, so specify all the inputs you need to install via the inputs key in .tmpl file
- A nice IPFS for accessing content is `https://ipfs.eth.aragon.network/ipfs/` (you append the CID at the end)
- A list of IPFS gateways is here `https://ipfs.github.io/public-gateway-checker/`
- subt hack of pull request 14 (lilypad) doesn't work, so I'm letting user pasting directly their url

## TODO
- understand `inputs` object in the .tmpl file 