sync:
	rsync -avz -e "ssh -i ./keys/id_rsa" --exclude '.git' --exclude 'keys' --progress  /home/matrik/Yandex.Disk/CM3070_FP/code matrik@raspberrypi:/home/matrik

generate_key:
	ssh-keygen -t rsa -b 2048

copy_pubkey_to_rpi:
	ssh-copy-id -i ./keys/id_rsa.pub matrik@raspberrypi

connect:
	ssh -i ./keys/id_rsa matrik@raspberrypi

start_backend:
	PYTHONPATH=src flask --app=src/backend/app run

start_frontend:
	cd src/frontend && GENERATE_SOURCEMAP=false npm start