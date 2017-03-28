import cv2, os, time
import numpy as np
from PIL import Image
from selenium import webdriver

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

recognizer = cv2.face.createLBPHFaceRecognizer()

def image_and_label(path):
    image_paths = [os.path.join(path,f) for f in os.listdir(path)]
    images=[]
    labels=[]
    for image_path in image_paths:
        image_pil = Image.open(image_path).convert('L')
        image = np.array(image_pil, 'uint8')
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject",""))
        faces = faceCascade.detectMultiScale(image)
        for (x,y,w,h) in faces:
            images.append(image[y:y+h,x:x+w])
            labels.append(nbr)
            cv2.imshow("Creating Database...", image[y:y+h,x:x+w])
            #cv2.waitKey(20)
    return images,labels
path = 'real_db'
images, labels = image_and_label(path)
cv2.destroyAllWindows()
camera_port = 0
ramp_frames = 30

cam = cv2.VideoCapture(camera_port)

def get_img():
    getval, im = cam.read()
    return im

for i in range(ramp_frames):
    temp = get_img()
    print("Capturing Image")

img = get_img()
file = "check//test.jpg"
cv2.imwrite(file, img)
recognizer.train(images,np.array(labels))
reco_path = 'check'
person = 16
image_paths = [os.path.join(reco_path,f) for f in os.listdir(reco_path)]
print(image_paths)
for image_path in image_paths:
    predict_image_pil = Image.open(image_path).convert('L')
    predict_image = np.array(predict_image_pil, 'uint8')
    faces = faceCascade.detectMultiScale(predict_image)
    for (x,y,w,h) in faces:
        nbr_predicted, conf = recognizer.predict(predict_image[y:y+h, x:x+w])
        #nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject",""))
        #if nbr_actual == nbr_predicted:
        #    print("{} is Correctly Recognized with confidence {}".format(nbr_actual, conf))
        #else:
        #    print("Not matched")
        print(conf)
        if nbr_predicted==person:
            driver = webdriver.Firefox(
                executable_path=r'geckodriver.exe')
            driver.get("https://facebook.com")
            email = "email"
            password = "pass"
            login = "loginbutton"
            emailelement = driver.find_element_by_name(email)
            passwordelement = driver.find_element_by_name(password)
            emailelement.send_keys("<<yourid>>")
            passwordelement.send_keys("<<yourpassword>>")
            loginelement = driver.find_element_by_id(login)
            loginelement.click()
            while(1):
                os.remove(file)
                time.sleep(5)
                img = get_img()
                cv2.imwrite(file, img)
                print("checking for person")
                for image_path in image_paths:
                    predict_image_pil = Image.open(image_path).convert('L')
                    predict_image = np.array(predict_image_pil, 'uint8')
                    faces = faceCascade.detectMultiScale(predict_image)
                    nbr_predicted=0
                    for (x, y, w, h) in faces:
                        nbr_predicted, conf = recognizer.predict(predict_image[y:y + h, x:x + w])
                if nbr_predicted!=person:
                    print("Person not found")
                    time.sleep(30)
                    os.remove(file)
                    time.sleep(5)
                    img = get_img()
                    cv2.imwrite(file, img)
                    for image_path in image_paths:
                        predict_image_pil = Image.open(image_path).convert('L')
                        predict_image = np.array(predict_image_pil, 'uint8')
                        faces = faceCascade.detectMultiScale(predict_image)
                        nbr_predicted=0
                        for (x, y, w, h) in faces:
                            nbr_predicted, conf = recognizer.predict(predict_image[y:y + h, x:x + w])
                    if nbr_predicted!=person:
                        print("Person gone")
                        logout1 = driver.find_element_by_css_selector("#userNavigationLabel")
                        logout1.click()
                        time.sleep(10)
                        logout2 = driver.find_element_by_css_selector(
                            "._w0d[action='https://www.facebook.com/logout.php']").submit()
                        # Closing Browser.
                        driver.quit()
                        print("User Logout Successfully !!")
                        break
                else:
                    print("Person found")
        else:
            print("Person Not recognised")
        cv2.waitKey(0)