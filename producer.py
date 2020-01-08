import sys
import time
import cv2
from kafka import KafkaProducer

topic = "stream-video"

def publish_video(video_file):
	producer = KafkaProducer(bootstrap_servers='localhost:9092')
	video  = cv2.VideoCapture(video_file)

	print('publicando video.....')

	while(video.isOpened()):
		success,frame = video.read()
		if not success:
			print('Bad read')
			break
		ret, buffer = cv2.imencode('.jpg',frame)

		producer.send(topic,buffer.tobytes())

		time.sleep(0.2)
	
	video.release()
	print('publicacion completa')

def publish_camera():
	producer = KafkaProducer(bootstrap_servers='localhost:9092')

	camera = cv2.VideoCapture(0)

	try:
		while(True):
			success,frame = camera.read()
			ret,buffer = cv2.imencode('.jpg',frame)
			producer.send(topic,buffer.tobytes())
			time.sleep(0.2) 
	except e:
		print("Terminando")
		sys.exit(1)
	
	camera.release()

if __name__ == '__main__':
	if(len(sys.argv) > 1):
		video_path =  sys.argv[1]
		publish_video(video_path)
	else:
		print("Publicando webcam")
		publish_camera()

