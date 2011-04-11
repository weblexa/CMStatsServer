from cmstats.utils.string import parse_modversion


def test_parse_modversion():
    rc = parse_modversion("CyanogenMod-7.0.0-RC2-N1")
    stable = parse_modversion("CyanogenMod-7.0.0-N1")
    nightly = parse_modversion("CyanogenMod-7-01012011-NIGHTLY-N1")
    kang1 = parse_modversion("CyanogenMod-7.0.0-RC2-N1-KANG")
    kang2 = parse_modversion("CyanogenMod-7-Negro90-V.3.1-MAGLDR")

    assert rc == "7.0.0-RC2"
    assert stable == "7.0.0"
    assert nightly == "Nightly"
    assert kang1 == None
    assert kang2 == None
