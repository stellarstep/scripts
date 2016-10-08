# resc
A variety of resource file reprocessors that optimized for working with xcode. Performs to all files in sub directories.

## aifc
- convert wav to aifc (IMA4/ADPCM)
- **Recommended when playing Loop, short or fast, and multiple sounds simultaneously.**

## caf
- convert wav to caf (AAC/ABR/128000)
- **Recommended when playing almost all local(non-streaming) sounds. BUT Only a single instance can play on the device at a time.**
- refer via apple's technical document : [Bit Rate Control Modes for AAC Encoding](https://developer.apple.com/library/ios/technotes/tn2271/_index.html)

## flacmp3
- convert flac to mp3
- using [flac](http://xiph.org/flac/)

## svgc
- minify svg files.
- using [svgo](https://github.com/svg/svgo)

## gss
- compress pdf files.
- using [gs](http://www.ghostscript.com/)

## appv
- rescale mp4 video files via provided sizes. (especially, it is helpful when needed to force the correct size in pixels.)
- using ffmpeg.
- example to use (upscaling to 1080x1920)
```
$ appv preview_video_750x1334.mp4 preview_video_1080x1920.mp4 1080 1920
```
