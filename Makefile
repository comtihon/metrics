.PHONY: build test_run run

test_build:
	python setup.py bdist_wheel
test_install: test_build
	sudo pip install dist/metric_tester-1.0.0-py3-none-any.whl
test_run: test_install
	metric_tester
build: 
	./build_images.sh
run: build
	docker-compose up -d
stop:
	docker-compose down
