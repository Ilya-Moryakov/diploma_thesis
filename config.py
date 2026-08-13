import os


BASE_URL = "https://market-delivery.yandex.ru"


CART_PARAMS = {
    "soft_multi": "true",
    "longitude": "49.31831758191744",
    "latitude": "53.61815720687113",
    "screen": "menu",
    "shippingType": "delivery",
    "autoTranslate": "false",
    "plus_subscription_toggle_state": "false"
}


AUTH_COOKIE_NAME = "Session_id"
AUTH_COOKIE_VALUE = os.getenv("YANDEX_SESSION_ID",
                              "3:1786464004.5.0.1786464004189:"
                              "Qtkg1A:c627.1.2:1|885165444."
                              "-1.20002.3:1786464004|3:"
                              "12106036.958906.6eSA0_OzTlDXxrv2rnOPwb2d_0Y")
