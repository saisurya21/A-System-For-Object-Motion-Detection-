import cv2
import time
from skimage.metrics import structural_similarity
from datetime import datetime
import beepy
import smtplib
import imghdr
import smtplib
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
# send_mail=example.jpeg
def spot_diff(frame1, frame2):

	frame1 = frame1[1]
	frame2 = frame2[1]

	g1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
	g2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

	g1 = cv2.blur(g1, (2,2))
	g2 = cv2.blur(g2, (2,2))

	(score, diff) = structural_similarity(g2, g1, full=True)

	print("Image similarity", score)

	diff = (diff * 255).astype("uint8")
	thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY_INV)[1] #replaced 100 to 50

	contors = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
	contors = [c for c in contors if cv2.contourArea(c) > 50]

	if len(contors):
		for c in contors:
		
			x,y,w,h = cv2.boundingRect(c)

			cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)	

	else:
		print("nothing stolen")
		return 0

	cv2.imshow("diff", thresh)
	cv2.imshow("win1", frame1)
	beepy.beep(sound=4)
	# send_mail=
	cv2.imwrite(f"stolens/{datetime.now().strftime('%H-%M-%S')}.jpeg", frame1)
	# cv2.imwrite(f"visitors/in/{datetime.now().strftime('%H-%M-%S')}.jpeg", frame1)
	
	ImgFileName=datetime.now().strftime('%H-%M-%S')
	img_data = open('stolens/'+ImgFileName+'.jpeg', 'rb').read()
	msg = MIMEMultipart()
	msg['Subject'] = 'Stolen Alert'
	msg['From'] = 'xxxxxxxxxxxxxxx@gmail.com.cc'
	msg['To'] = 'xxxxxxxxxx@gmail.com.cc'
	text = MIMEText("Object has been stolen. Send HELP")
	msg.attach(text)
	image = MIMEImage(img_data, name=os.path.basename('stolens/'+ImgFileName+'.jpeg'))
	msg.attach(image)
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login("xxxxxxxxxx@gmail.com", "key")
	s.sendmail("xxxxxxxxx@gmail.com", "xxxxxxxx@gmail.com", msg.as_string())
	s.quit()

	
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	return 1
# def sendEmail():
		



