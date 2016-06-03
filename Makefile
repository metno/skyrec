.PHONY: opencv skyrec

opencv:
	docker build --tag metno/opencv docker/opencv/

skyrec:
	docker build --no-cache --tag metno/skyrec docker/skyrec/
