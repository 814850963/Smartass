from django.http import JsonResponse
from django.views import View

from android.models import *
from smartass import Utils, settings
import cv2
import os
import pandas as pd  # 数据处理的库 Pandas
import dlib
from skimage import io
import csv
import numpy as np

# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()

# Dlib 人脸预测器
predictor = dlib.shape_predictor("android/view/data/data_dlib/shape_predictor_68_face_landmarks.dat")

# Dlib 人脸识别模型
# Face recognition model, the object maps human faces into 128D vectors
face_rec = dlib.face_recognition_model_v1("android/view/data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

#人脸录入
class RecordFaceData(View):
    # 返回单张图像的 128D 特征
    def return_128d_features(self,path_img):
        img_rd = io.imread(path_img)
        img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
        faces = detector(img_gray, 1)
        print("%-40s %-20s" % ("检测到人脸的图像 / image with faces detected:", path_img), '\n')
        # 因为有可能截下来的人脸再去检测，检测不出来人脸了
        # 所以要确保是 检测到人脸的人脸图像 拿去算特征
        if len(faces) != 0:
            shape = predictor(img_gray, faces[0])
            face_descriptor = face_rec.compute_face_descriptor(img_gray, shape)
        else:
            face_descriptor = 0
            print("no face")
        return face_descriptor

    # 将文件夹中照片特征提取出来, 写入 CSV
    def return_features_mean_personX(self,files):
        features_list_personX = []
        if files:
            for f in files:
                # 调用return_128d_features()得到128d特征
                print("%-40s %-20s正在读的人脸图像 / image to read:")
                features_128d = self.return_128d_features(f)
                #  print(features_128d)
                # 遇到没有检测出人脸的图片跳过
                if features_128d == 0:
                    pass
                else:
                    features_list_personX.append(features_128d)
        else:
            print("文件夹内图像文件为空 / Warning: No images in ", '\n')

        # 计算 128D 特征的均值
        # personX 的 N 张图像 x 128D -> 1 x 128D
        if features_list_personX:
            features_mean_personX = np.array(features_list_personX).mean(axis=0)
        else:
            features_mean_personX = '0'
        return features_mean_personX

    def post(self,request):
        files = request.FILES.getlist("img","")
        authon = request.POST.get('auth')
        identity = request.POST.get('identity')
        print(request.POST)
        print(request.FILES)
        # 获取已录入的最后一个人脸序号 / get the num of latest person
        filename = Utils.makerandomuuid('csv')
        with open("android/view/data/features/"+filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Get the mean/average features of face/personX, it will be a list with a length of 128D
            features_mean_personX = self.return_features_mean_personX(files)
            writer.writerow(features_mean_personX)
            print("特征均值 / The mean of features:", list(features_mean_personX))
            print("所有录入人脸数据存入 / Save all the features of faces registered into: "+filename)
            #0为老师
            if identity == 0:
                file = Teacher.objects.get(teacherid=authon).facedata
                if file !=None:
                    os.remove(file)
                Teacher.objects.filter(teacherid=authon).update(facedata="android/view/data/features/"+filename)
            else:
                file = Student.objects.get(studentid=authon).facedata
                if file !=None:
                    os.remove(file)
                Student.objects.filter(studentid=authon).update(facedata="android/view/data/features/" + filename)
        data = {
            "status": '1',
            "result": "ok",
            "authen": None
        }
        return JsonResponse(data)
# # 生成随机的名字
#         filename = Utils.makerandomuuid("jpeg")
#人脸登录
class FaceLogin(View):
    # 计算两个128D向量间的欧式距离
    # Compute the e-distance between two 128D features
    def return_euclidean_distance(self,feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    def post(self,request):
        files = request.FILES.getlist("img","")
        authon = request.POST.get('auth')
        identity = request.POST.get('identity')
        print(request.POST)
        print(request.FILES)
        # 1. Check 存放所有人脸特征的 csv
        # 0为老师
        if identity == 0:
            filename = Teacher.objects.get(teacherid=authon).facedata
        else:
            filename = Student.objects.get(studentid=authon).facedata
        print(filename)
        if filename == None:
            data = {
                "status": 0,
                "result": "考勤失败未设置人脸",
            }
            return JsonResponse(data)
        if os.path.exists(filename):
            csv_rd = pd.read_csv(filename, header=None)

            # 用来存放所有录入人脸特征的数组
            # The array to save the features of faces in the database
            features_known_arr = []

            # 2. 读取已知人脸数据
            # Print known faces
            # 从这里提取
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                for j in range(0, len(csv_rd.ix[i, :])):
                    features_someone_arr.append(csv_rd.ix[i, :][j])
                features_known_arr.append(features_someone_arr)
            print("Faces in Database：", len(features_known_arr))

            # Dlib 检测器和预测器
            # The detector and predictor will be used
            img_rd = io.imread(files[0])
            img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)
            # 从这里提取
            faces = detector(img_gray, 0)
            # 检测到人脸 when face detected
            if len(faces) != 0:
                # 4. 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
                # 4. Get the features captured and save into features_cap_arr
                features_cap_arr = []
                for i in range(len(faces)):
                    shape = predictor(img_rd, faces[i])
                    features_cap_arr.append(face_rec.compute_face_descriptor(img_rd, shape))
                # 5. 遍历捕获到的图像中所有的人脸
                # 5. Traversal all the faces in the database
                for k in range(len(faces)):
                    print("##### camera person", k + 1, "#####")
                    for i in range(len(features_known_arr)):
                        # 如果 person_X 数据不为空
                        if str(features_known_arr[i][0]) != '0.0':
                            print("with person", str(i + 1), "the e distance: ", end='')
                            # print(features_cap_arr[k])
                            # print("=====================")
                            # print(features_known_arr[i])
                            # print("*************************")
                            e_distance_tmp = self.return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                            print("欧氏距离"+str(e_distance_tmp))
                            e_distance=e_distance_tmp
                        else:
                            # 空数据 person_X
                            e_distance=999999999
                    if e_distance < 0.4:
                        data = {
                            "status": '1',
                            "result": "考勤成功",
                            "authen": None
                        }

                        return JsonResponse(data)
                    else:
                        print("Unknown person")
                        data = {
                            "status": 0,
                            "result": "考勤失败",
                        }
                        return JsonResponse(data)
        else:
            print('##### Warning #####', '\n')
            print("'features_all.py' not found!")
            print(
                "Please run 'get_faces_from_camera.py' and 'features_extraction_to_csv.py' before 'face_reco_from_camera.py'",
                '\n')
            print('##### Warning #####')
        data = {
            "status": 0,
            "result": "找不到人脸数据",
        }
        return JsonResponse(data)

