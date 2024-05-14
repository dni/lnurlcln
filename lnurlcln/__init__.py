import sys
import asyncio
from lnurl import decode, handle, execute
from lnurl.exceptions import LnurlException
from pyln.client import Plugin
from typing import Any

PLUGIN_NAME = "lnurlcln"
VERSION = "0.1.0"

lnurl_missing_error = {
    "code": -4700,
    "message": "Error missing LNURL argument",
}

lnurl_decode_error = {
    "code": -4701,
    "message": "Error decoding LNURL",
}

lnurl_auth_secret_error = {
    "code": -4702,
    "message": "LNURL auth error missing secret argument",
}

lnurl_pay_amount_error = {
    "code": -4703,
    "message": "LNURL pay error missing amount argument",
}

lnurl_withdraw_bolt11_error = {
    "code": -4704,
    "message": "LNURL withdraw error missing bolt11 argument",
}

lnurl_execute_value_error = {
    "code": -4705,
    "message": "LNURL execute error missing value argument",
}


def main():

    plugin = Plugin()

    @plugin.method(
        method_name="lnurl-decode",
        category="lnurl",
    )

    def lnurl_decode_method(
        lnurl: str = "",
    ) -> dict[str, Any]:
        """ Decode a LNURL and return the result """

        if lnurl == "":
            return lnurl_missing_error

        plugin.log(f"Decoding lnurl: {lnurl}")
        try:
            decoded = decode(lnurl)
        except LnurlException:
            return lnurl_decode_error
        return { "lnurl": decoded }


    @plugin.method(
        method_name="lnurl-handle",
        category="lnurl",
    )
    def lnurl_handle_method(
        lnurl: str = "",
    ) -> dict[str, Any]:
        """ Decode a LNURL and return the LnurlResponse """

        if lnurl == "":
            return lnurl_missing_error

        plugin.log(f"Handling lnurl: {lnurl}")
        try:
            res = asyncio.run(handle(lnurl))
        except LnurlException:
            return lnurl_decode_error
        return res.dict()


    @plugin.method(
        method_name="lnurl-execute",
        category="lnurl",
    )
    def lnurl_execute_method(
        lnurl: str = "",
        value: str = "",
    ) -> dict[str, Any]:
        """ LNURL execute a command """
        if lnurl == "":
            return lnurl_missing_error
        if value == "":
            return lnurl_execute_value_error

        plugin.log(f"Executing: {lnurl} with value: {value}")
        try:
            res = asyncio.run(execute(lnurl, value))
        except LnurlException:
            return lnurl_decode_error
        return res.dict()


    @plugin.method(
        method_name="lnurl-auth",
        category="lnurl",
    )
    def lnurl_auth_method(
        lnurl: str = "",
        secret: str = "",
    ) -> dict[str, Any]:
        """ LNURL Auth """
        if lnurl == "":
            return lnurl_missing_error
        if secret == "":
            return lnurl_auth_secret_error

        plugin.log(f"Executing LNURL auth: {lnurl}")
        try:
            res = asyncio.run(execute(lnurl, secret))
        except LnurlException:
            return lnurl_decode_error
        return res.dict()


    @plugin.method(
        method_name="lnurl-pay",
        category="lnurl",
    )
    def lnurl_pay_method(
        lnurl: str = "",
        amount_msat: int = 0,
    ) -> dict[str, Any]:
        """ LNURL Pay """
        if lnurl == "":
            return lnurl_missing_error
        if amount_msat == 0:
            return lnurl_pay_amount_error

        plugin.log(f"Executing pay amount: {amount_msat} to LNURL: {lnurl}")
        try:
            res = asyncio.run(execute(lnurl, str(amount_msat)))
        except LnurlException:
            return lnurl_decode_error
        return res.dict()


    @plugin.method(
        method_name="lnurl-withdraw",
        category="lnurl",
    )
    def lnurl_withdraw_method(
        lnurl: str = "",
        bolt11: str = "",
    ) -> dict[str, Any]:
        """ LNURL Withdraw """
        if lnurl == "":
            return lnurl_missing_error
        if bolt11 == 0:
            return lnurl_withdraw_bolt11_error

        plugin.log(f"Executing withdraw from LNURL: {lnurl} to {bolt11}")
        try:
            res = asyncio.run(execute(lnurl, bolt11))
        except LnurlException:
            return lnurl_decode_error
        return res.dict()


    @plugin.init()
    def init(
        options: dict[str, Any],
        configuration: dict[str, Any],
        plugin: Plugin,
        **kwargs: dict[str, Any],
    ) -> None:
        try:
            plugin.log(f"Plugin {PLUGIN_NAME} v{VERSION} initialized")
        except BaseException as e:
            plugin.log(f"Could not start {PLUGIN_NAME} v{VERSION}: {e}", level="warn")
            sys.exit(1)


    @plugin.subscribe("shutdown")
    def shutdown(**kwargs: dict[str, Any]) -> None:
        plugin.log(f"Plugin {PLUGIN_NAME} stopped")
        sys.exit(0)


    plugin.run()
