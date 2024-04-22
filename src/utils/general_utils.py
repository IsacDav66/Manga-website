import flag

def get_flag_emoji(country_code):
    try:
        flag_emoji = flag.flag(country_code)
        return flag_emoji
    except ValueError:
        return ""