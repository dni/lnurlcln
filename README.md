# Corelightning LNURL plugin
Support for LNURL Decoding, Paylinks, Withdraw and Auth

## corelightning commands
```console
=== lnurl ===

lnurl-decode [lnurl]
    Decode a LNURL and return the result

lnurl-handle [lnurl]
    Decode a LNURL and return the LnurlResponse

lnurl-execute [lnurl] [value]
    LNURL execute a command

lnurl-auth [lnurl] [secret]
    LNURL Auth

lnurl-pay [lnurl] [amount_msat]
    LNURL Pay

lnurl-withdraw [lnurl] [bolt11]
    LNURL Withdraw
```

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
