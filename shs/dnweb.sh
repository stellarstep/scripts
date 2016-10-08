target_host=$(echo "$1" | cut -d'/' -f3)

wget \
  --recursive \
  --no-clobber \
  --page-requisites \
  --html-extension \
  --convert-links \
  --restrict-file-names=windows \
  --domains $target_host \
  --no-parent \
			$1