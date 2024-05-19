sync:
	rsync -avz -e "ssh -i ./keys/id_rsa" --exclude '.git' --exclude 'keys' --exclude 'node_modules' --exclude 'videos' --exclude 'smartcam.sqlite' --progress  /home/matrik/Yandex.Disk/CM3070_FP/code matrik@raspberrypi:/home/matrik

generate_key:
	ssh-keygen -t rsa -b 2048

copy_pubkey_to_rpi:
	ssh-copy-id -i ./keys/id_rsa.pub matrik@raspberrypi

connect:
	ssh -i ./keys/id_rsa matrik@raspberrypi

start_backend_dev:
	PYTHONPATH=src flask --app=src/backend/app run

start_frontend_dev:
	cd src/frontend && GENERATE_SOURCEMAP=false npm start

start_prod:
	PYTHONPATH=src DEBUG=0 flask --app=src/backend/app run --host=0.0.0.0 --port=5000

start_daemon:
	cd src && PYTHONPATH=. python surveillance_daemon/main.py

build_frontend:
	cd src/frontend && GENERATE_SOURCEMAP=false npm run build

cleanup:
	rm videos/* && rm src/smartcam.sqlite