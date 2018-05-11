# maxi22

## overview

a web application that demonstrates responsive web ui that interacts with golang backend via python cgis.

## deployment

* apache2 - apache2 web server configurations.
* dockerfiles - dockerfile to create docker image of maxi22.
* muffin - a bootstrap web application.
* pastry - python cgi.
* go/src/grocer - go xml backend.

## create docker container

### maxi22 patio - development mode

* dockerfile.

    [maxi22patio.dockerfile](dockerfiles/maxi22patio.dockerfile)

* create maxi22patio docker image.
 
    ```
    docker build -f dockerfiles/maxi22patio.dockerfile -t jacobrepo/maxi22patio:0.01 .
    ```

* create maxi22patio docker container and start it in console mode.

    * create maxi22patio docker container

    ```
    docker create -it --name maxi22patio --dns 172.19.10.100 -p 8888:80 -v /home/jacob_shih/volumes/maxi22:/home/user/maxi22 jacobrepo/maxi22patio:0.01
    ```

    * start maxi22patio in console mode.

    ```
    docker start maxi22patio
    docker exec -it maxi22patio su user
    ```

* or, just run it as an http daemon.

    ```
    docker run -d --name maxi22patio --dns 172.19.10.100 -p 8888:80 -v /home/jacob_shih/volumes/maxi22:/home/user/maxi22 jacobrepo/maxi22patio:0.01
    ```

### ~~maxi22 lounge - static mode ***FIXME - to be done.***~~

* ~~dockerfile.~~

    ~~[maxi22lounge.dockerfile](dockerfiles/maxi22lounge.dockerfile)~~

* ~~create maxi22lounge docker image.~~
 
    ```
    docker build -f dockerfiles/maxi22lounge.dockerfile -t jacobrepo/maxi22lounge:0.01 .
    ```

* ~~run it as an http daemon.~~

    ```
    docker run -d --name maxi22lounge --dns 172.19.10.100 -p 8888:80 jacobrepo/maxi22lounge:0.01
    ```

## test web server

* launch the web page in browser.

    [http://localhost:8888/](http://localhost:8888/)

* test with command line

```
wget http://localhost:8888/
```

```
curl --get -o index.html http://localhost:8888/
```