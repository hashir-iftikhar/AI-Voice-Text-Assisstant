from assisstant import speak , gemini_reply , google

def test_speak():
    assert speak("Im working fine")


def test_google():
    assert google("youtube.com")