# from google.cloud import firestore, storage
# import os
# from werkzeug.utils import secure_filename
# from flask import Flask, request, jsonify, render_template, Response
# from datetime import datetime
# import cv2
# import torch
# import numpy as np
# from datetime import datetime
# import requests
# import base64
# import firebase_admin
# import time
# from firebase_admin import credentials, firestore, storage
# from dotenv import load_dotenv

# load_dotenv()


# app = Flask(__name__)

# # Set the path to your Firestore credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # Initialize Firestore
# db = firestore.Client()
# # storage_client = storage.Client()
# # bucket = storage_client.bucket("cloudpetproject1.appspot.com")  # Replace with your bucket name 


# UPLOAD_FOLDER = "uploads"
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     try:
#         if 'file' not in request.files:
#             return jsonify({"error": "No file part"}), 400

#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({"error": "No selected file"}), 400

#         # Secure filename & save locally
#         filename = secure_filename(file.filename)
#         local_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#         file.save(local_path)

#         # Upload to Firebase Storage
#         blob = bucket.blob(f"screenshots/{filename}")
#         blob.upload_from_filename(local_path)
#         blob.make_public()
#         os.remove(local_path) ### 这个后来加的
#         image_url = blob.public_url

#         # Store in Firestore with timestamp
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS
#         doc_ref = db.collection("screenshots").add({
#             "filename": filename,
#             "url": image_url,
#             "timestamp": timestamp
#         })

#         return jsonify({"message": "Image uploaded successfully!", "image_url": image_url, "timestamp": timestamp}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    

# @app.route('/get_screenshots', methods=['GET'])
# def get_screenshots():
#     try:
#         screenshots_ref = db.collection("screenshots")
#         docs = screenshots_ref.stream()
#         screenshot_list = [{"id": doc.id, **doc.to_dict()} for doc in docs]
#         return jsonify(screenshot_list), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/gallery')
# def gallery():
#     return render_template("gallery.html")





# @app.route('/add_pet_data', methods=['POST'])
# def add_pet_data():
#     try:
#         data = request.json
#         doc_ref = db.collection("pets").add(data)
#         return jsonify({"message": "Data added successfully!", "id": doc_ref[1].id}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/get_pet_data', methods=['GET'])
# def get_pet_data():
#     try:
#         pets_ref = db.collection("pets")
#         docs = pets_ref.stream()
#         pet_list = [{"id": doc.id, **doc.to_dict()} for doc in docs]
#         return jsonify(pet_list), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



# # Load YOLOv5 Model (COCO Pretrained)
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# def detect_objects(frame):
#     results = model(frame)
#     detections = results.pandas().xyxy[0]  # Get bounding box results

#     for _, row in detections.iterrows():
#         x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
#         label = f"{row['name']} {row['confidence']:.2f}"
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     return frame

# def generate_frames():
#     cap = cv2.VideoCapture(0)  # Open webcam
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         frame = detect_objects(frame)  # Detect objects
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cap.release()

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # @app.route('/stream')
# # def stream():
# #     return render_template('stream.html')

# @app.route('/coco_ssd')
# def coco_ssd():
#     return render_template("coco_ssd_test.html")




# ## noise detction part
# SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# # @app.route("/noise_alert", methods=["POST"])
# # def noise_alert():
# #     try:
# #         # Ensure request contains JSON data
# #         data = request.get_json()
# #         if not data or "noise_level" not in data:
# #             return jsonify({"error": "Invalid request, missing 'noise_level'"}), 400
        
# #         noise_level = data["noise_level"]
# #         threshold = 30  # Set your desired threshold

# #         if noise_level >= threshold:
# #             return jsonify({"message": "Loud noise detected!", "level": noise_level}), 200
# #         else:
# #             return jsonify({"message": "Noise level normal", "level": noise_level}), 200
    
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # @app.route('/noise_alert', methods=['POST'])
# # def noise_alert():
# #     try:
# #         data = request.json
# #         timestamp = data.get("timestamp")
# #         screenshot_base64 = data.get("screenshot")

# #         # Convert Base64 image to Firebase Storage URL
# #         image_filename = f"screenshots/noise_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
# #         blob = bucket.blob(image_filename)
# #         blob.upload_from_string(base64.b64decode(screenshot_base64.split(',')[1]), content_type="image/png")
# #         image_url = blob.public_url

# #         # Store screenshot event in Firestore
# #         db.collection("noise_events").add({
# #             "timestamp": timestamp,
# #             "screenshot_url": image_url
# #         })

# #         # Send Slack Alert
# #         slack_message = {
# #             "text": f"🚨 *Loud Noise Detected!*\n"
# #                     f"📅 *Timestamp:* {timestamp}\n"
# #                     f"🖼 *Screenshot:* <{image_url}|View Image>"
# #         }
# #         requests.post(SLACK_WEBHOOK_URL, json=slack_message)

# #         return jsonify({"message": "Noise event stored & Slack alert sent!", "screenshot_url": image_url}), 200

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500




# ## test for noise level threshold
# # @app.route('/noise_level', methods=['POST'])
# # def noise_level():
# #     try:
# #         data = request.json
# #         noise_value = data.get("noise_level", 0)  # Get the noise level from request

# #         print(f"Noise Level: {noise_value} dB")  # Show in terminal

# #         return jsonify({"message": "Received!", "noise_level": noise_value}), 200

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500





# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")  # 🔹 REPLACE with your Firestore key file
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})
# bucket = storage.bucket()

# # Capture Screenshot from Webcam
# def capture_screenshot():
#     cap = cv2.VideoCapture(0)  # Open webcam
#     ret, frame = cap.read()  # Capture frame
#     cap.release()
    
#     if ret:
#         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f"screenshot_{timestamp}.jpg"
#         cv2.imwrite(filename, frame)  # Save screenshot
        
#         return filename, timestamp
#     return None, None

# # Upload Screenshot to Firestore Storage
# def upload_to_firestore(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     image_url = blob.public_url  # Get the URL

#     # Save metadata to Firestore
#     doc_ref = db.collection("noise_alerts").document(timestamp)
#     doc_ref.set({"timestamp": timestamp, "image_url": image_url})

#     return image_url

# # Send Alert to Slack
# def send_slack_alert(noise_level, image_url):
#     message = {
#         "text": f"🚨 Loud Noise Detected! 🚨\nNoise Level: {noise_level} dB\nScreenshot: {image_url}"
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# # Test Firestore - Writing test data
# doc_ref = db.collection("test").document("test_doc")
# doc_ref.set({"message": "Firestore is working!"})
# print("✅ Firestore test data written!")

# # Test Storage - Upload a sample text file
# blob = bucket.blob("test_upload.txt")
# blob.upload_from_string("Firebase Storage is working!", content_type="text/plain")
# print("✅ Storage test file uploaded!")





# last_alert_time = 0  # Store the last alert timestamp

# # Noise Detection API
# @app.route('/noise_alert', methods=['POST'])
# def noise_alert():
#     global last_alert_time
#     current_time = time.time()

#     client_ip = request.remote_addr  # Get IP of the requester
#     print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Request from {client_ip}")

#     if current_time - last_alert_time < 10:
#         print("⚠️ Noise alert ignored due to cooldown!")
#         return jsonify({"status": "ignored", "message": "Cooldown active"}), 429

#     last_alert_time = current_time
#     print("✅ Noise alert processed")
#     return jsonify({"status": "success"}), 200    

#     # # If last alert was sent less than 10 seconds ago, ignore
#     # if current_time - last_alert_time < 10:
#     #     return jsonify({"status": "ignored", "message": "Cooldown active"}), 429

#     # last_alert_time = current_time
#     # print(f"Noise alert sent at {time.strftime('%Y-%m-%d %H:%M:%S')}")
#     # return jsonify({"status": "success"}), 200
#     # print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Noise alert triggered")
#     # return jsonify({"status": "success"}), 200
#     # try:
#     #     data = request.json
#     #     noise_level = data.get("noise_level", 0)

#     #     if noise_level >= 30:  # If noise is too loud
#     #         filename, timestamp = capture_screenshot()
#     #         if filename:
#     #             image_url = upload_to_firestore(filename, timestamp)  # Upload to Firebase
#     #             send_slack_alert(noise_level, image_url)  # Notify Slack
                
#     #             return jsonify({"message": "Loud noise detected!", "screenshot_url": image_url}), 200
#     #     return jsonify({"message": "Noise level OK"}), 200

#     # except Exception as e:
#     #     return jsonify({"error": str(e)}), 500

# # Webpage Route
# @app.route('/')
# def home():
#     return render_template('index.html')


# @app.before_request
# def block_teamviewer():
#     if "TeamViewer" in request.user_agent.string:
#         return jsonify({"error": "Blocked"}), 403





# if __name__ == '__main__':
#     app.run(debug=True)











# from google.cloud import firestore, storage
# import os
# from werkzeug.utils import secure_filename
# from flask import Flask, request, jsonify, render_template, Response
# from datetime import datetime
# import cv2
# import torch
# import numpy as np
# import requests
# import time
# import firebase_admin
# from firebase_admin import credentials, firestore, storage

# app = Flask(__name__)

# # 🔹 SET FIREBASE CREDENTIALS
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")  # Replace with your key file
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Initialize Firestore & Firebase Storage
# db = firestore.Client()
# bucket = storage.bucket()

# # 🔹 Uploads Folder
# UPLOAD_FOLDER = "uploads"
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # 🔹 SLACK WEBHOOK (For Alerts)
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"


# # ===========================
# # 📌 UPLOAD IMAGE FUNCTION
# # ===========================
# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     try:
#         if 'file' not in request.files:
#             return jsonify({"error": "No file part"}), 400

#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({"error": "No selected file"}), 400

#         # Secure filename & save locally
#         filename = secure_filename(file.filename)
#         local_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#         file.save(local_path)

#         # Upload to Firebase Storage
#         blob = bucket.blob(f"screenshots/{filename}")
#         blob.upload_from_filename(local_path)
#         blob.make_public()
#         image_url = blob.public_url

