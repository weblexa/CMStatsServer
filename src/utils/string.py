import re

def parseModVersion(modver):
    match = re.match(r"^CyanogenMod-(.*)-.*$", modver)
    if match:
        version = match.groups()[0]
        if "NIGHTLY" in version:
            version = "Nightly"
    else:
        version = "Unknown"

    return version