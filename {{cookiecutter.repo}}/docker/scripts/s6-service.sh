#!/command/with-contenv zsh

if [ "\$SKIP_S6_SERVICE" != "true" ]; then
    source /home/ubuntu/.zshrc &&
    x_env_activate_dev &&
    exec jupyter lab \
        --notebook-dir="/home/ubuntu/$REPO/notebooks" \
        --ip=0.0.0.0 \
        --no-browser \
        --allow-root \
        --port=8888 \
        --ServerApp.token="" \
        --ServerApp.password="" \
        --ServerApp.allow_origin="*" \
        --ServerApp.allow_remote_access=True \
        --ServerApp.authenticate_prometheus=False \
        --ServerApp.base_url="$NB_PREFIX";
fi;