#         # Store in Firestore with timestamp
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         db.collection("screenshots").add({
#             "filename": filename,
#             "url": image_url,
#             "timestamp": timestamp
#         })

#         return jsonify({"message": "Image uploaded successfully!", "image_url": image_url, "timestamp": timestamp}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # ===========================
# # 📌 FETCH SCREENSHOTS
# # ===========================
# @app.route('/get_screenshots', methods=['GET'])
# def get_screenshots():
#     try:
#         screenshots_ref = db.collection("screenshots")
#         docs = screenshots_ref.stream()
#         screenshot_list = [{"id": doc.id, **doc.to_dict()} for doc in docs]
#         return jsonify(screenshot_list), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # ===========================
# # 📌 ADD & FETCH PET DATA
# # ===========================
# @app.route('/add_pet_data', methods=['POST'])
# def add_pet_data():
#     try:
#         data = request.json
#         doc_ref = db.collection("pets").add(data)
#         return jsonify({"message": "Data added successfully!", "id": doc_ref[1].id}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/get_pet_data', methods=['GET'])
# def get_pet_data():
#     try:
#         pets_ref = db.collection("pets")
#         docs = pets_ref.stream()
#         pet_list = [{"id": doc.id, **doc.to_dict()} for doc in docs]
#         return jsonify(pet_list), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # ===========================
# # 📌 LOAD YOLOv5 MODEL
# # ===========================
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# def detect_objects(frame):
#     results = model(frame)
#     detections = results.pandas().xyxy[0]

#     for _, row in detections.iterrows():
#         x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
#         label = f"{row['name']} {row['confidence']:.2f}"
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     return frame


# # ===========================
# # 📌 VIDEO FEED
# # ===========================
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/coco_ssd')
# def coco_ssd():
#     return render_template("coco_ssd_test.html")


# # ===========================
# # 📌 SCREENSHOT & ALERT SYSTEM
# # ===========================
# def capture_screenshot():
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     cap.release()

#     if ret:
#         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f"screenshot_{timestamp}.jpg"
#         cv2.imwrite(filename, frame)
#         return filename, timestamp
#     return None, None


# def upload_to_firestore(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     image_url = blob.public_url

#     db.collection("noise_alerts").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url


# def send_slack_alert(noise_level, image_url):
#     message = {
#         "text": f"🚨 Loud Noise Detected! 🚨\nNoise Level: {noise_level} dB\nScreenshot: {image_url}"
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# # ===========================
# # 📌 NOISE DETECTION API
# # ===========================
# last_alert_time = 0  

# @app.route('/noise_alert', methods=['POST'])
# def noise_alert():
#     global last_alert_time
#     current_time = time.time()

#     client_ip = request.remote_addr  
#     print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Request from {client_ip}")

#     if current_time - last_alert_time < 10:
#         print("⚠️ Noise alert ignored due to cooldown!")
#         return jsonify({"status": "ignored", "message": "Cooldown active"}), 429

#     last_alert_time = current_time
#     print("✅ Noise alert processed")
#     return jsonify({"status": "success"}), 200    


# # ===========================
# # 📌 HOME & BLOCK TEAMVIEWER
# # ===========================
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.before_request
# def block_teamviewer():
#     if "TeamViewer" in request.user_agent.string:
#         return jsonify({"error": "Blocked"}), 403


# # ===========================
# # 📌 RUN APP
# # ===========================
# if __name__ == '__main__':
#     app.run(debug=True)












# ### 这版是run那个app。py 可是不可以开那个browser，只要detetc到noise他是可以开webcam ss后关掉然后给slack的，但是我要做可以开着那个website的
# import cv2
# import os
# import time
# from datetime import datetime
# import requests
# from flask import Flask, request, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials, firestore, storage

# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")  # Change if needed
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# bucket = storage.bucket()

# # 🔹 Slack Webhook for Notifications
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Noise Alert Cooldown (Seconds)
# ALERT_COOLDOWN = 0  
# last_alert_time = 0  

# # ===========================
# # 📌 AUTO-SCREENSHOT FUNCTION
# # ===========================
# def capture_screenshot():
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     cap.release()

#     if ret:
#         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f"screenshot_{timestamp}.jpg"
#         cv2.imwrite(filename, frame)
#         print(f"✅ Screenshot saved: {filename}")  # 🔍 Debugging Log
#         return filename, timestamp

#     print("❌ Screenshot capture failed!")  # 🔍 Debugging Log
#     return None, None


# def upload_to_firestore(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     # Store in Firestore
#     db.collection("noise_alerts").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url


# def send_slack_alert(noise_level, image_url):
#     message = {
#         "text": f"🚨 Loud Noise Detected! 🚨\nNoise Level: {noise_level} dB\nScreenshot: {image_url}"
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# # ===========================
# # 📌 NOISE DETECTION API
# # ===========================
# @app.route('/noise_alert', methods=['POST'])
# def noise_alert():
#     global last_alert_time
#     current_time = time.time()
    
#     try:
#         data = request.json
#         noise_level = data.get("noise_level", 0)

#         # 📌 **Only process if noise > 30 dB and cooldown passed**
#         if noise_level > 0 and (current_time - last_alert_time > ALERT_COOLDOWN):
#             last_alert_time = current_time  

#             filename, timestamp = capture_screenshot()
#             if filename:
#                 image_url = upload_to_firestore(filename, timestamp)
#                 send_slack_alert(noise_level, image_url)
#                 return jsonify({"status": "success", "noise_level": noise_level, "image_url": image_url}), 200
#             else:
#                 return jsonify({"status": "error", "message": "Screenshot capture failed"}), 500

#         return jsonify({"status": "ignored", "message": "Noise below threshold or cooldown active"}), 429

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # ===========================
# # 📌 RUN APP
# # ===========================
# if __name__ == '__main__':
#     app.run(debug=True)



##thhis version is i test open website and i try take screenshot from website one.
## this version i comment out first, but it will still works as previous and above sentence, but i comment out irst and use the claude version code first
# import cv2
# import os
# import time
# import threading
# from datetime import datetime
# import requests
# from flask import Flask, request, jsonify, Response
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials, firestore, storage

# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# bucket = storage.bucket()

# # 🔹 Slack Webhook for Notifications
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Noise Alert Cooldown (Seconds)
# ALERT_COOLDOWN = 10  
# last_alert_time = 0  

# # 🔹 Latest Frame Storage
# latest_frame = None
# frame_lock = threading.Lock()

# # ===========================
# # 📌 START VIDEO CAPTURE (Runs Automatically)
# # ===========================
# def capture_video():
#     """ Continuously captures frames and updates `latest_frame`. """
#     global latest_frame
#     cap = cv2.VideoCapture(0)

#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Error: Cannot read frame from webcam.")
#             break

#         with frame_lock:
#             latest_frame = frame.copy()  # ✅ Store the latest frame

#     cap.release()

# # ✅ Start capturing frames in the background when the app starts
# threading.Thread(target=capture_video, daemon=True).start()

# # ===========================
# # 📌 AUTO-SCREENSHOT FUNCTION
# # ===========================
# def capture_screenshot():
#     """ Saves the latest frame as a screenshot. """
#     global latest_frame

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None

#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     filename = f"screenshot_{timestamp}.jpg"

#     with frame_lock:
#         cv2.imwrite(filename, latest_frame)  # ✅ Save the latest frame as a screenshot

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp


# def upload_to_firestore(filename, timestamp):
#     """ Uploads the screenshot to Firebase Storage and saves the URL to Firestore. """
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     # Store in Firestore
#     db.collection("noise_alerts").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url


# def send_slack_alert(noise_level, image_url):
#     """ Sends a Slack notification with the noise level and screenshot. """
#     message = {
#         "text": f"🚨 Loud Noise Detected! 🚨\nNoise Level: {noise_level} dB\nScreenshot: {image_url}"
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# # ===========================
# # 📌 NOISE DETECTION API (AUTO SCREENSHOT)
# # ===========================
# @app.route('/noise_alert', methods=['POST'])
# def noise_alert():
#     """ Handles noise detection and triggers a screenshot if noise is detected. """
#     global last_alert_time
#     current_time = time.time()
    
#     try:
#         data = request.json
#         noise_level = data.get("noise_level", 0)

#         # 📌 **Only process if noise > 30 dB and cooldown passed**
#         if noise_level > 30 and (current_time - last_alert_time > ALERT_COOLDOWN):
#             last_alert_time = current_time  

#             filename, timestamp = capture_screenshot()
#             if filename:
#                 image_url = upload_to_firestore(filename, timestamp)
#                 send_slack_alert(noise_level, image_url)
#                 return jsonify({"status": "success", "noise_level": noise_level, "image_url": image_url}), 200
#             else:
#                 return jsonify({"status": "error", "message": "Screenshot capture failed"}), 500

#         return jsonify({"status": "ignored", "message": "Noise below threshold or cooldown active"}), 429

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # ===========================
# # 📌 LIVE VIDEO STREAMING
# # ===========================
# @app.route('/')
# def index():
#     """ Main page - starts the webcam automatically. """
#     return "✅ Webcam is running. Visit <a href='/video_feed'>Live Stream</a>."

# @app.route('/video_feed')
# def video_feed():
#     """ Streams the video feed. """
#     def generate_frames():
#         while True:
#             with frame_lock:
#                 if latest_frame is None:
#                     continue
#                 _, buffer = cv2.imencode('.jpg', latest_frame)
#                 frame_bytes = buffer.tobytes()
            
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# # ===========================
# # 📌 RUN APP
# # ===========================
# if __name__ == '__main__':
#     app.run(debug=True)








## 要test可不可以用website里面的frame 可是不可以，现在test回去之前
# import cv2
# import os
# import time
# from datetime import datetime
# import requests
# from flask import Flask, request, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials, firestore, storage
# from flask import Response
# import threading

# latest_frame = None
# frame_lock = threading.Lock()

# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")  # Change if needed
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# bucket = storage.bucket()

# # 🔹 Slack Webhook for Notifications
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Noise Alert Cooldown (Seconds)
# ALERT_COOLDOWN = 0  
# last_alert_time = 0  

# # ===========================
# # 📌 AUTO-SCREENSHOT FUNCTION
# # ===========================
# def capture_screenshot():
#     global latest_frame
#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None

#     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     with frame_lock:
#         cv2.imwrite(filename, latest_frame)  # ✅ Save the latest frame as a screenshot

#     print(f"✅ Screenshot saved as {filename}")
#     return filename


# # def capture_screenshot():
# #     cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
# #     ret, frame = cap.read()
# #     cap.release()

# #     if ret:
# #         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# #         filename = f"screenshot_{timestamp}.jpg"
# #         cv2.imwrite(filename, frame)
# #         print(f"✅ Screenshot saved: {filename}")  # 🔍 Debugging Log
# #         return filename, timestamp

# #     print("❌ Screenshot capture failed!")  # 🔍 Debugging Log
# #     return None, None


# def upload_to_firestore(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     # Store in Firestore
#     db.collection("noise_alerts").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url


# def send_slack_alert(noise_level, image_url):
#     message = {
#         "text": f"🚨 Loud Noise Detected! 🚨\nNoise Level: {noise_level} dB\nScreenshot: {image_url}"
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# # ===========================
# # 📌 NOISE DETECTION API
# # ===========================
# @app.route('/noise_alert', methods=['POST'])
# def noise_alert():
#     global last_alert_time, latest_frame
#     current_time = time.time()
    
#     try:
#         data = request.json
#         noise_level = data.get("noise_level", 0)

#         # 📌 **Only process if noise > 30 dB and cooldown passed**
#         if noise_level > 5 and (current_time - last_alert_time > ALERT_COOLDOWN):
#             last_alert_time = current_time  

#             filename, timestamp = capture_screenshot()
#             if filename:
#                 image_url = upload_to_firestore(filename, timestamp)
#                 send_slack_alert(noise_level, image_url)
#                 return jsonify({"status": "success", "noise_level": noise_level, "image_url": image_url}), 200
#             else:
#                 return jsonify({"status": "error", "message": "Screenshot capture failed"}), 500

#         return jsonify({"status": "ignored", "message": "Noise below threshold or cooldown active"}), 429

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# def generate_frames():
#     global latest_frame  # Use the global frame
#     cap = cv2.VideoCapture(0)

#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         # Store the latest frame
#         with frame_lock:
#             latest_frame = frame.copy()

#         # Encode and yield for video streaming
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cap.release()
# # @app.route('/video_feed')
# # def video_feed():
# #     global latest_frame

# #     def generate():
# #         cap = cv2.VideoCapture(0)
# #         while True:
# #             success, frame = cap.read()
# #             if not success:
# #                 break

# #             latest_frame = frame  # ✅ Store the latest frame globally

# #             ret, buffer = cv2.imencode('.jpg', frame)
# #             frame_bytes = buffer.tobytes()
# #             yield (b'--frame\r\n'
# #                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# #         cap.release()

# #     return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')





# # ===========================
# # 📌 RUN APP
# # ===========================
# if __name__ == '__main__':
#     app.run(debug=True)





# this version is i test the manually ss and video record function, first time can do but second time cannot
# import cv2
# import os
# import time
# import threading
# from datetime import datetime
# import requests
# from flask import Flask, request, jsonify, Response, render_template
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials, firestore, storage

# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# bucket = storage.bucket()

# # 🔹 Slack Webhook for Notifications
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Latest Frame Storage
# latest_frame = None
# frame_lock = threading.Lock()
# recording = False
# video_writer = None
# video_filename = None

# # ===========================
# # 📌 START VIDEO CAPTURE (Runs Automatically)
# # ===========================
# def capture_video():
#     """ Continuously captures frames and updates `latest_frame`. """
#     global latest_frame
#     cap = cv2.VideoCapture(0)

#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Error: Cannot read frame from webcam.")
#             break

#         with frame_lock:
#             latest_frame = frame.copy()  # ✅ Store the latest frame

#     cap.release()

# # ✅ Start capturing frames in the background when the app starts
# threading.Thread(target=capture_video, daemon=True).start()

# # ===========================
# # 📌 AUTO-SCREENSHOT FUNCTION
# # ===========================
# def capture_screenshot():
#     """ Saves the latest frame as a screenshot. """
#     global latest_frame

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None

#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     filename = f"screenshot_{timestamp}.jpg"

#     with frame_lock:
#         cv2.imwrite(filename, latest_frame)  # ✅ Save the latest frame as a screenshot

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp


# def upload_to_firestore(filename, timestamp, file_type):
#     """ Uploads the file to Firebase Storage and saves the URL to Firestore. """
#     blob = bucket.blob(f"{file_type}/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     file_url = blob.public_url

#     # Store in Firestore
#     db.collection(file_type).document(timestamp).set({
#         "timestamp": timestamp,
#         "file_url": file_url
#     })

#     return file_url


# def send_slack_alert(action, file_url):
#     """ Sends a Slack notification with the action (screenshot/video) and file URL. """
#     message = {
#         "text": f"📷 {action} taken!\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nFile: {file_url}"
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# # ===========================
# # 📌 MANUAL SCREENSHOT API
# # ===========================
# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     """ Manually triggered screenshot function. """
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_to_firestore(filename, timestamp, "screenshots")
#         send_slack_alert("Screenshot", image_url)
#         return jsonify({"status": "success", "image_url": image_url}), 200
#     else:
#         return jsonify({"status": "error", "message": "Screenshot capture failed"}), 500

# # ===========================
# # 📌 MANUAL VIDEO RECORDING API
# # ===========================
# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     """ Start or stop recording manually. """
#     global recording, video_writer, video_filename

#     if not recording:
#         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"video_{timestamp}.avi"
#         fourcc = cv2.VideoWriter_fourcc(*'XVID')
#         video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))
#         recording = True
#         return jsonify({"status": "started", "video_filename": video_filename}), 200
#     else:
#         recording = False
#         video_writer.release()
#         video_writer = None
#         video_url = upload_to_firestore(video_filename, timestamp, "videos")
#         send_slack_alert("Video Recording", video_url)
#         return jsonify({"status": "stopped", "video_url": video_url}), 200

# # ===========================
# # 📌 LIVE VIDEO STREAMING
# # ===========================
# @app.route('/')
# def index():
#     """ Main page with video feed and buttons. """
#     return render_template("index.html")

# @app.route('/video_feed')
# def video_feed():
#     """ Streams the video feed. """
#     def generate_frames():
#         global recording, video_writer

#         while True:
#             with frame_lock:
#                 if latest_frame is None:
#                     continue
#                 _, buffer = cv2.imencode('.jpg', latest_frame)
#                 frame_bytes = buffer.tobytes()

#                 # 🔴 Save frames if recording is active
#                 if recording and video_writer:
#                     video_writer.write(latest_frame)

#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# # ===========================
# # 📌 RUN APP
# # ===========================
# if __name__ == '__main__':
#     app.run(debug=True)






# this version now ss and recording works, but no sound and have avi and mp4 and cannot saveto firestore
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess


# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam


# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")

#         # 🔹 Convert to MP4 with sound using ffmpeg
#         filename_avi = f"recording_{start_time}.avi"
#         filename_mp4 = f"recording_{start_time}.mp4"

#         # FFmpeg command to add system audio
#         ffmpeg_cmd = [
#             "ffmpeg", "-y", "-i", filename_avi, 
#             "-f", "dshow", "-i", "audio=Microphone (Realtek(R) Audio)",
#             "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
#             "-c:a", "aac", "-b:a", "128k", filename_mp4
#         ]

#         subprocess.run(ffmpeg_cmd)

#         print(f"✅ Converted to {filename_mp4}")

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": filename_mp4
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         filename = f"recording_{start_time}.avi"

#         fourcc = cv2.VideoWriter_fourcc(*'XVID')
#         out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

#         print(f"🔴 Video recording started! Saving to {filename}")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started",
#             "video_url": filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     blob = bucket.blob(f"videos/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     video_url = blob.public_url

#     db.collection("videos").document(filename).set({
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "video_url": video_url
#     })

#     return video_url

# def send_slack_video(video_url):
#     message = {"text": f"🎥 Video Recording Uploaded!\n🔗 {video_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     app.run(debug=True)





## claude version
# try to solve avi and mp4 and cannot saveto firestore
# now can solve save to firebase but from slack cannot see  video. code down there will try to solve using claude
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess


# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam


# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         print(f"🔴 Video recording started! Saving to {video_filename}")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage
#     try:
#         blob = bucket.blob(f"videos/{filename}")
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {"text": f"🎥 Video Recording Uploaded!\n🔗 {video_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     app.run(debug=True)



# try solving the cannot see video from slack, user need to manually downloaad the video then can see  the video, this is one of the limiattion, xianfangzheba, now do the noise detection
# now here also try the noise detection function  and noise report, and so far all is ok
# overall all can work,, down code there test for object detection
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime, timedelta
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess
# import atexit
# import sys
# import pyaudio
# import numpy as np
# import random  # For our debug logging
# from collections import defaultdict


# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam

# # Global variables for audio detection



# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/')
# def index():
#     # Start noise detection automatically for testing
#     global is_listening
#     if not is_listening:
#         setup_audio_detection()
#         is_listening = True
#         threading.Thread(target=noise_detection_loop, daemon=True).start()
#         print("🔄 Noise detection started automatically")
    
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         print(f"🔴 Video recording started! Saving to {video_filename}")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage with correct MIME type
#     try:
#         blob = bucket.blob(f"videos/{filename}")
        
#         # Set the correct MIME type for MP4
#         blob.content_type = 'video/mp4'
        
#         # Set content disposition to inline so browsers will play it
#         blob.content_disposition = 'inline'
        
#         # Upload the file
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {
#         "text": "🎥 Video Recording Uploaded!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "🎥 *Video Recording Uploaded!*"
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"<{video_url}|Click here to view or download the video>"
#                 }
#             }
#         ]
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# #noise detection
# def setup_audio_detection():
#     """Initialize the audio detection system"""
#     global audio_stream
    
#     print("🔄 Initializing audio detection system...")
#     try:
#         # Initialize PyAudio
#         p = pyaudio.PyAudio()
        
#         # Configure audio stream
#         audio_stream = p.open(
#             format=pyaudio.paInt16,
#             channels=1,
#             rate=44100,
#             input=True,
#             frames_per_buffer=1024
#         )
        
#         print("✅ Audio detection system initialized successfully")
#         return True
#     except Exception as e:
#         print(f"❌ Error initializing audio: {e}")
#         return False

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold
#             if audio_level > noise_threshold:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
                    
#                     # Prevent multiple captures by waiting
#                     time.sleep(2)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# def calculate_audio_level(data):
#     """Calculate the audio level from raw audio data"""
#     # Convert audio data to numpy array
#     audio_data = np.frombuffer(data, dtype=np.int16)
    
#     # Calculate RMS value (root mean square)
#     rms = np.sqrt(np.mean(np.square(audio_data)))
    
#     # Convert to decibels (normalized)
#     if rms > 0:
#         db = 20 * np.log10(rms)
#     else:
#         db = 0
        
#     return db

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream, last_noise_alert_time
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold and not in cooldown period
#             current_time = time.time()
#             cooldown_elapsed = True
            
#             if last_noise_alert_time is not None:
#                 elapsed_time = current_time - last_noise_alert_time
#                 cooldown_elapsed = elapsed_time > noise_cooldown_seconds
                
#             if audio_level > noise_threshold and cooldown_elapsed:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Update last alert time for cooldown
#                 last_noise_alert_time = current_time
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# @app.route('/set_cooldown', methods=['POST'])
# def set_cooldown():
#     global noise_cooldown_seconds
    
#     data = request.get_json()
#     if data and 'cooldown' in data:
#         try:
#             noise_cooldown_seconds = int(data['cooldown'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise alert cooldown set to {noise_cooldown_seconds} seconds"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid cooldown value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No cooldown value provided"
#         }), 400

# def record_noise_event(level, timestamp, image_url):
#     """Record noise event in Firestore for dashboard reporting"""
#     event_data = {
#         "timestamp": timestamp,
#         "level": float(level),
#         "image_url": image_url,
#         "date": datetime.now().strftime("%Y-%m-%d"),
#         "hour": datetime.now().hour,
#         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#         "month": datetime.now().strftime("%Y-%m")
#     }
    
#     # Add to noise_events collection
#     db.collection("noise_events").document(timestamp).set(event_data)
#     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# def send_noise_alert_to_slack(level, image_url, timestamp):
#     """Send noise alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     message = {
#         "text": f"🔊 Loud Noise Detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"Noise Event Screenshot ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Noise event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print("✅ Noise alert sent to Slack")

# @app.route('/start_noise_detection', methods=['POST'])
# def start_noise_detection():
#     global is_listening, noise_detection_thread, noise_threshold
    
#     # Get custom threshold if provided
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#         except (ValueError, TypeError):
#             pass
    
#     if not is_listening:
#         # Initialize audio if not already done
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Start detection in background thread
#         is_listening = True
#         noise_detection_thread = threading.Thread(target=noise_detection_loop)
#         noise_detection_thread.daemon = True
#         noise_detection_thread.start()
        
#         return jsonify({
#             "status": "success", 
#             "message": f"Noise detection started with threshold {noise_threshold} dB"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection already running"
#         })

# @app.route('/stop_noise_detection', methods=['POST'])
# def stop_noise_detection():
#     global is_listening
    
#     if is_listening:
#         is_listening = False
#         # Thread will exit on its own due to while loop condition
#         return jsonify({
#             "status": "success", 
#             "message": "Noise detection stopped"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection not running"
#         })

# @app.route('/set_noise_threshold', methods=['POST'])
# def set_noise_threshold():
#     global noise_threshold
    
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise threshold set to {noise_threshold} dB"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid threshold value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No threshold provided"
#         }), 400

# @app.route('/test_audio', methods=['GET'])
# def test_audio():
#     try:
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Read a sample
#         data = audio_stream.read(1024, exception_on_overflow=False)
#         level = calculate_audio_level(data)
        
#         return jsonify({
#             "status": "success",
#             "audio_level": float(level),
#             "threshold": float(noise_threshold)
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"Audio test failed: {str(e)}"
#         }), 500

# # Add this route to get noise data for the dashboard
# @app.route('/get_noise_data', methods=['GET'])
# def get_noise_data():
#     try:
#         # Get current date and time
#         now = datetime.now()
#         today = now.strftime("%Y-%m-%d")
#         current_week = now.strftime("%Y-W%U")
#         current_month = now.strftime("%Y-%m")
        
#         # Initialize data structures
#         daily_data = [0] * 24
#         weekly_data = [0] * 7
#         monthly_data = [0] * 31  # Maximum days in a month
#         recent_events = []
        
#         # Query Firestore for noise events
#         # Daily data (today's events by hour)
#         daily_query = db.collection("noise_events").where("date", "==", today)
#         daily_results = daily_query.stream()
        
#         for doc in daily_results:
#             data = doc.to_dict()
#             hour = data.get('hour', 0)
#             if 0 <= hour < 24:
#                 daily_data[hour] += 1
        
#         # Weekly data (this week's events by day)
#         # Calculate start of week (Sunday)
#         start_of_week = now - timedelta(days=now.weekday() + 1)
#         for day in range(7):
#             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             weekly_data[day] = day_count
        
#         # Monthly data (this month's events by day)
#         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
#         for day in range(1, days_in_month + 1):
#             date = f"{now.year}-{now.month:02d}-{day:02d}"
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             monthly_data[day - 1] = day_count
        
#         # Recent events (limit to 10)
#         recent_query = (db.collection("noise_events")
#                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
#                         .limit(10))
        
#         recent_docs = recent_query.stream()
#         for doc in recent_docs:
#             data = doc.to_dict()
#             # Convert timestamp string to datetime for proper sorting
#             try:
#                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
#                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             except:
#                 formatted_timestamp = data.get('timestamp', '')
                
#             recent_events.append({
#                 "timestamp": formatted_timestamp,
#                 "level": data.get('level', 0),
#                 "image_url": data.get('image_url', '')
#             })
        
#         return jsonify({
#             "status": "success",
#             "daily_data": daily_data,
#             "weekly_data": weekly_data,
#             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
#             "recent_events": recent_events
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting noise data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "daily_data": [0] * 24,
#             "weekly_data": [0] * 7,
#             "monthly_data": [0] * 31,
#             "recent_events": []
#         }), 500


# ## Object detection



# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     # Initialize audio system
#     setup_audio_detection()
    
#     # Register cleanup handler
#     atexit.register(lambda: setattr(sys.modules[__name__], 'is_listening', False))
    
#     app.run(debug=True)





















# test for object detection. overall all can works perfectly, down code test yearly, max recording, and gallery section
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime, timedelta
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess
# import atexit
# import sys
# import pyaudio
# import numpy as np
# import random  # For our debug logging
# from collections import defaultdict



# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam

# # Global variables for audio detection
# audio_stream = None
# is_listening = False
# noise_threshold = 80  # Default threshold, can be adjusted
# noise_detection_thread = None
# last_noise_alert_time = None
# noise_cooldown_seconds = 30  # Default cooldown of 10 seconds

# # Global variables for object detection
# detection_model = None
# category_index = None
# detection_enabled = False
# target_object = None  # Object that triggers monitoring (e.g., "couch")
# monitor_object = None  # Object to watch for (e.g., "cat")
# cooldown_period = 10  # Seconds between alerts for the same detection
# last_detection_time = None
# detection_threshold = 0.5  # Confidence threshold for detection
# proximity_threshold = 0.2  # How close objects need to be (as a fraction of image size)

# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/')
# def index():
#     # Start noise detection automatically for testing
#     global is_listening
#     if not is_listening:
#         setup_audio_detection()
#         is_listening = True
#         threading.Thread(target=noise_detection_loop, daemon=True).start()
#         print("🔄 Noise detection started automatically")
    
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         print(f"🔴 Video recording started! Saving to {video_filename}")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage with correct MIME type
#     try:
#         blob = bucket.blob(f"videos/{filename}")
        
#         # Set the correct MIME type for MP4
#         blob.content_type = 'video/mp4'
        
#         # Set content disposition to inline so browsers will play it
#         blob.content_disposition = 'inline'
        
#         # Upload the file
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {
#         "text": "🎥 Video Recording Uploaded!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "🎥 *Video Recording Uploaded!*"
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"<{video_url}|Click here to view or download the video>"
#                 }
#             }
#         ]
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# #noise detection
# def setup_audio_detection():
#     """Initialize the audio detection system"""
#     global audio_stream
    
#     print("🔄 Initializing audio detection system...")
#     try:
#         # Initialize PyAudio
#         p = pyaudio.PyAudio()
        
#         # Configure audio stream
#         audio_stream = p.open(
#             format=pyaudio.paInt16,
#             channels=1,
#             rate=44100,
#             input=True,
#             frames_per_buffer=1024
#         )
        
#         print("✅ Audio detection system initialized successfully")
#         return True
#     except Exception as e:
#         print(f"❌ Error initializing audio: {e}")
#         return False

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold
#             if audio_level > noise_threshold:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
                    
#                     # Prevent multiple captures by waiting
#                     time.sleep(2)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# def calculate_audio_level(data):
#     """Calculate the audio level from raw audio data"""
#     # Convert audio data to numpy array
#     audio_data = np.frombuffer(data, dtype=np.int16)
    
#     # Calculate RMS value (root mean square)
#     rms = np.sqrt(np.mean(np.square(audio_data)))
    
#     # Convert to decibels (normalized)
#     if rms > 0:
#         db = 20 * np.log10(rms)
#     else:
#         db = 0
        
#     return db

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream, last_noise_alert_time
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold and not in cooldown period
#             current_time = time.time()
#             cooldown_elapsed = True
            
#             if last_noise_alert_time is not None:
#                 elapsed_time = current_time - last_noise_alert_time
#                 cooldown_elapsed = elapsed_time > noise_cooldown_seconds
                
#             if audio_level > noise_threshold and cooldown_elapsed:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Update last alert time for cooldown
#                 last_noise_alert_time = current_time
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# @app.route('/set_cooldown', methods=['POST'])
# def set_cooldown():
#     global noise_cooldown_seconds
    
#     data = request.get_json()
#     if data and 'cooldown' in data:
#         try:
#             noise_cooldown_seconds = int(data['cooldown'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise alert cooldown set to {noise_cooldown_seconds} seconds"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid cooldown value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No cooldown value provided"
#         }), 400

# def record_noise_event(level, timestamp, image_url):
#     """Record noise event in Firestore for dashboard reporting"""
#     event_data = {
#         "timestamp": timestamp,
#         "level": float(level),
#         "image_url": image_url,
#         "date": datetime.now().strftime("%Y-%m-%d"),
#         "hour": datetime.now().hour,
#         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#         "month": datetime.now().strftime("%Y-%m")
#     }
    
#     # Add to noise_events collection
#     db.collection("noise_events").document(timestamp).set(event_data)
#     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# def send_noise_alert_to_slack(level, image_url, timestamp):
#     """Send noise alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     message = {
#         "text": f"🔊 Loud Noise Detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"Noise Event Screenshot ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Noise event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print("✅ Noise alert sent to Slack")

# @app.route('/start_noise_detection', methods=['POST'])
# def start_noise_detection():
#     global is_listening, noise_detection_thread, noise_threshold
    
#     # Get custom threshold if provided
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#         except (ValueError, TypeError):
#             pass
    
#     if not is_listening:
#         # Initialize audio if not already done
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Start detection in background thread
#         is_listening = True
#         noise_detection_thread = threading.Thread(target=noise_detection_loop)
#         noise_detection_thread.daemon = True
#         noise_detection_thread.start()
        
#         return jsonify({
#             "status": "success", 
#             "message": f"Noise detection started with threshold {noise_threshold} dB"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection already running"
#         })

# @app.route('/stop_noise_detection', methods=['POST'])
# def stop_noise_detection():
#     global is_listening
    
#     if is_listening:
#         is_listening = False
#         # Thread will exit on its own due to while loop condition
#         return jsonify({
#             "status": "success", 
#             "message": "Noise detection stopped"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection not running"
#         })

# @app.route('/set_noise_threshold', methods=['POST'])
# def set_noise_threshold():
#     global noise_threshold
    
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise threshold set to {noise_threshold} dB"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid threshold value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No threshold provided"
#         }), 400

# @app.route('/test_audio', methods=['GET'])
# def test_audio():
#     try:
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Read a sample
#         data = audio_stream.read(1024, exception_on_overflow=False)
#         level = calculate_audio_level(data)
        
#         return jsonify({
#             "status": "success",
#             "audio_level": float(level),
#             "threshold": float(noise_threshold)
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"Audio test failed: {str(e)}"
#         }), 500

# # Add this route to get noise data for the dashboard
# @app.route('/get_noise_data', methods=['GET'])
# def get_noise_data():
#     try:
#         # Get current date and time
#         now = datetime.now()
#         today = now.strftime("%Y-%m-%d")
#         current_week = now.strftime("%Y-W%U")
#         current_month = now.strftime("%Y-%m")
        
#         # Initialize data structures
#         daily_data = [0] * 24
#         weekly_data = [0] * 7
#         monthly_data = [0] * 31  # Maximum days in a month
#         recent_events = []
        
#         # Query Firestore for noise events
#         # Daily data (today's events by hour)
#         daily_query = db.collection("noise_events").where("date", "==", today)
#         daily_results = daily_query.stream()
        
#         for doc in daily_results:
#             data = doc.to_dict()
#             hour = data.get('hour', 0)
#             if 0 <= hour < 24:
#                 daily_data[hour] += 1
        
#         # Weekly data (this week's events by day)
#         # Calculate start of week (Sunday)
#         start_of_week = now - timedelta(days=now.weekday() + 1)
#         for day in range(7):
#             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             weekly_data[day] = day_count
        
#         # Monthly data (this month's events by day)
#         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
#         for day in range(1, days_in_month + 1):
#             date = f"{now.year}-{now.month:02d}-{day:02d}"
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             monthly_data[day - 1] = day_count
        
#         # Recent events (limit to 10)
#         recent_query = (db.collection("noise_events")
#                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
#                         .limit(10))
        
#         recent_docs = recent_query.stream()
#         for doc in recent_docs:
#             data = doc.to_dict()
#             # Convert timestamp string to datetime for proper sorting
#             try:
#                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
#                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             except:
#                 formatted_timestamp = data.get('timestamp', '')
                
#             recent_events.append({
#                 "timestamp": formatted_timestamp,
#                 "level": data.get('level', 0),
#                 "image_url": data.get('image_url', '')
#             })
        
#         return jsonify({
#             "status": "success",
#             "daily_data": daily_data,
#             "weekly_data": weekly_data,
#             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
#             "recent_events": recent_events
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting noise data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "daily_data": [0] * 24,
#             "weekly_data": [0] * 7,
#             "monthly_data": [0] * 31,
#             "recent_events": []
#         }), 500


# ## Object detection
# # ==========================
# # 📌 OBJECT DETECTION SCREENSHOT
# # ==========================
# @app.route('/object_detection_screenshot', methods=['POST'])
# def object_detection_screenshot():
#     data = request.get_json()
#     primary_object = data.get('primaryObject', 'object')
#     secondary_object = data.get('secondaryObject', 'location')
    
#     # Capture the screenshot
#     filename, timestamp = capture_screenshot()
    
#     if filename:
#         # Upload to Firebase
#         image_url = upload_screenshot(filename, timestamp)
        
#         # Record detection event in Firestore
#         event_data = {
#             "timestamp": timestamp,
#             "primaryObject": primary_object,
#             "secondaryObject": secondary_object,
#             "image_url": image_url,
#             "date": datetime.now().strftime("%Y-%m-%d"),
#             "hour": datetime.now().hour,
#             "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#             "month": datetime.now().strftime("%Y-%m")
#         }
        
#         # Add to detection_events collection
#         db.collection("detection_events").document(timestamp).set(event_data)
        
#         # Send to Slack
#         send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"{primary_object} near {secondary_object} detected!",
#             "image_url": image_url
#         })
    
#     return jsonify({
#         "status": "error", 
#         "message": "Failed to capture screenshot"
#     }), 500

# def send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp):
#     """Send object detection alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     emoji_map = {
#         "cat": "🐱",
#         "dog": "🐶",
#         "bird": "🐦",
#         "person": "👤",
#         "couch": "🛋️",
#         "bed": "🛏️",
#         "laptop": "💻",
#         "keyboard": "⌨️",
#         "cell phone": "📱",
#         "tv": "📺",
#         "oven": "🔥"
#     }
    
#     primary_emoji = emoji_map.get(primary_object.lower(), "📷")
#     secondary_emoji = emoji_map.get(secondary_object.lower(), "📍")
    
#     message = {
#         "text": f"{primary_emoji} {primary_object.title()} near {secondary_object} detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*{primary_emoji} {primary_object.title()} near {secondary_object} detected! {secondary_emoji}*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"{primary_object.title()} near {secondary_object} ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Detection event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print(f"✅ Object detection alert sent to Slack: {primary_object} near {secondary_object}")


# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     # Initialize audio system
#     setup_audio_detection()
    
#     # Register cleanup handler
#     atexit.register(lambda: setattr(sys.modules[__name__], 'is_listening', False))
    
#     app.run(debug=True)












# test for yearly, max recording, and gallery section
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime, timedelta
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess
# import atexit
# import sys
# import pyaudio
# import numpy as np
# import random  # For our debug logging
# from collections import defaultdict



# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam

# # Global variables for audio detection
# audio_stream = None
# is_listening = False
# noise_threshold = 80  # Default threshold, can be adjusted
# noise_detection_thread = None
# last_noise_alert_time = None
# noise_cooldown_seconds = 30  # Default cooldown of 10 seconds

# # Global variables for object detection
# detection_model = None
# category_index = None
# detection_enabled = False
# target_object = None  # Object that triggers monitoring (e.g., "couch")
# monitor_object = None  # Object to watch for (e.g., "cat")
# cooldown_period = 10  # Seconds between alerts for the same detection
# last_detection_time = None
# detection_threshold = 0.5  # Confidence threshold for detection
# proximity_threshold = 0.2  # How close objects need to be (as a fraction of image size)

# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/')
# def index():
#     # Start noise detection automatically for testing
#     global is_listening
#     if not is_listening:
#         setup_audio_detection()
#         is_listening = True
#         threading.Thread(target=noise_detection_loop, daemon=True).start()
#         print("🔄 Noise detection started automatically")
    
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# @app.route('/toggle_recording', methods=['POST'])
# # def toggle_recording():
# #     global is_recording, out, start_time, video_filename

# #     if is_recording:
# #         is_recording = False
# #         if out is not None:
# #             out.release()  # Stop video recording

# #         print("🛑 Video recording stopped!")
        
# #         # Upload to Firebase Storage
# #         video_url = upload_video(video_filename)
        
# #         # Send to Slack
# #         if video_url:
# #             send_slack_video(video_url)

# #         return jsonify({
# #             "status": "stopped",
# #             "message": "Recording stopped",
# #             "video_url": video_url if video_url else None
# #         }), 200
# #     else:
# #         is_recording = True
# #         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# #         video_filename = f"recording_{start_time}.mp4"
        
# #         # Use MP4V codec (H.264) for mp4 files
# #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
# #         # Get the camera dimensions
# #         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# #         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
# #         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

# #         print(f"🔴 Video recording started! Saving to {video_filename}")

# #         return jsonify({
# #             "status": "recording",
# #             "message": "Recording started",
# #             "video_url": video_filename
# #         }), 200

# #this test for 60 min max
# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         # Add a timer to stop recording after 60 minutes
#         def stop_after_timeout():
#             global is_recording
#             time.sleep(60 * 60)  # 60 minutes in seconds
#             if is_recording:
#                 print("🕒 Maximum recording time (60 minutes) reached. Stopping recording.")
#                 requests.post('http://localhost:5000/toggle_recording')
                
#         # Start timer in a separate thread
#         timer_thread = threading.Thread(target=stop_after_timeout)
#         timer_thread.daemon = True
#         timer_thread.start()

#         print(f"🔴 Video recording started! Saving to {video_filename} (Max 60 minutes)")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started (Max 60 minutes)",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage with correct MIME type
#     try:
#         blob = bucket.blob(f"videos/{filename}")
        
#         # Set the correct MIME type for MP4
#         blob.content_type = 'video/mp4'
        
#         # Set content disposition to inline so browsers will play it
#         blob.content_disposition = 'inline'
        
#         # Upload the file
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {
#         "text": "🎥 Video Recording Uploaded!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "🎥 *Video Recording Uploaded!*"
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"<{video_url}|Click here to view or download the video>"
#                 }
#             }
#         ]
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# #noise detection
# def setup_audio_detection():
#     """Initialize the audio detection system"""
#     global audio_stream
    
#     print("🔄 Initializing audio detection system...")
#     try:
#         # Initialize PyAudio
#         p = pyaudio.PyAudio()
        
#         # Configure audio stream
#         audio_stream = p.open(
#             format=pyaudio.paInt16,
#             channels=1,
#             rate=44100,
#             input=True,
#             frames_per_buffer=1024
#         )
        
#         print("✅ Audio detection system initialized successfully")
#         return True
#     except Exception as e:
#         print(f"❌ Error initializing audio: {e}")
#         return False

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold
#             if audio_level > noise_threshold:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
                    
#                     # Prevent multiple captures by waiting
#                     time.sleep(2)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# def calculate_audio_level(data):
#     """Calculate the audio level from raw audio data"""
#     # Convert audio data to numpy array
#     audio_data = np.frombuffer(data, dtype=np.int16)
    
#     # Calculate RMS value (root mean square)
#     rms = np.sqrt(np.mean(np.square(audio_data)))
    
#     # Convert to decibels (normalized)
#     if rms > 0:
#         db = 20 * np.log10(rms)
#     else:
#         db = 0
        
#     return db

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream, last_noise_alert_time
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold and not in cooldown period
#             current_time = time.time()
#             cooldown_elapsed = True
            
#             if last_noise_alert_time is not None:
#                 elapsed_time = current_time - last_noise_alert_time
#                 cooldown_elapsed = elapsed_time > noise_cooldown_seconds
                
#             if audio_level > noise_threshold and cooldown_elapsed:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Update last alert time for cooldown
#                 last_noise_alert_time = current_time
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# @app.route('/set_cooldown', methods=['POST'])
# def set_cooldown():
#     global noise_cooldown_seconds
    
#     data = request.get_json()
#     if data and 'cooldown' in data:
#         try:
#             noise_cooldown_seconds = int(data['cooldown'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise alert cooldown set to {noise_cooldown_seconds} seconds"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid cooldown value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No cooldown value provided"
#         }), 400

# # def record_noise_event(level, timestamp, image_url):
# #     """Record noise event in Firestore for dashboard reporting"""
# #     event_data = {
# #         "timestamp": timestamp,
# #         "level": float(level),
# #         "image_url": image_url,
# #         "date": datetime.now().strftime("%Y-%m-%d"),
# #         "hour": datetime.now().hour,
# #         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
# #         "month": datetime.now().strftime("%Y-%m")
# #     }
    
# #     # Add to noise_events collection
# #     db.collection("noise_events").document(timestamp).set(event_data)
# #     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# # testing to add yearly
# def record_noise_event(level, timestamp, image_url):
#     """Record noise event in Firestore for dashboard reporting"""
#     event_data = {
#         "timestamp": timestamp,
#         "level": float(level),
#         "image_url": image_url,
#         "date": datetime.now().strftime("%Y-%m-%d"),
#         "hour": datetime.now().hour,
#         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#         "month": datetime.now().strftime("%Y-%m"),
#         "year": datetime.now().strftime("%Y")  # Add year
#     }
    
#     # Add to noise_events collection
#     db.collection("noise_events").document(timestamp).set(event_data)
#     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# #add a new endpoint to get yearly data
# @app.route('/get_yearly_data', methods=['GET'])
# def get_yearly_data():
#     try:
#         # Get current year
#         now = datetime.now()
#         current_year = now.strftime("%Y")
        
#         # Initialize yearly data (monthly counts for the current year)
#         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         yearly_data = [0] * 12
        
#         # Query for each month in the current year
#         for month_idx in range(12):
#             month_num = month_idx + 1
#             month_query = db.collection("noise_events").where(
#                 "month", "==", f"{current_year}-{month_num:02d}")
#             month_count = len(list(month_query.stream()))
#             yearly_data[month_idx] = month_count
        
#         return jsonify({
#             "status": "success",
#             "yearly_data": yearly_data,
#             "months": months
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting yearly data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "yearly_data": [0] * 12,
#             "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         }), 500

# def send_noise_alert_to_slack(level, image_url, timestamp):
#     """Send noise alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     message = {
#         "text": f"🔊 Loud Noise Detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"Noise Event Screenshot ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Noise event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print("✅ Noise alert sent to Slack")

# @app.route('/start_noise_detection', methods=['POST'])
# def start_noise_detection():
#     global is_listening, noise_detection_thread, noise_threshold
    
#     # Get custom threshold if provided
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#         except (ValueError, TypeError):
#             pass
    
#     if not is_listening:
#         # Initialize audio if not already done
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Start detection in background thread
#         is_listening = True
#         noise_detection_thread = threading.Thread(target=noise_detection_loop)
#         noise_detection_thread.daemon = True
#         noise_detection_thread.start()
        
#         return jsonify({
#             "status": "success", 
#             "message": f"Noise detection started with threshold {noise_threshold} dB"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection already running"
#         })

# @app.route('/stop_noise_detection', methods=['POST'])
# def stop_noise_detection():
#     global is_listening
    
#     if is_listening:
#         is_listening = False
#         # Thread will exit on its own due to while loop condition
#         return jsonify({
#             "status": "success", 
#             "message": "Noise detection stopped"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection not running"
#         })

# @app.route('/set_noise_threshold', methods=['POST'])
# def set_noise_threshold():
#     global noise_threshold
    
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise threshold set to {noise_threshold} dB"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid threshold value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No threshold provided"
#         }), 400

# @app.route('/test_audio', methods=['GET'])
# def test_audio():
#     try:
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Read a sample
#         data = audio_stream.read(1024, exception_on_overflow=False)
#         level = calculate_audio_level(data)
        
#         return jsonify({
#             "status": "success",
#             "audio_level": float(level),
#             "threshold": float(noise_threshold)
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"Audio test failed: {str(e)}"
#         }), 500

# # Add this route to get noise data for the dashboard
# @app.route('/get_noise_data', methods=['GET'])
# # def get_noise_data():
# #     try:
# #         # Get current date and time
# #         now = datetime.now()
# #         today = now.strftime("%Y-%m-%d")
# #         current_week = now.strftime("%Y-W%U")
# #         current_month = now.strftime("%Y-%m")
        
# #         # Initialize data structures
# #         daily_data = [0] * 24
# #         weekly_data = [0] * 7
# #         monthly_data = [0] * 31  # Maximum days in a month
# #         recent_events = []
        
# #         # Query Firestore for noise events
# #         # Daily data (today's events by hour)
# #         daily_query = db.collection("noise_events").where("date", "==", today)
# #         daily_results = daily_query.stream()
        
# #         for doc in daily_results:
# #             data = doc.to_dict()
# #             hour = data.get('hour', 0)
# #             if 0 <= hour < 24:
# #                 daily_data[hour] += 1
        
# #         # Weekly data (this week's events by day)
# #         # Calculate start of week (Sunday)
# #         start_of_week = now - timedelta(days=now.weekday() + 1)
# #         for day in range(7):
# #             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
# #             day_query = db.collection("noise_events").where("date", "==", date)
# #             day_count = len(list(day_query.stream()))
# #             weekly_data[day] = day_count
        
# #         # Monthly data (this month's events by day)
# #         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
# #         for day in range(1, days_in_month + 1):
# #             date = f"{now.year}-{now.month:02d}-{day:02d}"
# #             day_query = db.collection("noise_events").where("date", "==", date)
# #             day_count = len(list(day_query.stream()))
# #             monthly_data[day - 1] = day_count
        
# #         # Recent events (limit to 10)
# #         recent_query = (db.collection("noise_events")
# #                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
# #                         .limit(10))
        
# #         recent_docs = recent_query.stream()
# #         for doc in recent_docs:
# #             data = doc.to_dict()
# #             # Convert timestamp string to datetime for proper sorting
# #             try:
# #                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
# #                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
# #             except:
# #                 formatted_timestamp = data.get('timestamp', '')
                
# #             recent_events.append({
# #                 "timestamp": formatted_timestamp,
# #                 "level": data.get('level', 0),
# #                 "image_url": data.get('image_url', '')
# #             })
        
# #         return jsonify({
# #             "status": "success",
# #             "daily_data": daily_data,
# #             "weekly_data": weekly_data,
# #             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
# #             "recent_events": recent_events
# #         })
    
# #     except Exception as e:
# #         print(f"❌ Error getting noise data: {e}")
# #         return jsonify({
# #             "status": "error",
# #             "message": str(e),
# #             "daily_data": [0] * 24,
# #             "weekly_data": [0] * 7,
# #             "monthly_data": [0] * 31,
# #             "recent_events": []
# #         }), 500

# # add the year data
# @app.route('/get_noise_data', methods=['GET'])
# def get_noise_data():
#     try:
#         # Get current date and time
#         now = datetime.now()
#         today = now.strftime("%Y-%m-%d")
#         current_week = now.strftime("%Y-W%U")
#         current_month = now.strftime("%Y-%m")
#         current_year = now.strftime("%Y")
        
#         # Initialize data structures
#         daily_data = [0] * 24
#         weekly_data = [0] * 7
#         monthly_data = [0] * 31  # Maximum days in a month
#         yearly_data = [0] * 12   # 12 months in a year
#         recent_events = []
        
#         # Query Firestore for noise events
#         # Daily data (today's events by hour)
#         daily_query = db.collection("noise_events").where("date", "==", today)
#         daily_results = daily_query.stream()
        
#         for doc in daily_results:
#             data = doc.to_dict()
#             hour = data.get('hour', 0)
#             if 0 <= hour < 24:
#                 daily_data[hour] += 1
        
#         # Weekly data (this week's events by day)
#         # Calculate start of week (Sunday)
#         start_of_week = now - timedelta(days=now.weekday() + 1)
#         for day in range(7):
#             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             weekly_data[day] = day_count
        
#         # Monthly data (this month's events by day)
#         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
#         for day in range(1, days_in_month + 1):
#             date = f"{now.year}-{now.month:02d}-{day:02d}"
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             monthly_data[day - 1] = day_count
            
#         # Yearly data (this year's events by month)
#         for month in range(1, 13):
#             month_prefix = f"{current_year}-{month:02d}"
#             month_query = db.collection("noise_events").where("month", ">=", month_prefix).where("month", "<", f"{current_year}-{month+1:02d}")
#             month_count = len(list(month_query.stream()))
#             yearly_data[month - 1] = month_count
        
#         # Recent events (limit to 10)
#         recent_query = (db.collection("noise_events")
#                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
#                         .limit(10))
        
#         recent_docs = recent_query.stream()
#         for doc in recent_docs:
#             data = doc.to_dict()
#             # Convert timestamp string to datetime for proper sorting
#             try:
#                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
#                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             except:
#                 formatted_timestamp = data.get('timestamp', '')
                
#             recent_events.append({
#                 "timestamp": formatted_timestamp,
#                 "level": data.get('level', 0),
#                 "image_url": data.get('image_url', '')
#             })
        
#         return jsonify({
#             "status": "success",
#             "daily_data": daily_data,
#             "weekly_data": weekly_data,
#             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
#             "yearly_data": yearly_data,  # Add yearly data
#             "recent_events": recent_events
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting noise data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "daily_data": [0] * 24,
#             "weekly_data": [0] * 7,
#             "monthly_data": [0] * 31,
#             "yearly_data": [0] * 12,  # Add yearly data
#             "recent_events": []
#         }), 500

# ## Object detection
# # ==========================
# # 📌 OBJECT DETECTION SCREENSHOT
# # ==========================
# @app.route('/object_detection_screenshot', methods=['POST'])
# def object_detection_screenshot():
#     data = request.get_json()
#     primary_object = data.get('primaryObject', 'object')
#     secondary_object = data.get('secondaryObject', 'location')
    
#     # Capture the screenshot
#     filename, timestamp = capture_screenshot()
    
#     if filename:
#         # Upload to Firebase
#         image_url = upload_screenshot(filename, timestamp)
        
#         # Record detection event in Firestore
#         event_data = {
#             "timestamp": timestamp,
#             "primaryObject": primary_object,
#             "secondaryObject": secondary_object,
#             "image_url": image_url,
#             "date": datetime.now().strftime("%Y-%m-%d"),
#             "hour": datetime.now().hour,
#             "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#             "month": datetime.now().strftime("%Y-%m")
#         }
        
#         # Add to detection_events collection
#         db.collection("detection_events").document(timestamp).set(event_data)
        
#         # Send to Slack
#         send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"{primary_object} near {secondary_object} detected!",
#             "image_url": image_url
#         })
    
#     return jsonify({
#         "status": "error", 
#         "message": "Failed to capture screenshot"
#     }), 500

# def send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp):
#     """Send object detection alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     emoji_map = {
#         "cat": "🐱",
#         "dog": "🐶",
#         "bird": "🐦",
#         "person": "👤",
#         "couch": "🛋️",
#         "bed": "🛏️",
#         "laptop": "💻",
#         "keyboard": "⌨️",
#         "cell phone": "📱",
#         "tv": "📺",
#         "oven": "🔥"
#     }
    
#     primary_emoji = emoji_map.get(primary_object.lower(), "📷")
#     secondary_emoji = emoji_map.get(secondary_object.lower(), "📍")
    
#     message = {
#         "text": f"{primary_emoji} {primary_object.title()} near {secondary_object} detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*{primary_emoji} {primary_object.title()} near {secondary_object} detected! {secondary_emoji}*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"{primary_object.title()} near {secondary_object} ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Detection event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print(f"✅ Object detection alert sent to Slack: {primary_object} near {secondary_object}")


# # ==========================
# # 📌 Backend API for Gallery
# # ==========================
# @app.route('/get_screenshots', methods=['GET'])
# def get_screenshots():
#     try:
#         # Get manual screenshots
#         manual_screenshots = []
#         screenshots_ref = db.collection("screenshots").limit(50).stream()
#         for doc in screenshots_ref:
#             data = doc.to_dict()
#             if "noise_detection" not in data:  # Only manual screenshots
#                 manual_screenshots.append(data)
        
#         # Get noise detection screenshots
#         noise_screenshots = []
#         noise_ref = db.collection("noise_events").limit(50).stream()
#         for doc in noise_ref:
#             data = doc.to_dict()
#             noise_screenshots.append(data)
        
#         # Get object detection screenshots (if implemented)
#         object_screenshots = []
#         # Placeholder for object detection 
        
#         # Get video recordings
#         videos = []
#         videos_ref = db.collection("videos").limit(20).stream()
#         for doc in videos_ref:
#             data = doc.to_dict()
#             videos.append(data)
            
#         return jsonify({
#             "status": "success",
#             "manual_screenshots": manual_screenshots,
#             "noise_screenshots": noise_screenshots,
#             "object_screenshots": object_screenshots,
#             "videos": videos
#         })
    
#     except Exception as e:
#         print(f"❌ Error fetching gallery data: {e}")
#         return jsonify({
#             "status": "error", 
#             "message": str(e),
#             "manual_screenshots": [],
#             "noise_screenshots": [],
#             "object_screenshots": [],
#             "videos": []
#         }), 500

# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     # Initialize audio system
#     setup_audio_detection()
    
#     # Register cleanup handler
#     atexit.register(lambda: setattr(sys.modules[__name__], 'is_listening', False))
    
#     app.run(debug=True)














# a copy version of code above to test cline, but cline mcm not free so i use this code whihc is same as above to modify some bug that oocurs.
# i will use this code to ask claude pro
#now object detection have problem and noise detection are now set to 0db but also cannot doo, now fixing this
# now object detection and noise detection cannot work, noise cannot detect and allways 0db, object detection shows error, and gallllery section is the current time not the time that previouslly taken
# i will copy the above code again and put after this code and try to redo again because code above i think no this issue.
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime, timedelta
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess
# import atexit
# import sys
# import pyaudio
# import numpy as np
# import random  # For our debug logging
# from collections import defaultdict



# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam

# # Global variables for audio detection
# audio_stream = None
# is_listening = False
# noise_threshold = 80  # Default threshold, can be adjusted
# noise_detection_thread = None
# last_noise_alert_time = None
# noise_cooldown_seconds = 30  # Default cooldown of 10 seconds

# # Global variables for object detection
# detection_model = None
# category_index = None
# detection_enabled = False
# target_object = None  # Object that triggers monitoring (e.g., "couch")
# monitor_object = None  # Object to watch for (e.g., "cat")
# cooldown_period = 10  # Seconds between alerts for the same detection
# last_detection_time = None
# detection_threshold = 0.5  # Confidence threshold for detection
# proximity_threshold = 0.2  # How close objects need to be (as a fraction of image size)

# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/')
# def index():
#     # Start noise detection automatically for testing
#     global is_listening
#     if not is_listening:
#         setup_audio_detection()
#         is_listening = True
#         threading.Thread(target=noise_detection_loop, daemon=True).start()
#         print("🔄 Noise detection started automatically")
    
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# @app.route('/toggle_recording', methods=['POST'])
# # def toggle_recording():
# #     global is_recording, out, start_time, video_filename

# #     if is_recording:
# #         is_recording = False
# #         if out is not None:
# #             out.release()  # Stop video recording

# #         print("🛑 Video recording stopped!")
        
# #         # Upload to Firebase Storage
# #         video_url = upload_video(video_filename)
        
# #         # Send to Slack
# #         if video_url:
# #             send_slack_video(video_url)

# #         return jsonify({
# #             "status": "stopped",
# #             "message": "Recording stopped",
# #             "video_url": video_url if video_url else None
# #         }), 200
# #     else:
# #         is_recording = True
# #         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# #         video_filename = f"recording_{start_time}.mp4"
        
# #         # Use MP4V codec (H.264) for mp4 files
# #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
# #         # Get the camera dimensions
# #         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# #         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
# #         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

# #         print(f"🔴 Video recording started! Saving to {video_filename}")

# #         return jsonify({
# #             "status": "recording",
# #             "message": "Recording started",
# #             "video_url": video_filename
# #         }), 200

# #this test for 60 min max
# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         # Add a timer to stop recording after 60 minutes
#         def stop_after_timeout():
#             global is_recording
#             time.sleep(60 * 60)  # 60 minutes in seconds
#             if is_recording:
#                 print("🕒 Maximum recording time (60 minutes) reached. Stopping recording.")
#                 requests.post('http://localhost:5000/toggle_recording')
                
#         # Start timer in a separate thread
#         timer_thread = threading.Thread(target=stop_after_timeout)
#         timer_thread.daemon = True
#         timer_thread.start()

#         print(f"🔴 Video recording started! Saving to {video_filename} (Max 60 minutes)")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started (Max 60 minutes)",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage with correct MIME type
#     try:
#         blob = bucket.blob(f"videos/{filename}")
        
#         # Set the correct MIME type for MP4
#         blob.content_type = 'video/mp4'
        
#         # Set content disposition to inline so browsers will play it
#         blob.content_disposition = 'inline'
        
#         # Upload the file
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {
#         "text": "🎥 Video Recording Uploaded!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "🎥 *Video Recording Uploaded!*"
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"<{video_url}|Click here to view or download the video>"
#                 }
#             }
#         ]
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# #noise detection
# def setup_audio_detection():
#     """Initialize the audio detection system"""
#     global audio_stream
    
#     print("🔄 Initializing audio detection system...")
#     try:
#         # Initialize PyAudio
#         p = pyaudio.PyAudio()
        
#         # Configure audio stream
#         audio_stream = p.open(
#             format=pyaudio.paInt16,
#             channels=1,
#             rate=44100,
#             input=True,
#             frames_per_buffer=1024
#         )
        
#         print("✅ Audio detection system initialized successfully")
#         return True
#     except Exception as e:
#         print(f"❌ Error initializing audio: {e}")
#         return False

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold
#             if audio_level > noise_threshold:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
                    
#                     # Prevent multiple captures by waiting
#                     time.sleep(2)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# def calculate_audio_level(data):
#     """Calculate the audio level from raw audio data"""
#     # Convert audio data to numpy array
#     audio_data = np.frombuffer(data, dtype=np.int16)
    
#     # Calculate RMS value (root mean square)
#     rms = np.sqrt(np.mean(np.square(audio_data)))
    
#     # Convert to decibels (normalized)
#     if rms > 0:
#         db = 20 * np.log10(rms)
#     else:
#         db = 0
        
#     return db

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream, last_noise_alert_time
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold and not in cooldown period
#             current_time = time.time()
#             cooldown_elapsed = True
            
#             if last_noise_alert_time is not None:
#                 elapsed_time = current_time - last_noise_alert_time
#                 cooldown_elapsed = elapsed_time > noise_cooldown_seconds
                
#             if audio_level > noise_threshold and cooldown_elapsed:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Update last alert time for cooldown
#                 last_noise_alert_time = current_time
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# @app.route('/set_cooldown', methods=['POST'])
# def set_cooldown():
#     global noise_cooldown_seconds
    
#     data = request.get_json()
#     if data and 'cooldown' in data:
#         try:
#             noise_cooldown_seconds = int(data['cooldown'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise alert cooldown set to {noise_cooldown_seconds} seconds"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid cooldown value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No cooldown value provided"
#         }), 400

# # def record_noise_event(level, timestamp, image_url):
# #     """Record noise event in Firestore for dashboard reporting"""
# #     event_data = {
# #         "timestamp": timestamp,
# #         "level": float(level),
# #         "image_url": image_url,
# #         "date": datetime.now().strftime("%Y-%m-%d"),
# #         "hour": datetime.now().hour,
# #         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
# #         "month": datetime.now().strftime("%Y-%m")
# #     }
    
# #     # Add to noise_events collection
# #     db.collection("noise_events").document(timestamp).set(event_data)
# #     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# # testing to add yearly
# def record_noise_event(level, timestamp, image_url):
#     """Record noise event in Firestore for dashboard reporting"""
#     event_data = {
#         "timestamp": timestamp,
#         "level": float(level),
#         "image_url": image_url,
#         "date": datetime.now().strftime("%Y-%m-%d"),
#         "hour": datetime.now().hour,
#         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#         "month": datetime.now().strftime("%Y-%m"),
#         "year": datetime.now().strftime("%Y")  # Add year
#     }
    
#     # Add to noise_events collection
#     db.collection("noise_events").document(timestamp).set(event_data)
#     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# #add a new endpoint to get yearly data
# @app.route('/get_yearly_data', methods=['GET'])
# def get_yearly_data():
#     try:
#         # Get current year
#         now = datetime.now()
#         current_year = now.strftime("%Y")
        
#         # Initialize yearly data (monthly counts for the current year)
#         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         yearly_data = [0] * 12
        
#         # Query for each month in the current year
#         for month_idx in range(12):
#             month_num = month_idx + 1
#             month_query = db.collection("noise_events").where(
#                 "month", "==", f"{current_year}-{month_num:02d}")
#             month_count = len(list(month_query.stream()))
#             yearly_data[month_idx] = month_count
        
#         return jsonify({
#             "status": "success",
#             "yearly_data": yearly_data,
#             "months": months
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting yearly data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "yearly_data": [0] * 12,
#             "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         }), 500

# def send_noise_alert_to_slack(level, image_url, timestamp):
#     """Send noise alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     message = {
#         "text": f"🔊 Loud Noise Detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"Noise Event Screenshot ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Noise event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print("✅ Noise alert sent to Slack")

# @app.route('/start_noise_detection', methods=['POST'])
# def start_noise_detection():
#     global is_listening, noise_detection_thread, noise_threshold
    
#     # Get custom threshold if provided
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#         except (ValueError, TypeError):
#             pass
    
#     if not is_listening:
#         # Initialize audio if not already done
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Start detection in background thread
#         is_listening = True
#         noise_detection_thread = threading.Thread(target=noise_detection_loop)
#         noise_detection_thread.daemon = True
#         noise_detection_thread.start()
        
#         return jsonify({
#             "status": "success", 
#             "message": f"Noise detection started with threshold {noise_threshold} dB"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection already running"
#         })

# @app.route('/stop_noise_detection', methods=['POST'])
# def stop_noise_detection():
#     global is_listening
    
#     if is_listening:
#         is_listening = False
#         # Thread will exit on its own due to while loop condition
#         return jsonify({
#             "status": "success", 
#             "message": "Noise detection stopped"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection not running"
#         })

# @app.route('/set_noise_threshold', methods=['POST'])
# def set_noise_threshold():
#     global noise_threshold
    
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise threshold set to {noise_threshold} dB"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid threshold value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No threshold provided"
#         }), 400

# @app.route('/test_audio', methods=['GET'])
# def test_audio():
#     try:
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Read multiple samples to get a more accurate reading
#         samples = []
#         for _ in range(5):
#             data = audio_stream.read(1024, exception_on_overflow=False)
#             samples.append(calculate_audio_level(data))
        
#         # Take the maximum level
#         level = max(samples)
        
#         return jsonify({
#             "status": "success",
#             "audio_level": float(level),
#             "threshold": float(noise_threshold)
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"Audio test failed: {str(e)}"
#         }), 500


# # Add this route to get noise data for the dashboard
# # add the year data
# # Add this at line 650 or so, after the get_noise_data route declaration
# @app.route('/get_noise_data', methods=['GET'])
# def get_noise_data():
#     try:
#         # Get current date and time
#         now = datetime.now()
#         today = now.strftime("%Y-%m-%d")
#         current_week = now.strftime("%Y-W%U")
#         current_month = now.strftime("%Y-%m")
#         current_year = now.strftime("%Y")
        
#         # Initialize data structures
#         daily_data = [0] * 24
#         weekly_data = [0] * 7
#         monthly_data = [0] * 31  # Maximum days in a month
#         yearly_data = [0] * 12   # 12 months in a year
#         recent_events = []
        
#         # Query Firestore for noise events
#         # Daily data (today's events by hour)
#         daily_query = db.collection("noise_events").where("date", "==", today)
#         daily_results = list(daily_query.stream())
        
#         for doc in daily_results:
#             data = doc.to_dict()
#             hour = data.get('hour', 0)
#             if 0 <= hour < 24:
#                 daily_data[hour] += 1
        
#         # Weekly data (this week's events by day)
#         # Calculate start of week (Sunday)
#         start_of_week = now - timedelta(days=now.weekday() + 1)
#         for day in range(7):
#             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             weekly_data[day] = day_count
        
#         # Monthly data (this month's events by day)
#         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
#         for day in range(1, days_in_month + 1):
#             day_str = f"{day:02d}"
#             month_str = f"{now.month:02d}"
#             date = f"{now.year}-{month_str}-{day_str}"
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             monthly_data[day - 1] = day_count
            
#         # Yearly data (this year's events by month)
#         for month in range(1, 13):
#             month_prefix = f"{current_year}-{month:02d}"
#             month_query = db.collection("noise_events").where(
#                 "month", "==", month_prefix)
#             month_count = len(list(month_query.stream()))
#             yearly_data[month - 1] = month_count
        
#         # Recent events (limit to 10)
#         recent_query = (db.collection("noise_events")
#                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
#                         .limit(10))
        
#         recent_docs = list(recent_query.stream())
#         for doc in recent_docs:
#             data = doc.to_dict()
#             # Convert timestamp string to datetime for proper sorting
#             try:
#                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
#                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             except:
#                 formatted_timestamp = data.get('timestamp', '')
                
#             recent_events.append({
#                 "timestamp": data.get('timestamp', ''),
#                 "level": data.get('level', 0),
#                 "image_url": data.get('image_url', '')
#             })
        
#         return jsonify({
#             "status": "success",
#             "daily_data": daily_data,
#             "weekly_data": weekly_data,
#             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
#             "yearly_data": yearly_data,
#             "recent_events": recent_events
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting noise data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "daily_data": [0] * 24,
#             "weekly_data": [0] * 7,
#             "monthly_data": [0] * 31,
#             "yearly_data": [0] * 12,
#             "recent_events": []
#         }), 500

# ## Object detection
# # ==========================
# # 📌 OBJECT DETECTION SCREENSHOT
# # ==========================
# @app.route('/object_detection_screenshot', methods=['POST'])
# def object_detection_screenshot():
#     data = request.get_json()
#     primary_object = data.get('primaryObject', 'object')
#     secondary_object = data.get('secondaryObject', 'location')
    
#     # Capture the screenshot
#     filename, timestamp = capture_screenshot()
    
#     if filename:
#         # Upload to Firebase
#         image_url = upload_screenshot(filename, timestamp)
        
#         # Record detection event in Firestore
#         event_data = {
#             "timestamp": timestamp,
#             "primaryObject": primary_object,
#             "secondaryObject": secondary_object,
#             "image_url": image_url,
#             "date": datetime.now().strftime("%Y-%m-%d"),
#             "hour": datetime.now().hour,
#             "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#             "month": datetime.now().strftime("%Y-%m")
#         }
        
#         # Add to detection_events collection
#         db.collection("detection_events").document(timestamp).set(event_data)
        
#         # Send to Slack
#         send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"{primary_object} near {secondary_object} detected!",
#             "image_url": image_url
#         })
    
#     return jsonify({
#         "status": "error", 
#         "message": "Failed to capture screenshot"
#     }), 500

# def send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp):
#     """Send object detection alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     emoji_map = {
#         "cat": "🐱",
#         "dog": "🐶",
#         "bird": "🐦",
#         "person": "👤",
#         "couch": "🛋️",
#         "bed": "🛏️",
#         "laptop": "💻",
#         "keyboard": "⌨️",
#         "cell phone": "📱",
#         "tv": "📺",
#         "oven": "🔥"
#     }
    
#     primary_emoji = emoji_map.get(primary_object.lower(), "📷")
#     secondary_emoji = emoji_map.get(secondary_object.lower(), "📍")
    
#     message = {
#         "text": f"{primary_emoji} {primary_object.title()} near {secondary_object} detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*{primary_emoji} {primary_object.title()} near {secondary_object} detected! {secondary_emoji}*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"{primary_object.title()} near {secondary_object} ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Detection event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print(f"✅ Object detection alert sent to Slack: {primary_object} near {secondary_object}")


# # ==========================
# # 📌 Backend API for Gallery
# # ==========================
# @app.route('/get_screenshots', methods=['GET'])
# def get_screenshots():
#     try:
#         # Get manual screenshots
#         manual_screenshots = []
#         screenshots_ref = db.collection("screenshots").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in screenshots_ref:
#             data = doc.to_dict()
#             manual_screenshots.append(data)
        
#         # Get noise detection screenshots
#         noise_screenshots = []
#         noise_ref = db.collection("noise_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in noise_ref:
#             data = doc.to_dict()
#             noise_screenshots.append(data)
        
#         # Get object detection screenshots
#         object_screenshots = []
#         object_ref = db.collection("detection_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in object_ref:
#             data = doc.to_dict()
#             object_screenshots.append(data)
        
#         # Get video recordings
#         videos = []
#         videos_ref = db.collection("videos").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()
#         for doc in videos_ref:
#             data = doc.to_dict()
#             videos.append(data)
            
#         return jsonify({
#             "status": "success",
#             "manual_screenshots": manual_screenshots,
#             "noise_screenshots": noise_screenshots,
#             "object_screenshots": object_screenshots,
#             "videos": videos
#         })
    
#     except Exception as e:
#         print(f"❌ Error fetching gallery data: {e}")
#         return jsonify({
#             "status": "error", 
#             "message": str(e),
#             "manual_screenshots": [],
#             "noise_screenshots": [],
#             "object_screenshots": [],
#             "videos": []
#         }), 500
    
# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     # Initialize audio system
#     setup_audio_detection()
    
#     # Register cleanup handler
#     atexit.register(lambda: setattr(sys.modules[__name__], 'is_listening', False))
    
#     app.run(debug=True)










#because previiously i done evrything and finallly gonna look llike gonna done, but at lat many thing cannot done, so i redo, and llater that if one thing done then give a copy
# current issue: noise detection 0db, noise event no chart type, no reall time update and cannot see data inside, media gallery no have those pictures along with timestamps. the status of object detection is white colour.
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime, timedelta
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess
# import atexit
# import sys
# import pyaudio
# import numpy as np
# import random  # For our debug logging
# from collections import defaultdict



# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam

# # Global variables for audio detection
# audio_stream = None
# is_listening = False
# noise_threshold = 80  # Default threshold, can be adjusted
# noise_detection_thread = None
# last_noise_alert_time = None
# noise_cooldown_seconds = 30  # Default cooldown of 10 seconds

# # Global variables for object detection
# detection_model = None
# category_index = None
# detection_enabled = False
# target_object = None  # Object that triggers monitoring (e.g., "couch")
# monitor_object = None  # Object to watch for (e.g., "cat")
# cooldown_period = 10  # Seconds between alerts for the same detection
# last_detection_time = None
# detection_threshold = 0.5  # Confidence threshold for detection
# proximity_threshold = 0.2  # How close objects need to be (as a fraction of image size)

# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/')
# def index():
#     # Start noise detection automatically for testing
#     global is_listening
#     if not is_listening:
#         setup_audio_detection()
#         is_listening = True
#         threading.Thread(target=noise_detection_loop, daemon=True).start()
#         print("🔄 Noise detection started automatically")
    
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# @app.route('/toggle_recording', methods=['POST'])
# # def toggle_recording():
# #     global is_recording, out, start_time, video_filename

# #     if is_recording:
# #         is_recording = False
# #         if out is not None:
# #             out.release()  # Stop video recording

# #         print("🛑 Video recording stopped!")
        
# #         # Upload to Firebase Storage
# #         video_url = upload_video(video_filename)
        
# #         # Send to Slack
# #         if video_url:
# #             send_slack_video(video_url)

# #         return jsonify({
# #             "status": "stopped",
# #             "message": "Recording stopped",
# #             "video_url": video_url if video_url else None
# #         }), 200
# #     else:
# #         is_recording = True
# #         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# #         video_filename = f"recording_{start_time}.mp4"
        
# #         # Use MP4V codec (H.264) for mp4 files
# #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
# #         # Get the camera dimensions
# #         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# #         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
# #         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

# #         print(f"🔴 Video recording started! Saving to {video_filename}")

# #         return jsonify({
# #             "status": "recording",
# #             "message": "Recording started",
# #             "video_url": video_filename
# #         }), 200

# #this test for 60 min max
# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         # Add a timer to stop recording after 60 minutes
#         def stop_after_timeout():
#             global is_recording
#             time.sleep(60 * 60)  # 60 minutes in seconds
#             if is_recording:
#                 print("🕒 Maximum recording time (60 minutes) reached. Stopping recording.")
#                 requests.post('http://localhost:5000/toggle_recording')
                
#         # Start timer in a separate thread
#         timer_thread = threading.Thread(target=stop_after_timeout)
#         timer_thread.daemon = True
#         timer_thread.start()

#         print(f"🔴 Video recording started! Saving to {video_filename} (Max 60 minutes)")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started (Max 60 minutes)",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage with correct MIME type
#     try:
#         blob = bucket.blob(f"videos/{filename}")
        
#         # Set the correct MIME type for MP4
#         blob.content_type = 'video/mp4'
        
#         # Set content disposition to inline so browsers will play it
#         blob.content_disposition = 'inline'
        
#         # Upload the file
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {
#         "text": "🎥 Video Recording Uploaded!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "🎥 *Video Recording Uploaded!*"
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"<{video_url}|Click here to view or download the video>"
#                 }
#             }
#         ]
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# #noise detection
# def setup_audio_detection():
#     """Initialize the audio detection system"""
#     global audio_stream
    
#     print("🔄 Initializing audio detection system...")
#     try:
#         # Initialize PyAudio
#         p = pyaudio.PyAudio()
        
#         # Configure audio stream
#         audio_stream = p.open(
#             format=pyaudio.paInt16,
#             channels=1,
#             rate=44100,
#             input=True,
#             frames_per_buffer=1024
#         )
        
#         print("✅ Audio detection system initialized successfully")
#         return True
#     except Exception as e:
#         print(f"❌ Error initializing audio: {e}")
#         return False

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold
#             if audio_level > noise_threshold:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
                    
#                     # Prevent multiple captures by waiting
#                     time.sleep(2)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# def calculate_audio_level(data):
#     """Calculate the audio level from raw audio data"""
#     # Convert audio data to numpy array
#     audio_data = np.frombuffer(data, dtype=np.int16)
    
#     # Calculate RMS value (root mean square)
#     rms = np.sqrt(np.mean(np.square(audio_data)))
    
#     # Convert to decibels (normalized)
#     if rms > 0:
#         db = 20 * np.log10(rms)
#     else:
#         db = 0
        
#     return db

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream, last_noise_alert_time
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold and not in cooldown period
#             current_time = time.time()
#             cooldown_elapsed = True
            
#             if last_noise_alert_time is not None:
#                 elapsed_time = current_time - last_noise_alert_time
#                 cooldown_elapsed = elapsed_time > noise_cooldown_seconds
                
#             if audio_level > noise_threshold and cooldown_elapsed:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Update last alert time for cooldown
#                 last_noise_alert_time = current_time
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# @app.route('/set_cooldown', methods=['POST'])
# def set_cooldown():
#     global noise_cooldown_seconds
    
#     data = request.get_json()
#     if data and 'cooldown' in data:
#         try:
#             noise_cooldown_seconds = int(data['cooldown'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise alert cooldown set to {noise_cooldown_seconds} seconds"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid cooldown value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No cooldown value provided"
#         }), 400

# # def record_noise_event(level, timestamp, image_url):
# #     """Record noise event in Firestore for dashboard reporting"""
# #     event_data = {
# #         "timestamp": timestamp,
# #         "level": float(level),
# #         "image_url": image_url,
# #         "date": datetime.now().strftime("%Y-%m-%d"),
# #         "hour": datetime.now().hour,
# #         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
# #         "month": datetime.now().strftime("%Y-%m")
# #     }
    
# #     # Add to noise_events collection
# #     db.collection("noise_events").document(timestamp).set(event_data)
# #     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# # testing to add yearly
# def record_noise_event(level, timestamp, image_url):
#     """Record noise event in Firestore for dashboard reporting"""
#     event_data = {
#         "timestamp": timestamp,
#         "level": float(level),
#         "image_url": image_url,
#         "date": datetime.now().strftime("%Y-%m-%d"),
#         "hour": datetime.now().hour,
#         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#         "month": datetime.now().strftime("%Y-%m"),
#         "year": datetime.now().strftime("%Y")  # Add year
#     }
    
#     # Add to noise_events collection
#     db.collection("noise_events").document(timestamp).set(event_data)
#     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# #add a new endpoint to get yearly data
# @app.route('/get_yearly_data', methods=['GET'])
# def get_yearly_data():
#     try:
#         # Get current year
#         now = datetime.now()
#         current_year = now.strftime("%Y")
        
#         # Initialize yearly data (monthly counts for the current year)
#         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         yearly_data = [0] * 12
        
#         # Query for each month in the current year
#         for month_idx in range(12):
#             month_num = month_idx + 1
#             month_query = db.collection("noise_events").where(
#                 "month", "==", f"{current_year}-{month_num:02d}")
#             month_count = len(list(month_query.stream()))
#             yearly_data[month_idx] = month_count
        
#         return jsonify({
#             "status": "success",
#             "yearly_data": yearly_data,
#             "months": months
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting yearly data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "yearly_data": [0] * 12,
#             "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         }), 500

# def send_noise_alert_to_slack(level, image_url, timestamp):
#     """Send noise alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     message = {
#         "text": f"🔊 Loud Noise Detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"Noise Event Screenshot ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Noise event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print("✅ Noise alert sent to Slack")

# @app.route('/start_noise_detection', methods=['POST'])
# def start_noise_detection():
#     global is_listening, noise_detection_thread, noise_threshold
    
#     # Get custom threshold if provided
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#         except (ValueError, TypeError):
#             pass
    
#     if not is_listening:
#         # Initialize audio if not already done
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Start detection in background thread
#         is_listening = True
#         noise_detection_thread = threading.Thread(target=noise_detection_loop)
#         noise_detection_thread.daemon = True
#         noise_detection_thread.start()
        
#         return jsonify({
#             "status": "success", 
#             "message": f"Noise detection started with threshold {noise_threshold} dB"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection already running"
#         })

# @app.route('/stop_noise_detection', methods=['POST'])
# def stop_noise_detection():
#     global is_listening
    
#     if is_listening:
#         is_listening = False
#         # Thread will exit on its own due to while loop condition
#         return jsonify({
#             "status": "success", 
#             "message": "Noise detection stopped"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection not running"
#         })

# @app.route('/set_noise_threshold', methods=['POST'])
# def set_noise_threshold():
#     global noise_threshold
    
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise threshold set to {noise_threshold} dB"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid threshold value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No threshold provided"
#         }), 400

# @app.route('/test_audio', methods=['GET'])
# def test_audio():
#     try:
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Read a sample
#         data = audio_stream.read(1024, exception_on_overflow=False)
#         level = calculate_audio_level(data)
        
#         return jsonify({
#             "status": "success",
#             "audio_level": float(level),
#             "threshold": float(noise_threshold)
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"Audio test failed: {str(e)}"
#         }), 500

# # add the year data
# @app.route('/get_noise_data', methods=['GET'])
# def get_noise_data():
#     try:
#         # Get current date and time
#         now = datetime.now()
#         today = now.strftime("%Y-%m-%d")
#         current_week = now.strftime("%Y-W%U")
#         current_month = now.strftime("%Y-%m")
#         current_year = now.strftime("%Y")
        
#         # Initialize data structures
#         daily_data = [0] * 24
#         weekly_data = [0] * 7
#         monthly_data = [0] * 31  # Maximum days in a month
#         yearly_data = [0] * 12   # 12 months in a year
#         recent_events = []
        
#         # Query Firestore for noise events
#         # Daily data (today's events by hour)
#         daily_query = db.collection("noise_events").where("date", "==", today)
#         daily_results = daily_query.stream()
        
#         for doc in daily_results:
#             data = doc.to_dict()
#             hour = data.get('hour', 0)
#             if 0 <= hour < 24:
#                 daily_data[hour] += 1
        
#         # Weekly data (this week's events by day)
#         # Calculate start of week (Sunday)
#         start_of_week = now - timedelta(days=now.weekday() + 1)
#         for day in range(7):
#             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             weekly_data[day] = day_count
        
#         # Monthly data (this month's events by day)
#         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
#         for day in range(1, days_in_month + 1):
#             date = f"{now.year}-{now.month:02d}-{day:02d}"
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             monthly_data[day - 1] = day_count
            
#         # Yearly data (this year's events by month)
#         for month in range(1, 13):
#             month_prefix = f"{current_year}-{month:02d}"
#             month_query = db.collection("noise_events").where("month", ">=", month_prefix).where("month", "<", f"{current_year}-{month+1:02d}")
#             month_count = len(list(month_query.stream()))
#             yearly_data[month - 1] = month_count
        
#         # Recent events (limit to 10)
#         recent_query = (db.collection("noise_events")
#                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
#                         .limit(10))
        
#         recent_docs = recent_query.stream()
#         for doc in recent_docs:
#             data = doc.to_dict()
#             # Convert timestamp string to datetime for proper sorting
#             try:
#                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
#                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             except:
#                 formatted_timestamp = data.get('timestamp', '')
                
#             recent_events.append({
#                 "timestamp": formatted_timestamp,
#                 "level": data.get('level', 0),
#                 "image_url": data.get('image_url', '')
#             })
        
#         return jsonify({
#             "status": "success",
#             "daily_data": daily_data,
#             "weekly_data": weekly_data,
#             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
#             "yearly_data": yearly_data,  # Add yearly data
#             "recent_events": recent_events
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting noise data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "daily_data": [0] * 24,
#             "weekly_data": [0] * 7,
#             "monthly_data": [0] * 31,
#             "yearly_data": [0] * 12,  # Add yearly data
#             "recent_events": []
#         }), 500

# ## Object detection
# # ==========================
# # 📌 OBJECT DETECTION SCREENSHOT
# # ==========================
# @app.route('/object_detection_screenshot', methods=['POST'])
# def object_detection_screenshot():
#     data = request.get_json()
#     primary_object = data.get('primaryObject', 'object')
#     secondary_object = data.get('secondaryObject', 'location')
    
#     # Capture the screenshot
#     filename, timestamp = capture_screenshot()
    
#     if filename:
#         # Upload to Firebase
#         image_url = upload_screenshot(filename, timestamp)
        
#         # Record detection event in Firestore
#         event_data = {
#             "timestamp": timestamp,
#             "primaryObject": primary_object,
#             "secondaryObject": secondary_object,
#             "image_url": image_url,
#             "date": datetime.now().strftime("%Y-%m-%d"),
#             "hour": datetime.now().hour,
#             "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#             "month": datetime.now().strftime("%Y-%m")
#         }
        
#         # Add to detection_events collection
#         db.collection("detection_events").document(timestamp).set(event_data)
        
#         # Send to Slack
#         send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"{primary_object} near {secondary_object} detected!",
#             "image_url": image_url
#         })
    
#     return jsonify({
#         "status": "error", 
#         "message": "Failed to capture screenshot"
#     }), 500

# def send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp):
#     """Send object detection alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     emoji_map = {
#         "cat": "🐱",
#         "dog": "🐶",
#         "bird": "🐦",
#         "person": "👤",
#         "couch": "🛋️",
#         "bed": "🛏️",
#         "laptop": "💻",
#         "keyboard": "⌨️",
#         "cell phone": "📱",
#         "tv": "📺",
#         "oven": "🔥"
#     }
    
#     primary_emoji = emoji_map.get(primary_object.lower(), "📷")
#     secondary_emoji = emoji_map.get(secondary_object.lower(), "📍")
    
#     message = {
#         "text": f"{primary_emoji} {primary_object.title()} near {secondary_object} detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*{primary_emoji} {primary_object.title()} near {secondary_object} detected! {secondary_emoji}*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"{primary_object.title()} near {secondary_object} ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Detection event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print(f"✅ Object detection alert sent to Slack: {primary_object} near {secondary_object}")


# # ==========================
# # 📌 Backend API for Gallery
# # ==========================
# @app.route('/get_screenshots', methods=['GET'])
# def get_screenshots():
#     try:
#         # Get manual screenshots
#         manual_screenshots = []
#         screenshots_ref = db.collection("screenshots").limit(50).stream()
#         for doc in screenshots_ref:
#             data = doc.to_dict()
#             if "noise_detection" not in data:  # Only manual screenshots
#                 manual_screenshots.append(data)
        
#         # Get noise detection screenshots
#         noise_screenshots = []
#         noise_ref = db.collection("noise_events").limit(50).stream()
#         for doc in noise_ref:
#             data = doc.to_dict()
#             noise_screenshots.append(data)
        
#         # Get object detection screenshots (if implemented)
#         object_screenshots = []
#         # Placeholder for object detection 
        
#         # Get video recordings
#         videos = []
#         videos_ref = db.collection("videos").limit(20).stream()
#         for doc in videos_ref:
#             data = doc.to_dict()
#             videos.append(data)
            
#         return jsonify({
#             "status": "success",
#             "manual_screenshots": manual_screenshots,
#             "noise_screenshots": noise_screenshots,
#             "object_screenshots": object_screenshots,
#             "videos": videos
#         })
    
#     except Exception as e:
#         print(f"❌ Error fetching gallery data: {e}")
#         return jsonify({
#             "status": "error", 
#             "message": str(e),
#             "manual_screenshots": [],
#             "noise_screenshots": [],
#             "object_screenshots": [],
#             "videos": []
#         }), 500

# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     # Initialize audio system
#     setup_audio_detection()
    
#     # Register cleanup handler
#     atexit.register(lambda: setattr(sys.modules[__name__], 'is_listening', False))
    
#     app.run(debug=True)








# code from Modifying App Code for Noise Events Dashboard, idk what have done, usee this to test first
# status colour have done, galllery can scroll now, object detection working
# Current main issue: media gallery invalid date, noise detection.
# Minor issue: chart type is at the right side, should be at left side, when enlarge photo, the photo not in middle. All photos and recording will store locally( I think this can keep lah)
# code below try to solve media gallery date and noise detection, doing media gallery date first
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime, timedelta
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess
# import atexit
# import sys
# import pyaudio
# import numpy as np
# import random  # For our debug logging
# from collections import defaultdict



# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam

# # Global variables for audio detection
# audio_stream = None
# is_listening = False
# noise_threshold = 80  # Default threshold, can be adjusted
# noise_detection_thread = None
# last_noise_alert_time = None
# noise_cooldown_seconds = 30  # Default cooldown of 10 seconds

# # Global variables for object detection
# detection_model = None
# category_index = None
# detection_enabled = False
# target_object = None  # Object that triggers monitoring (e.g., "couch")
# monitor_object = None  # Object to watch for (e.g., "cat")
# cooldown_period = 10  # Seconds between alerts for the same detection
# last_detection_time = None
# detection_threshold = 0.5  # Confidence threshold for detection
# proximity_threshold = 0.2  # How close objects need to be (as a fraction of image size)

# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/')
# def index():
#     # Start noise detection automatically for testing
#     global is_listening
#     if not is_listening:
#         setup_audio_detection()
#         is_listening = True
#         threading.Thread(target=noise_detection_loop, daemon=True).start()
#         print("🔄 Noise detection started automatically")
    
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# @app.route('/toggle_recording', methods=['POST'])
# # def toggle_recording():
# #     global is_recording, out, start_time, video_filename

# #     if is_recording:
# #         is_recording = False
# #         if out is not None:
# #             out.release()  # Stop video recording

# #         print("🛑 Video recording stopped!")
        
# #         # Upload to Firebase Storage
# #         video_url = upload_video(video_filename)
        
# #         # Send to Slack
# #         if video_url:
# #             send_slack_video(video_url)

# #         return jsonify({
# #             "status": "stopped",
# #             "message": "Recording stopped",
# #             "video_url": video_url if video_url else None
# #         }), 200
# #     else:
# #         is_recording = True
# #         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# #         video_filename = f"recording_{start_time}.mp4"
        
# #         # Use MP4V codec (H.264) for mp4 files
# #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
# #         # Get the camera dimensions
# #         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# #         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
# #         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

# #         print(f"🔴 Video recording started! Saving to {video_filename}")

# #         return jsonify({
# #             "status": "recording",
# #             "message": "Recording started",
# #             "video_url": video_filename
# #         }), 200

# #this test for 60 min max
# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         # Add a timer to stop recording after 60 minutes
#         def stop_after_timeout():
#             global is_recording
#             time.sleep(60 * 60)  # 60 minutes in seconds
#             if is_recording:
#                 print("🕒 Maximum recording time (60 minutes) reached. Stopping recording.")
#                 requests.post('http://localhost:5000/toggle_recording')
                
#         # Start timer in a separate thread
#         timer_thread = threading.Thread(target=stop_after_timeout)
#         timer_thread.daemon = True
#         timer_thread.start()

#         print(f"🔴 Video recording started! Saving to {video_filename} (Max 60 minutes)")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started (Max 60 minutes)",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage with correct MIME type
#     try:
#         blob = bucket.blob(f"videos/{filename}")
        
#         # Set the correct MIME type for MP4
#         blob.content_type = 'video/mp4'
        
#         # Set content disposition to inline so browsers will play it
#         blob.content_disposition = 'inline'
        
#         # Upload the file
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {
#         "text": "🎥 Video Recording Uploaded!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "🎥 *Video Recording Uploaded!*"
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"<{video_url}|Click here to view or download the video>"
#                 }
#             }
#         ]
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# #noise detection
# def setup_audio_detection():
#     """Initialize the audio detection system"""
#     global audio_stream
    
#     print("🔄 Initializing audio detection system...")
#     try:
#         # Initialize PyAudio
#         p = pyaudio.PyAudio()
        
#         # Configure audio stream
#         audio_stream = p.open(
#             format=pyaudio.paInt16,
#             channels=1,
#             rate=44100,
#             input=True,
#             frames_per_buffer=1024
#         )
        
#         print("✅ Audio detection system initialized successfully")
#         return True
#     except Exception as e:
#         print(f"❌ Error initializing audio: {e}")
#         return False

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold
#             if audio_level > noise_threshold:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
                    
#                     # Prevent multiple captures by waiting
#                     time.sleep(2)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# def calculate_audio_level(data):
#     """Calculate the audio level from raw audio data"""
#     # Convert audio data to numpy array
#     audio_data = np.frombuffer(data, dtype=np.int16)
    
#     # Calculate RMS value (root mean square)
#     rms = np.sqrt(np.mean(np.square(audio_data)))
    
#     # Convert to decibels (normalized)
#     if rms > 0:
#         db = 20 * np.log10(rms)
#     else:
#         db = 0
        
#     return db

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream, last_noise_alert_time
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold and not in cooldown period
#             current_time = time.time()
#             cooldown_elapsed = True
            
#             if last_noise_alert_time is not None:
#                 elapsed_time = current_time - last_noise_alert_time
#                 cooldown_elapsed = elapsed_time > noise_cooldown_seconds
                
#             if audio_level > noise_threshold and cooldown_elapsed:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Update last alert time for cooldown
#                 last_noise_alert_time = current_time
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# @app.route('/set_cooldown', methods=['POST'])
# def set_cooldown():
#     global noise_cooldown_seconds
    
#     data = request.get_json()
#     if data and 'cooldown' in data:
#         try:
#             noise_cooldown_seconds = int(data['cooldown'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise alert cooldown set to {noise_cooldown_seconds} seconds"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid cooldown value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No cooldown value provided"
#         }), 400

# # def record_noise_event(level, timestamp, image_url):
# #     """Record noise event in Firestore for dashboard reporting"""
# #     event_data = {
# #         "timestamp": timestamp,
# #         "level": float(level),
# #         "image_url": image_url,
# #         "date": datetime.now().strftime("%Y-%m-%d"),
# #         "hour": datetime.now().hour,
# #         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
# #         "month": datetime.now().strftime("%Y-%m")
# #     }
    
# #     # Add to noise_events collection
# #     db.collection("noise_events").document(timestamp).set(event_data)
# #     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# # testing to add yearly
# def record_noise_event(level, timestamp, image_url):
#     """Record noise event in Firestore for dashboard reporting"""
#     event_data = {
#         "timestamp": timestamp,
#         "level": float(level),
#         "image_url": image_url,
#         "date": datetime.now().strftime("%Y-%m-%d"),
#         "hour": datetime.now().hour,
#         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#         "month": datetime.now().strftime("%Y-%m"),
#         "year": datetime.now().strftime("%Y")  # Add year
#     }
    
#     # Add to noise_events collection
#     db.collection("noise_events").document(timestamp).set(event_data)
#     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# #add a new endpoint to get yearly data
# @app.route('/get_yearly_data', methods=['GET'])
# def get_yearly_data():
#     try:
#         # Get current year
#         now = datetime.now()
#         current_year = now.strftime("%Y")
        
#         # Initialize yearly data (monthly counts for the current year)
#         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         yearly_data = [0] * 12
        
#         # Query for each month in the current year
#         for month_idx in range(12):
#             month_num = month_idx + 1
#             month_query = db.collection("noise_events").where(
#                 "month", "==", f"{current_year}-{month_num:02d}")
#             month_count = len(list(month_query.stream()))
#             yearly_data[month_idx] = month_count
        
#         return jsonify({
#             "status": "success",
#             "yearly_data": yearly_data,
#             "months": months
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting yearly data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "yearly_data": [0] * 12,
#             "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         }), 500

# def send_noise_alert_to_slack(level, image_url, timestamp):
#     """Send noise alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     message = {
#         "text": f"🔊 Loud Noise Detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"Noise Event Screenshot ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Noise event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print("✅ Noise alert sent to Slack")

# @app.route('/start_noise_detection', methods=['POST'])
# def start_noise_detection():
#     global is_listening, noise_detection_thread, noise_threshold
    
#     # Get custom threshold if provided
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#         except (ValueError, TypeError):
#             pass
    
#     if not is_listening:
#         # Initialize audio if not already done
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Start detection in background thread
#         is_listening = True
#         noise_detection_thread = threading.Thread(target=noise_detection_loop)
#         noise_detection_thread.daemon = True
#         noise_detection_thread.start()
        
#         return jsonify({
#             "status": "success", 
#             "message": f"Noise detection started with threshold {noise_threshold} dB"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection already running"
#         })

# @app.route('/stop_noise_detection', methods=['POST'])
# def stop_noise_detection():
#     global is_listening
    
#     if is_listening:
#         is_listening = False
#         # Thread will exit on its own due to while loop condition
#         return jsonify({
#             "status": "success", 
#             "message": "Noise detection stopped"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection not running"
#         })

# @app.route('/set_noise_threshold', methods=['POST'])
# def set_noise_threshold():
#     global noise_threshold
    
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise threshold set to {noise_threshold} dB"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid threshold value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No threshold provided"
#         }), 400

# @app.route('/test_audio', methods=['GET'])
# def test_audio():
#     try:
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Read a sample
#         data = audio_stream.read(1024, exception_on_overflow=False)
#         level = calculate_audio_level(data)
        
#         return jsonify({
#             "status": "success",
#             "audio_level": float(level),
#             "threshold": float(noise_threshold)
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"Audio test failed: {str(e)}"
#         }), 500

# # Add this route to get noise data for the dashboard
# # add the year data
# # Add this at line 650 or so, after the get_noise_data route declaration
# @app.route('/get_noise_data', methods=['GET'])
# def get_noise_data():
#     try:
#         # Get current date and time
#         now = datetime.now()
#         today = now.strftime("%Y-%m-%d")
#         current_week = now.strftime("%Y-W%U")
#         current_month = now.strftime("%Y-%m")
#         current_year = now.strftime("%Y")
        
#         # Initialize data structures
#         daily_data = [0] * 24
#         weekly_data = [0] * 7
#         monthly_data = [0] * 31  # Maximum days in a month
#         yearly_data = [0] * 12   # 12 months in a year
#         recent_events = []
        
#         # Query Firestore for noise events
#         # Daily data (today's events by hour)
#         daily_query = db.collection("noise_events").where("date", "==", today)
#         daily_results = list(daily_query.stream())
        
#         for doc in daily_results:
#             data = doc.to_dict()
#             hour = data.get('hour', 0)
#             if 0 <= hour < 24:
#                 daily_data[hour] += 1
        
#         # Weekly data (this week's events by day)
#         # Calculate start of week (Sunday)
#         start_of_week = now - timedelta(days=now.weekday() + 1)
#         for day in range(7):
#             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             weekly_data[day] = day_count
        
#         # Monthly data (this month's events by day)
#         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
#         for day in range(1, days_in_month + 1):
#             day_str = f"{day:02d}"
#             month_str = f"{now.month:02d}"
#             date = f"{now.year}-{month_str}-{day_str}"
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             monthly_data[day - 1] = day_count
            
#         # Yearly data (this year's events by month)
#         for month in range(1, 13):
#             month_prefix = f"{current_year}-{month:02d}"
#             month_query = db.collection("noise_events").where(
#                 "month", "==", month_prefix)
#             month_count = len(list(month_query.stream()))
#             yearly_data[month - 1] = month_count
        
#         # Recent events (limit to 10)
#         recent_query = (db.collection("noise_events")
#                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
#                         .limit(10))
        
#         recent_docs = list(recent_query.stream())
#         for doc in recent_docs:
#             data = doc.to_dict()
#             # Convert timestamp string to datetime for proper sorting
#             try:
#                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
#                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             except:
#                 formatted_timestamp = data.get('timestamp', '')
                
#             recent_events.append({
#                 "timestamp": data.get('timestamp', ''),
#                 "level": data.get('level', 0),
#                 "image_url": data.get('image_url', '')
#             })
        
#         return jsonify({
#             "status": "success",
#             "daily_data": daily_data,
#             "weekly_data": weekly_data,
#             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
#             "yearly_data": yearly_data,
#             "recent_events": recent_events
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting noise data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "daily_data": [0] * 24,
#             "weekly_data": [0] * 7,
#             "monthly_data": [0] * 31,
#             "yearly_data": [0] * 12,
#             "recent_events": []
#         }), 500

# ## Object detection
# # ==========================
# # 📌 OBJECT DETECTION SCREENSHOT
# # ==========================
# @app.route('/object_detection_screenshot', methods=['POST'])
# def object_detection_screenshot():
#     data = request.get_json()
#     primary_object = data.get('primaryObject', 'object')
#     secondary_object = data.get('secondaryObject', 'location')
    
#     # Capture the screenshot
#     filename, timestamp = capture_screenshot()
    
#     if filename:
#         # Upload to Firebase
#         image_url = upload_screenshot(filename, timestamp)
        
#         # Record detection event in Firestore
#         event_data = {
#             "timestamp": timestamp,
#             "primaryObject": primary_object,
#             "secondaryObject": secondary_object,
#             "image_url": image_url,
#             "date": datetime.now().strftime("%Y-%m-%d"),
#             "hour": datetime.now().hour,
#             "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#             "month": datetime.now().strftime("%Y-%m")
#         }
        
#         # Add to detection_events collection
#         db.collection("detection_events").document(timestamp).set(event_data)
        
#         # Send to Slack
#         send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"{primary_object} near {secondary_object} detected!",
#             "image_url": image_url
#         })
    
#     return jsonify({
#         "status": "error", 
#         "message": "Failed to capture screenshot"
#     }), 500

# def send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp):
#     """Send object detection alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     emoji_map = {
#         "cat": "🐱",
#         "dog": "🐶",
#         "bird": "🐦",
#         "person": "👤",
#         "couch": "🛋️",
#         "bed": "🛏️",
#         "laptop": "💻",
#         "keyboard": "⌨️",
#         "cell phone": "📱",
#         "tv": "📺",
#         "oven": "🔥"
#     }
    
#     primary_emoji = emoji_map.get(primary_object.lower(), "📷")
#     secondary_emoji = emoji_map.get(secondary_object.lower(), "📍")
    
#     message = {
#         "text": f"{primary_emoji} {primary_object.title()} near {secondary_object} detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*{primary_emoji} {primary_object.title()} near {secondary_object} detected! {secondary_emoji}*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"{primary_object.title()} near {secondary_object} ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Detection event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print(f"✅ Object detection alert sent to Slack: {primary_object} near {secondary_object}")


# # ==========================
# # 📌 Backend API for Gallery
# # ==========================
# @app.route('/get_screenshots', methods=['GET'])
# def get_screenshots():
#     try:
#         # Get manual screenshots
#         manual_screenshots = []
#         screenshots_ref = db.collection("screenshots").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in screenshots_ref:
#             data = doc.to_dict()
#             manual_screenshots.append(data)
        
#         # Get noise detection screenshots
#         noise_screenshots = []
#         noise_ref = db.collection("noise_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in noise_ref:
#             data = doc.to_dict()
#             noise_screenshots.append(data)
        
#         # Get object detection screenshots
#         object_screenshots = []
#         object_ref = db.collection("detection_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in object_ref:
#             data = doc.to_dict()
#             object_screenshots.append(data)
        
#         # Get video recordings
#         videos = []
#         videos_ref = db.collection("videos").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()
#         for doc in videos_ref:
#             data = doc.to_dict()
#             videos.append(data)
            
#         return jsonify({
#             "status": "success",
#             "manual_screenshots": manual_screenshots,
#             "noise_screenshots": noise_screenshots,
#             "object_screenshots": object_screenshots,
#             "videos": videos
#         })
    
#     except Exception as e:
#         print(f"❌ Error fetching gallery data: {e}")
#         return jsonify({
#             "status": "error", 
#             "message": str(e),
#             "manual_screenshots": [],
#             "noise_screenshots": [],
#             "object_screenshots": [],
#             "videos": []
#         }), 500
    
# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     # Initialize audio system
#     setup_audio_detection()
    
#     # Register cleanup handler
#     atexit.register(lambda: setattr(sys.modules[__name__], 'is_listening', False))
    
#     app.run(debug=True)







# code from Modifying App Code for Noise Events Dashboard, idk what have done, usee this to test first
# Current main issue: media gallery invalid date, noise detection.
# Minor issue: chart type is at the right side, should be at left side, when enlarge photo, the photo not in middle. All photos and recording will store locally( I think this can keep lah)
# code try to solve media gallery date and noise detection, now now now doing media gallery date first
# now galllery time issue fixed, now try noise detection
# this will keep as copy, codde ddown will be trying the noise ddetection, using the very first version.
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime, timedelta
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess
# import atexit
# import sys
# import pyaudio
# import numpy as np
# import random  # For our debug logging
# from collections import defaultdict



# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam

# # Global variables for audio detection
# audio_stream = None
# is_listening = False
# noise_threshold = 80  # Default threshold, can be adjusted
# noise_detection_thread = None
# last_noise_alert_time = None
# noise_cooldown_seconds = 30  # Default cooldown of 10 seconds

# # Global variables for object detection
# detection_model = None
# category_index = None
# detection_enabled = False
# target_object = None  # Object that triggers monitoring (e.g., "couch")
# monitor_object = None  # Object to watch for (e.g., "cat")
# cooldown_period = 10  # Seconds between alerts for the same detection
# last_detection_time = None
# detection_threshold = 0.5  # Confidence threshold for detection
# proximity_threshold = 0.2  # How close objects need to be (as a fraction of image size)

# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/')
# def index():
#     # Start noise detection automatically for testing
#     global is_listening
#     if not is_listening:
#         setup_audio_detection()
#         is_listening = True
#         threading.Thread(target=noise_detection_loop, daemon=True).start()
#         print("🔄 Noise detection started automatically")
    
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# # @app.route('/toggle_recording', methods=['POST'])
# # def toggle_recording():
# #     global is_recording, out, start_time, video_filename

# #     if is_recording:
# #         is_recording = False
# #         if out is not None:
# #             out.release()  # Stop video recording

# #         print("🛑 Video recording stopped!")
        
# #         # Upload to Firebase Storage
# #         video_url = upload_video(video_filename)
        
# #         # Send to Slack
# #         if video_url:
# #             send_slack_video(video_url)

# #         return jsonify({
# #             "status": "stopped",
# #             "message": "Recording stopped",
# #             "video_url": video_url if video_url else None
# #         }), 200
# #     else:
# #         is_recording = True
# #         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# #         video_filename = f"recording_{start_time}.mp4"
        
# #         # Use MP4V codec (H.264) for mp4 files
# #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
# #         # Get the camera dimensions
# #         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# #         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
# #         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

# #         print(f"🔴 Video recording started! Saving to {video_filename}")

# #         return jsonify({
# #             "status": "recording",
# #             "message": "Recording started",
# #             "video_url": video_filename
# #         }), 200

# #this test for 60 min max
# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         # Add a timer to stop recording after 60 minutes
#         def stop_after_timeout():
#             global is_recording
#             time.sleep(60 * 60)  # 60 minutes in seconds
#             if is_recording:
#                 print("🕒 Maximum recording time (60 minutes) reached. Stopping recording.")
#                 requests.post('http://localhost:5000/toggle_recording')
                
#         # Start timer in a separate thread
#         timer_thread = threading.Thread(target=stop_after_timeout)
#         timer_thread.daemon = True
#         timer_thread.start()

#         print(f"🔴 Video recording started! Saving to {video_filename} (Max 60 minutes)")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started (Max 60 minutes)",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage with correct MIME type
#     try:
#         blob = bucket.blob(f"videos/{filename}")
        
#         # Set the correct MIME type for MP4
#         blob.content_type = 'video/mp4'
        
#         # Set content disposition to inline so browsers will play it
#         blob.content_disposition = 'inline'
        
#         # Upload the file
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {
#         "text": "🎥 Video Recording Uploaded!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "🎥 *Video Recording Uploaded!*"
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"<{video_url}|Click here to view or download the video>"
#                 }
#             }
#         ]
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# #noise detection
# def setup_audio_detection():
#     """Initialize the audio detection system with fallback options"""
#     global audio_stream
    
#     print("🔄 Initializing audio detection system...")
#     try:
#         # Initialize PyAudio
#         p = pyaudio.PyAudio()
        
#         # List available input devices for debugging
#         device_count = p.get_device_count()
#         print(f"Found {device_count} audio devices:")
#         input_devices = []
        
#         for i in range(device_count):
#             device_info = p.get_device_info_by_index(i)
#             if device_info['maxInputChannels'] > 0:  # Input device
#                 print(f"  Input Device {i}: {device_info['name']} (Channels: {device_info['maxInputChannels']})")
#                 input_devices.append(i)
        
#         if not input_devices:
#             print("❌ Error: No input device found")
#             return False
        
#         # Try devices in this order: device 1 (typical microphone), then 0 (Sound Mapper), then others
#         devices_to_try = []
#         if 1 in input_devices:
#             devices_to_try.append(1)  # Often the main microphone
#         if 0 in input_devices:
#             devices_to_try.append(0)  # Microsoft Sound Mapper is usually reliable
#         # Add remaining devices
#         devices_to_try.extend([d for d in input_devices if d not in devices_to_try])
        
#         # Try each device until one works
#         for device_index in devices_to_try:
#             try:
#                 print(f"Trying input device {device_index}...")
#                 # Configure audio stream with explicit device index
#                 stream = p.open(
#                     format=pyaudio.paInt16,
#                     channels=1,
#                     rate=44100,
#                     input=True,
#                     input_device_index=device_index,
#                     frames_per_buffer=1024
#                 )
                
#                 # Test the stream with a sample read
#                 data = stream.read(1024, exception_on_overflow=False)
#                 level = calculate_audio_level(data)
#                 print(f"✅ Device {device_index} works! Initial audio level: {level:.2f} dB")
                
#                 # If we got here, the device works
#                 audio_stream = stream
#                 return True
                
#             except Exception as e:
#                 print(f"⚠️ Device {device_index} failed: {e}")
#                 continue
        
#         print("❌ Error: Could not initialize any audio device")
#         return False
        
#     except Exception as e:
#         print(f"❌ Error initializing audio: {e}")
#         return False
    
# @app.route('/select_audio_device', methods=['POST'])
# def select_audio_device():
#     """Manually select an audio input device"""
#     global audio_stream
    
#     data = request.get_json()
#     if not data or 'device_index' not in data:
#         return jsonify({
#             "status": "error",
#             "message": "No device index provided"
#         }), 400
    
#     try:
#         device_index = int(data['device_index'])
        
#         # Close existing stream if open
#         if audio_stream is not None:
#             audio_stream.close()
#             audio_stream = None
        
#         # Initialize PyAudio
#         p = pyaudio.PyAudio()
        
#         # Try to open the specified device
#         audio_stream = p.open(
#             format=pyaudio.paInt16,
#             channels=1,
#             rate=44100,
#             input=True,
#             input_device_index=device_index,
#             frames_per_buffer=1024
#         )
        
#         # Test the stream
#         data = audio_stream.read(1024, exception_on_overflow=False)
#         level = calculate_audio_level(data)
        
#         return jsonify({
#             "status": "success",
#             "message": f"Audio device {device_index} selected successfully",
#             "audio_level": float(level)
#         })
        
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"Error selecting audio device: {str(e)}"
#         }), 500

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold
#             if audio_level > noise_threshold:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
                    
#                     # Prevent multiple captures by waiting
#                     time.sleep(2)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying

# # def calculate_audio_level(data):
# #     """Calculate the audio level from raw audio data"""
# #     # Convert audio data to numpy array
# #     audio_data = np.frombuffer(data, dtype=np.int16)
    
# #     # Calculate RMS value (root mean square)
# #     rms = np.sqrt(np.mean(np.square(audio_data)))
    
# #     # Convert to decibels (normalized)
# #     if rms > 0:
# #         db = 20 * np.log10(rms)
# #     else:
# #         db = 0
        
# #     return db

# #this version try not doing the 0db
# def calculate_audio_level(data):
#     """Calculate the audio level from raw audio data"""
#     try:
#         # Convert audio data to numpy array
#         audio_data = np.frombuffer(data, dtype=np.int16)
        
#         # Check if we have any audio data
#         if len(audio_data) == 0:
#             print("❌ Warning: Empty audio data received")
#             return 0
            
#         # Calculate RMS value (root mean square)
#         rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
        
#         # Get the maximum absolute sample value for reference
#         max_sample = np.max(np.abs(audio_data))
        
#         # Debug print once in a while
#         if random.random() < 0.01:  # 1% chance to print
#             print(f"Debug audio: RMS={rms:.2f}, Max sample={max_sample}")
        
#         # Convert to decibels relative to full scale
#         # Use a small epsilon to avoid log(0)
#         epsilon = 1e-10
#         if rms > 0:
#             # 32768 is the max value for 16-bit audio
#             db_fs = 20 * np.log10(rms / 32768)
            
#             # Convert to a more intuitive dB scale (0-100)
#             # -60 dB FS (very quiet) maps to about 0 dB in our scale
#             # 0 dB FS (maximum) maps to about 60 dB in our scale
#             db = 60 + db_fs
            
#             # Ensure we don't return negative values
#             return max(0, db)
#         else:
#             return 0
#     except Exception as e:
#         print(f"❌ Error calculating audio level: {e}")
#         return 0
    

# def noise_detection_loop():
#     """Main loop for noise detection"""
#     global is_listening, audio_stream, last_noise_alert_time
    
#     print("🔊 Noise detection started")
    
#     while is_listening:
#         try:
#             # Read audio data
#             data = audio_stream.read(1024, exception_on_overflow=False)
            
#             # Calculate audio level
#             audio_level = calculate_audio_level(data)
            
#             # Log the audio level periodically for debugging
#             if random.random() < 0.02:  # Log roughly 2% of readings
#                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
#             # Check if noise exceeds threshold and not in cooldown period
#             current_time = time.time()
#             cooldown_elapsed = True
            
#             if last_noise_alert_time is not None:
#                 elapsed_time = current_time - last_noise_alert_time
#                 cooldown_elapsed = elapsed_time > noise_cooldown_seconds
                
#             if audio_level > noise_threshold and cooldown_elapsed:
#                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
#                 # Update last alert time for cooldown
#                 last_noise_alert_time = current_time
                
#                 # Capture screenshot
#                 filename, timestamp = capture_screenshot()
                
#                 if filename:
#                     print(f"📸 Screenshot captured: {filename}")
#                     # Upload to Firebase
#                     image_url = upload_screenshot(filename, timestamp)
                    
#                     # Record noise event in Firestore
#                     record_noise_event(audio_level, timestamp, image_url)
                    
#                     # Send to Slack
#                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
#                 else:
#                     print("❌ Screenshot capture failed")
            
#             # Small delay to prevent excessive CPU usage
#             time.sleep(0.1)
#         except IOError as e:
#             # Common PyAudio error that we can recover from
#             print(f"⚠️ Audio stream IOError (can be normal): {e}")
#             time.sleep(0.2)
#         except Exception as e:
#             print(f"❌ Error in noise detection loop: {e}")
#             time.sleep(1)  # Wait before retrying


# @app.route('/debug_audio', methods=['GET'])
# def debug_audio():
#     """Test audio input with more detailed diagnostics"""
#     try:
#         if audio_stream is None:
#             setup_audio_detection()
        
#         if audio_stream is None:
#             return jsonify({
#                 "status": "error",
#                 "message": "Failed to initialize audio stream"
#             }), 500
        
#         # Read multiple samples to get a better picture
#         samples = []
#         for _ in range(10):
#             data = audio_stream.read(1024, exception_on_overflow=False)
#             audio_data = np.frombuffer(data, dtype=np.int16)
#             rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
#             max_value = np.max(np.abs(audio_data))
#             level = calculate_audio_level(data)
#             samples.append({
#                 "rms": float(rms),
#                 "max_value": int(max_value),
#                 "level": float(level)
#             })
#             time.sleep(0.1)
        
#         # Get PyAudio device info
#         p = pyaudio.PyAudio()
#         devices = []
#         device_count = p.get_device_count()
#         for i in range(device_count):
#             device_info = p.get_device_info_by_index(i)
#             if device_info['maxInputChannels'] > 0:
#                 devices.append({
#                     "index": i,
#                     "name": device_info['name'],
#                     "channels": device_info['maxInputChannels'],
#                     "sampleRate": device_info['defaultSampleRate']
#                 })
        
#         return jsonify({
#             "status": "success",
#             "samples": samples,
#             "devices": devices,
#             "threshold": float(noise_threshold)
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error", 
#             "message": f"Audio debug failed: {str(e)}"
#         }), 500
    

# @app.route('/set_cooldown', methods=['POST'])
# def set_cooldown():
#     global noise_cooldown_seconds
    
#     data = request.get_json()
#     if data and 'cooldown' in data:
#         try:
#             noise_cooldown_seconds = int(data['cooldown'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise alert cooldown set to {noise_cooldown_seconds} seconds"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid cooldown value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No cooldown value provided"
#         }), 400

# # def record_noise_event(level, timestamp, image_url):
# #     """Record noise event in Firestore for dashboard reporting"""
# #     event_data = {
# #         "timestamp": timestamp,
# #         "level": float(level),
# #         "image_url": image_url,
# #         "date": datetime.now().strftime("%Y-%m-%d"),
# #         "hour": datetime.now().hour,
# #         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
# #         "month": datetime.now().strftime("%Y-%m")
# #     }
    
# #     # Add to noise_events collection
# #     db.collection("noise_events").document(timestamp).set(event_data)
# #     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# # testing to add yearly
# def record_noise_event(level, timestamp, image_url):
#     """Record noise event in Firestore for dashboard reporting"""
#     event_data = {
#         "timestamp": timestamp,
#         "level": float(level),
#         "image_url": image_url,
#         "date": datetime.now().strftime("%Y-%m-%d"),
#         "hour": datetime.now().hour,
#         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#         "month": datetime.now().strftime("%Y-%m"),
#         "year": datetime.now().strftime("%Y")  # Add year
#     }
    
#     # Add to noise_events collection
#     db.collection("noise_events").document(timestamp).set(event_data)
#     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# #add a new endpoint to get yearly data
# @app.route('/get_yearly_data', methods=['GET'])
# def get_yearly_data():
#     try:
#         # Get current year
#         now = datetime.now()
#         current_year = now.strftime("%Y")
        
#         # Initialize yearly data (monthly counts for the current year)
#         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         yearly_data = [0] * 12
        
#         # Query for each month in the current year
#         for month_idx in range(12):
#             month_num = month_idx + 1
#             month_query = db.collection("noise_events").where(
#                 "month", "==", f"{current_year}-{month_num:02d}")
#             month_count = len(list(month_query.stream()))
#             yearly_data[month_idx] = month_count
        
#         return jsonify({
#             "status": "success",
#             "yearly_data": yearly_data,
#             "months": months
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting yearly data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "yearly_data": [0] * 12,
#             "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         }), 500

# def send_noise_alert_to_slack(level, image_url, timestamp):
#     """Send noise alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     message = {
#         "text": f"🔊 Loud Noise Detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"Noise Event Screenshot ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Noise event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print("✅ Noise alert sent to Slack")

# @app.route('/start_noise_detection', methods=['POST'])
# def start_noise_detection():
#     global is_listening, noise_detection_thread, noise_threshold
    
#     # Get custom threshold if provided
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#         except (ValueError, TypeError):
#             pass
    
#     if not is_listening:
#         # Initialize audio if not already done
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Start detection in background thread
#         is_listening = True
#         noise_detection_thread = threading.Thread(target=noise_detection_loop)
#         noise_detection_thread.daemon = True
#         noise_detection_thread.start()
        
#         return jsonify({
#             "status": "success", 
#             "message": f"Noise detection started with threshold {noise_threshold} dB"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection already running"
#         })

# @app.route('/stop_noise_detection', methods=['POST'])
# def stop_noise_detection():
#     global is_listening
    
#     if is_listening:
#         is_listening = False
#         # Thread will exit on its own due to while loop condition
#         return jsonify({
#             "status": "success", 
#             "message": "Noise detection stopped"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection not running"
#         })

# @app.route('/set_noise_threshold', methods=['POST'])
# def set_noise_threshold():
#     global noise_threshold
    
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_threshold = float(data['threshold'])
#             return jsonify({
#                 "status": "success", 
#                 "message": f"Noise threshold set to {noise_threshold} dB"
#             })
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid threshold value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No threshold provided"
#         }), 400

# @app.route('/test_audio', methods=['GET'])
# def test_audio():
#     try:
#         if audio_stream is None:
#             setup_audio_detection()
        
#         # Read a sample
#         data = audio_stream.read(1024, exception_on_overflow=False)
#         level = calculate_audio_level(data)
        
#         return jsonify({
#             "status": "success",
#             "audio_level": float(level),
#             "threshold": float(noise_threshold)
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"Audio test failed: {str(e)}"
#         }), 500

# # Add this route to get noise data for the dashboard
# # add the year data
# # Add this at line 650 or so, after the get_noise_data route declaration
# @app.route('/get_noise_data', methods=['GET'])
# def get_noise_data():
#     try:
#         # Get current date and time
#         now = datetime.now()
#         today = now.strftime("%Y-%m-%d")
#         current_week = now.strftime("%Y-W%U")
#         current_month = now.strftime("%Y-%m")
#         current_year = now.strftime("%Y")
        
#         # Initialize data structures
#         daily_data = [0] * 24
#         weekly_data = [0] * 7
#         monthly_data = [0] * 31  # Maximum days in a month
#         yearly_data = [0] * 12   # 12 months in a year
#         recent_events = []
        
#         # Query Firestore for noise events
#         # Daily data (today's events by hour)
#         daily_query = db.collection("noise_events").where("date", "==", today)
#         daily_results = list(daily_query.stream())
        
#         for doc in daily_results:
#             data = doc.to_dict()
#             hour = data.get('hour', 0)
#             if 0 <= hour < 24:
#                 daily_data[hour] += 1
        
#         # Weekly data (this week's events by day)
#         # Calculate start of week (Sunday)
#         start_of_week = now - timedelta(days=now.weekday() + 1)
#         for day in range(7):
#             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             weekly_data[day] = day_count
        
#         # Monthly data (this month's events by day)
#         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
#         for day in range(1, days_in_month + 1):
#             day_str = f"{day:02d}"
#             month_str = f"{now.month:02d}"
#             date = f"{now.year}-{month_str}-{day_str}"
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             monthly_data[day - 1] = day_count
            
#         # Yearly data (this year's events by month)
#         for month in range(1, 13):
#             month_prefix = f"{current_year}-{month:02d}"
#             month_query = db.collection("noise_events").where(
#                 "month", "==", month_prefix)
#             month_count = len(list(month_query.stream()))
#             yearly_data[month - 1] = month_count
        
#         # Recent events (limit to 10)
#         recent_query = (db.collection("noise_events")
#                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
#                         .limit(10))
        
#         recent_docs = list(recent_query.stream())
#         for doc in recent_docs:
#             data = doc.to_dict()
#             # Convert timestamp string to datetime for proper sorting
#             try:
#                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
#                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             except:
#                 formatted_timestamp = data.get('timestamp', '')
                
#             recent_events.append({
#                 "timestamp": data.get('timestamp', ''),
#                 "level": data.get('level', 0),
#                 "image_url": data.get('image_url', '')
#             })
        
#         return jsonify({
#             "status": "success",
#             "daily_data": daily_data,
#             "weekly_data": weekly_data,
#             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
#             "yearly_data": yearly_data,
#             "recent_events": recent_events
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting noise data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "daily_data": [0] * 24,
#             "weekly_data": [0] * 7,
#             "monthly_data": [0] * 31,
#             "yearly_data": [0] * 12,
#             "recent_events": []
#         }), 500


# @app.route('/list_audio_devices', methods=['GET'])
# def list_audio_devices():
#     """List all available audio input devices for debugging"""
#     try:
#         p = pyaudio.PyAudio()
#         devices = []
        
#         # Get device count
#         device_count = p.get_device_count()
        
#         # Loop through all devices
#         for i in range(device_count):
#             device_info = p.get_device_info_by_index(i)
#             if device_info['maxInputChannels'] > 0:  # Input device
#                 devices.append({
#                     'index': i,
#                     'name': device_info['name'],
#                     'channels': device_info['maxInputChannels'],
#                     'sample_rate': device_info['defaultSampleRate']
#                 })
        
#         p.terminate()
        
#         return jsonify({
#             "status": "success",
#             "devices": devices
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# ## Object detection
# # ==========================
# # 📌 OBJECT DETECTION SCREENSHOT
# # ==========================
# @app.route('/object_detection_screenshot', methods=['POST'])
# def object_detection_screenshot():
#     data = request.get_json()
#     primary_object = data.get('primaryObject', 'object')
#     secondary_object = data.get('secondaryObject', 'location')
    
#     # Capture the screenshot
#     filename, timestamp = capture_screenshot()
    
#     if filename:
#         # Upload to Firebase
#         image_url = upload_screenshot(filename, timestamp)
        
#         # Record detection event in Firestore
#         event_data = {
#             "timestamp": timestamp,
#             "primaryObject": primary_object,
#             "secondaryObject": secondary_object,
#             "image_url": image_url,
#             "date": datetime.now().strftime("%Y-%m-%d"),
#             "hour": datetime.now().hour,
#             "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#             "month": datetime.now().strftime("%Y-%m")
#         }
        
#         # Add to detection_events collection
#         db.collection("detection_events").document(timestamp).set(event_data)
        
#         # Send to Slack
#         send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"{primary_object} near {secondary_object} detected!",
#             "image_url": image_url
#         })
    
#     return jsonify({
#         "status": "error", 
#         "message": "Failed to capture screenshot"
#     }), 500

# def send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp):
#     """Send object detection alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     emoji_map = {
#         "cat": "🐱",
#         "dog": "🐶",
#         "bird": "🐦",
#         "person": "👤",
#         "couch": "🛋️",
#         "bed": "🛏️",
#         "laptop": "💻",
#         "keyboard": "⌨️",
#         "cell phone": "📱",
#         "tv": "📺",
#         "oven": "🔥"
#     }
    
#     primary_emoji = emoji_map.get(primary_object.lower(), "📷")
#     secondary_emoji = emoji_map.get(secondary_object.lower(), "📍")
    
#     message = {
#         "text": f"{primary_emoji} {primary_object.title()} near {secondary_object} detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*{primary_emoji} {primary_object.title()} near {secondary_object} detected! {secondary_emoji}*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"{primary_object.title()} near {secondary_object} ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Detection event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print(f"✅ Object detection alert sent to Slack: {primary_object} near {secondary_object}")


# # ==========================
# # 📌 Backend API for Gallery
# # ==========================
# @app.route('/get_screenshots', methods=['GET'])
# def get_screenshots():
#     try:
#         # Get manual screenshots
#         manual_screenshots = []
#         screenshots_ref = db.collection("screenshots").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in screenshots_ref:
#             data = doc.to_dict()
#             manual_screenshots.append(data)
        
#         # Get noise detection screenshots
#         noise_screenshots = []
#         noise_ref = db.collection("noise_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in noise_ref:
#             data = doc.to_dict()
#             noise_screenshots.append(data)
        
#         # Get object detection screenshots
#         object_screenshots = []
#         object_ref = db.collection("detection_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in object_ref:
#             data = doc.to_dict()
#             object_screenshots.append(data)
        
#         # Get video recordings
#         videos = []
#         videos_ref = db.collection("videos").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()
#         for doc in videos_ref:
#             data = doc.to_dict()
#             videos.append(data)
            
#         return jsonify({
#             "status": "success",
#             "manual_screenshots": manual_screenshots,
#             "noise_screenshots": noise_screenshots,
#             "object_screenshots": object_screenshots,
#             "videos": videos
#         })
    
#     except Exception as e:
#         print(f"❌ Error fetching gallery data: {e}")
#         return jsonify({
#             "status": "error", 
#             "message": str(e),
#             "manual_screenshots": [],
#             "noise_screenshots": [],
#             "object_screenshots": [],
#             "videos": []
#         }), 500
    
# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     # Initialize audio system
#     setup_audio_detection()
    
#     # Register cleanup handler
#     atexit.register(lambda: setattr(sys.modules[__name__], 'is_listening', False))
    
#     app.run(debug=True)











# code from Modifying App Code for Noise Events Dashboard, idk what have done, usee this to test first
# Current main issue: media gallery invalid date, noise detection.
# Minor issue: chart type is at the right side, should be at left side, when enlarge photo, the photo not in middle. All photos and recording will store locally( I think this can keep lah)
# code try to solve media gallery date and noise detection, now now now doing media gallery date first
# now galllery time issue fixed, now try noise detection
# this try  the noise detection, like i want to redo.
# now using  claude to do solve my problem,, ok now noise detection works also just need to choose the device 1 first
# code down try change the env, login authentication, responsive web design
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime, timedelta
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess
# import atexit
# import sys
# import pyaudio
# import numpy as np
# import random  # For our debug logging
# from collections import defaultdict
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO, 
#                     format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger('noise_detection')
# class NoiseDetector:
#     def __init__(self, threshold=30, cooldown=10):
#         """Initialize the noise detector with configurable threshold and cooldown"""
#         self.threshold = threshold  # Default threshold in dB
#         self.cooldown = cooldown    # Default cooldown in seconds
#         self.is_listening = False   # Tracking if detector is active
#         self.audio_stream = None    # PyAudio stream
#         self.pyaudio_instance = None  # PyAudio instance
#         self.detection_thread = None  # Thread for detection loop
#         self.last_alert_time = 0    # Last time an alert was triggered
#         self.callback = None        # Callback for when noise is detected
        
#     def start(self, callback=None):
#         """Start the noise detection"""
#         if self.is_listening:
#             logger.warning("Noise detection already running")
#             return False
        
#         self.callback = callback
        
#         # Initialize PyAudio if not already done
#         if not self._initialize_audio():
#             logger.error("Failed to initialize audio")
#             return False
        
#         # Start detection thread
#         self.is_listening = True
#         self.detection_thread = threading.Thread(target=self._detection_loop)
#         self.detection_thread.daemon = True
#         self.detection_thread.start()
#         logger.info(f"Noise detection started with threshold {self.threshold}dB")
#         return True
    
#     def stop(self):
#         """Stop the noise detection"""
#         if not self.is_listening:
#             logger.warning("Noise detection not running")
#             return False
        
#         self.is_listening = False
#         # Thread will exit on its own due to while loop condition
#         logger.info("Noise detection stopped")
#         return True
    
#     def set_threshold(self, threshold):
#         """Set the noise detection threshold"""
#         try:
#             self.threshold = float(threshold)
#             logger.info(f"Threshold set to {self.threshold}dB")
#             return True
#         except (ValueError, TypeError):
#             logger.error(f"Invalid threshold value: {threshold}")
#             return False
    
#     def set_cooldown(self, cooldown):
#         """Set the cooldown period between alerts"""
#         try:
#             self.cooldown = int(cooldown)
#             logger.info(f"Cooldown set to {self.cooldown} seconds")
#             return True
#         except (ValueError, TypeError):
#             logger.error(f"Invalid cooldown value: {cooldown}")
#             return False
    
#     def get_current_level(self):
#         """Get the current audio level"""
#         if not self.audio_stream:
#             if not self._initialize_audio():
#                 return 0
        
#         try:
#             # Read audio data
#             data = self.audio_stream.read(2048, exception_on_overflow=False)
#             # Calculate level
#             level = self._calculate_audio_level(data)
#             return level
#         except Exception as e:
#             logger.error(f"Error getting audio level: {e}")
#             return 0
    
#     def _initialize_audio(self):
#         """Initialize the audio system with proper error handling"""
#         try:
#             # Clean up existing resources if any
#             if self.audio_stream:
#                 self.audio_stream.stop_stream()
#                 self.audio_stream.close()
            
#             if self.pyaudio_instance:
#                 self.pyaudio_instance.terminate()
            
#             # Initialize PyAudio
#             self.pyaudio_instance = pyaudio.PyAudio()
            
#             # Find input devices
#             input_devices = []
#             for i in range(self.pyaudio_instance.get_device_count()):
#                 device_info = self.pyaudio_instance.get_device_info_by_index(i)
#                 if device_info['maxInputChannels'] > 0:
#                     input_devices.append(i)
#                     logger.info(f"Found input device {i}: {device_info['name']}")
            
#             if not input_devices:
#                 logger.error("No audio input devices found")
#                 return False
            
#             # Try to open the default input device first (usually index 0)
#             device_to_use = input_devices[0]
            
#             # Open audio stream
#             self.audio_stream = self.pyaudio_instance.open(
#                 format=pyaudio.paInt16,
#                 channels=1,
#                 rate=44100,
#                 input=True,
#                 input_device_index=device_to_use,
#                 frames_per_buffer=2048
#             )
            
#             # Test the stream
#             test_data = self.audio_stream.read(2048, exception_on_overflow=False)
#             test_level = self._calculate_audio_level(test_data)
#             logger.info(f"Audio initialized. Test level: {test_level:.2f}dB")
            
#             return True
            
#         except Exception as e:
#             logger.error(f"Error initializing audio: {e}")
#             return False
    
#     def _calculate_audio_level(self, data):
#         """Calculate audio level in decibels using a reliable method"""
#         try:
#             # Convert buffer to numpy array
#             samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            
#             # Prevent division by zero with a small epsilon
#             epsilon = 1e-10
            
#             # Calculate RMS (Root Mean Square)
#             rms = np.sqrt(np.mean(np.square(samples)) + epsilon)
            
#             # Convert to decibels
#             # Reference: maximum possible value for 16-bit audio
#             max_possible_value = 32768.0
            
#             # Calculate dB relative to full scale (dBFS)
#             db_fs = 20 * np.log10(rms / max_possible_value)
            
#             # Convert to a positive scale where:
#             # - Silence is around 0-10 dB
#             # - Normal conversation is around 40-60 dB
#             # - Loud noises are 70+ dB
#             normalized_db = 60 + db_fs  # Shift by 60dB to make it positive
            
#             # Ensure we don't return negative values
#             return max(0, normalized_db)
            
#         except Exception as e:
#             logger.error(f"Error calculating audio level: {e}")
#             return 0
    
#     def _detection_loop(self):
#         """Main loop for noise detection"""
#         logger.info("Noise detection loop started")
        
#         consecutive_loud_samples = 0
#         required_loud_samples = 3  # Number of consecutive samples needed to trigger
        
#         while self.is_listening:
#             try:
#                 # Read audio data
#                 data = self.audio_stream.read(2048, exception_on_overflow=False)
                
#                 # Calculate audio level
#                 audio_level = self._calculate_audio_level(data)
                
#                 # Occasionally log the current level for debugging
#                 if np.random.random() < 0.01:  # 1% chance to log
#                     logger.debug(f"Current audio level: {audio_level:.2f}dB (Threshold: {self.threshold}dB)")
                
#                 # Check if noise exceeds threshold
#                 if audio_level > self.threshold:
#                     consecutive_loud_samples += 1
                    
#                     # Check if we have enough consecutive samples and not in cooldown
#                     current_time = time.time()
#                     time_since_last_alert = current_time - self.last_alert_time
                    
#                     if (consecutive_loud_samples >= required_loud_samples and 
#                         time_since_last_alert > self.cooldown):
                        
#                         logger.info(f"Loud noise detected! Level: {audio_level:.2f}dB")
                        
#                         # Update last alert time
#                         self.last_alert_time = current_time
                        
#                         # Call the callback if set
#                         if self.callback:
#                             self.callback(audio_level)
                        
#                         # Reset counter
#                         consecutive_loud_samples = 0
#                 else:
#                     # Reset counter if current sample is not loud
#                     consecutive_loud_samples = 0
                
#                 # Small delay to prevent excessive CPU usage
#                 time.sleep(0.05)
                
#             except IOError as e:
#                 # Handle common PyAudio errors (buffer overflow, etc.)
#                 logger.warning(f"Audio stream IO error (can be normal): {e}")
#                 time.sleep(0.1)
                
#             except Exception as e:
#                 logger.error(f"Error in noise detection loop: {e}")
#                 time.sleep(0.5)  # Longer delay on error
                
#                 # Try to reinitialize audio if there's a persistent problem
#                 if not self._is_stream_active():
#                     logger.warning("Audio stream appears inactive, attempting to reconnect...")
#                     self._initialize_audio()
    
#     def _is_stream_active(self):
#         """Check if the audio stream is still active"""
#         try:
#             return self.audio_stream and self.audio_stream.is_active()
#         except:
#             return False

#     def list_devices(self):
#         """List all available audio input devices"""
#         devices = []
#         try:
#             p = pyaudio.PyAudio()
#             for i in range(p.get_device_count()):
#                 device_info = p.get_device_info_by_index(i)
#                 if device_info['maxInputChannels'] > 0:
#                     devices.append({
#                         'index': i,
#                         'name': device_info['name'],
#                         'channels': device_info['maxInputChannels'],
#                         'sample_rate': device_info['defaultSampleRate']
#                     })
#             p.terminate()
#             return devices
#         except Exception as e:
#             logger.error(f"Error listing devices: {e}")
#             return []
    
#     def select_device(self, device_index):
#         """Select a specific audio input device"""
#         try:
#             # Stop current stream if active
#             if self.is_listening:
#                 self.stop()
                
#             # Close current resources
#             if self.audio_stream:
#                 self.audio_stream.stop_stream()
#                 self.audio_stream.close()
#                 self.audio_stream = None
            
#             if self.pyaudio_instance:
#                 self.pyaudio_instance.terminate()
#                 self.pyaudio_instance = None
            
#             # Initialize PyAudio
#             self.pyaudio_instance = pyaudio.PyAudio()
            
#             # Validate device exists
#             device_info = self.pyaudio_instance.get_device_info_by_index(device_index)
#             if device_info['maxInputChannels'] <= 0:
#                 logger.error(f"Device {device_index} is not an input device")
#                 return False
            
#             # Open stream with selected device
#             self.audio_stream = self.pyaudio_instance.open(
#                 format=pyaudio.paInt16,
#                 channels=1,
#                 rate=44100,
#                 input=True,
#                 input_device_index=device_index,
#                 frames_per_buffer=2048
#             )
            
#             # Test stream
#             test_data = self.audio_stream.read(2048, exception_on_overflow=False)
#             test_level = self._calculate_audio_level(test_data)
            
#             logger.info(f"Selected device {device_index}: {device_info['name']}. Test level: {test_level:.2f}dB")
#             return True
            
#         except Exception as e:
#             logger.error(f"Error selecting device {device_index}: {e}")
#             return False

#     def get_device_diagnostics(self):
#         """Get detailed diagnostic information about the audio system"""
#         try:
#             # Get device info
#             devices = self.list_devices()
            
#             # Collect sample data
#             samples = []
#             if self.audio_stream:
#                 for _ in range(5):  # Get 5 samples
#                     data = self.audio_stream.read(2048, exception_on_overflow=False)
#                     audio_data = np.frombuffer(data, dtype=np.int16)
                    
#                     # Calculate statistics
#                     rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
#                     max_value = np.max(np.abs(audio_data)) if len(audio_data) > 0 else 0
#                     level = self._calculate_audio_level(data)
                    
#                     samples.append({
#                         "rms": float(rms),
#                         "max_value": int(max_value),
#                         "level": float(level)
#                     })
#                     time.sleep(0.1)
            
#             return {
#                 "devices": devices,
#                 "samples": samples,
#                 "threshold": float(self.threshold),
#                 "is_listening": self.is_listening
#             }
            
#         except Exception as e:
#             logger.error(f"Error getting diagnostics: {e}")
#             return {
#                 "error": str(e),
#                 "devices": [],
#                 "samples": [],
#                 "threshold": float(self.threshold),
#                 "is_listening": self.is_listening
#             }

# app = Flask(__name__)

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"

# # 🔹 Initialize Firebase Admin SDK
# cred = credentials.Certificate("cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'cloudpetproject1.appspot.com'})

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam

# # # Global variables for audio detection
# # sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# # Initialize Noise Detector
# noise_detector = NoiseDetector(threshold=30, cooldown=10)  # Default values


# # Global variables for object detection
# detection_model = None
# category_index = None
# detection_enabled = False
# target_object = None  # Object that triggers monitoring (e.g., "couch")
# monitor_object = None  # Object to watch for (e.g., "cat")
# cooldown_period = 10  # Seconds between alerts for the same detection
# last_detection_time = None
# detection_threshold = 0.5  # Confidence threshold for detection
# proximity_threshold = 0.2  # How close objects need to be (as a fraction of image size)


# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# # @app.route('/')
# # def index():
# #     # Start noise detection automatically for testing
# #     # global is_listening
# #     # if not is_listening:
# #     #     setup_audio_detection()
# #     #     is_listening = True
# #     #     threading.Thread(target=noise_detection_loop, daemon=True).start()
# #     #     print("🔄 Noise detection started automatically")
    
# #     return render_template('index.html')

# @app.route('/')
# def index():
#     # Ensure noise detector is running
#     global noise_detector
#     if not noise_detector.is_listening:
#         logger.info("🔄 Starting noise detection from index page")
#         noise_detector.start(callback=on_noise_detected)
    
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# # @app.route('/toggle_recording', methods=['POST'])
# # def toggle_recording():
# #     global is_recording, out, start_time, video_filename

# #     if is_recording:
# #         is_recording = False
# #         if out is not None:
# #             out.release()  # Stop video recording

# #         print("🛑 Video recording stopped!")
        
# #         # Upload to Firebase Storage
# #         video_url = upload_video(video_filename)
        
# #         # Send to Slack
# #         if video_url:
# #             send_slack_video(video_url)

# #         return jsonify({
# #             "status": "stopped",
# #             "message": "Recording stopped",
# #             "video_url": video_url if video_url else None
# #         }), 200
# #     else:
# #         is_recording = True
# #         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# #         video_filename = f"recording_{start_time}.mp4"
        
# #         # Use MP4V codec (H.264) for mp4 files
# #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
# #         # Get the camera dimensions
# #         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# #         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
# #         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

# #         print(f"🔴 Video recording started! Saving to {video_filename}")

# #         return jsonify({
# #             "status": "recording",
# #             "message": "Recording started",
# #             "video_url": video_filename
# #         }), 200

# #this test for 60 min max
# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         # Add a timer to stop recording after 60 minutes
#         def stop_after_timeout():
#             global is_recording
#             time.sleep(60 * 60)  # 60 minutes in seconds
#             if is_recording:
#                 print("🕒 Maximum recording time (60 minutes) reached. Stopping recording.")
#                 requests.post('http://localhost:5000/toggle_recording')
                
#         # Start timer in a separate thread
#         timer_thread = threading.Thread(target=stop_after_timeout)
#         timer_thread.daemon = True
#         timer_thread.start()

#         print(f"🔴 Video recording started! Saving to {video_filename} (Max 60 minutes)")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started (Max 60 minutes)",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage with correct MIME type
#     try:
#         blob = bucket.blob(f"videos/{filename}")
        
#         # Set the correct MIME type for MP4
#         blob.content_type = 'video/mp4'
        
#         # Set content disposition to inline so browsers will play it
#         blob.content_disposition = 'inline'
        
#         # Upload the file
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {
#         "text": "🎥 Video Recording Uploaded!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "🎥 *Video Recording Uploaded!*"
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"<{video_url}|Click here to view or download the video>"
#                 }
#             }
#         ]
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# # #noise detection 
# # def noise_detection_loop():
# #     """Main loop for noise detection"""
# #     global is_listening, audio_stream, last_noise_alert_time
    
# #     print("🔊 Noise detection started")
    
# #     while is_listening:
# #         try:
# #             # Read audio data
# #             data = audio_stream.read(1024, exception_on_overflow=False)
            
# #             # Calculate audio level
# #             audio_level = calculate_audio_level(data)
            
# #             # Log the audio level periodically for debugging
# #             if random.random() < 0.02:  # Log roughly 2% of readings
# #                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
# #             # Check if noise exceeds threshold and not in cooldown period
# #             current_time = time.time()
# #             cooldown_elapsed = True
            
# #             if last_noise_alert_time is not None:
# #                 elapsed_time = current_time - last_noise_alert_time
# #                 cooldown_elapsed = elapsed_time > noise_cooldown_seconds
                
# #             if audio_level > noise_threshold and cooldown_elapsed:
# #                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
# #                 # Update last alert time for cooldown
# #                 last_noise_alert_time = current_time
                
# #                 # Capture screenshot
# #                 filename, timestamp = capture_screenshot()
                
# #                 if filename:
# #                     print(f"📸 Screenshot captured: {filename}")
# #                     # Upload to Firebase
# #                     image_url = upload_screenshot(filename, timestamp)
                    
# #                     # Record noise event in Firestore
# #                     record_noise_event(audio_level, timestamp, image_url)
                    
# #                     # Send to Slack
# #                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
# #                 else:
# #                     print("❌ Screenshot capture failed")
            
# #             # Small delay to prevent excessive CPU usage
# #             time.sleep(0.1)
# #         except IOError as e:
# #             # Common PyAudio error that we can recover from
# #             print(f"⚠️ Audio stream IOError (can be normal): {e}")
# #             time.sleep(0.2)
# #         except Exception as e:
# #             print(f"❌ Error in noise detection loop: {e}")
# #             time.sleep(1)  # Wait before retrying

 


# # def record_noise_event(level, timestamp, image_url):
# #     """Record noise event in Firestore for dashboard reporting"""
# #     event_data = {
# #         "timestamp": timestamp,
# #         "level": float(level),
# #         "image_url": image_url,
# #         "date": datetime.now().strftime("%Y-%m-%d"),
# #         "hour": datetime.now().hour,
# #         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
# #         "month": datetime.now().strftime("%Y-%m")
# #     }
    
# #     # Add to noise_events collection
# #     db.collection("noise_events").document(timestamp).set(event_data)
# #     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# # here using claude version 22/3/2025
# @app.route('/start_noise_detection', methods=['POST'])
# def start_noise_detection():
#     global noise_detector
    
#     # Get custom threshold if provided
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_detector.set_threshold(float(data['threshold']))
#         except (ValueError, TypeError):
#             pass
    
#     # Start detection with callback
#     success = noise_detector.start(callback=on_noise_detected)
    
#     if success:
#         return jsonify({
#             "status": "success", 
#             "message": f"Noise detection started with threshold {noise_detector.threshold} dB"
#         })
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "Failed to start noise detection"
#         }), 500

# @app.route('/stop_noise_detection', methods=['POST'])
# def stop_noise_detection():
#     global noise_detector
    
#     success = noise_detector.stop()
    
#     if success:
#         return jsonify({
#             "status": "success", 
#             "message": "Noise detection stopped"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection not running"
#         })

# @app.route('/set_noise_threshold', methods=['POST'])
# def set_noise_threshold():
#     global noise_detector
    
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             success = noise_detector.set_threshold(float(data['threshold']))
#             if success:
#                 return jsonify({
#                     "status": "success", 
#                     "message": f"Noise threshold set to {noise_detector.threshold} dB"
#                 })
#             else:
#                 return jsonify({
#                     "status": "error", 
#                     "message": "Failed to set threshold"
#                 }), 400
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid threshold value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No threshold provided"
#         }), 400

# @app.route('/set_cooldown', methods=['POST'])
# def set_cooldown():
#     global noise_detector
    
#     data = request.get_json()
#     if data and 'cooldown' in data:
#         try:
#             success = noise_detector.set_cooldown(int(data['cooldown']))
#             if success:
#                 return jsonify({
#                     "status": "success", 
#                     "message": f"Noise alert cooldown set to {noise_detector.cooldown} seconds"
#                 })
#             else:
#                 return jsonify({
#                     "status": "error", 
#                     "message": "Failed to set cooldown"
#                 }), 400
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid cooldown value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No cooldown value provided"
#         }), 400

# @app.route('/test_audio', methods=['GET'])
# def test_audio():
#     global noise_detector
    
#     try:
#         level = noise_detector.get_current_level()
        
#         return jsonify({
#             "status": "success",
#             "audio_level": float(level),
#             "threshold": float(noise_detector.threshold)
#         })
#     except Exception as e:
#         logger.error(f"Error in test_audio: {e}")
#         return jsonify({
#             "status": "error",
#             "message": f"Audio test failed: {str(e)}"
#         }), 500

# @app.route('/debug_audio', methods=['GET'])
# def debug_audio():
#     global noise_detector
    
#     try:
#         diagnostics = noise_detector.get_device_diagnostics()
#         diagnostics["status"] = "success"
#         return jsonify(diagnostics)
#     except Exception as e:
#         logger.error(f"Error in debug_audio: {e}")
#         return jsonify({
#             "status": "error",
#             "message": f"Audio diagnostic failed: {str(e)}"
#         }), 500

# @app.route('/list_audio_devices', methods=['GET'])
# def list_audio_devices():
#     global noise_detector
    
#     try:
#         devices = noise_detector.list_devices()
#         return jsonify({
#             "status": "success",
#             "devices": devices
#         })
#     except Exception as e:
#         logger.error(f"Error listing audio devices: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/select_audio_device', methods=['POST'])
# def select_audio_device():
#     global noise_detector
    
#     data = request.get_json()
#     if not data or 'device_index' not in data:
#         return jsonify({
#             "status": "error",
#             "message": "No device index provided"
#         }), 400
    
#     try:
#         device_index = int(data['device_index'])
#         success = noise_detector.select_device(device_index)
        
#         if success:
#             # Get current level with new device
#             level = noise_detector.get_current_level()
            
#             return jsonify({
#                 "status": "success",
#                 "message": f"Audio device {device_index} selected successfully",
#                 "audio_level": float(level)
#             })
#         else:
#             return jsonify({
#                 "status": "error",
#                 "message": f"Failed to select device {device_index}"
#             }), 500
#     except Exception as e:
#         logger.error(f"Error selecting audio device: {e}")
#         return jsonify({
#             "status": "error",
#             "message": f"Error selecting audio device: {str(e)}"
#         }), 500



# # Callback function for noise detection
# # def on_noise_detected(level):
# #     """Callback function when noise is detected"""
# #     try:
# #         # Capture screenshot
# #         filename, timestamp = capture_screenshot()
        
# #         if filename:
# #             # Upload to Firebase
# #             image_url = upload_screenshot(filename, timestamp)
            
# #             # Record noise event in Firestore
# #             record_noise_event(level, timestamp, image_url)
            
# #             # Send notification to Slack
# #             send_noise_alert_to_slack(level, image_url, timestamp)
            
# #             # Log success
# #             print(f"✅ Noise event recorded: {level:.2f} dB")
# #         else:
# #             print("❌ Failed to capture screenshot for noise event")
            
# #     except Exception as e:
# #         print(f"❌ Error processing noise event: {e}")

# def on_noise_detected(level):
#     """Callback function when noise is detected"""
#     logger.info(f"🔔 NOISE DETECTED - Level: {level:.2f} dB")
    
#     try:
#         # Capture screenshot
#         logger.info("📸 Capturing screenshot...")
#         filename, timestamp = capture_screenshot()
        
#         if filename:
#             logger.info(f"📸 Screenshot captured: {filename}")
            
#             # Upload to Firebase
#             logger.info("☁️ Uploading screenshot to Firebase...")
#             image_url = upload_screenshot(filename, timestamp)
            
#             # Record noise event in Firestore
#             logger.info("📝 Recording noise event in Firestore...")
#             event_data = record_noise_event(level, timestamp, image_url)
            
#             # Send notification to Slack
#             logger.info("📨 Sending notification to Slack...")
#             send_noise_alert_to_slack(level, image_url, timestamp)
            
#             # Log success
#             logger.info(f"✅ Noise event fully processed: {level:.2f} dB at {timestamp}")
            
#             # Clean up local file if desired
#             try:
#                 os.remove(filename)
#                 logger.info(f"🧹 Cleaned up local file: {filename}")
#             except Exception as e:
#                 logger.warning(f"⚠️ Could not remove local file {filename}: {e}")
            
#             return True
#         else:
#             logger.error("❌ Failed to capture screenshot for noise event")
#             return False
            
#     except Exception as e:
#         logger.error(f"❌ Error processing noise event: {e}")
#         import traceback
#         logger.error(traceback.format_exc())
#         return False


# # testing to add yearly
# def record_noise_event(level, timestamp, image_url):
#     """Record noise event in Firestore for dashboard reporting"""
#     # Parse timestamp from format YYYYMMdd_HHMMSS to a datetime object
#     try:
#         event_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
#     except Exception as e:
#         logger.error(f"Error parsing timestamp {timestamp}: {e}")
#         event_time = datetime.now()  # Fallback to current time
    
#     # Create event data with correctly formatted fields
#     event_data = {
#         "timestamp": timestamp,
#         "level": float(level),
#         "image_url": image_url,
#         "date": event_time.strftime("%Y-%m-%d"),
#         "hour": event_time.hour,
#         "week": event_time.strftime("%Y-W%U"),  # Year-Week format
#         "month": event_time.strftime("%Y-%m"),
#         "year": event_time.strftime("%Y")  # Add year
#     }
    
#     # Add to noise_events collection
#     db.collection("noise_events").document(timestamp).set(event_data)
#     logger.info(f"✅ Noise event recorded in Firestore: {level:.2f} dB")
#     return event_data


# #add a new endpoint to get yearly data
# @app.route('/get_yearly_data', methods=['GET'])
# def get_yearly_data():
#     try:
#         # Get current year
#         now = datetime.now()
#         current_year = now.strftime("%Y")
        
#         # Initialize yearly data (monthly counts for the current year)
#         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         yearly_data = [0] * 12
        
#         # Query for each month in the current year
#         for month_idx in range(12):
#             month_num = month_idx + 1
#             month_query = db.collection("noise_events").where(
#                 "month", "==", f"{current_year}-{month_num:02d}")
#             month_count = len(list(month_query.stream()))
#             yearly_data[month_idx] = month_count
        
#         return jsonify({
#             "status": "success",
#             "yearly_data": yearly_data,
#             "months": months
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting yearly data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "yearly_data": [0] * 12,
#             "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         }), 500

# def send_noise_alert_to_slack(level, image_url, timestamp):
#     """Send noise alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     message = {
#         "text": f"🔊 Loud Noise Detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"Noise Event Screenshot ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Noise event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print("✅ Noise alert sent to Slack")

# @app.route('/noise_detector_status', methods=['GET'])
# def noise_detector_status():
#     """Return detailed status of the noise detector for troubleshooting"""
#     global noise_detector
    
#     try:
#         # Get current audio level
#         current_level = noise_detector.get_current_level()
        
#         # Get active device info
#         devices = noise_detector.list_devices()
#         active_device = None
#         for device in devices:
#             if device.get('active', False):
#                 active_device = device
        
#         # Collect status info
#         status_info = {
#             "status": "success",
#             "is_listening": noise_detector.is_listening,
#             "threshold": noise_detector.threshold,
#             "cooldown": noise_detector.cooldown,
#             "current_level": float(current_level),
#             "last_alert_time": noise_detector.last_alert_time,
#             "time_since_last_alert": time.time() - noise_detector.last_alert_time if noise_detector.last_alert_time else None,
#             "audio_stream_active": noise_detector._is_stream_active(),
#             "active_device": active_device,
#             "available_devices": devices,
#             "system_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
        
#         return jsonify(status_info)
#     except Exception as e:
#         logger.error(f"Error getting noise detector status: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "error_type": str(type(e)),
#             "error_traceback": str(e.__traceback__)
#         }), 500



# # Add this route to get noise data for the dashboard
# # add the year data
# # Add this at line 650 or so, after the get_noise_data route declaration
# @app.route('/get_noise_data', methods=['GET'])
# def get_noise_data():
#     try:
#         # Get current date and time
#         now = datetime.now()
#         today = now.strftime("%Y-%m-%d")
#         current_week = now.strftime("%Y-W%U")
#         current_month = now.strftime("%Y-%m")
#         current_year = now.strftime("%Y")
        
#         # Initialize data structures
#         daily_data = [0] * 24
#         weekly_data = [0] * 7
#         monthly_data = [0] * 31  # Maximum days in a month
#         yearly_data = [0] * 12   # 12 months in a year
#         recent_events = []
        
#         # Query Firestore for noise events
#         # Daily data (today's events by hour)
#         daily_query = db.collection("noise_events").where("date", "==", today)
#         daily_results = list(daily_query.stream())
        
#         for doc in daily_results:
#             data = doc.to_dict()
#             hour = data.get('hour', 0)
#             if 0 <= hour < 24:
#                 daily_data[hour] += 1
        
#         # Weekly data (this week's events by day)
#         # Calculate start of week (Sunday)
#         start_of_week = now - timedelta(days=now.weekday() + 1)
#         for day in range(7):
#             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             weekly_data[day] = day_count
        
#         # Monthly data (this month's events by day)
#         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
#         for day in range(1, days_in_month + 1):
#             day_str = f"{day:02d}"
#             month_str = f"{now.month:02d}"
#             date = f"{now.year}-{month_str}-{day_str}"
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             monthly_data[day - 1] = day_count
            
#         # Yearly data (this year's events by month)
#         for month in range(1, 13):
#             month_prefix = f"{current_year}-{month:02d}"
#             month_query = db.collection("noise_events").where(
#                 "month", "==", month_prefix)
#             month_count = len(list(month_query.stream()))
#             yearly_data[month - 1] = month_count
        
#         # Recent events (limit to 10)
#         recent_query = (db.collection("noise_events")
#                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
#                         .limit(10))
        
#         recent_docs = list(recent_query.stream())
#         for doc in recent_docs:
#             data = doc.to_dict()
#             # Convert timestamp string to datetime for proper sorting
#             try:
#                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
#                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             except:
#                 formatted_timestamp = data.get('timestamp', '')
                
#             recent_events.append({
#                 "timestamp": data.get('timestamp', ''),
#                 "level": data.get('level', 0),
#                 "image_url": data.get('image_url', '')
#             })
        
#         return jsonify({
#             "status": "success",
#             "daily_data": daily_data,
#             "weekly_data": weekly_data,
#             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
#             "yearly_data": yearly_data,
#             "recent_events": recent_events
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting noise data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "daily_data": [0] * 24,
#             "weekly_data": [0] * 7,
#             "monthly_data": [0] * 31,
#             "yearly_data": [0] * 12,
#             "recent_events": []
#         }), 500



# ## Object detection
# # ==========================
# # 📌 OBJECT DETECTION SCREENSHOT
# # ==========================
# @app.route('/object_detection_screenshot', methods=['POST'])
# def object_detection_screenshot():
#     data = request.get_json()
#     primary_object = data.get('primaryObject', 'object')
#     secondary_object = data.get('secondaryObject', 'location')
    
#     # Capture the screenshot
#     filename, timestamp = capture_screenshot()
    
#     if filename:
#         # Upload to Firebase
#         image_url = upload_screenshot(filename, timestamp)
        
#         # Record detection event in Firestore
#         event_data = {
#             "timestamp": timestamp,
#             "primaryObject": primary_object,
#             "secondaryObject": secondary_object,
#             "image_url": image_url,
#             "date": datetime.now().strftime("%Y-%m-%d"),
#             "hour": datetime.now().hour,
#             "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#             "month": datetime.now().strftime("%Y-%m")
#         }
        
#         # Add to detection_events collection
#         db.collection("detection_events").document(timestamp).set(event_data)
        
#         # Send to Slack
#         send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"{primary_object} near {secondary_object} detected!",
#             "image_url": image_url
#         })
    
#     return jsonify({
#         "status": "error", 
#         "message": "Failed to capture screenshot"
#     }), 500

# def send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp):
#     """Send object detection alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     emoji_map = {
#         "cat": "🐱",
#         "dog": "🐶",
#         "bird": "🐦",
#         "person": "👤",
#         "couch": "🛋️",
#         "bed": "🛏️",
#         "laptop": "💻",
#         "keyboard": "⌨️",
#         "cell phone": "📱",
#         "tv": "📺",
#         "oven": "🔥"
#     }
    
#     primary_emoji = emoji_map.get(primary_object.lower(), "📷")
#     secondary_emoji = emoji_map.get(secondary_object.lower(), "📍")
    
#     message = {
#         "text": f"{primary_emoji} {primary_object.title()} near {secondary_object} detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*{primary_emoji} {primary_object.title()} near {secondary_object} detected! {secondary_emoji}*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"{primary_object.title()} near {secondary_object} ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Detection event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print(f"✅ Object detection alert sent to Slack: {primary_object} near {secondary_object}")


# # ==========================
# # 📌 Backend API for Gallery
# # ==========================
# @app.route('/get_screenshots', methods=['GET'])
# def get_screenshots():
#     try:
#         # Get manual screenshots
#         manual_screenshots = []
#         screenshots_ref = db.collection("screenshots").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in screenshots_ref:
#             data = doc.to_dict()
#             manual_screenshots.append(data)
        
#         # Get noise detection screenshots
#         noise_screenshots = []
#         noise_ref = db.collection("noise_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in noise_ref:
#             data = doc.to_dict()
#             noise_screenshots.append(data)
        
#         # Get object detection screenshots
#         object_screenshots = []
#         object_ref = db.collection("detection_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in object_ref:
#             data = doc.to_dict()
#             object_screenshots.append(data)
        
#         # Get video recordings
#         videos = []
#         videos_ref = db.collection("videos").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()
#         for doc in videos_ref:
#             data = doc.to_dict()
#             videos.append(data)
            
#         return jsonify({
#             "status": "success",
#             "manual_screenshots": manual_screenshots,
#             "noise_screenshots": noise_screenshots,
#             "object_screenshots": object_screenshots,
#             "videos": videos
#         })
    
#     except Exception as e:
#         print(f"❌ Error fetching gallery data: {e}")
#         return jsonify({
#             "status": "error", 
#             "message": str(e),
#             "manual_screenshots": [],
#             "noise_screenshots": [],
#             "object_screenshots": [],
#             "videos": []
#         }), 500
    
# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     # Initialize noise detector
#     logger.info("Starting application and initializing noise detector...")
#     noise_detector.start(callback=on_noise_detected)
    
#     # Auto-start noise detection
#     if noise_detector._initialize_audio():
#         logger.info("✅ Noise detector initialized successfully")
#     else:
#         logger.warning("⚠️ Noise detector initialization failed")
    
#     # Register cleanup handler
#     atexit.register(lambda: noise_detector.stop())
    
#     # Run the Flask app
#     app.run(debug=True)





















# all fucntions works
# code here try change the env, login authentication, responsive web design
# responsive web design done, code down try recording with sound and login,, do video first
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime, timedelta
# import requests
# from flask import Flask, request, render_template, Response, jsonify
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess
# import atexit
# import sys
# import pyaudio
# import numpy as np
# import random  # For our debug logging
# from collections import defaultdict
# import logging
# from dotenv import load_dotenv


# # Set up logging
# logging.basicConfig(level=logging.INFO, 
#                     format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger('noise_detection')
# class NoiseDetector:
#     def __init__(self, threshold=30, cooldown=10):
#         """Initialize the noise detector with configurable threshold and cooldown"""
#         self.threshold = threshold  # Default threshold in dB
#         self.cooldown = cooldown    # Default cooldown in seconds
#         self.is_listening = False   # Tracking if detector is active
#         self.audio_stream = None    # PyAudio stream
#         self.pyaudio_instance = None  # PyAudio instance
#         self.detection_thread = None  # Thread for detection loop
#         self.last_alert_time = 0    # Last time an alert was triggered
#         self.callback = None        # Callback for when noise is detected
        
#     def start(self, callback=None):
#         """Start the noise detection"""
#         if self.is_listening:
#             logger.warning("Noise detection already running")
#             return False
        
#         self.callback = callback
        
#         # Initialize PyAudio if not already done
#         if not self._initialize_audio():
#             logger.error("Failed to initialize audio")
#             return False
        
#         # Start detection thread
#         self.is_listening = True
#         self.detection_thread = threading.Thread(target=self._detection_loop)
#         self.detection_thread.daemon = True
#         self.detection_thread.start()
#         logger.info(f"Noise detection started with threshold {self.threshold}dB")
#         return True
    
#     def stop(self):
#         """Stop the noise detection"""
#         if not self.is_listening:
#             logger.warning("Noise detection not running")
#             return False
        
#         self.is_listening = False
#         # Thread will exit on its own due to while loop condition
#         logger.info("Noise detection stopped")
#         return True
    
#     def set_threshold(self, threshold):
#         """Set the noise detection threshold"""
#         try:
#             self.threshold = float(threshold)
#             logger.info(f"Threshold set to {self.threshold}dB")
#             return True
#         except (ValueError, TypeError):
#             logger.error(f"Invalid threshold value: {threshold}")
#             return False
    
#     def set_cooldown(self, cooldown):
#         """Set the cooldown period between alerts"""
#         try:
#             self.cooldown = int(cooldown)
#             logger.info(f"Cooldown set to {self.cooldown} seconds")
#             return True
#         except (ValueError, TypeError):
#             logger.error(f"Invalid cooldown value: {cooldown}")
#             return False
    
#     def get_current_level(self):
#         """Get the current audio level"""
#         if not self.audio_stream:
#             if not self._initialize_audio():
#                 return 0
        
#         try:
#             # Read audio data
#             data = self.audio_stream.read(2048, exception_on_overflow=False)
#             # Calculate level
#             level = self._calculate_audio_level(data)
#             return level
#         except Exception as e:
#             logger.error(f"Error getting audio level: {e}")
#             return 0
    
#     def _initialize_audio(self):
#         """Initialize the audio system with proper error handling"""
#         try:
#             # Clean up existing resources if any
#             if self.audio_stream:
#                 self.audio_stream.stop_stream()
#                 self.audio_stream.close()
            
#             if self.pyaudio_instance:
#                 self.pyaudio_instance.terminate()
            
#             # Initialize PyAudio
#             self.pyaudio_instance = pyaudio.PyAudio()
            
#             # Find input devices
#             input_devices = []
#             for i in range(self.pyaudio_instance.get_device_count()):
#                 device_info = self.pyaudio_instance.get_device_info_by_index(i)
#                 if device_info['maxInputChannels'] > 0:
#                     input_devices.append(i)
#                     logger.info(f"Found input device {i}: {device_info['name']}")
            
#             if not input_devices:
#                 logger.error("No audio input devices found")
#                 return False
            
#             # Try to open the default input device first (usually index 0)
#             device_to_use = input_devices[0]
            
#             # Open audio stream
#             self.audio_stream = self.pyaudio_instance.open(
#                 format=pyaudio.paInt16,
#                 channels=1,
#                 rate=44100,
#                 input=True,
#                 input_device_index=device_to_use,
#                 frames_per_buffer=2048
#             )
            
#             # Test the stream
#             test_data = self.audio_stream.read(2048, exception_on_overflow=False)
#             test_level = self._calculate_audio_level(test_data)
#             logger.info(f"Audio initialized. Test level: {test_level:.2f}dB")
            
#             return True
            
#         except Exception as e:
#             logger.error(f"Error initializing audio: {e}")
#             return False
    
#     def _calculate_audio_level(self, data):
#         """Calculate audio level in decibels using a reliable method"""
#         try:
#             # Convert buffer to numpy array
#             samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            
#             # Prevent division by zero with a small epsilon
#             epsilon = 1e-10
            
#             # Calculate RMS (Root Mean Square)
#             rms = np.sqrt(np.mean(np.square(samples)) + epsilon)
            
#             # Convert to decibels
#             # Reference: maximum possible value for 16-bit audio
#             max_possible_value = 32768.0
            
#             # Calculate dB relative to full scale (dBFS)
#             db_fs = 20 * np.log10(rms / max_possible_value)
            
#             # Convert to a positive scale where:
#             # - Silence is around 0-10 dB
#             # - Normal conversation is around 40-60 dB
#             # - Loud noises are 70+ dB
#             normalized_db = 60 + db_fs  # Shift by 60dB to make it positive
            
#             # Ensure we don't return negative values
#             return max(0, normalized_db)
            
#         except Exception as e:
#             logger.error(f"Error calculating audio level: {e}")
#             return 0
    
#     def _detection_loop(self):
#         """Main loop for noise detection"""
#         logger.info("Noise detection loop started")
        
#         consecutive_loud_samples = 0
#         required_loud_samples = 3  # Number of consecutive samples needed to trigger
        
#         while self.is_listening:
#             try:
#                 # Read audio data
#                 data = self.audio_stream.read(2048, exception_on_overflow=False)
                
#                 # Calculate audio level
#                 audio_level = self._calculate_audio_level(data)
                
#                 # Occasionally log the current level for debugging
#                 if np.random.random() < 0.01:  # 1% chance to log
#                     logger.debug(f"Current audio level: {audio_level:.2f}dB (Threshold: {self.threshold}dB)")
                
#                 # Check if noise exceeds threshold
#                 if audio_level > self.threshold:
#                     consecutive_loud_samples += 1
                    
#                     # Check if we have enough consecutive samples and not in cooldown
#                     current_time = time.time()
#                     time_since_last_alert = current_time - self.last_alert_time
                    
#                     if (consecutive_loud_samples >= required_loud_samples and 
#                         time_since_last_alert > self.cooldown):
                        
#                         logger.info(f"Loud noise detected! Level: {audio_level:.2f}dB")
                        
#                         # Update last alert time
#                         self.last_alert_time = current_time
                        
#                         # Call the callback if set
#                         if self.callback:
#                             self.callback(audio_level)
                        
#                         # Reset counter
#                         consecutive_loud_samples = 0
#                 else:
#                     # Reset counter if current sample is not loud
#                     consecutive_loud_samples = 0
                
#                 # Small delay to prevent excessive CPU usage
#                 time.sleep(0.05)
                
#             except IOError as e:
#                 # Handle common PyAudio errors (buffer overflow, etc.)
#                 logger.warning(f"Audio stream IO error (can be normal): {e}")
#                 time.sleep(0.1)
                
#             except Exception as e:
#                 logger.error(f"Error in noise detection loop: {e}")
#                 time.sleep(0.5)  # Longer delay on error
                
#                 # Try to reinitialize audio if there's a persistent problem
#                 if not self._is_stream_active():
#                     logger.warning("Audio stream appears inactive, attempting to reconnect...")
#                     self._initialize_audio()
    
#     def _is_stream_active(self):
#         """Check if the audio stream is still active"""
#         try:
#             return self.audio_stream and self.audio_stream.is_active()
#         except:
#             return False

#     def list_devices(self):
#         """List all available audio input devices"""
#         devices = []
#         try:
#             p = pyaudio.PyAudio()
#             for i in range(p.get_device_count()):
#                 device_info = p.get_device_info_by_index(i)
#                 if device_info['maxInputChannels'] > 0:
#                     devices.append({
#                         'index': i,
#                         'name': device_info['name'],
#                         'channels': device_info['maxInputChannels'],
#                         'sample_rate': device_info['defaultSampleRate']
#                     })
#             p.terminate()
#             return devices
#         except Exception as e:
#             logger.error(f"Error listing devices: {e}")
#             return []
    
#     def select_device(self, device_index):
#         """Select a specific audio input device"""
#         try:
#             # Stop current stream if active
#             if self.is_listening:
#                 self.stop()
                
#             # Close current resources
#             if self.audio_stream:
#                 self.audio_stream.stop_stream()
#                 self.audio_stream.close()
#                 self.audio_stream = None
            
#             if self.pyaudio_instance:
#                 self.pyaudio_instance.terminate()
#                 self.pyaudio_instance = None
            
#             # Initialize PyAudio
#             self.pyaudio_instance = pyaudio.PyAudio()
            
#             # Validate device exists
#             device_info = self.pyaudio_instance.get_device_info_by_index(device_index)
#             if device_info['maxInputChannels'] <= 0:
#                 logger.error(f"Device {device_index} is not an input device")
#                 return False
            
#             # Open stream with selected device
#             self.audio_stream = self.pyaudio_instance.open(
#                 format=pyaudio.paInt16,
#                 channels=1,
#                 rate=44100,
#                 input=True,
#                 input_device_index=device_index,
#                 frames_per_buffer=2048
#             )
            
#             # Test stream
#             test_data = self.audio_stream.read(2048, exception_on_overflow=False)
#             test_level = self._calculate_audio_level(test_data)
            
#             logger.info(f"Selected device {device_index}: {device_info['name']}. Test level: {test_level:.2f}dB")
#             return True
            
#         except Exception as e:
#             logger.error(f"Error selecting device {device_index}: {e}")
#             return False

#     def get_device_diagnostics(self):
#         """Get detailed diagnostic information about the audio system"""
#         try:
#             # Get device info
#             devices = self.list_devices()
            
#             # Collect sample data
#             samples = []
#             if self.audio_stream:
#                 for _ in range(5):  # Get 5 samples
#                     data = self.audio_stream.read(2048, exception_on_overflow=False)
#                     audio_data = np.frombuffer(data, dtype=np.int16)
                    
#                     # Calculate statistics
#                     rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
#                     max_value = np.max(np.abs(audio_data)) if len(audio_data) > 0 else 0
#                     level = self._calculate_audio_level(data)
                    
#                     samples.append({
#                         "rms": float(rms),
#                         "max_value": int(max_value),
#                         "level": float(level)
#                     })
#                     time.sleep(0.1)
            
#             return {
#                 "devices": devices,
#                 "samples": samples,
#                 "threshold": float(self.threshold),
#                 "is_listening": self.is_listening
#             }
            
#         except Exception as e:
#             logger.error(f"Error getting diagnostics: {e}")
#             return {
#                 "error": str(e),
#                 "devices": [],
#                 "samples": [],
#                 "threshold": float(self.threshold),
#                 "is_listening": self.is_listening
#             }

# app = Flask(__name__)

# load_dotenv()  # Load environment variables from .env file

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "firestore_key.json")

# # 🔹 Initialize Firebase Admin SDK
# firebase_admin_file = os.getenv("FIREBASE_ADMIN_SDK_FILE", "cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# cred = credentials.Certificate(firebase_admin_file)
# firebase_admin.initialize_app(cred, {
#     'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET", "cloudpetproject1.appspot.com")
# })

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
# if not SLACK_WEBHOOK_URL:
#     logger.warning("⚠️ SLACK_WEBHOOK_URL not set in environment variables!")

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam

# # # Global variables for audio detection
# # sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# # Initialize Noise Detector
# noise_detector = NoiseDetector(threshold=30, cooldown=10)  # Default values


# # Global variables for object detection
# detection_model = None
# category_index = None
# detection_enabled = False
# target_object = None  # Object that triggers monitoring (e.g., "couch")
# monitor_object = None  # Object to watch for (e.g., "cat")
# cooldown_period = 10  # Seconds between alerts for the same detection
# last_detection_time = None
# detection_threshold = 0.5  # Confidence threshold for detection
# proximity_threshold = 0.2  # How close objects need to be (as a fraction of image size)


# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# # @app.route('/')
# # def index():
# #     # Start noise detection automatically for testing
# #     # global is_listening
# #     # if not is_listening:
# #     #     setup_audio_detection()
# #     #     is_listening = True
# #     #     threading.Thread(target=noise_detection_loop, daemon=True).start()
# #     #     print("🔄 Noise detection started automatically")
    
# #     return render_template('index.html')

# @app.route('/')
# def index():
#     # Ensure noise detector is running
#     global noise_detector
#     if not noise_detector.is_listening:
#         logger.info("🔄 Starting noise detection from index page")
#         noise_detector.start(callback=on_noise_detected)
    
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(SLACK_WEBHOOK_URL, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# # @app.route('/toggle_recording', methods=['POST'])
# # def toggle_recording():
# #     global is_recording, out, start_time, video_filename

# #     if is_recording:
# #         is_recording = False
# #         if out is not None:
# #             out.release()  # Stop video recording

# #         print("🛑 Video recording stopped!")
        
# #         # Upload to Firebase Storage
# #         video_url = upload_video(video_filename)
        
# #         # Send to Slack
# #         if video_url:
# #             send_slack_video(video_url)

# #         return jsonify({
# #             "status": "stopped",
# #             "message": "Recording stopped",
# #             "video_url": video_url if video_url else None
# #         }), 200
# #     else:
# #         is_recording = True
# #         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# #         video_filename = f"recording_{start_time}.mp4"
        
# #         # Use MP4V codec (H.264) for mp4 files
# #         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
# #         # Get the camera dimensions
# #         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# #         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
# #         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

# #         print(f"🔴 Video recording started! Saving to {video_filename}")

# #         return jsonify({
# #             "status": "recording",
# #             "message": "Recording started",
# #             "video_url": video_filename
# #         }), 200

# #this test for 60 min max
# @app.route('/toggle_recording', methods=['POST'])
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         # Add a timer to stop recording after 60 minutes
#         def stop_after_timeout():
#             global is_recording
#             time.sleep(60 * 60)  # 60 minutes in seconds
#             if is_recording:
#                 print("🕒 Maximum recording time (60 minutes) reached. Stopping recording.")
#                 requests.post('http://localhost:5000/toggle_recording')
                
#         # Start timer in a separate thread
#         timer_thread = threading.Thread(target=stop_after_timeout)
#         timer_thread.daemon = True
#         timer_thread.start()

#         print(f"🔴 Video recording started! Saving to {video_filename} (Max 60 minutes)")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started (Max 60 minutes)",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage with correct MIME type
#     try:
#         blob = bucket.blob(f"videos/{filename}")
        
#         # Set the correct MIME type for MP4
#         blob.content_type = 'video/mp4'
        
#         # Set content disposition to inline so browsers will play it
#         blob.content_disposition = 'inline'
        
#         # Upload the file
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {
#         "text": "🎥 Video Recording Uploaded!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "🎥 *Video Recording Uploaded!*"
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"<{video_url}|Click here to view or download the video>"
#                 }
#             }
#         ]
#     }
#     requests.post(SLACK_WEBHOOK_URL, json=message)


# # #noise detection 
# # def noise_detection_loop():
# #     """Main loop for noise detection"""
# #     global is_listening, audio_stream, last_noise_alert_time
    
# #     print("🔊 Noise detection started")
    
# #     while is_listening:
# #         try:
# #             # Read audio data
# #             data = audio_stream.read(1024, exception_on_overflow=False)
            
# #             # Calculate audio level
# #             audio_level = calculate_audio_level(data)
            
# #             # Log the audio level periodically for debugging
# #             if random.random() < 0.02:  # Log roughly 2% of readings
# #                 print(f"🔊 Current audio level: {audio_level:.2f} dB (Threshold: {noise_threshold} dB)")
            
# #             # Check if noise exceeds threshold and not in cooldown period
# #             current_time = time.time()
# #             cooldown_elapsed = True
            
# #             if last_noise_alert_time is not None:
# #                 elapsed_time = current_time - last_noise_alert_time
# #                 cooldown_elapsed = elapsed_time > noise_cooldown_seconds
                
# #             if audio_level > noise_threshold and cooldown_elapsed:
# #                 print(f"🔔 Loud noise detected! Level: {audio_level:.2f} dB")
                
# #                 # Update last alert time for cooldown
# #                 last_noise_alert_time = current_time
                
# #                 # Capture screenshot
# #                 filename, timestamp = capture_screenshot()
                
# #                 if filename:
# #                     print(f"📸 Screenshot captured: {filename}")
# #                     # Upload to Firebase
# #                     image_url = upload_screenshot(filename, timestamp)
                    
# #                     # Record noise event in Firestore
# #                     record_noise_event(audio_level, timestamp, image_url)
                    
# #                     # Send to Slack
# #                     send_noise_alert_to_slack(audio_level, image_url, timestamp)
# #                 else:
# #                     print("❌ Screenshot capture failed")
            
# #             # Small delay to prevent excessive CPU usage
# #             time.sleep(0.1)
# #         except IOError as e:
# #             # Common PyAudio error that we can recover from
# #             print(f"⚠️ Audio stream IOError (can be normal): {e}")
# #             time.sleep(0.2)
# #         except Exception as e:
# #             print(f"❌ Error in noise detection loop: {e}")
# #             time.sleep(1)  # Wait before retrying

 


# # def record_noise_event(level, timestamp, image_url):
# #     """Record noise event in Firestore for dashboard reporting"""
# #     event_data = {
# #         "timestamp": timestamp,
# #         "level": float(level),
# #         "image_url": image_url,
# #         "date": datetime.now().strftime("%Y-%m-%d"),
# #         "hour": datetime.now().hour,
# #         "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
# #         "month": datetime.now().strftime("%Y-%m")
# #     }
    
# #     # Add to noise_events collection
# #     db.collection("noise_events").document(timestamp).set(event_data)
# #     print(f"✅ Noise event recorded in Firestore: {level:.2f} dB")

# # here using claude version 22/3/2025
# @app.route('/start_noise_detection', methods=['POST'])
# def start_noise_detection():
#     global noise_detector
    
#     # Get custom threshold if provided
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_detector.set_threshold(float(data['threshold']))
#         except (ValueError, TypeError):
#             pass
    
#     # Start detection with callback
#     success = noise_detector.start(callback=on_noise_detected)
    
#     if success:
#         return jsonify({
#             "status": "success", 
#             "message": f"Noise detection started with threshold {noise_detector.threshold} dB"
#         })
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "Failed to start noise detection"
#         }), 500

# @app.route('/stop_noise_detection', methods=['POST'])
# def stop_noise_detection():
#     global noise_detector
    
#     success = noise_detector.stop()
    
#     if success:
#         return jsonify({
#             "status": "success", 
#             "message": "Noise detection stopped"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection not running"
#         })

# @app.route('/set_noise_threshold', methods=['POST'])
# def set_noise_threshold():
#     global noise_detector
    
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             success = noise_detector.set_threshold(float(data['threshold']))
#             if success:
#                 return jsonify({
#                     "status": "success", 
#                     "message": f"Noise threshold set to {noise_detector.threshold} dB"
#                 })
#             else:
#                 return jsonify({
#                     "status": "error", 
#                     "message": "Failed to set threshold"
#                 }), 400
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid threshold value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No threshold provided"
#         }), 400

# @app.route('/set_cooldown', methods=['POST'])
# def set_cooldown():
#     global noise_detector
    
#     data = request.get_json()
#     if data and 'cooldown' in data:
#         try:
#             success = noise_detector.set_cooldown(int(data['cooldown']))
#             if success:
#                 return jsonify({
#                     "status": "success", 
#                     "message": f"Noise alert cooldown set to {noise_detector.cooldown} seconds"
#                 })
#             else:
#                 return jsonify({
#                     "status": "error", 
#                     "message": "Failed to set cooldown"
#                 }), 400
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid cooldown value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No cooldown value provided"
#         }), 400

# @app.route('/test_audio', methods=['GET'])
# def test_audio():
#     global noise_detector
    
#     try:
#         level = noise_detector.get_current_level()
        
#         return jsonify({
#             "status": "success",
#             "audio_level": float(level),
#             "threshold": float(noise_detector.threshold)
#         })
#     except Exception as e:
#         logger.error(f"Error in test_audio: {e}")
#         return jsonify({
#             "status": "error",
#             "message": f"Audio test failed: {str(e)}"
#         }), 500

# @app.route('/debug_audio', methods=['GET'])
# def debug_audio():
#     global noise_detector
    
#     try:
#         diagnostics = noise_detector.get_device_diagnostics()
#         diagnostics["status"] = "success"
#         return jsonify(diagnostics)
#     except Exception as e:
#         logger.error(f"Error in debug_audio: {e}")
#         return jsonify({
#             "status": "error",
#             "message": f"Audio diagnostic failed: {str(e)}"
#         }), 500

# @app.route('/list_audio_devices', methods=['GET'])
# def list_audio_devices():
#     global noise_detector
    
#     try:
#         devices = noise_detector.list_devices()
#         return jsonify({
#             "status": "success",
#             "devices": devices
#         })
#     except Exception as e:
#         logger.error(f"Error listing audio devices: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/select_audio_device', methods=['POST'])
# def select_audio_device():
#     global noise_detector
    
#     data = request.get_json()
#     if not data or 'device_index' not in data:
#         return jsonify({
#             "status": "error",
#             "message": "No device index provided"
#         }), 400
    
#     try:
#         device_index = int(data['device_index'])
#         success = noise_detector.select_device(device_index)
        
#         if success:
#             # Get current level with new device
#             level = noise_detector.get_current_level()
            
#             return jsonify({
#                 "status": "success",
#                 "message": f"Audio device {device_index} selected successfully",
#                 "audio_level": float(level)
#             })
#         else:
#             return jsonify({
#                 "status": "error",
#                 "message": f"Failed to select device {device_index}"
#             }), 500
#     except Exception as e:
#         logger.error(f"Error selecting audio device: {e}")
#         return jsonify({
#             "status": "error",
#             "message": f"Error selecting audio device: {str(e)}"
#         }), 500



# # Callback function for noise detection
# # def on_noise_detected(level):
# #     """Callback function when noise is detected"""
# #     try:
# #         # Capture screenshot
# #         filename, timestamp = capture_screenshot()
        
# #         if filename:
# #             # Upload to Firebase
# #             image_url = upload_screenshot(filename, timestamp)
            
# #             # Record noise event in Firestore
# #             record_noise_event(level, timestamp, image_url)
            
# #             # Send notification to Slack
# #             send_noise_alert_to_slack(level, image_url, timestamp)
            
# #             # Log success
# #             print(f"✅ Noise event recorded: {level:.2f} dB")
# #         else:
# #             print("❌ Failed to capture screenshot for noise event")
            
# #     except Exception as e:
# #         print(f"❌ Error processing noise event: {e}")

# def on_noise_detected(level):
#     """Callback function when noise is detected"""
#     logger.info(f"🔔 NOISE DETECTED - Level: {level:.2f} dB")
    
#     try:
#         # Capture screenshot
#         logger.info("📸 Capturing screenshot...")
#         filename, timestamp = capture_screenshot()
        
#         if filename:
#             logger.info(f"📸 Screenshot captured: {filename}")
            
#             # Upload to Firebase
#             logger.info("☁️ Uploading screenshot to Firebase...")
#             image_url = upload_screenshot(filename, timestamp)
            
#             # Record noise event in Firestore
#             logger.info("📝 Recording noise event in Firestore...")
#             event_data = record_noise_event(level, timestamp, image_url)
            
#             # Send notification to Slack
#             logger.info("📨 Sending notification to Slack...")
#             send_noise_alert_to_slack(level, image_url, timestamp)
            
#             # Log success
#             logger.info(f"✅ Noise event fully processed: {level:.2f} dB at {timestamp}")
            
#             # Clean up local file if desired
#             try:
#                 os.remove(filename)
#                 logger.info(f"🧹 Cleaned up local file: {filename}")
#             except Exception as e:
#                 logger.warning(f"⚠️ Could not remove local file {filename}: {e}")
            
#             return True
#         else:
#             logger.error("❌ Failed to capture screenshot for noise event")
#             return False
            
#     except Exception as e:
#         logger.error(f"❌ Error processing noise event: {e}")
#         import traceback
#         logger.error(traceback.format_exc())
#         return False


# # testing to add yearly
# def record_noise_event(level, timestamp, image_url):
#     """Record noise event in Firestore for dashboard reporting"""
#     # Parse timestamp from format YYYYMMdd_HHMMSS to a datetime object
#     try:
#         event_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
#     except Exception as e:
#         logger.error(f"Error parsing timestamp {timestamp}: {e}")
#         event_time = datetime.now()  # Fallback to current time
    
#     # Create event data with correctly formatted fields
#     event_data = {
#         "timestamp": timestamp,
#         "level": float(level),
#         "image_url": image_url,
#         "date": event_time.strftime("%Y-%m-%d"),
#         "hour": event_time.hour,
#         "week": event_time.strftime("%Y-W%U"),  # Year-Week format
#         "month": event_time.strftime("%Y-%m"),
#         "year": event_time.strftime("%Y")  # Add year
#     }
    
#     # Add to noise_events collection
#     db.collection("noise_events").document(timestamp).set(event_data)
#     logger.info(f"✅ Noise event recorded in Firestore: {level:.2f} dB")
#     return event_data


# #add a new endpoint to get yearly data
# @app.route('/get_yearly_data', methods=['GET'])
# def get_yearly_data():
#     try:
#         # Get current year
#         now = datetime.now()
#         current_year = now.strftime("%Y")
        
#         # Initialize yearly data (monthly counts for the current year)
#         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         yearly_data = [0] * 12
        
#         # Query for each month in the current year
#         for month_idx in range(12):
#             month_num = month_idx + 1
#             month_query = db.collection("noise_events").where(
#                 "month", "==", f"{current_year}-{month_num:02d}")
#             month_count = len(list(month_query.stream()))
#             yearly_data[month_idx] = month_count
        
#         return jsonify({
#             "status": "success",
#             "yearly_data": yearly_data,
#             "months": months
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting yearly data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "yearly_data": [0] * 12,
#             "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         }), 500

# def send_noise_alert_to_slack(level, image_url, timestamp):
#     """Send noise alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     message = {
#         "text": f"🔊 Loud Noise Detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"Noise Event Screenshot ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Noise event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print("✅ Noise alert sent to Slack")

# def send_slack_alert(noise_level, image_url):
#     if not SLACK_WEBHOOK_URL:
#         logger.warning("Cannot send Slack alert: SLACK_WEBHOOK_URL not set")
#         return False
        
#     message = {
#         "text": f"🚨 Loud Noise Detected! 🚨\nNoise Level: {noise_level} dB\nScreenshot: {image_url}"
#     }
#     response = requests.post(SLACK_WEBHOOK_URL, json=message)
#     return response.status_code == 200

# @app.route('/noise_detector_status', methods=['GET'])
# def noise_detector_status():
#     """Return detailed status of the noise detector for troubleshooting"""
#     global noise_detector
    
#     try:
#         # Get current audio level
#         current_level = noise_detector.get_current_level()
        
#         # Get active device info
#         devices = noise_detector.list_devices()
#         active_device = None
#         for device in devices:
#             if device.get('active', False):
#                 active_device = device
        
#         # Collect status info
#         status_info = {
#             "status": "success",
#             "is_listening": noise_detector.is_listening,
#             "threshold": noise_detector.threshold,
#             "cooldown": noise_detector.cooldown,
#             "current_level": float(current_level),
#             "last_alert_time": noise_detector.last_alert_time,
#             "time_since_last_alert": time.time() - noise_detector.last_alert_time if noise_detector.last_alert_time else None,
#             "audio_stream_active": noise_detector._is_stream_active(),
#             "active_device": active_device,
#             "available_devices": devices,
#             "system_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
        
#         return jsonify(status_info)
#     except Exception as e:
#         logger.error(f"Error getting noise detector status: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "error_type": str(type(e)),
#             "error_traceback": str(e.__traceback__)
#         }), 500



# # Add this route to get noise data for the dashboard
# # add the year data
# # Add this at line 650 or so, after the get_noise_data route declaration
# @app.route('/get_noise_data', methods=['GET'])
# def get_noise_data():
#     try:
#         # Get current date and time
#         now = datetime.now()
#         today = now.strftime("%Y-%m-%d")
#         current_week = now.strftime("%Y-W%U")
#         current_month = now.strftime("%Y-%m")
#         current_year = now.strftime("%Y")
        
#         # Initialize data structures
#         daily_data = [0] * 24
#         weekly_data = [0] * 7
#         monthly_data = [0] * 31  # Maximum days in a month
#         yearly_data = [0] * 12   # 12 months in a year
#         recent_events = []
        
#         # Query Firestore for noise events
#         # Daily data (today's events by hour)
#         daily_query = db.collection("noise_events").where("date", "==", today)
#         daily_results = list(daily_query.stream())
        
#         for doc in daily_results:
#             data = doc.to_dict()
#             hour = data.get('hour', 0)
#             if 0 <= hour < 24:
#                 daily_data[hour] += 1
        
#         # Weekly data (this week's events by day)
#         # Calculate start of week (Sunday)
#         start_of_week = now - timedelta(days=now.weekday() + 1)
#         for day in range(7):
#             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             weekly_data[day] = day_count
        
#         # Monthly data (this month's events by day)
#         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
#         for day in range(1, days_in_month + 1):
#             day_str = f"{day:02d}"
#             month_str = f"{now.month:02d}"
#             date = f"{now.year}-{month_str}-{day_str}"
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             monthly_data[day - 1] = day_count
            
#         # Yearly data (this year's events by month)
#         for month in range(1, 13):
#             month_prefix = f"{current_year}-{month:02d}"
#             month_query = db.collection("noise_events").where(
#                 "month", "==", month_prefix)
#             month_count = len(list(month_query.stream()))
#             yearly_data[month - 1] = month_count
        
#         # Recent events (limit to 10)
#         recent_query = (db.collection("noise_events")
#                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
#                         .limit(10))
        
#         recent_docs = list(recent_query.stream())
#         for doc in recent_docs:
#             data = doc.to_dict()
#             # Convert timestamp string to datetime for proper sorting
#             try:
#                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
#                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             except:
#                 formatted_timestamp = data.get('timestamp', '')
                
#             recent_events.append({
#                 "timestamp": data.get('timestamp', ''),
#                 "level": data.get('level', 0),
#                 "image_url": data.get('image_url', '')
#             })
        
#         return jsonify({
#             "status": "success",
#             "daily_data": daily_data,
#             "weekly_data": weekly_data,
#             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
#             "yearly_data": yearly_data,
#             "recent_events": recent_events
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting noise data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "daily_data": [0] * 24,
#             "weekly_data": [0] * 7,
#             "monthly_data": [0] * 31,
#             "yearly_data": [0] * 12,
#             "recent_events": []
#         }), 500



# ## Object detection
# # ==========================
# # 📌 OBJECT DETECTION SCREENSHOT
# # ==========================
# @app.route('/object_detection_screenshot', methods=['POST'])
# def object_detection_screenshot():
#     data = request.get_json()
#     primary_object = data.get('primaryObject', 'object')
#     secondary_object = data.get('secondaryObject', 'location')
    
#     # Capture the screenshot
#     filename, timestamp = capture_screenshot()
    
#     if filename:
#         # Upload to Firebase
#         image_url = upload_screenshot(filename, timestamp)
        
#         # Record detection event in Firestore
#         event_data = {
#             "timestamp": timestamp,
#             "primaryObject": primary_object,
#             "secondaryObject": secondary_object,
#             "image_url": image_url,
#             "date": datetime.now().strftime("%Y-%m-%d"),
#             "hour": datetime.now().hour,
#             "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#             "month": datetime.now().strftime("%Y-%m")
#         }
        
#         # Add to detection_events collection
#         db.collection("detection_events").document(timestamp).set(event_data)
        
#         # Send to Slack
#         send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"{primary_object} near {secondary_object} detected!",
#             "image_url": image_url
#         })
    
#     return jsonify({
#         "status": "error", 
#         "message": "Failed to capture screenshot"
#     }), 500

# def send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp):
#     """Send object detection alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     emoji_map = {
#         "cat": "🐱",
#         "dog": "🐶",
#         "bird": "🐦",
#         "person": "👤",
#         "couch": "🛋️",
#         "bed": "🛏️",
#         "laptop": "💻",
#         "keyboard": "⌨️",
#         "cell phone": "📱",
#         "tv": "📺",
#         "oven": "🔥"
#     }
    
#     primary_emoji = emoji_map.get(primary_object.lower(), "📷")
#     secondary_emoji = emoji_map.get(secondary_object.lower(), "📍")
    
#     message = {
#         "text": f"{primary_emoji} {primary_object.title()} near {secondary_object} detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*{primary_emoji} {primary_object.title()} near {secondary_object} detected! {secondary_emoji}*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"{primary_object.title()} near {secondary_object} ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Detection event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL, json=message)
#     print(f"✅ Object detection alert sent to Slack: {primary_object} near {secondary_object}")


# # ==========================
# # 📌 Backend API for Gallery
# # ==========================
# @app.route('/get_screenshots', methods=['GET'])
# def get_screenshots():
#     try:
#         # Get manual screenshots
#         manual_screenshots = []
#         screenshots_ref = db.collection("screenshots").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in screenshots_ref:
#             data = doc.to_dict()
#             manual_screenshots.append(data)
        
#         # Get noise detection screenshots
#         noise_screenshots = []
#         noise_ref = db.collection("noise_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in noise_ref:
#             data = doc.to_dict()
#             noise_screenshots.append(data)
        
#         # Get object detection screenshots
#         object_screenshots = []
#         object_ref = db.collection("detection_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in object_ref:
#             data = doc.to_dict()
#             object_screenshots.append(data)
        
#         # Get video recordings
#         videos = []
#         videos_ref = db.collection("videos").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()
#         for doc in videos_ref:
#             data = doc.to_dict()
#             videos.append(data)
            
#         return jsonify({
#             "status": "success",
#             "manual_screenshots": manual_screenshots,
#             "noise_screenshots": noise_screenshots,
#             "object_screenshots": object_screenshots,
#             "videos": videos
#         })
    
#     except Exception as e:
#         print(f"❌ Error fetching gallery data: {e}")
#         return jsonify({
#             "status": "error", 
#             "message": str(e),
#             "manual_screenshots": [],
#             "noise_screenshots": [],
#             "object_screenshots": [],
#             "videos": []
#         }), 500
    
# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     # Initialize noise detector
#     logger.info("Starting application and initializing noise detector...")
#     noise_detector.start(callback=on_noise_detected)
    
#     # Auto-start noise detection
#     if noise_detector._initialize_audio():
#         logger.info("✅ Noise detector initialized successfully")
#     else:
#         logger.warning("⚠️ Noise detector initialization failed")
    
#     # Register cleanup handler
#     atexit.register(lambda: noise_detector.stop())
    
#     # Run the Flask app
#     app.run(debug=True)






    










# # all fucntions works
# # responsive web design done, code here try login
# # if u see this means already undo
# # k now try do login, login done. code down do cloud.
# import cv2
# import os
# import time
# import threading
# import subprocess
# from datetime import datetime, timedelta
# import requests
# from flask import Flask, request, jsonify, Response, render_template, redirect, url_for
# from google.cloud import firestore, storage
# import firebase_admin
# from firebase_admin import credentials
# import subprocess
# import atexit
# import sys
# import pyaudio
# import numpy as np
# import random  # For our debug logging
# from collections import defaultdict
# import logging
# from dotenv import load_dotenv
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# from werkzeug.security import generate_password_hash, check_password_hash

# load_dotenv()


# app = Flask(__name__)
# app.secret_key = os.getenv('APP_SECRET_KEY')

# # # If you want a fallback in case the environment variable is missing
# # if not app.secret_key:
# #     # Print warning
# #     print("WARNING: No APP_SECRET_KEY found in environment variables. Using a default key - not secure for production!")
# #     # Set a default (not recommended for production)
# #     app.secret_key = os.urandom(24)

# # Initialize LoginManager
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# # Simple User class
# class User(UserMixin):
#     def __init__(self, id, username, password_hash):
#         self.id = id
#         self.username = username
#         self.password_hash = password_hash

# # User loader function
# @login_manager.user_loader
# def load_user(user_id):
#     # In a real app, you'd fetch from the database
#     if user_id == '1':
#         return User(1, os.environ.get('APP_USERNAME', 'admin'), 
#                    os.environ.get('APP_PASSWORD_HASH', generate_password_hash('password')))
#     return None

# # Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
        
#         # Get the default user
#         user = User(1, os.environ.get('APP_USERNAME', 'admin'), 
#                    os.environ.get('APP_PASSWORD_HASH', generate_password_hash('password')))
        
#         # Check credentials
#         if username == user.username and check_password_hash(user.password_hash, password):
#             login_user(user)
#             next_page = request.args.get('next', '/')
#             return redirect(next_page)
        
#         return render_template('login.html', error="Invalid credentials")
    
#     return render_template('login.html')

# # Logout route
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect('/login')

# #reset password route
# @app.route('/reset_password', methods=['GET', 'POST'])
# @login_required
# def reset_password():
#     if request.method == 'POST':
#         recovery_code = request.form.get('recovery_code')
#         new_password = request.form.get('new_password')
        
#         if recovery_code == os.getenv('RECOVERY_CODE'):
#             # Generate new password hash
#             new_hash = generate_password_hash(new_password)
            
#             # Here you would update your user's password
#             # For this simple example, we'll just show that it worked
#             return render_template('password_reset_success.html')
#         else:
#             return render_template('reset_password.html', error="Invalid recovery code")
    
#     return render_template('reset_password.html')


# # Set up logging
# logging.basicConfig(level=logging.INFO, 
#                     format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger('noise_detection')
# class NoiseDetector:
#     def __init__(self, threshold=30, cooldown=10):
#         """Initialize the noise detector with configurable threshold and cooldown"""
#         self.threshold = threshold  # Default threshold in dB
#         self.cooldown = cooldown    # Default cooldown in seconds
#         self.is_listening = False   # Tracking if detector is active
#         self.audio_stream = None    # PyAudio stream
#         self.pyaudio_instance = None  # PyAudio instance
#         self.detection_thread = None  # Thread for detection loop
#         self.last_alert_time = 0    # Last time an alert was triggered
#         self.callback = None        # Callback for when noise is detected
        
#     def start(self, callback=None):
#         """Start the noise detection"""
#         if self.is_listening:
#             logger.warning("Noise detection already running")
#             return False
        
#         self.callback = callback
        
#         # Initialize PyAudio if not already done
#         if not self._initialize_audio():
#             logger.error("Failed to initialize audio")
#             return False
        
#         # Start detection thread
#         self.is_listening = True
#         self.detection_thread = threading.Thread(target=self._detection_loop)
#         self.detection_thread.daemon = True
#         self.detection_thread.start()
#         logger.info(f"Noise detection started with threshold {self.threshold}dB")
#         return True
    
#     def stop(self):
#         """Stop the noise detection"""
#         if not self.is_listening:
#             logger.warning("Noise detection not running")
#             return False
        
#         self.is_listening = False
#         # Thread will exit on its own due to while loop condition
#         logger.info("Noise detection stopped")
#         return True
    
#     def set_threshold(self, threshold):
#         """Set the noise detection threshold"""
#         try:
#             self.threshold = float(threshold)
#             logger.info(f"Threshold set to {self.threshold}dB")
#             return True
#         except (ValueError, TypeError):
#             logger.error(f"Invalid threshold value: {threshold}")
#             return False
    
#     def set_cooldown(self, cooldown):
#         """Set the cooldown period between alerts"""
#         try:
#             self.cooldown = int(cooldown)
#             logger.info(f"Cooldown set to {self.cooldown} seconds")
#             return True
#         except (ValueError, TypeError):
#             logger.error(f"Invalid cooldown value: {cooldown}")
#             return False
    
#     def get_current_level(self):
#         """Get the current audio level"""
#         if not self.audio_stream:
#             if not self._initialize_audio():
#                 return 0
        
#         try:
#             # Read audio data
#             data = self.audio_stream.read(2048, exception_on_overflow=False)
#             # Calculate level
#             level = self._calculate_audio_level(data)
#             return level
#         except Exception as e:
#             logger.error(f"Error getting audio level: {e}")
#             return 0
    
#     def _initialize_audio(self):
#         """Initialize the audio system with proper error handling"""
#         try:
#             # Clean up existing resources if any
#             if self.audio_stream:
#                 self.audio_stream.stop_stream()
#                 self.audio_stream.close()
            
#             if self.pyaudio_instance:
#                 self.pyaudio_instance.terminate()
            
#             # Initialize PyAudio
#             self.pyaudio_instance = pyaudio.PyAudio()
            
#             # Find input devices
#             input_devices = []
#             for i in range(self.pyaudio_instance.get_device_count()):
#                 device_info = self.pyaudio_instance.get_device_info_by_index(i)
#                 if device_info['maxInputChannels'] > 0:
#                     input_devices.append(i)
#                     logger.info(f"Found input device {i}: {device_info['name']}")
            
#             if not input_devices:
#                 logger.error("No audio input devices found")
#                 return False
            
#             # Try to open the default input device first (usually index 0)
#             device_to_use = input_devices[0]
            
#             # Open audio stream
#             self.audio_stream = self.pyaudio_instance.open(
#                 format=pyaudio.paInt16,
#                 channels=1,
#                 rate=44100,
#                 input=True,
#                 input_device_index=device_to_use,
#                 frames_per_buffer=2048
#             )
            
#             # Test the stream
#             test_data = self.audio_stream.read(2048, exception_on_overflow=False)
#             test_level = self._calculate_audio_level(test_data)
#             logger.info(f"Audio initialized. Test level: {test_level:.2f}dB")
            
#             return True
            
#         except Exception as e:
#             logger.error(f"Error initializing audio: {e}")
#             return False
    
#     def _calculate_audio_level(self, data):
#         """Calculate audio level in decibels using a reliable method"""
#         try:
#             # Convert buffer to numpy array
#             samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            
#             # Prevent division by zero with a small epsilon
#             epsilon = 1e-10
            
#             # Calculate RMS (Root Mean Square)
#             rms = np.sqrt(np.mean(np.square(samples)) + epsilon)
            
#             # Convert to decibels
#             # Reference: maximum possible value for 16-bit audio
#             max_possible_value = 32768.0
            
#             # Calculate dB relative to full scale (dBFS)
#             db_fs = 20 * np.log10(rms / max_possible_value)
            
#             # Convert to a positive scale where:
#             # - Silence is around 0-10 dB
#             # - Normal conversation is around 40-60 dB
#             # - Loud noises are 70+ dB
#             normalized_db = 60 + db_fs  # Shift by 60dB to make it positive
            
#             # Ensure we don't return negative values
#             return max(0, normalized_db)
            
#         except Exception as e:
#             logger.error(f"Error calculating audio level: {e}")
#             return 0
    
#     def _detection_loop(self):
#         """Main loop for noise detection"""
#         logger.info("Noise detection loop started")
        
#         consecutive_loud_samples = 0
#         required_loud_samples = 3  # Number of consecutive samples needed to trigger
        
#         while self.is_listening:
#             try:
#                 # Read audio data
#                 data = self.audio_stream.read(2048, exception_on_overflow=False)
                
#                 # Calculate audio level
#                 audio_level = self._calculate_audio_level(data)
                
#                 # Occasionally log the current level for debugging
#                 if np.random.random() < 0.01:  # 1% chance to log
#                     logger.debug(f"Current audio level: {audio_level:.2f}dB (Threshold: {self.threshold}dB)")
                
#                 # Check if noise exceeds threshold
#                 if audio_level > self.threshold:
#                     consecutive_loud_samples += 1
                    
#                     # Check if we have enough consecutive samples and not in cooldown
#                     current_time = time.time()
#                     time_since_last_alert = current_time - self.last_alert_time
                    
#                     if (consecutive_loud_samples >= required_loud_samples and 
#                         time_since_last_alert > self.cooldown):
                        
#                         logger.info(f"Loud noise detected! Level: {audio_level:.2f}dB")
                        
#                         # Update last alert time
#                         self.last_alert_time = current_time
                        
#                         # Call the callback if set
#                         if self.callback:
#                             self.callback(audio_level)
                        
#                         # Reset counter
#                         consecutive_loud_samples = 0
#                 else:
#                     # Reset counter if current sample is not loud
#                     consecutive_loud_samples = 0
                
#                 # Small delay to prevent excessive CPU usage
#                 time.sleep(0.05)
                
#             except IOError as e:
#                 # Handle common PyAudio errors (buffer overflow, etc.)
#                 logger.warning(f"Audio stream IO error (can be normal): {e}")
#                 time.sleep(0.1)
                
#             except Exception as e:
#                 logger.error(f"Error in noise detection loop: {e}")
#                 time.sleep(0.5)  # Longer delay on error
                
#                 # Try to reinitialize audio if there's a persistent problem
#                 if not self._is_stream_active():
#                     logger.warning("Audio stream appears inactive, attempting to reconnect...")
#                     self._initialize_audio()
    
#     def _is_stream_active(self):
#         """Check if the audio stream is still active"""
#         try:
#             return self.audio_stream and self.audio_stream.is_active()
#         except:
#             return False

#     def list_devices(self):
#         """List all available audio input devices"""
#         devices = []
#         try:
#             p = pyaudio.PyAudio()
#             for i in range(p.get_device_count()):
#                 device_info = p.get_device_info_by_index(i)
#                 if device_info['maxInputChannels'] > 0:
#                     devices.append({
#                         'index': i,
#                         'name': device_info['name'],
#                         'channels': device_info['maxInputChannels'],
#                         'sample_rate': device_info['defaultSampleRate']
#                     })
#             p.terminate()
#             return devices
#         except Exception as e:
#             logger.error(f"Error listing devices: {e}")
#             return []
    
#     def select_device(self, device_index):
#         """Select a specific audio input device"""
#         try:
#             # Stop current stream if active
#             if self.is_listening:
#                 self.stop()
                
#             # Close current resources
#             if self.audio_stream:
#                 self.audio_stream.stop_stream()
#                 self.audio_stream.close()
#                 self.audio_stream = None
            
#             if self.pyaudio_instance:
#                 self.pyaudio_instance.terminate()
#                 self.pyaudio_instance = None
            
#             # Initialize PyAudio
#             self.pyaudio_instance = pyaudio.PyAudio()
            
#             # Validate device exists
#             device_info = self.pyaudio_instance.get_device_info_by_index(device_index)
#             if device_info['maxInputChannels'] <= 0:
#                 logger.error(f"Device {device_index} is not an input device")
#                 return False
            
#             # Open stream with selected device
#             self.audio_stream = self.pyaudio_instance.open(
#                 format=pyaudio.paInt16,
#                 channels=1,
#                 rate=44100,
#                 input=True,
#                 input_device_index=device_index,
#                 frames_per_buffer=2048
#             )
            
#             # Test stream
#             test_data = self.audio_stream.read(2048, exception_on_overflow=False)
#             test_level = self._calculate_audio_level(test_data)
            
#             logger.info(f"Selected device {device_index}: {device_info['name']}. Test level: {test_level:.2f}dB")
#             return True
            
#         except Exception as e:
#             logger.error(f"Error selecting device {device_index}: {e}")
#             return False

#     def get_device_diagnostics(self):
#         """Get detailed diagnostic information about the audio system"""
#         try:
#             # Get device info
#             devices = self.list_devices()
            
#             # Collect sample data
#             samples = []
#             if self.audio_stream:
#                 for _ in range(5):  # Get 5 samples
#                     data = self.audio_stream.read(2048, exception_on_overflow=False)
#                     audio_data = np.frombuffer(data, dtype=np.int16)
                    
#                     # Calculate statistics
#                     rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
#                     max_value = np.max(np.abs(audio_data)) if len(audio_data) > 0 else 0
#                     level = self._calculate_audio_level(data)
                    
#                     samples.append({
#                         "rms": float(rms),
#                         "max_value": int(max_value),
#                         "level": float(level)
#                     })
#                     time.sleep(0.1)
            
#             return {
#                 "devices": devices,
#                 "samples": samples,
#                 "threshold": float(self.threshold),
#                 "is_listening": self.is_listening
#             }
            
#         except Exception as e:
#             logger.error(f"Error getting diagnostics: {e}")
#             return {
#                 "error": str(e),
#                 "devices": [],
#                 "samples": [],
#                 "threshold": float(self.threshold),
#                 "is_listening": self.is_listening
#             }

# # 🔹 Set Firebase credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "firestore_key.json")

# # 🔹 Initialize Firebase Admin SDK
# firebase_admin_file = os.getenv("FIREBASE_ADMIN_SDK_FILE", "cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
# cred = credentials.Certificate(firebase_admin_file)
# firebase_admin.initialize_app(cred, {
#     'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET", "cloudpetproject1.appspot.com")
# })

# # 🔹 Firestore & Storage
# db = firestore.Client()
# storage_client = storage.Client()
# bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# # 🔹 Slack Webhook
# SLACK_WEBHOOK_URL_NOISE = os.getenv("SLACK_WEBHOOK_URL_NOISE")
# SLACK_WEBHOOK_URL_OBJECT = os.getenv("SLACK_WEBHOOK_URL_OBJECT") 
# SLACK_WEBHOOK_URL_SCREENSHOT = os.getenv("SLACK_WEBHOOK_URL_SCREENSHOT")
# SLACK_WEBHOOK_URL_RECORDING = os.getenv("SLACK_WEBHOOK_URL_RECORDING")

# # if not SLACK_WEBHOOK_URL:
# #     logger.warning("⚠️ SLACK_WEBHOOK_URL not set in environment variables!")

# # 🔹 Global Variables
# latest_frame = None
# video_writer = None
# recording = False
# video_filename = None
# video_process = None
# is_recording = False  # 🔹 Track recording status
# out = None  # 🔹 Video writer object
# start_time = None  # 🔹 Store timestamp of recording start

# cap = cv2.VideoCapture(0)  # Open webcam

# # Initialize Noise Detector
# noise_detector = NoiseDetector(threshold=30, cooldown=10)  # Default values


# # Global variables for object detection
# detection_model = None
# category_index = None
# detection_enabled = False
# target_object = None  # Object that triggers monitoring (e.g., "couch")
# monitor_object = None  # Object to watch for (e.g., "cat")
# cooldown_period = 10  # Seconds between alerts for the same detection
# last_detection_time = None
# detection_threshold = 0.5  # Confidence threshold for detection
# proximity_threshold = 0.2  # How close objects need to be (as a fraction of image size)


# # ==========================
# # 📌 LIVE VIDEO STREAMING
# # ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# @app.route('/')
# @login_required
# def index():
#     # Ensure noise detector is running
#     global noise_detector
#     if not noise_detector.is_listening:
#         logger.info("🔄 Starting noise detection from index page")
#         noise_detector.start(callback=on_noise_detected)
    
#     return render_template('index.html')

# @app.route('/video_feed')
# @login_required
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # ==========================
# # 📌 SCREENSHOT FUNCTION
# # ==========================
# def capture_screenshot():
#     global latest_frame
#     print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

#     if latest_frame is None:
#         print("❌ Error: No frame available for screenshot.")
#         return None, None
        

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"screenshot_{timestamp}.jpg"
#     cv2.imwrite(filename, latest_frame)

#     print(f"✅ Screenshot saved: {filename}")
#     return filename, timestamp

# def upload_screenshot(filename, timestamp):
#     blob = bucket.blob(f"screenshots/{filename}")
#     blob.upload_from_filename(filename)
#     blob.make_public()
#     image_url = blob.public_url

#     db.collection("screenshots").document(timestamp).set({
#         "timestamp": timestamp,
#         "image_url": image_url
#     })

#     return image_url

# def send_slack_screenshot(image_url):
#     slack_url = SLACK_WEBHOOK_URL_SCREENSHOT
    
#     if not slack_url:
#         logger.warning("Cannot send screenshot alert: SLACK_WEBHOOK_URL_SCREENSHOT not set")
#         return
    
#     message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
#     requests.post(slack_url, json=message)

# @app.route('/take_screenshot', methods=['POST'])
# @login_required
# def take_screenshot():
#     filename, timestamp = capture_screenshot()
#     if filename:
#         image_url = upload_screenshot(filename, timestamp)
#         send_slack_screenshot(image_url)
#         return jsonify({"status": "success", "image_url": image_url})
#     return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# # ==========================
# # 📌 VIDEO RECORDING FUNCTION
# # ==========================
# recording_thread = None

# #this test for 60 min max
# @app.route('/toggle_recording', methods=['POST'])
# @login_required
# def toggle_recording():
#     global is_recording, out, start_time, video_filename

#     if is_recording:
#         is_recording = False
#         if out is not None:
#             out.release()  # Stop video recording

#         print("🛑 Video recording stopped!")
        
#         # Upload to Firebase Storage
#         video_url = upload_video(video_filename)
        
#         # Send to Slack
#         if video_url:
#             send_slack_video(video_url)

#         return jsonify({
#             "status": "stopped",
#             "message": "Recording stopped",
#             "video_url": video_url if video_url else None
#         }), 200
#     else:
#         is_recording = True
#         start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         video_filename = f"recording_{start_time}.mp4"
        
#         # Use MP4V codec (H.264) for mp4 files
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
#         # Get the camera dimensions
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
#         out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

#         # Add a timer to stop recording after 60 minutes
#         def stop_after_timeout():
#             global is_recording
#             time.sleep(60 * 60)  # 60 minutes in seconds
#             if is_recording:
#                 print("🕒 Maximum recording time (60 minutes) reached. Stopping recording.")
#                 requests.post('http://localhost:5000/toggle_recording')
                
#         # Start timer in a separate thread
#         timer_thread = threading.Thread(target=stop_after_timeout)
#         timer_thread.daemon = True
#         timer_thread.start()

#         print(f"🔴 Video recording started! Saving to {video_filename} (Max 60 minutes)")

#         return jsonify({
#             "status": "recording",
#             "message": "Recording started (Max 60 minutes)",
#             "video_url": video_filename
#         }), 200

# @app.route('/start_recording', methods=['POST'])
# @login_required
# def start_recording():
#     global recording, video_filename, video_process
#     if recording:
#         return jsonify({"status": "error", "message": "Already recording"}), 400

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     video_filename = f"recording_{timestamp}.mp4"

#     # 🔹 Start recording video with sound using FFmpeg
#     video_process = subprocess.Popen([
#         "ffmpeg",
#         "-f", "dshow",
#         "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
#         "-t", "10",  # Set max recording duration (adjust as needed)
#         "-y", video_filename
#     ])

#     recording = True
#     return jsonify({"status": "success", "message": "Recording started"})

# @app.route('/stop_recording', methods=['POST'])
# @login_required
# def stop_recording():
#     global recording, video_filename, video_process
#     if not recording:
#         return jsonify({"status": "error", "message": "Not recording"}), 400

#     video_process.terminate()  # Stop FFmpeg
#     recording = False

#     # Upload to Firebase
#     video_url = upload_video(video_filename)
#     send_slack_video(video_url)

#     return jsonify({"status": "success", "video_url": video_url})

# def upload_video(filename):
#     # Give the system time to close the file
#     time.sleep(1)
    
#     # Check if file exists
#     if not os.path.exists(filename):
#         print(f"❌ Error: Video file {filename} not found")
#         return None
        
#     # Upload to Firebase Storage with correct MIME type
#     try:
#         blob = bucket.blob(f"videos/{filename}")
        
#         # Set the correct MIME type for MP4
#         blob.content_type = 'video/mp4'
        
#         # Set content disposition to inline so browsers will play it
#         blob.content_disposition = 'inline'
        
#         # Upload the file
#         blob.upload_from_filename(filename)
#         blob.make_public()
#         video_url = blob.public_url

#         # Store metadata in Firestore
#         db.collection("videos").document(os.path.basename(filename)).set({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "video_url": video_url
#         })
        
#         print(f"✅ Video uploaded: {video_url}")
#         return video_url
#     except Exception as e:
#         print(f"❌ Error uploading video: {e}")
#         return None

# def send_slack_video(video_url):
#     message = {
#         "text": "🎥 Video Recording Uploaded!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "🎥 *Video Recording Uploaded!*"
#                 }
#             },
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"<{video_url}|Click here to view or download the video>"
#                 }
#             }
#         ]
#     }
#     requests.post(SLACK_WEBHOOK_URL_RECORDING, json=message)

# # here using claude version 22/3/2025
# @app.route('/start_noise_detection', methods=['POST'])
# @login_required
# def start_noise_detection():
#     global noise_detector
    
#     # Get custom threshold if provided
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             noise_detector.set_threshold(float(data['threshold']))
#         except (ValueError, TypeError):
#             pass
    
#     # Start detection with callback
#     success = noise_detector.start(callback=on_noise_detected)
    
#     if success:
#         return jsonify({
#             "status": "success", 
#             "message": f"Noise detection started with threshold {noise_detector.threshold} dB"
#         })
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "Failed to start noise detection"
#         }), 500

# @app.route('/stop_noise_detection', methods=['POST'])
# @login_required
# def stop_noise_detection():
#     global noise_detector
    
#     success = noise_detector.stop()
    
#     if success:
#         return jsonify({
#             "status": "success", 
#             "message": "Noise detection stopped"
#         })
#     else:
#         return jsonify({
#             "status": "warning", 
#             "message": "Noise detection not running"
#         })

# @app.route('/set_noise_threshold', methods=['POST'])
# @login_required
# def set_noise_threshold():
#     global noise_detector
    
#     data = request.get_json()
#     if data and 'threshold' in data:
#         try:
#             success = noise_detector.set_threshold(float(data['threshold']))
#             if success:
#                 return jsonify({
#                     "status": "success", 
#                     "message": f"Noise threshold set to {noise_detector.threshold} dB"
#                 })
#             else:
#                 return jsonify({
#                     "status": "error", 
#                     "message": "Failed to set threshold"
#                 }), 400
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid threshold value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No threshold provided"
#         }), 400

# @app.route('/set_cooldown', methods=['POST'])
# @login_required
# def set_cooldown():
#     global noise_detector
    
#     data = request.get_json()
#     if data and 'cooldown' in data:
#         try:
#             success = noise_detector.set_cooldown(int(data['cooldown']))
#             if success:
#                 return jsonify({
#                     "status": "success", 
#                     "message": f"Noise alert cooldown set to {noise_detector.cooldown} seconds"
#                 })
#             else:
#                 return jsonify({
#                     "status": "error", 
#                     "message": "Failed to set cooldown"
#                 }), 400
#         except (ValueError, TypeError):
#             return jsonify({
#                 "status": "error", 
#                 "message": "Invalid cooldown value"
#             }), 400
#     else:
#         return jsonify({
#             "status": "error", 
#             "message": "No cooldown value provided"
#         }), 400

# @app.route('/test_audio', methods=['GET'])
# @login_required
# def test_audio():
#     global noise_detector
    
#     try:
#         level = noise_detector.get_current_level()
        
#         return jsonify({
#             "status": "success",
#             "audio_level": float(level),
#             "threshold": float(noise_detector.threshold)
#         })
#     except Exception as e:
#         logger.error(f"Error in test_audio: {e}")
#         return jsonify({
#             "status": "error",
#             "message": f"Audio test failed: {str(e)}"
#         }), 500

# @app.route('/debug_audio', methods=['GET'])
# @login_required
# def debug_audio():
#     global noise_detector
    
#     try:
#         diagnostics = noise_detector.get_device_diagnostics()
#         diagnostics["status"] = "success"
#         return jsonify(diagnostics)
#     except Exception as e:
#         logger.error(f"Error in debug_audio: {e}")
#         return jsonify({
#             "status": "error",
#             "message": f"Audio diagnostic failed: {str(e)}"
#         }), 500

# @app.route('/list_audio_devices', methods=['GET'])
# @login_required
# def list_audio_devices():
#     global noise_detector
    
#     try:
#         devices = noise_detector.list_devices()
#         return jsonify({
#             "status": "success",
#             "devices": devices
#         })
#     except Exception as e:
#         logger.error(f"Error listing audio devices: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/select_audio_device', methods=['POST'])
# @login_required
# def select_audio_device():
#     global noise_detector
    
#     data = request.get_json()
#     if not data or 'device_index' not in data:
#         return jsonify({
#             "status": "error",
#             "message": "No device index provided"
#         }), 400
    
#     try:
#         device_index = int(data['device_index'])
#         success = noise_detector.select_device(device_index)
        
#         if success:
#             # Get current level with new device
#             level = noise_detector.get_current_level()
            
#             return jsonify({
#                 "status": "success",
#                 "message": f"Audio device {device_index} selected successfully",
#                 "audio_level": float(level)
#             })
#         else:
#             return jsonify({
#                 "status": "error",
#                 "message": f"Failed to select device {device_index}"
#             }), 500
#     except Exception as e:
#         logger.error(f"Error selecting audio device: {e}")
#         return jsonify({
#             "status": "error",
#             "message": f"Error selecting audio device: {str(e)}"
#         }), 500



# # Callback function for noise detection
# def on_noise_detected(level):
#     """Callback function when noise is detected"""
#     logger.info(f"🔔 NOISE DETECTED - Level: {level:.2f} dB")
    
#     try:
#         # Capture screenshot
#         logger.info("📸 Capturing screenshot...")
#         filename, timestamp = capture_screenshot()
        
#         if filename:
#             logger.info(f"📸 Screenshot captured: {filename}")
            
#             # Upload to Firebase
#             logger.info("☁️ Uploading screenshot to Firebase...")
#             image_url = upload_screenshot(filename, timestamp)
            
#             # Record noise event in Firestore
#             logger.info("📝 Recording noise event in Firestore...")
#             event_data = record_noise_event(level, timestamp, image_url)
            
#             # Send notification to Slack
#             logger.info("📨 Sending notification to Slack...")
#             send_noise_alert_to_slack(level, image_url, timestamp)
            
#             # Log success
#             logger.info(f"✅ Noise event fully processed: {level:.2f} dB at {timestamp}")
            
#             # Clean up local file if desired
#             try:
#                 os.remove(filename)
#                 logger.info(f"🧹 Cleaned up local file: {filename}")
#             except Exception as e:
#                 logger.warning(f"⚠️ Could not remove local file {filename}: {e}")
            
#             return True
#         else:
#             logger.error("❌ Failed to capture screenshot for noise event")
#             return False
            
#     except Exception as e:
#         logger.error(f"❌ Error processing noise event: {e}")
#         import traceback
#         logger.error(traceback.format_exc())
#         return False


# # testing to add yearly
# def record_noise_event(level, timestamp, image_url):
#     """Record noise event in Firestore for dashboard reporting"""
#     # Parse timestamp from format YYYYMMdd_HHMMSS to a datetime object
#     try:
#         event_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
#     except Exception as e:
#         logger.error(f"Error parsing timestamp {timestamp}: {e}")
#         event_time = datetime.now()  # Fallback to current time
    
#     # Create event data with correctly formatted fields
#     event_data = {
#         "timestamp": timestamp,
#         "level": float(level),
#         "image_url": image_url,
#         "date": event_time.strftime("%Y-%m-%d"),
#         "hour": event_time.hour,
#         "week": event_time.strftime("%Y-W%U"),  # Year-Week format
#         "month": event_time.strftime("%Y-%m"),
#         "year": event_time.strftime("%Y")  # Add year
#     }
    
#     # Add to noise_events collection
#     db.collection("noise_events").document(timestamp).set(event_data)
#     logger.info(f"✅ Noise event recorded in Firestore: {level:.2f} dB")
#     return event_data


# #add a new endpoint to get yearly data
# @app.route('/get_yearly_data', methods=['GET'])
# @login_required
# def get_yearly_data():
#     try:
#         # Get current year
#         now = datetime.now()
#         current_year = now.strftime("%Y")
        
#         # Initialize yearly data (monthly counts for the current year)
#         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         yearly_data = [0] * 12
        
#         # Query for each month in the current year
#         for month_idx in range(12):
#             month_num = month_idx + 1
#             month_query = db.collection("noise_events").where(
#                 "month", "==", f"{current_year}-{month_num:02d}")
#             month_count = len(list(month_query.stream()))
#             yearly_data[month_idx] = month_count
        
#         return jsonify({
#             "status": "success",
#             "yearly_data": yearly_data,
#             "months": months
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting yearly data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "yearly_data": [0] * 12,
#             "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         }), 500

# def send_noise_alert_to_slack(level, image_url, timestamp):
#     """Send noise alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     slack_url = SLACK_WEBHOOK_URL_NOISE

#     if not slack_url:
#         logger.warning("Cannot send noise alert: SLACK_WEBHOOK_URL_NOISE not set")
#         return
    
#     message = {
#         "text": f"🔊 Loud Noise Detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"Noise Event Screenshot ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Noise event screenshot"
#             }
#         ]
#     }
    
#     requests.post(slack_url, json=message)
#     print("✅ Noise alert sent to Slack")

# def send_slack_alert(noise_level, image_url):
#     if not SLACK_WEBHOOK_URL_NOISE:
#         logger.warning("Cannot send Slack alert: SLACK_WEBHOOK_URL not set")
#         return False
        
#     message = {
#         "text": f"🚨 Loud Noise Detected! 🚨\nNoise Level: {noise_level} dB\nScreenshot: {image_url}"
#     }
#     response = requests.post(SLACK_WEBHOOK_URL_NOISE, json=message)
#     return response.status_code == 200

# @app.route('/noise_detector_status', methods=['GET'])
# @login_required
# def noise_detector_status():
#     """Return detailed status of the noise detector for troubleshooting"""
#     global noise_detector
    
#     try:
#         # Get current audio level
#         current_level = noise_detector.get_current_level()
        
#         # Get active device info
#         devices = noise_detector.list_devices()
#         active_device = None
#         for device in devices:
#             if device.get('active', False):
#                 active_device = device
        
#         # Collect status info
#         status_info = {
#             "status": "success",
#             "is_listening": noise_detector.is_listening,
#             "threshold": noise_detector.threshold,
#             "cooldown": noise_detector.cooldown,
#             "current_level": float(current_level),
#             "last_alert_time": noise_detector.last_alert_time,
#             "time_since_last_alert": time.time() - noise_detector.last_alert_time if noise_detector.last_alert_time else None,
#             "audio_stream_active": noise_detector._is_stream_active(),
#             "active_device": active_device,
#             "available_devices": devices,
#             "system_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
        
#         return jsonify(status_info)
#     except Exception as e:
#         logger.error(f"Error getting noise detector status: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "error_type": str(type(e)),
#             "error_traceback": str(e.__traceback__)
#         }), 500



# # Add this route to get noise data for the dashboard
# # add the year data
# # Add this at line 650 or so, after the get_noise_data route declaration
# @app.route('/get_noise_data', methods=['GET'])
# @login_required
# def get_noise_data():
#     try:
#         # Get current date and time
#         now = datetime.now()
#         today = now.strftime("%Y-%m-%d")
#         current_week = now.strftime("%Y-W%U")
#         current_month = now.strftime("%Y-%m")
#         current_year = now.strftime("%Y")
        
#         # Initialize data structures
#         daily_data = [0] * 24
#         weekly_data = [0] * 7
#         monthly_data = [0] * 31  # Maximum days in a month
#         yearly_data = [0] * 12   # 12 months in a year
#         recent_events = []
        
#         # Query Firestore for noise events
#         # Daily data (today's events by hour)
#         daily_query = db.collection("noise_events").where("date", "==", today)
#         daily_results = list(daily_query.stream())
        
#         for doc in daily_results:
#             data = doc.to_dict()
#             hour = data.get('hour', 0)
#             if 0 <= hour < 24:
#                 daily_data[hour] += 1
        
#         # Weekly data (this week's events by day)
#         # Calculate start of week (Sunday)
#         start_of_week = now - timedelta(days=now.weekday() + 1)
#         for day in range(7):
#             date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             weekly_data[day] = day_count
        
#         # Monthly data (this month's events by day)
#         days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
#         for day in range(1, days_in_month + 1):
#             day_str = f"{day:02d}"
#             month_str = f"{now.month:02d}"
#             date = f"{now.year}-{month_str}-{day_str}"
#             day_query = db.collection("noise_events").where("date", "==", date)
#             day_count = len(list(day_query.stream()))
#             monthly_data[day - 1] = day_count
            
#         # Yearly data (this year's events by month)
#         for month in range(1, 13):
#             month_prefix = f"{current_year}-{month:02d}"
#             month_query = db.collection("noise_events").where(
#                 "month", "==", month_prefix)
#             month_count = len(list(month_query.stream()))
#             yearly_data[month - 1] = month_count
        
#         # Recent events (limit to 10)
#         recent_query = (db.collection("noise_events")
#                         .order_by("timestamp", direction=firestore.Query.DESCENDING)
#                         .limit(10))
        
#         recent_docs = list(recent_query.stream())
#         for doc in recent_docs:
#             data = doc.to_dict()
#             # Convert timestamp string to datetime for proper sorting
#             try:
#                 event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
#                 formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             except:
#                 formatted_timestamp = data.get('timestamp', '')
                
#             recent_events.append({
#                 "timestamp": data.get('timestamp', ''),
#                 "level": data.get('level', 0),
#                 "image_url": data.get('image_url', '')
#             })
        
#         return jsonify({
#             "status": "success",
#             "daily_data": daily_data,
#             "weekly_data": weekly_data,
#             "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
#             "yearly_data": yearly_data,
#             "recent_events": recent_events
#         })
    
#     except Exception as e:
#         print(f"❌ Error getting noise data: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#             "daily_data": [0] * 24,
#             "weekly_data": [0] * 7,
#             "monthly_data": [0] * 31,
#             "yearly_data": [0] * 12,
#             "recent_events": []
#         }), 500



# ## Object detection
# # ==========================
# # 📌 OBJECT DETECTION SCREENSHOT
# # ==========================
# @app.route('/object_detection_screenshot', methods=['POST'])
# @login_required
# def object_detection_screenshot():
#     data = request.get_json()
#     primary_object = data.get('primaryObject', 'object')
#     secondary_object = data.get('secondaryObject', 'location')
    
#     # Capture the screenshot
#     filename, timestamp = capture_screenshot()
    
#     if filename:
#         # Upload to Firebase
#         image_url = upload_screenshot(filename, timestamp)
        
#         # Record detection event in Firestore
#         event_data = {
#             "timestamp": timestamp,
#             "primaryObject": primary_object,
#             "secondaryObject": secondary_object,
#             "image_url": image_url,
#             "date": datetime.now().strftime("%Y-%m-%d"),
#             "hour": datetime.now().hour,
#             "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
#             "month": datetime.now().strftime("%Y-%m")
#         }
        
#         # Add to detection_events collection
#         db.collection("detection_events").document(timestamp).set(event_data)
        
#         # Send to Slack
#         send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp)
        
#         return jsonify({
#             "status": "success", 
#             "message": f"{primary_object} near {secondary_object} detected!",
#             "image_url": image_url
#         })
    
#     return jsonify({
#         "status": "error", 
#         "message": "Failed to capture screenshot"
#     }), 500

# def send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp):
#     """Send object detection alert with screenshot to Slack"""
#     formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
#     emoji_map = {
#         "cat": "🐱",
#         "dog": "🐶",
#         "bird": "🐦",
#         "person": "👤",
#         "couch": "🛋️",
#         "bed": "🛏️",
#         "laptop": "💻",
#         "keyboard": "⌨️",
#         "cell phone": "📱",
#         "tv": "📺",
#         "oven": "🔥"
#     }
    
#     primary_emoji = emoji_map.get(primary_object.lower(), "📷")
#     secondary_emoji = emoji_map.get(secondary_object.lower(), "📍")
    
#     message = {
#         "text": f"{primary_emoji} {primary_object.title()} near {secondary_object} detected!",
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": f"*{primary_emoji} {primary_object.title()} near {secondary_object} detected! {secondary_emoji}*\n• Time: {formatted_time}"
#                 }
#             },
#             {
#                 "type": "image",
#                 "title": {
#                     "type": "plain_text",
#                     "text": f"{primary_object.title()} near {secondary_object} ({formatted_time})"
#                 },
#                 "image_url": image_url,
#                 "alt_text": "Detection event screenshot"
#             }
#         ]
#     }
    
#     requests.post(SLACK_WEBHOOK_URL_OBJECT, json=message)
#     print(f"✅ Object detection alert sent to Slack: {primary_object} near {secondary_object}")


# # ==========================
# # 📌 Backend API for Gallery
# # ==========================
# @app.route('/get_screenshots', methods=['GET'])
# @login_required
# def get_screenshots():
#     try:
#         # Get manual screenshots
#         manual_screenshots = []
#         screenshots_ref = db.collection("screenshots").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in screenshots_ref:
#             data = doc.to_dict()
#             manual_screenshots.append(data)
        
#         # Get noise detection screenshots
#         noise_screenshots = []
#         noise_ref = db.collection("noise_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in noise_ref:
#             data = doc.to_dict()
#             noise_screenshots.append(data)
        
#         # Get object detection screenshots
#         object_screenshots = []
#         object_ref = db.collection("detection_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
#         for doc in object_ref:
#             data = doc.to_dict()
#             object_screenshots.append(data)
        
#         # Get video recordings
#         videos = []
#         videos_ref = db.collection("videos").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()
#         for doc in videos_ref:
#             data = doc.to_dict()
#             videos.append(data)
            
#         return jsonify({
#             "status": "success",
#             "manual_screenshots": manual_screenshots,
#             "noise_screenshots": noise_screenshots,
#             "object_screenshots": object_screenshots,
#             "videos": videos
#         })
    
#     except Exception as e:
#         print(f"❌ Error fetching gallery data: {e}")
#         return jsonify({
#             "status": "error", 
#             "message": str(e),
#             "manual_screenshots": [],
#             "noise_screenshots": [],
#             "object_screenshots": [],
#             "videos": []
#         }), 500
    
# # ==========================
# # 📌 RUN APP
# # ==========================
# if __name__ == '__main__':
#     # Initialize noise detector
#     logger.info("Starting application and initializing noise detector...")
#     noise_detector.start(callback=on_noise_detected)
    
#     # Auto-start noise detection
#     if noise_detector._initialize_audio():
#         logger.info("✅ Noise detector initialized successfully")
#     else:
#         logger.warning("⚠️ Noise detector initialization failed")
    
#     # Register cleanup handler
#     atexit.register(lambda: noise_detector.stop())
    
#     # Run the Flask app
#     app.run(debug=True)
    


























# all fucntions works
# responsive web design done
# if u see this means already undo sd
# k now try deploy to cloud.
import cv2
import os
import time
import threading
import subprocess
from datetime import datetime, timedelta
import requests
from flask import Flask, request, jsonify, Response, render_template, redirect, url_for
from google.cloud import firestore, storage
import firebase_admin
from firebase_admin import credentials
import subprocess
import atexit
import sys
import pyaudio
import numpy as np
import random  # For our debug logging
from collections import defaultdict
import logging
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

# # If you want a fallback in case the environment variable is missing
# if not app.secret_key:
#     # Print warning
#     print("WARNING: No APP_SECRET_KEY found in environment variables. Using a default key - not secure for production!")
#     # Set a default (not recommended for production)
#     app.secret_key = os.urandom(24)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple User class
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# User loader function
@login_manager.user_loader
def load_user(user_id):
    # In a real app, you'd fetch from the database
    if user_id == '1':
        return User(1, os.environ.get('APP_USERNAME', 'admin'), 
                   os.environ.get('APP_PASSWORD_HASH', generate_password_hash('password')))
    return None

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Get the default user
        user = User(1, os.environ.get('APP_USERNAME', 'admin'), 
                   os.environ.get('APP_PASSWORD_HASH', generate_password_hash('password')))
        
        # Check credentials
        if username == user.username and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next', '/')
            return redirect(next_page)
        
        return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

#reset password route
@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == 'POST':
        recovery_code = request.form.get('recovery_code')
        new_password = request.form.get('new_password')
        
        if recovery_code == os.getenv('RECOVERY_CODE'):
            # Generate new password hash
            new_hash = generate_password_hash(new_password)
            
            # Here you would update your user's password
            # For this simple example, we'll just show that it worked
            return render_template('password_reset_success.html')
        else:
            return render_template('reset_password.html', error="Invalid recovery code")
    
    return render_template('reset_password.html')


# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('noise_detection')
class NoiseDetector:
    def __init__(self, threshold=30, cooldown=10):
        """Initialize the noise detector with configurable threshold and cooldown"""
        self.threshold = threshold  # Default threshold in dB
        self.cooldown = cooldown    # Default cooldown in seconds
        self.is_listening = False   # Tracking if detector is active
        self.audio_stream = None    # PyAudio stream
        self.pyaudio_instance = None  # PyAudio instance
        self.detection_thread = None  # Thread for detection loop
        self.last_alert_time = 0    # Last time an alert was triggered
        self.callback = None        # Callback for when noise is detected
        self.cloud_mode = os.getenv("CLOUD_MODE", "false").lower() == "true"  # Flag for cloud deployment


    def start(self, callback=None):
        """Start the noise detection"""
        if self.is_listening:
            logger.warning("Noise detection already running")
            return False
        
        self.callback = callback
        
        # Initialize PyAudio if not already done
        if not self._initialize_audio():
            logger.error("Failed to initialize audio")
            return False
        
        # Start detection thread
        self.is_listening = True
        self.detection_thread = threading.Thread(target=self._detection_loop)
        self.detection_thread.daemon = True
        self.detection_thread.start()
        logger.info(f"Noise detection started with threshold {self.threshold}dB")
        return True
    
    def stop(self):
        """Stop the noise detection"""
        if not self.is_listening:
            logger.warning("Noise detection not running")
            return False
        
        self.is_listening = False
        # Thread will exit on its own due to while loop condition
        logger.info("Noise detection stopped")
        return True
    
    def set_threshold(self, threshold):
        """Set the noise detection threshold"""
        try:
            self.threshold = float(threshold)
            logger.info(f"Threshold set to {self.threshold}dB")
            return True
        except (ValueError, TypeError):
            logger.error(f"Invalid threshold value: {threshold}")
            return False
    
    def set_cooldown(self, cooldown):
        """Set the cooldown period between alerts"""
        try:
            self.cooldown = int(cooldown)
            logger.info(f"Cooldown set to {self.cooldown} seconds")
            return True
        except (ValueError, TypeError):
            logger.error(f"Invalid cooldown value: {cooldown}")
            return False
    
    def get_current_level(self):
        """Get the current audio level"""
        if not self.audio_stream:
            if not self._initialize_audio():
                return 0
        
        try:
            # Read audio data
            data = self.audio_stream.read(2048, exception_on_overflow=False)
            # Calculate level
            level = self._calculate_audio_level(data)
            return level
        except Exception as e:
            logger.error(f"Error getting audio level: {e}")
            return 0
    
    def _initialize_audio(self):
        """Initialize the audio system with proper error handling"""
            # If in cloud mode, just return a simulated success
        if self.cloud_mode:
            logger.info("Running in cloud mode, audio detection simulated")
            return True
        
        try:
            # Clean up existing resources if any
            if self.audio_stream:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            
            if self.pyaudio_instance:
                self.pyaudio_instance.terminate()
            
            # Initialize PyAudio
            self.pyaudio_instance = pyaudio.PyAudio()
            
            # Find input devices
            input_devices = []
            for i in range(self.pyaudio_instance.get_device_count()):
                device_info = self.pyaudio_instance.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    input_devices.append(i)
                    logger.info(f"Found input device {i}: {device_info['name']}")
            
            if not input_devices:
                logger.error("No audio input devices found")
                return False
            
            # Try to open the default input device first (usually index 0)
            device_to_use = input_devices[0]
            
            # Open audio stream
            self.audio_stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                input_device_index=device_to_use,
                frames_per_buffer=2048
            )
            
            # Test the stream
            test_data = self.audio_stream.read(2048, exception_on_overflow=False)
            test_level = self._calculate_audio_level(test_data)
            logger.info(f"Audio initialized. Test level: {test_level:.2f}dB")
            
            return True
            
        except Exception as e:
            logger.error(f"Error initializing audio: {e}")
            return False
    
    def _calculate_audio_level(self, data):
        """Calculate audio level in decibels using a reliable method"""
        try:
            # Convert buffer to numpy array
            samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            
            # Prevent division by zero with a small epsilon
            epsilon = 1e-10
            
            # Calculate RMS (Root Mean Square)
            rms = np.sqrt(np.mean(np.square(samples)) + epsilon)
            
            # Convert to decibels
            # Reference: maximum possible value for 16-bit audio
            max_possible_value = 32768.0
            
            # Calculate dB relative to full scale (dBFS)
            db_fs = 20 * np.log10(rms / max_possible_value)
            
            # Convert to a positive scale where:
            # - Silence is around 0-10 dB
            # - Normal conversation is around 40-60 dB
            # - Loud noises are 70+ dB
            normalized_db = 60 + db_fs  # Shift by 60dB to make it positive
            
            # Ensure we don't return negative values
            return max(0, normalized_db)
            
        except Exception as e:
            logger.error(f"Error calculating audio level: {e}")
            return 0
    
    def _detection_loop(self):
        """Main loop for noise detection"""
        logger.info("Noise detection loop started")
        
            # In cloud mode, just simulate occasional noise detection
        if self.cloud_mode:
            import random
            while self.is_listening:
                time.sleep(10)  # Check every 10 seconds
                if random.random() < 0.1 and self.callback:  # 10% chance of "detecting" noise
                    logger.info("Simulating noise detection in cloud mode")
                    self.callback(random.uniform(65, 90))  # Random noise level
            return
        
    # Regular implementation for non-cloud mode
        consecutive_loud_samples = 0
        required_loud_samples = 3  # Number of consecutive samples needed to trigger
        
        while self.is_listening:
            try:
                # Read audio data
                data = self.audio_stream.read(2048, exception_on_overflow=False)
                
                # Calculate audio level
                audio_level = self._calculate_audio_level(data)
                
                # Occasionally log the current level for debugging
                if np.random.random() < 0.01:  # 1% chance to log
                    logger.debug(f"Current audio level: {audio_level:.2f}dB (Threshold: {self.threshold}dB)")
                
                # Check if noise exceeds threshold
                if audio_level > self.threshold:
                    consecutive_loud_samples += 1
                    
                    # Check if we have enough consecutive samples and not in cooldown
                    current_time = time.time()
                    time_since_last_alert = current_time - self.last_alert_time
                    
                    if (consecutive_loud_samples >= required_loud_samples and 
                        time_since_last_alert > self.cooldown):
                        
                        logger.info(f"Loud noise detected! Level: {audio_level:.2f}dB")
                        
                        # Update last alert time
                        self.last_alert_time = current_time
                        
                        # Call the callback if set
                        if self.callback:
                            self.callback(audio_level)
                        
                        # Reset counter
                        consecutive_loud_samples = 0
                else:
                    # Reset counter if current sample is not loud
                    consecutive_loud_samples = 0
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.05)
                
            except IOError as e:
                # Handle common PyAudio errors (buffer overflow, etc.)
                logger.warning(f"Audio stream IO error (can be normal): {e}")
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in noise detection loop: {e}")
                time.sleep(0.5)  # Longer delay on error
                
                # Try to reinitialize audio if there's a persistent problem
                if not self._is_stream_active():
                    logger.warning("Audio stream appears inactive, attempting to reconnect...")
                    self._initialize_audio()
    
    def _is_stream_active(self):
        """Check if the audio stream is still active"""
        try:
            return self.audio_stream and self.audio_stream.is_active()
        except:
            return False

    def list_devices(self):
        """List all available audio input devices"""
        devices = []
        try:
            p = pyaudio.PyAudio()
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxInputChannels'],
                        'sample_rate': device_info['defaultSampleRate']
                    })
            p.terminate()
            return devices
        except Exception as e:
            logger.error(f"Error listing devices: {e}")
            return []
    
    def select_device(self, device_index):
        """Select a specific audio input device"""
        try:
            # Stop current stream if active
            if self.is_listening:
                self.stop()
                
            # Close current resources
            if self.audio_stream:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
                self.audio_stream = None
            
            if self.pyaudio_instance:
                self.pyaudio_instance.terminate()
                self.pyaudio_instance = None
            
            # Initialize PyAudio
            self.pyaudio_instance = pyaudio.PyAudio()
            
            # Validate device exists
            device_info = self.pyaudio_instance.get_device_info_by_index(device_index)
            if device_info['maxInputChannels'] <= 0:
                logger.error(f"Device {device_index} is not an input device")
                return False
            
            # Open stream with selected device
            self.audio_stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=2048
            )
            
            # Test stream
            test_data = self.audio_stream.read(2048, exception_on_overflow=False)
            test_level = self._calculate_audio_level(test_data)
            
            logger.info(f"Selected device {device_index}: {device_info['name']}. Test level: {test_level:.2f}dB")
            return True
            
        except Exception as e:
            logger.error(f"Error selecting device {device_index}: {e}")
            return False

    def get_device_diagnostics(self):
        """Get detailed diagnostic information about the audio system"""
        try:
            # Get device info
            devices = self.list_devices()
            
            # Collect sample data
            samples = []
            if self.audio_stream:
                for _ in range(5):  # Get 5 samples
                    data = self.audio_stream.read(2048, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    
                    # Calculate statistics
                    rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
                    max_value = np.max(np.abs(audio_data)) if len(audio_data) > 0 else 0
                    level = self._calculate_audio_level(data)
                    
                    samples.append({
                        "rms": float(rms),
                        "max_value": int(max_value),
                        "level": float(level)
                    })
                    time.sleep(0.1)
            
            return {
                "devices": devices,
                "samples": samples,
                "threshold": float(self.threshold),
                "is_listening": self.is_listening
            }
            
        except Exception as e:
            logger.error(f"Error getting diagnostics: {e}")
            return {
                "error": str(e),
                "devices": [],
                "samples": [],
                "threshold": float(self.threshold),
                "is_listening": self.is_listening
            }

# 🔹 Set Firebase credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "firestore_key.json")

# 🔹 Initialize Firebase Admin SDK
firebase_admin_file = os.getenv("FIREBASE_ADMIN_SDK_FILE", "cloudpetproject1-firebase-adminsdk-fbsvc-08db834ba8.json")
cred = credentials.Certificate(firebase_admin_file)
firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET", "cloudpetproject1.appspot.com")
})

# 🔹 Firestore & Storage
db = firestore.Client()
storage_client = storage.Client()
bucket = storage_client.bucket("cloudpetproject1.appspot.com")

# 🔹 Slack Webhook
SLACK_WEBHOOK_URL_NOISE = os.getenv("SLACK_WEBHOOK_URL_NOISE")
SLACK_WEBHOOK_URL_OBJECT = os.getenv("SLACK_WEBHOOK_URL_OBJECT") 
SLACK_WEBHOOK_URL_SCREENSHOT = os.getenv("SLACK_WEBHOOK_URL_SCREENSHOT")
SLACK_WEBHOOK_URL_RECORDING = os.getenv("SLACK_WEBHOOK_URL_RECORDING")

# if not SLACK_WEBHOOK_URL:
#     logger.warning("⚠️ SLACK_WEBHOOK_URL not set in environment variables!")

# 🔹 Global Variables
latest_frame = None
video_writer = None
recording = False
video_filename = None
video_process = None
is_recording = False  # 🔹 Track recording status
out = None  # 🔹 Video writer object
start_time = None  # 🔹 Store timestamp of recording start


# This is test for locally
# cap = cv2.VideoCapture(0)  # Open webcam

ip_webcam_url = os.getenv("IP_WEBCAM_URL", "http://192.168.x.x:8080/video") # Replace with your IP Webcam URL
cap = cv2.VideoCapture(ip_webcam_url)  # Connect to IP Webcam

# Add a check to ensure the connection is successful
if not cap.isOpened():
    logger.error(f"Failed to connect to IP Webcam at {ip_webcam_url}")
    # Fallback to local webcam if IP webcam fails
    cap = cv2.VideoCapture(0)
    logger.info("Falling back to local webcam")

# Initialize Noise Detector
noise_detector = NoiseDetector(threshold=30, cooldown=10)  # Default values


# Global variables for object detection
detection_model = None
category_index = None
detection_enabled = False
target_object = None  # Object that triggers monitoring (e.g., "couch")
monitor_object = None  # Object to watch for (e.g., "cat")
cooldown_period = 10  # Seconds between alerts for the same detection
last_detection_time = None
detection_threshold = 0.5  # Confidence threshold for detection
proximity_threshold = 0.2  # How close objects need to be (as a fraction of image size)


# ==========================
# 📌 LIVE VIDEO STREAMING
# ==========================
# def generate_frames():
#     global latest_frame, is_recording, out
#     while True:
#         success, frame = cap.read()
#         if not success:
#             print("❌ Failed to grab frame")
#             break
#         else:
#             # Store latest frame for screenshots
#             latest_frame = frame  # 🔴 This is the critical line for screenshots
            
#             # Write frames if recording is ON
#             if is_recording and out is not None:
#                 out.write(frame)
            
#             # Encode frame for streaming
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def generate_frames():
    global latest_frame, is_recording, out
    retry_count = 0
    max_retries = 5
    
    while True:
        success, frame = cap.read()
        if not success:
            retry_count += 1
            logger.warning(f"Failed to read frame, retry {retry_count}/{max_retries}")
            if retry_count > max_retries:
                # Try to reconnect to the camera
                reconnect_camera()
                retry_count = 0
            time.sleep(0.5)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')
            continue
        
        # Reset retry count on success
        retry_count = 0
        
        # Store latest frame for screenshots
        latest_frame = frame.copy()  # Make a copy to avoid reference issues
        
        # Write frames if recording is ON
        if is_recording and out is not None:
            out.write(frame)
        
        # Encode frame for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def reconnect_camera():
    """Attempt to reconnect to the IP camera"""
    global cap
    logger.info("Attempting to reconnect to camera...")
    
    # Close existing connection
    if cap is not None:
        cap.release()
    
    # Try to reconnect
    ip_cam_url = os.getenv("IP_CAM_URL", "http://192.168.1.X:8080/video")
    cap = cv2.VideoCapture(ip_cam_url)
    
    if not cap.isOpened():
        logger.error(f"Failed to reconnect to IP camera")

@app.route('/')
@login_required
def index():
    # Ensure noise detector is running
    global noise_detector
    if not noise_detector.is_listening:
        logger.info("🔄 Starting noise detection from index page")
        noise_detector.start(callback=on_noise_detected)
    
    return render_template('index.html')

@app.route('/video_feed')
@login_required
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ==========================
# 📌 SCREENSHOT FUNCTION
# ==========================
def capture_screenshot():
    global latest_frame
    print("🔄 Capturing frame...") if latest_frame is not None else print("❌ Frame is None")

    if latest_frame is None:
        print("❌ Error: No frame available for screenshot.")
        return None, None
        

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.jpg"
    filepath = get_temp_path(filename)
    cv2.imwrite(filepath, latest_frame)

    print(f"✅ Screenshot saved: {filename}")
    return filename, timestamp

def upload_screenshot(filename, timestamp):
    blob = bucket.blob(f"screenshots/{filename}")
    blob.upload_from_filename(filename)
    blob.make_public()
    image_url = blob.public_url

    db.collection("screenshots").document(timestamp).set({
        "timestamp": timestamp,
        "image_url": image_url
    })

    return image_url

def send_slack_screenshot(image_url):
    slack_url = SLACK_WEBHOOK_URL_SCREENSHOT
    
    if not slack_url:
        logger.warning("Cannot send screenshot alert: SLACK_WEBHOOK_URL_SCREENSHOT not set")
        return
    
    message = {"text": f"📸 Screenshot Taken!\n🔗 {image_url}"}
    requests.post(slack_url, json=message)

@app.route('/take_screenshot', methods=['POST'])
@login_required
def take_screenshot():
    filename, timestamp = capture_screenshot()
    if filename:
        image_url = upload_screenshot(filename, timestamp)
        send_slack_screenshot(image_url)
        return jsonify({"status": "success", "image_url": image_url})
    return jsonify({"status": "error", "message": "Screenshot failed"}), 500

# ==========================
# 📌 VIDEO RECORDING FUNCTION
# ==========================
recording_thread = None

#this test for 60 min max
@app.route('/toggle_recording', methods=['POST'])
@login_required
def toggle_recording():
    global is_recording, out, start_time, video_filename

    if is_recording:
        is_recording = False
        if out is not None:
            out.release()  # Stop video recording

        print("🛑 Video recording stopped!")
        
        # Upload to Firebase Storage
        video_url = upload_video(video_filename)
        
        # Send to Slack
        if video_url:
            send_slack_video(video_url)

        return jsonify({
            "status": "stopped",
            "message": "Recording stopped",
            "video_url": video_url if video_url else None
        }), 200
    else:
        is_recording = True
        start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_filename = f"recording_{start_time}.mp4"
        
        # Use MP4V codec (H.264) for mp4 files
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        
        # Get the camera dimensions
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

        # Add a timer to stop recording after 60 minutes
        def stop_after_timeout():
            global is_recording
            time.sleep(60 * 60)  # 60 minutes in seconds
            if is_recording:
                print("🕒 Maximum recording time (60 minutes) reached. Stopping recording.")
                requests.post('http://localhost:5000/toggle_recording')
                
        # Start timer in a separate thread
        timer_thread = threading.Thread(target=stop_after_timeout)
        timer_thread.daemon = True
        timer_thread.start()

        print(f"🔴 Video recording started! Saving to {video_filename} (Max 60 minutes)")

        return jsonify({
            "status": "recording",
            "message": "Recording started (Max 60 minutes)",
            "video_url": video_filename
        }), 200

@app.route('/start_recording', methods=['POST'])
@login_required
def start_recording():
    global recording, video_filename, video_process
    if recording:
        return jsonify({"status": "error", "message": "Already recording"}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"recording_{timestamp}.mp4"

    # 🔹 Start recording video with sound using FFmpeg
    video_process = subprocess.Popen([
        "ffmpeg",
        "-f", "dshow",
        "-i", "video=Integrated Camera:audio=Microphone (Realtek(R) Audio)",  # Change this to match your device
        "-t", "10",  # Set max recording duration (adjust as needed)
        "-y", video_filename
    ])

    recording = True
    return jsonify({"status": "success", "message": "Recording started"})

@app.route('/stop_recording', methods=['POST'])
@login_required
def stop_recording():
    global recording, video_filename, video_process
    if not recording:
        return jsonify({"status": "error", "message": "Not recording"}), 400

    video_process.terminate()  # Stop FFmpeg
    recording = False

    # Upload to Firebase
    video_url = upload_video(video_filename)
    send_slack_video(video_url)

    return jsonify({"status": "success", "video_url": video_url})

def upload_video(filename):
    # Give the system time to close the file
    time.sleep(1)
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"❌ Error: Video file {filename} not found")
        return None
        
    # Upload to Firebase Storage with correct MIME type
    try:
        blob = bucket.blob(f"videos/{filename}")
        
        # Set the correct MIME type for MP4
        blob.content_type = 'video/mp4'
        
        # Set content disposition to inline so browsers will play it
        blob.content_disposition = 'inline'
        
        # Upload the file
        blob.upload_from_filename(filename)
        blob.make_public()
        video_url = blob.public_url

        # Store metadata in Firestore
        db.collection("videos").document(os.path.basename(filename)).set({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "video_url": video_url
        })
        
        print(f"✅ Video uploaded: {video_url}")
        return video_url
    except Exception as e:
        print(f"❌ Error uploading video: {e}")
        return None

def send_slack_video(video_url):
    message = {
        "text": "🎥 Video Recording Uploaded!",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🎥 *Video Recording Uploaded!*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{video_url}|Click here to view or download the video>"
                }
            }
        ]
    }
    requests.post(SLACK_WEBHOOK_URL_RECORDING, json=message)

# here using claude version 22/3/2025
@app.route('/start_noise_detection', methods=['POST'])
@login_required
def start_noise_detection():
    global noise_detector
    
    # Get custom threshold if provided
    data = request.get_json()
    if data and 'threshold' in data:
        try:
            noise_detector.set_threshold(float(data['threshold']))
        except (ValueError, TypeError):
            pass
    
    # Start detection with callback
    success = noise_detector.start(callback=on_noise_detected)
    
    if success:
        return jsonify({
            "status": "success", 
            "message": f"Noise detection started with threshold {noise_detector.threshold} dB"
        })
    else:
        return jsonify({
            "status": "error", 
            "message": "Failed to start noise detection"
        }), 500

@app.route('/stop_noise_detection', methods=['POST'])
@login_required
def stop_noise_detection():
    global noise_detector
    
    success = noise_detector.stop()
    
    if success:
        return jsonify({
            "status": "success", 
            "message": "Noise detection stopped"
        })
    else:
        return jsonify({
            "status": "warning", 
            "message": "Noise detection not running"
        })

@app.route('/set_noise_threshold', methods=['POST'])
@login_required
def set_noise_threshold():
    global noise_detector
    
    data = request.get_json()
    if data and 'threshold' in data:
        try:
            success = noise_detector.set_threshold(float(data['threshold']))
            if success:
                return jsonify({
                    "status": "success", 
                    "message": f"Noise threshold set to {noise_detector.threshold} dB"
                })
            else:
                return jsonify({
                    "status": "error", 
                    "message": "Failed to set threshold"
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "status": "error", 
                "message": "Invalid threshold value"
            }), 400
    else:
        return jsonify({
            "status": "error", 
            "message": "No threshold provided"
        }), 400

@app.route('/set_cooldown', methods=['POST'])
@login_required
def set_cooldown():
    global noise_detector
    
    data = request.get_json()
    if data and 'cooldown' in data:
        try:
            success = noise_detector.set_cooldown(int(data['cooldown']))
            if success:
                return jsonify({
                    "status": "success", 
                    "message": f"Noise alert cooldown set to {noise_detector.cooldown} seconds"
                })
            else:
                return jsonify({
                    "status": "error", 
                    "message": "Failed to set cooldown"
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "status": "error", 
                "message": "Invalid cooldown value"
            }), 400
    else:
        return jsonify({
            "status": "error", 
            "message": "No cooldown value provided"
        }), 400

@app.route('/test_audio', methods=['GET'])
@login_required
def test_audio():
    global noise_detector
    
    try:
        level = noise_detector.get_current_level()
        
        return jsonify({
            "status": "success",
            "audio_level": float(level),
            "threshold": float(noise_detector.threshold)
        })
    except Exception as e:
        logger.error(f"Error in test_audio: {e}")
        return jsonify({
            "status": "error",
            "message": f"Audio test failed: {str(e)}"
        }), 500

@app.route('/debug_audio', methods=['GET'])
@login_required
def debug_audio():
    global noise_detector
    
    try:
        diagnostics = noise_detector.get_device_diagnostics()
        diagnostics["status"] = "success"
        return jsonify(diagnostics)
    except Exception as e:
        logger.error(f"Error in debug_audio: {e}")
        return jsonify({
            "status": "error",
            "message": f"Audio diagnostic failed: {str(e)}"
        }), 500

@app.route('/list_audio_devices', methods=['GET'])
@login_required
def list_audio_devices():
    global noise_detector
    
    try:
        devices = noise_detector.list_devices()
        return jsonify({
            "status": "success",
            "devices": devices
        })
    except Exception as e:
        logger.error(f"Error listing audio devices: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/select_audio_device', methods=['POST'])
@login_required
def select_audio_device():
    global noise_detector
    
    data = request.get_json()
    if not data or 'device_index' not in data:
        return jsonify({
            "status": "error",
            "message": "No device index provided"
        }), 400
    
    try:
        device_index = int(data['device_index'])
        success = noise_detector.select_device(device_index)
        
        if success:
            # Get current level with new device
            level = noise_detector.get_current_level()
            
            return jsonify({
                "status": "success",
                "message": f"Audio device {device_index} selected successfully",
                "audio_level": float(level)
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"Failed to select device {device_index}"
            }), 500
    except Exception as e:
        logger.error(f"Error selecting audio device: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error selecting audio device: {str(e)}"
        }), 500

def setup_ip_camera_audio():
    """Set up audio streaming from IP camera"""
    global audio_stream
    
    ip_cam_url = os.getenv("IP_CAM_URL", "http://192.168.1.X:8080")
    audio_url = f"{ip_cam_url}/audio.wav"
    
    try:
        # Test if audio stream is available
        response = requests.head(audio_url, timeout=5)
        if response.status_code == 200:
            logger.info(f"IP camera audio stream available at {audio_url}")
            return True
        else:
            logger.warning(f"IP camera audio stream not available")
            return False
    except Exception as e:
        logger.error(f"Error checking IP camera audio: {e}")
        return False

# Callback function for noise detection
def on_noise_detected(level):
    """Callback function when noise is detected"""
    logger.info(f"🔔 NOISE DETECTED - Level: {level:.2f} dB")
    
    try:
        # Capture screenshot
        logger.info("📸 Capturing screenshot...")
        filename, timestamp = capture_screenshot()
        
        if filename:
            logger.info(f"📸 Screenshot captured: {filename}")
            
            # Upload to Firebase
            logger.info("☁️ Uploading screenshot to Firebase...")
            image_url = upload_screenshot(filename, timestamp)
            
            # Record noise event in Firestore
            logger.info("📝 Recording noise event in Firestore...")
            event_data = record_noise_event(level, timestamp, image_url)
            
            # Send notification to Slack
            logger.info("📨 Sending notification to Slack...")
            send_noise_alert_to_slack(level, image_url, timestamp)
            
            # Log success
            logger.info(f"✅ Noise event fully processed: {level:.2f} dB at {timestamp}")
            
            # Clean up local file if desired
            try:
                os.remove(filename)
                logger.info(f"🧹 Cleaned up local file: {filename}")
            except Exception as e:
                logger.warning(f"⚠️ Could not remove local file {filename}: {e}")
            
            return True
        else:
            logger.error("❌ Failed to capture screenshot for noise event")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error processing noise event: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


# testing to add yearly
def record_noise_event(level, timestamp, image_url):
    """Record noise event in Firestore for dashboard reporting"""
    # Parse timestamp from format YYYYMMdd_HHMMSS to a datetime object
    try:
        event_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
    except Exception as e:
        logger.error(f"Error parsing timestamp {timestamp}: {e}")
        event_time = datetime.now()  # Fallback to current time
    
    # Create event data with correctly formatted fields
    event_data = {
        "timestamp": timestamp,
        "level": float(level),
        "image_url": image_url,
        "date": event_time.strftime("%Y-%m-%d"),
        "hour": event_time.hour,
        "week": event_time.strftime("%Y-W%U"),  # Year-Week format
        "month": event_time.strftime("%Y-%m"),
        "year": event_time.strftime("%Y")  # Add year
    }
    
    # Add to noise_events collection
    db.collection("noise_events").document(timestamp).set(event_data)
    logger.info(f"✅ Noise event recorded in Firestore: {level:.2f} dB")
    return event_data


#add a new endpoint to get yearly data
@app.route('/get_yearly_data', methods=['GET'])
@login_required
def get_yearly_data():
    try:
        # Get current year
        now = datetime.now()
        current_year = now.strftime("%Y")
        
        # Initialize yearly data (monthly counts for the current year)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        yearly_data = [0] * 12
        
        # Query for each month in the current year
        for month_idx in range(12):
            month_num = month_idx + 1
            month_query = db.collection("noise_events").where(
                "month", "==", f"{current_year}-{month_num:02d}")
            month_count = len(list(month_query.stream()))
            yearly_data[month_idx] = month_count
        
        return jsonify({
            "status": "success",
            "yearly_data": yearly_data,
            "months": months
        })
    
    except Exception as e:
        print(f"❌ Error getting yearly data: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "yearly_data": [0] * 12,
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        }), 500

def send_noise_alert_to_slack(level, image_url, timestamp):
    """Send noise alert with screenshot to Slack"""
    formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
    slack_url = SLACK_WEBHOOK_URL_NOISE

    if not slack_url:
        logger.warning("Cannot send noise alert: SLACK_WEBHOOK_URL_NOISE not set")
        return
    
    message = {
        "text": f"🔊 Loud Noise Detected!",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🔊 Loud Noise Detected!*\n• Level: *{level:.2f} dB*\n• Time: {formatted_time}"
                }
            },
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": f"Noise Event Screenshot ({formatted_time})"
                },
                "image_url": image_url,
                "alt_text": "Noise event screenshot"
            }
        ]
    }
    
    requests.post(slack_url, json=message)
    print("✅ Noise alert sent to Slack")

