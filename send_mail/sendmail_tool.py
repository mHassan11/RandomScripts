import pandas as pd
import csv
import os
from datetime import datetime
import sys
import zipfile
from string import Template
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

def get_contacts_channel():
	email_channel_list = []
	with open('result_list_email.csv', 'r', encoding = 'utf-8') as f:
		data = f.read().split('\n')
		for line in data:
			row = line.split(',')
	        # print(row)
			row = [string for string in row if string != ""]
			if(len(row)!=0):
				email_channel_list.append(row)

	return email_channel_list

def zip_file_func(channels_list, zip_path):
	with zipfile.ZipFile(zip_path, 'w') as zipMe:        
		    for file in channels_list:
		        # zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)

		        for base, dirs, files in os.walk(file):
			        for file in files:
			            fn = os.path.join(base, file)
			            zipMe.write(fn, compress_type=zipfile.ZIP_DEFLATED)
	# pass

def read_template(filename):
	with open(filename, 'r', encoding='utf-8') as template_file:
		template_file_content = template_file.read()
	return Template(template_file_content)

def send_mail(recp_email, subject, message, zip_path):
	
	# server = smtplib.SMTP(host='smtp.gmail.com', port=587)
	# server.ehlo()
	# s.starttls()
	# server.ehlo()
	
	my_email = config.email
	my_password = config.password

	# s.login(my_email, my_password)

	subject = subject
	body = message
	receiver_email = recp_email

	sender_email = my_email
	password = my_password

	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = subject
	message["Bcc"] = receiver_email  # Recommended for mass emails

	# Add body to email
	message.attach(MIMEText(body, "plain"))

	filename = zip_path
	
	with open(filename, "rb") as attachment:
	    # Add file as application/octet-stream
	    # Email client can usually download this automatically as attachment
		part = MIMEBase("application", "octet-stream")
		part.set_payload(attachment.read())

	# Encode file in ASCII characters to send by email    
	encoders.encode_base64(part)

	# Add header as key/value pair to attachment part
	part.add_header(
	    "Content-Disposition",
	    f"attachment; filename= {filename}",
	)

	# Add attachment to message and convert message to string
	message.attach(part)
	text = message.as_string()


	# Log in to server using secure context and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, text)


def main(argv):
	# print(argv[0])
	graph_dir = "./graphs/"+argv[0]
	channels = os.listdir(graph_dir)
	# print(channels)

	get_list = get_contacts_channel()
	# print(get_list)
	
	for row in get_list:
		contact_name = row[0]
		contact_email = row[1]
		channels_list = row[2:]
		
		# elements = ['%{0}%'.format(element) for element in elements]
		channels_list = [graph_dir+"/"+channels_dir for channels_dir in channels_list]

		print(contact_name, "("+contact_email+") ->", channels_list)
		
		# lista_files = ["12.csv","13.csv","14.csv"]
		path = argv[0]
		if not os.path.exists(path):
			os.makedirs(path)

		zip_path = path+"/"+contact_email+'.zip'

		zip_file_func(channels_list, zip_path)
		message_template = read_template('message.txt')
		message = message_template.substitute(PERSON_NAME=contact_name.title(), DATE=argv[0])
		subject = "Graphs for Channel(s)"

		send_mail(contact_email, subject, message, zip_path)

		# need to send file at  "zip_path" to "contact_email" whose name is "contact_name" and the message body is "message" with "subject"
if __name__ == '__main__':
	main(sys.argv[1:])