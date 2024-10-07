import cv2
import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from PIL import Image, ImageTk

# 建立主視窗
root = tk.Tk()
root.title("簡單的人臉替換")

# 全域變數
img = None
replacement_face = None

# 載入待替換的圖像
def load_image():
    global img, panel

    img_path = filedialog.askopenfilename(title="選擇待檢測的圖像", 
                                          filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if img_path:
        print(f"選擇的圖片路徑: {img_path}")  # 打印路徑
        img = cv2.imread(img_path)
        if img is None:
            print("無法載入圖片，請檢查文件路徑或格式。")
            return
        show_image(img)


# 載入替換的面部圖像
def load_replacement_face():
    global replacement_face

    face_img_path = filedialog.askopenfilename(title="選擇替換面部的圖像", 
                                               filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if face_img_path:
        replacement_face = cv2.imread(face_img_path)

# 進行人臉替換
def replace_faces():
    global img, replacement_face

    if img is None or replacement_face is None:
        return

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        resized_face = cv2.resize(replacement_face, (w, h))
        img[y:y+h, x:x+w] = resized_face

    show_image(img)

# 顯示圖像
def show_image(image):
    cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=pil_image)
    panel.configure(image=imgtk)
    panel.image = imgtk

# 建立按鈕和圖像顯示區域
load_img_btn = ttk.Button(root, text="載入待檢測圖像", command=load_image, padding=5,width=15)
load_img_btn.pack()

load_face_btn = ttk.Button(root, text="載入替換面部圖像", command=load_replacement_face, padding=5,width=15)
load_face_btn.pack()

replace_btn = ttk.Button(root, text="執行面部替換", command=replace_faces, padding=5,width=15)
replace_btn.pack()

# 圖片顯示區域
panel = tk.Label(root)
panel.pack()

# 開始主循環
root.mainloop()
