sync:
	rsync -avz -e "ssh -i ./keys/id_rsa" --exclude '.git' --exclude 'keys' --progress  /home/matrik/Yandex.Disk/CM3070_FP/code matrik@raspberrypi:/home/matrik

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
	PYTHONPATH=src DEBUG=0 flask --app=src/backend/app run