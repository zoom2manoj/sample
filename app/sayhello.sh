
#!/bin/sh
#echo "Hello, my name is Wait! Who am I talking to?"
#echo Type your name to continue:Manoj
#read name
#echo --------------------------
#echo Nice to meet you $name!.
#echo You have done a great job.
#echo 💥 Congratulations $name and see you later 💥
#echo --------------------------


set -e
until curl --output /dev/null --silent --head --fail "$WAIT_HOSTS"; do
  >&2 echo "Mysql is unavailable - sleeping"
  sleep 1
done
>&2
source /usr/local/bin/docker-entrypoint

