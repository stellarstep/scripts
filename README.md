# scripts
Several small scripts and workflows(for mac os automation).

### xcpd
- v0.0.1

A git script for deploying Xcode project.<br/>
Automatically increment build number and push to specific branch without currently working content.<br/>
Safe from conflict or loss.

```
~/YOUR_PROJECT$ xcpd
```

If throw any error, simply just do below.
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

###### flacmp3
- convert flac to mp3 
- using [flac](http://xiph.org/flac/)

###### wav2aifc
- convert wav to aifc (IMA4/ADPCM)

###### svgc
- minify svg files.
- using [svgo](https://github.com/svg/svgo)
 
###### gss
- compress pdf files.
- using [gs](http://www.ghostscript.com/)
