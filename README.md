# docker-zenoss4
`docker-zenoss4` is a dockerized, Debian 7 based, image for [Zenoss Core v4.2.5](http://wiki.zenoss.org/Install_Zenoss#Zenoss_Core_4.2.5), based on [Hydruid's core-autodeploy for Ubuntu/Debian](https://github.com/hydruid/zenoss/).

## Description
In continuing my journey to learn Docker's Best Practices, I had the need to dockerize the Battle-tested, Zenoss 4.2.5. This time around, I knew that Zenoss4 has dependencies on other processes to work properly at 100%. So in true, docker spirit, I have segregated all the major services that comprises the Zenoss4 Stack into its own dockerized images, utilizing docker's default image library for the following:

* [mariadb](https://hub.docker.com/_/mariadb/) - `mariadb` 5.5 Database based instead of `mysql` 5.5
* [memcached](https://hub.docker.com/_/memcached/) - memcached distributed memory caching system 
* [redis](https://hub.docker.com/_/redis/) - `redis` is an open-source, networked, in-memory, key-value data store
* [rabbitmq](https://hub.docker.com/_/rabbitmq/) - `rabbitmq` implements the Advanced Message Queuing Protocol (AMQP)
* [nginx](https://hub.docker.com/_/nginx/) - `nginx` reverse http proxy 

The main glue for all of this orchestration is really the [docker-compose.yml file](https://github.com/krull/docker-zenoss4/docker-compose.yml) that pulls everything together. You can read more information on `docker-compose` and how to install it on your docker host at [docker's website](https://docs.docker.com/compose/).

The [Dockerfile](https://github.com/krull/docker-zenoss4/Dockerfile) for the `zenoss4-core` build has directives that points to the necessary hostnames of each dockerized services mentioned above to function properly and collectively.

For the automated build go to [hub.docker.com](https://hub.docker.com/r/mcroth/docker-zenoss4/)

You can use this image directly from [hub.docker.com](https://hub.docker.com/r/mcroth/docker-zenoss4/) by issuing the following docker commands:
```
docker pull mcroth/docker-zenoss4:latest
```

Many thanks for [hydruid](https://github.com/hydruid/zenoss/) for providing us a way to install zenoss4 on debian-based systems! Thanks for all the fish, Hydruid!

I have tried to build the image with docker best practices in mind. Should there be anything of note you notice, please do not hesitate to leave a comment.

