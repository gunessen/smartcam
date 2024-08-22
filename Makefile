sync:
	rsync -avz -e "ssh -i ./keys/id_rsa" --exclude '.git' --exclude 'keys' --exclude 'node_modules' --exclude 'videos' --exclude 'smartcam.sqlite' --exclude 'full-ds' --progress /home/matrik/Yandex.Disk/CM3070_FP/code matrik@raspberrypi:/home/matrik

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
	PYTHONPATH=src DEBUG=0 OPENCV_LOG_LEVEL=ERROR flask --app=src/backend/app run --host=0.0.0.0 --port=5000

start_daemon:
	cd src && PYTHONPATH=. python surveillance_daemon/main.py

build_frontend:
	cd src/frontend && GENERATE_SOURCEMAP=false npm run build

cleanup:
	rm videos/* || rm src/smartcam.sqlite

dl_yolov7_weights:
	cd model_conversion/yolov7 && wget https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-tiny.pt

convert_yolov7_onnx:
	cd model_conversion/yolov7 && python export.py --weights yolov7-tiny.pt --grid --end2end --simplify --topk-all 100 --iou-thres 0.65 --conf-thres 0.35 --img-size 640 640 --max-wh 640

convert_yolov_tf:
	cd model_conversion/yolov7 && onnx-tf convert -i yolov7-tiny.onnx -o weights

convert_yolov_tf_to_tflite:
	cd model_conversion/yolov7 && python tf_to_tflite.py