Example of web service.

Used NGINX, Python, async Quart server, MySQL and Docker.

If you want to start then type ./compose.sh

Break using ctrl C.

After that ./decompose.sh

visit when service is active:
127.0.0.1/logo.png
127.0.0.1/var-and-peace.txt
127.0.0.1/test
127.0.0.1/cats
127.0.0.1/dump  - after that goto ./storage/private and look at .txt file
                  it is data from MySQL db that was inited in ./mysql/init/*.sql
