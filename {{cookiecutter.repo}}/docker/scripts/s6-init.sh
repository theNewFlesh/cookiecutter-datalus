#!/command/with-contenv bash

if [ "$SKIP_S6_SERVICE" != "true" ]; then
    cp -r /home/ubuntu/$REPO/docker/config/jupyter /home/ubuntu/.jupyter;
    cp /home/ubuntu/$REPO/docker/config/zshrc /home/ubuntu/.zshrc;
fi;
