EMOJI = {
    "settings": "5870982283724328568",
    "profile": "5870994129244131212",
    "users": "5870772616305839506",
    "file": "5870528606328852614",
    "smile": "5870764288364252592",
    "stats": "5870921681735781843",
    "home": "5873147866364514353",
    "lock": "6037249452824072506",
    "megaphone": "6039422865189638057",
    "check": "5870633910337015697",
    "cross": "5870657884844462243",
    "code": "5940433880585605708",
    "loading": "5345906554510012647",
    "time": "5983150113483134607",
    "gift": "6032644646587338669",
}


def pemoji(name: str, fallback: str = "⚙️") -> str:
    emoji_id = EMOJI.get(name, EMOJI["settings"])
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'
