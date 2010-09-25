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

if __name__ == '__main__':
    print parseModVersion("CyanogenMod-6-01012010-NIGHTLY-N1")
    print parseModVersion("CyanogenMod-6.0-N1")
    print parseModVersion("CyanogenMod-6.1.0-RC0-Droid")