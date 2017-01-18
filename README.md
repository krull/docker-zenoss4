# docker-zenoss4
`docker-zenoss4` is a dockerized, Debian 7 based, image for [Zenoss Core v4.2.5](http://wiki.zenoss.org/Install_Zenoss#Zenoss_Core_4.2.5), based on [Hydruid's core-autodeploy for Ubuntu/Debian](https://github.com/hydruid/zenoss/), with alterations, enhancements and security improvements in accordance to Docker's ephemeral ecosystem. Hydruid's work was based on OS Virtualization/Bare-metal installs, and for its time was sufficient for the task.

## description
In continuing my journey to learn Docker's Best Practices, I had the need to dockerize the Battle-tested, Zenoss 4.2.5. This time around, I knew that Zenoss4 has dependencies on other processes to work properly at 100%. So in true, docker spirit, I have segregated all the major services that comprises the Zenoss4 Stack into its own dockerized images, utilizing docker's default image library for the following:

* [memcached](https://hub.docker.com/_/memcached/), a distributed memory caching system, named `zenoss4-memcached`
* [rabbitmq](https://hub.docker.com/_/rabbitmq/), the Advanced Message Queuing Protocol (AMQP), named `zenoss4-rabbitmq`
* [redis](https://hub.docker.com/_/redis/), a networked, in-memory, key-value data store, named `zenoss4-redis`
* [mariadb](https://hub.docker.com/_/mariadb/), SQL Database backwards compatible to `mysql 5.5`, named `zenoss4-mariadb` 
* [nginx](https://hub.docker.com/_/nginx/), reverse http proxy, named `zenoss4-nginx`

The dockerized image of zenoss v4.2.5 is aptly named `zenoss4-core`.

The main glue for all of this orchestration is really the [docker-compose.yml file](https://github.com/krull/docker-zenoss4/blob/master/docker-compose.yml) which pulls everything together. You can read more information on `docker-compose` and how to install it on your docker host at [docker's website](https://docs.docker.com/compose/).

The [Dockerfile](https://github.com/krull/docker-zenoss4/blob/master/Dockerfile) for the `zenoss4-core` build has directives that points to the necessary hostnames of each dockerized services mentioned above to function properly and collectively. There is a `.dockerignore` file that ignores the whole `init_fs` folder upon build time. Moreover, I have excluded some environmental variables in files called `.env` and `.env_make`. I have added sample `.smpl` files. Just rename them accordingly.

Many thanks for [hydruid](https://github.com/hydruid/zenoss/) for providing us a way to install zenoss4 on debian-based systems! Thanks for all the fish, Hydruid!

I have tried to build the image with docker best practices in mind. Should there be anything of note you notice, please do not hesitate to leave a comment.

## quickstart 
```
root@mcroth:~/sandbox# git clone https://github.com/krull/docker-zenoss4.git
Cloning into 'docker-zenoss4'...
remote: Counting objects: 69, done.
remote: Compressing objects: 100% (53/53), done.
remote: Total 69 (delta 19), reused 59 (delta 13), pack-reused 0
Unpacking objects: 100% (69/69), done.
Checking connectivity... done.
root@mcroth:~/sandbox# cd docker-zenoss4/
root@mcroth:~/sandbox/docker-zenoss4# docker-compose up -d
Creating network "dockerzenoss4_front-tier" with driver "bridge"
Creating network "dockerzenoss4_back-tier" with driver "bridge"
Creating zenoss4-memcached
Creating zenoss4-rabbitmq
Creating zenoss4-redis
Creating zenoss4-mariadb
Creating zenoss4-core
Creating zenoss4-nginx
Attaching to zenoss4-memcached, zenoss4-rabbitmq, zenoss4-redis, zenoss4-mariadb, zenoss4-core, zenoss4-nginx
...

root@mcroth:~/sandbox/docker-zenoss4# docker ps -a
CONTAINER ID        IMAGE                   COMMAND                  CREATED              STATUS              PORTS                                                    NAMES
14edce6dbf4a        nginx                   "nginx -g 'daemon off"   About a minute ago   Up About a minute   0.0.0.0:80->80/tcp, 443/tcp                              zenoss4-nginx
0690ca546ee7        mcroth/docker-zenoss4   "docker-entrypoint.sh"   About a minute ago   Up About a minute   0.0.0.0:32833->8080/tcp                                  zenoss4-core
c75bb844f5d3        mariadb:5.5             "docker-entrypoint.sh"   About a minute ago   Up About a minute   0.0.0.0:32832->3306/tcp                                  zenoss4-mariadb
69a71a9d3151        redis:3.0               "docker-entrypoint.sh"   About a minute ago   Up About a minute   0.0.0.0:32831->6379/tcp                                  zenoss4-redis
5814c80111c3        rabbitmq:3.6            "docker-entrypoint.sh"   About a minute ago   Up About a minute   4369/tcp, 5671/tcp, 25672/tcp, 0.0.0.0:32830->5672/tcp   zenoss4-rabbitmq
97f1d528d9eb        memcached:1.4           "docker-entrypoint.sh"   About a minute ago   Up About a minute   0.0.0.0:32829->11211/tcp                                 zenoss4-memcached
```

Once the init is done, you ought to have a full, 100% working `zenoss4` docker install located at `http://localhost`! Default zenoss logins: `admin`/`zenoss`

For the automated build go to [hub.docker.com](https://hub.docker.com/r/mcroth/docker-zenoss4/).

You can use this image directly from [hub.docker.com](https://hub.docker.com/r/mcroth/docker-zenoss4/) by issuing the following docker commands:
```
docker pull mcroth/docker-zenoss4:latest
```

## ssl encryption
According to [this wiki.zenoss.org entry](http://wiki.zenoss.org/Newsletter:5/Encrypt_All_the_Bits), you can proxy pass all zenoss traffic via NGINX, and in our case our `zenoss4-nginx` image instance.

You will need to ofcourse provide your own SSL Certificates for your own domain name that is guaranteed by a Certifying Authority (CA). My suggestion is to use [Let's Encrypt's](https://letsencrypt.org/) [SSL For Free](https://www.sslforfree.com/) if you want to just test the waters on a fully SSL enabled Zenoss Install without reverting to a self-signed SSL certificate/key pair.

Here are `zenoss4-nginx`'s server blocks for `mnt.example.com` to accomodate SSL encryption:
```
server {
    listen 80;
    server_name mnt.example.com;

    return 301 http://mnt.example.com$request_uri;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
}

server {
    listen 443 ssl http2;
    server_name mnt.example.com;

    add_header Strict-Transport-Security "max-age=31536000; includeSubdomains";

    ssl_certificate /etc/nginx/ssl/mnt_example_com.crt;
    ssl_certificate_key /etc/nginx/ssl/mnt_example_com.key;

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";

    location / {
        rewrite  ^(.*)$ /VirtualHostBase/https/$host:443$1 break;

        proxy_cache STATIC;
        proxy_cache_bypass  $http_cache_control;
        add_header X-Proxy-Cache $upstream_cache_status;
        proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://zenoss4-core:8080;
    }

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
}
```

Notice I have redirected all http traffic to it's https equivalent. Save it as `default.conf` in `./init_fs/etc/nginx/`, and make certain that in your `docker-compose.yml` file you will have the following `volume` entry:
```
  zenoss4-nginx:
    image: nginx:alpine
    container_name: zenoss4-nginx
    hostname: zenoss4-nginx
    volumes:
      - "./init_fs/etc/nginx/conf.d/default.conf:/etc/nginx/conf.d/default.conf:ro"
      - "./init_fs/etc/nginx/ssl:/etc/nginx/ssl:ro"
    links:
      - zenoss4-core
    depends_on:
      - zenoss4-core
    ports:
      - "80:80"
      - "443:443"
    networks:
      - back-tier
      - front-tier
```

Take note of the ssl directory for your crts/key file pair as well as the 443/80 port mappings. Once up, `zenoss4-core` will show up at `https://mnt.example.com`. Please be aware that `zenoss4-core` will still try to load http traffic from 3rd party locations.

## sms gateway integration
With the help of [SMSeagle's Zenoss SMS Integration page](https://www.smseagle.eu/integration-plugins/zenoss-sms-integration/), I have managed to integrate successfully the following SMS gateways in Zenoss:

* SMSEagle
* Plivo
* Twilio
* BulkSMS

Just follow the instructions on the page above, and browse through the sms scripts located [here](https://github.com/krull/docker-misc/tree/master/init_fs/usr/local/zenoss/bin), so far only `zenoss_plvsms` is published. 

## default build
There is a `Makefile`, with some directives on building `docker-zenoss4`. Have a look at that file and check the options. Issuing a `make` will run the default build.

