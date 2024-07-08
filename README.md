# MyScribe (Working Title)

This is a re-creation of the awesome [Subvert App](https://github.com/aschmelyun/subvert) by [aschmelyun](https://github.com/aschmelyun)
I decided to re-make it with reflex.dev as I wanted to add local AI capabilities (instead of only API based), and I'm in no way a proper 'dev', but I knew I could fumble through it in python.

This is the reflex project, it's not built at the minute as I'm still working on it. But I'm happy for anyone to grab it and do whatever they want with it.

It currently only works with local faster-whisper and llama3:8b via ollama. I focused on adding the local AI features first, although the settings have been implemented for add API for Open AI, Gemini & Claude, so I'm hoping to implement those next.

## Other ideas:
- Implement libretranslate to translate the subtitles/transcript from english to any language it supports.
- If a video was provided, add the option to 'burn in' the generated subtitles via ffmpeg.
- It'd be awesome to be able to edit the subtitles, and even better, see them along-side the video/audio, cick a word & it take you to that timestamp in the video etc, but, that's probably way above my pay grade lol.