def send_slack_alert(noise_level, image_url):
    if not SLACK_WEBHOOK_URL_NOISE:
        logger.warning("Cannot send Slack alert: SLACK_WEBHOOK_URL not set")
        return False
        
    message = {
        "text": f"🚨 Loud Noise Detected! 🚨\nNoise Level: {noise_level} dB\nScreenshot: {image_url}"
    }
    response = requests.post(SLACK_WEBHOOK_URL_NOISE, json=message)
    return response.status_code == 200

@app.route('/noise_detector_status', methods=['GET'])
@login_required
def noise_detector_status():
    """Return detailed status of the noise detector for troubleshooting"""
    global noise_detector
    
    try:
        # Get current audio level
        current_level = noise_detector.get_current_level()
        
        # Get active device info
        devices = noise_detector.list_devices()
        active_device = None
        for device in devices:
            if device.get('active', False):
                active_device = device
        
        # Collect status info
        status_info = {
            "status": "success",
            "is_listening": noise_detector.is_listening,
            "threshold": noise_detector.threshold,
            "cooldown": noise_detector.cooldown,
            "current_level": float(current_level),
            "last_alert_time": noise_detector.last_alert_time,
            "time_since_last_alert": time.time() - noise_detector.last_alert_time if noise_detector.last_alert_time else None,
            "audio_stream_active": noise_detector._is_stream_active(),
            "active_device": active_device,
            "available_devices": devices,
            "system_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return jsonify(status_info)
    except Exception as e:
        logger.error(f"Error getting noise detector status: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error_type": str(type(e)),
            "error_traceback": str(e.__traceback__)
        }), 500



