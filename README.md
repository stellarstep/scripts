# scripts
Several small scripts and workflows(for mac os automation).

### xcp
- v1.0

The most simplest, safe, and config zero git pipelines, xcp lets you manage version of your Xcode project without currently working content. Safe from conflict or loss.

#### xcpd

Push to branch 'release-beta' with automatically increment build number, and create tag.(b/{buildNumber})

```
~/YOUR_PROJECT$ xcpd
```

#### xcpa

Squash merge, and push version of release onto master branch from specific tag.

```
~/YOUR_PROJECT$ xcpda {tag name of release version}

ex) ~/YOUR_PROJECT$ xcpda 1.0
```

#### xcpn

If your app succesfully released AppStore, Let's start with new CFBundleShortVersionString.

```
~/YOUR_PROJECT$ xcpn {target name} {new version name}

ex) ~/YOUR_PROJECT$ xcpn project1 1.1
```

#### xcpmake

Add your new git tasks and create. xcpmake will automatically wrap general git tasks up.

##### Make your own source script
example filename : xcpexample-src

```
# your git commands are here.
```

##### And then
```
~/YOUR_PROJECT$ xcpmake {source script file name} {file name to create}

ex) ~/YOUR_PROJECT$ xcpmake xcpexample-src xcpex
```

Or, you can test with shaped like below.

```
source $(dirname $0)/xcp-shared
source $(dirname $0)/xcp-begin
# your git commands are here.
source $(dirname $0)/xcp-end
```

#### If and when it throw any error..

Simply just do below.
```
~/YOUR_PROJECT$ git stash pop
```

### clean_itunes
- v1.0
- Requirements: Yosemite(for use JXA)


Clean your broken or dead tracks perfectly.

```
$ clean_itunes
```

### resc
A variety of resource file reprocessors that optimized for working with xcode. Performs to all files in sub directories.

###### aifc
- convert wav to aifc (IMA4/ADPCM)
- **Recommended when playing Loop, short or fast, and multiple sounds simultaneously.**

###### caf
- convert wav to caf (AAC/ABR/128000)
- **Recommended when playing almost all local(non-streaming) sounds. BUT Only a single instance can play on the device at a time.**
- refer via apple's technical document : [Bit Rate Control Modes for AAC Encoding](https://developer.apple.com/library/ios/technotes/tn2271/_index.html)

###### flacmp3
- convert flac to mp3
- using [flac](http://xiph.org/flac/)

###### svgc
- minify svg files.
- using [svgo](https://github.com/svg/svgo)

###### gss
- compress pdf files.
- using [gs](http://www.ghostscript.com/)

###### appv
- rescale mp4 video files via provided sizes. (especially, it is helpful when needed to force the correct size in pixels.)
- using ffmpeg.
- example to use (upscaling to 1080x1920)
```
$ appv preview_video_750x1334.mp4 preview_video_1080x1920.mp4 1080 1920
```

### shs

shell scripts

###### rename_all.sh

Recursive replace of directory and file names in the current directory. (excluding '.git')

```
$ rename_all.sh foo bar

/path/to/file_fooname.txt -> /path/to/file_barname.txt
```
