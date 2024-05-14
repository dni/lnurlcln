# Corelightning LNURL plugin

## requirements
corelightning, python3.10 and poetry

## install
```console
git clone git@github.com:dni/lnurlcln.git
cd lnurlcln
poetry install
```

## run
```console
lightning-cli plugin start $(poetry env info --path)/bin/lnurlcln
lightning-cli plugin stop $(poetry env info --path)/bin/lnurlcln
```

### dev
watch the logs if your node
```console
docker logs -f regtest-clightning-1-1
```
watch for changes and restart the plugin inside the regtest
```console
find lnurlcln/*.py | entr -s "./dev.sh regtest-clightning-1-1"
```