# Add this route to get noise data for the dashboard
# add the year data
# Add this at line 650 or so, after the get_noise_data route declaration
@app.route('/get_noise_data', methods=['GET'])
@login_required
def get_noise_data():
    try:
        # Get current date and time
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        current_week = now.strftime("%Y-W%U")
        current_month = now.strftime("%Y-%m")
        current_year = now.strftime("%Y")
        
        # Initialize data structures
        daily_data = [0] * 24
        weekly_data = [0] * 7
        monthly_data = [0] * 31  # Maximum days in a month
        yearly_data = [0] * 12   # 12 months in a year
        recent_events = []
        
        # Query Firestore for noise events
        # Daily data (today's events by hour)
        daily_query = db.collection("noise_events").where("date", "==", today)
        daily_results = list(daily_query.stream())
        
        for doc in daily_results:
            data = doc.to_dict()
            hour = data.get('hour', 0)
            if 0 <= hour < 24:
                daily_data[hour] += 1
        
        # Weekly data (this week's events by day)
        # Calculate start of week (Sunday)
        start_of_week = now - timedelta(days=now.weekday() + 1)
        for day in range(7):
            date = (start_of_week + timedelta(days=day)).strftime("%Y-%m-%d")
            day_query = db.collection("noise_events").where("date", "==", date)
            day_count = len(list(day_query.stream()))
            weekly_data[day] = day_count
        
        # Monthly data (this month's events by day)
        days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
        for day in range(1, days_in_month + 1):
            day_str = f"{day:02d}"
            month_str = f"{now.month:02d}"
            date = f"{now.year}-{month_str}-{day_str}"
            day_query = db.collection("noise_events").where("date", "==", date)
            day_count = len(list(day_query.stream()))
            monthly_data[day - 1] = day_count
            
        # Yearly data (this year's events by month)
        for month in range(1, 13):
            month_prefix = f"{current_year}-{month:02d}"
            month_query = db.collection("noise_events").where(
                "month", "==", month_prefix)
            month_count = len(list(month_query.stream()))
            yearly_data[month - 1] = month_count
        
        # Recent events (limit to 10)
        recent_query = (db.collection("noise_events")
                        .order_by("timestamp", direction=firestore.Query.DESCENDING)
                        .limit(10))
        
        recent_docs = list(recent_query.stream())
        for doc in recent_docs:
            data = doc.to_dict()
            # Convert timestamp string to datetime for proper sorting
            try:
                event_timestamp = datetime.strptime(data.get('timestamp', ''), "%Y%m%d_%H%M%S")
                formatted_timestamp = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_timestamp = data.get('timestamp', '')
                
            recent_events.append({
                "timestamp": data.get('timestamp', ''),
                "level": data.get('level', 0),
                "image_url": data.get('image_url', '')
            })
        
        return jsonify({
            "status": "success",
            "daily_data": daily_data,
            "weekly_data": weekly_data,
            "monthly_data": monthly_data[:days_in_month],  # Trim to actual days in month
            "yearly_data": yearly_data,
            "recent_events": recent_events
        })
    
    except Exception as e:
        print(f"❌ Error getting noise data: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "daily_data": [0] * 24,
            "weekly_data": [0] * 7,
            "monthly_data": [0] * 31,
            "yearly_data": [0] * 12,
            "recent_events": []
        }), 500



## Object detection
# ==========================
# 📌 OBJECT DETECTION SCREENSHOT
# ==========================
@app.route('/object_detection_screenshot', methods=['POST'])
@login_required
def object_detection_screenshot():
    data = request.get_json()
    primary_object = data.get('primaryObject', 'object')
    secondary_object = data.get('secondaryObject', 'location')
    
    # Capture the screenshot
    filename, timestamp = capture_screenshot()
    
    if filename:
        # Upload to Firebase
        image_url = upload_screenshot(filename, timestamp)
        
        # Record detection event in Firestore
        event_data = {
            "timestamp": timestamp,
            "primaryObject": primary_object,
            "secondaryObject": secondary_object,
            "image_url": image_url,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "hour": datetime.now().hour,
            "week": datetime.now().strftime("%Y-W%U"),  # Year-Week format
            "month": datetime.now().strftime("%Y-%m")
        }
        
        # Add to detection_events collection
        db.collection("detection_events").document(timestamp).set(event_data)
        
        # Send to Slack
        send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp)
        
        return jsonify({
            "status": "success", 
            "message": f"{primary_object} near {secondary_object} detected!",
            "image_url": image_url
        })
    
    return jsonify({
        "status": "error", 
        "message": "Failed to capture screenshot"
    }), 500

def send_detection_alert_to_slack(primary_object, secondary_object, image_url, timestamp):
    """Send object detection alert with screenshot to Slack"""
    formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
    emoji_map = {
        "cat": "🐱",
        "dog": "🐶",
        "bird": "🐦",
        "person": "👤",
        "couch": "🛋️",
        "bed": "🛏️",
        "laptop": "💻",
        "keyboard": "⌨️",
        "cell phone": "📱",
        "tv": "📺",
        "oven": "🔥"
    }
    
    primary_emoji = emoji_map.get(primary_object.lower(), "📷")
    secondary_emoji = emoji_map.get(secondary_object.lower(), "📍")
    
    message = {
        "text": f"{primary_emoji} {primary_object.title()} near {secondary_object} detected!",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{primary_emoji} {primary_object.title()} near {secondary_object} detected! {secondary_emoji}*\n• Time: {formatted_time}"
                }
            },
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": f"{primary_object.title()} near {secondary_object} ({formatted_time})"
                },
                "image_url": image_url,
                "alt_text": "Detection event screenshot"
            }
        ]
    }
    
    requests.post(SLACK_WEBHOOK_URL_OBJECT, json=message)
    print(f"✅ Object detection alert sent to Slack: {primary_object} near {secondary_object}")


# ==========================
# 📌 Backend API for Gallery
# ==========================
@app.route('/get_screenshots', methods=['GET'])
@login_required
def get_screenshots():
    try:
        # Get manual screenshots
        manual_screenshots = []
        screenshots_ref = db.collection("screenshots").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
        for doc in screenshots_ref:
            data = doc.to_dict()
            manual_screenshots.append(data)
        
        # Get noise detection screenshots
        noise_screenshots = []
        noise_ref = db.collection("noise_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
        for doc in noise_ref:
            data = doc.to_dict()
            noise_screenshots.append(data)
        
        # Get object detection screenshots
        object_screenshots = []
        object_ref = db.collection("detection_events").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
        for doc in object_ref:
            data = doc.to_dict()
            object_screenshots.append(data)
        
        # Get video recordings
        videos = []
        videos_ref = db.collection("videos").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()
        for doc in videos_ref:
            data = doc.to_dict()
            videos.append(data)
            
        return jsonify({
            "status": "success",
            "manual_screenshots": manual_screenshots,
            "noise_screenshots": noise_screenshots,
            "object_screenshots": object_screenshots,
            "videos": videos
        })
    
    except Exception as e:
        print(f"❌ Error fetching gallery data: {e}")
        return jsonify({
            "status": "error", 
            "message": str(e),
            "manual_screenshots": [],
            "noise_screenshots": [],
            "object_screenshots": [],
            "videos": []
        }), 500
    


# Add these functions to save to temporary directory that gets cleaned up
def get_temp_path(filename):
    temp_dir = os.getenv("TEMP_DIR", "uploads")
    os.makedirs(temp_dir, exist_ok=True)
    return os.path.join(temp_dir, filename)

# Add regular cleanup for temporary files:
def cleanup_temp_files():
    """Clean up temporary files older than 1 hour"""
    temp_dir = os.getenv("TEMP_DIR", "uploads")
    threshold = time.time() - 3600  # 1 hour ago
    
    try:
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            if os.path.isfile(filepath) and os.path.getmtime(filepath) < threshold:
                os.remove(filepath)
                logger.info(f"Cleaned up old file: {filepath}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

# Add a health check endpoint:
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "camera_connected": cap.isOpened(),
        "noise_detector_active": noise_detector.is_listening
    })


# ==========================
# 📌 RUN APP
# ==========================
if __name__ == '__main__':
    # Initialize noise detector
    logger.info("Starting application and initializing noise detector...")
    noise_detector.start(callback=on_noise_detected)
    
    # Auto-start noise detection
    if noise_detector._initialize_audio():
        logger.info("✅ Noise detector initialized successfully")
    else:
        logger.warning("⚠️ Noise detector initialization failed")
    
    # Register cleanup handler
    atexit.register(lambda: noise_detector.stop())
    
    # Run the Flask app locally
    # app.run(debug=True)

    # Run the flask app on the cloud
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  



# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hello, Fly.io!"