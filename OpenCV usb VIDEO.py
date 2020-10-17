import cv2
import os
import time


cap = cv2.VideoCapture(1)                
#启用外接摄像头                                        

fourcc = cv2.VideoWriter_fourcc(*'XVID')
#规定视频编码器

out = cv2.VideoWriter('C:\\Users\\Specialized\\Desktop\\output.mp4',fourcc, 30.0, (640,480))
#规定视频输出路径，编码器，帧率，画幅

sum_time = 0
#初始化计时器

pic_num = 0
#初始化保存图片的后缀数

while(cap.isOpened()):
    time_start = time.time()
    #开始计时

    ret, frame = cap.read()

    if ret==True:
        frame = cv2.flip(frame,0)             #视频旋转180°，因为我外接的摄像头线太靠下放不到桌子上，我把它翻了过来


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #设置图像灰度
        xmlfile = r'E:\\VS2017\\Anaconda3_64\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml'
        #人脸识别分类器目录，现在我把它也在工程目录下拷贝了一份

        face_cascade = cv2.CascadeClassifier(xmlfile)
        #载入人脸识别分类器

        faces = face_cascade.detectMultiScale(
            gray,                             #灰度转化
            scaleFactor=1.5,                  #比例因子，抵消补偿人脸与摄像头间距
            minNeighbors=5,                   #可检测目标数
            minSize=(30, 30),                 #窗口大小
        )
        print("发现{0}个人脸!".format(len(faces)))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + w), (0, 255, 0), 2)
        #设置框住人脸的矩形长度

        out.write(frame)                      #写入视频流

        cv2.imshow('frame',frame)             #展示监视器

        if cv2.waitKey(1) == ord('q'):        #每间隔1ms判断是否有q的退出指令从键盘输入
            break
    else:
        break


    time_end = time.time()
    #结束计时
    sum_time = (time_end - time_start)+sum_time
    #计算总时长

    if sum_time >= 4.9:                      #测试时每5秒保存一次，如果需要30分钟的话，改成1800即可
        cv2.imwrite("%s/output%d.jpeg" %('C:\\Users\\Specialized\\Desktop' , pic_num), cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA))
        #图片保存地址以及格式，画幅，像素插值
        pic_num += 1
        #图片后缀数递增
        sum_time = 0
        #计时归零



cap.release()
out.release()
cv2.destroyAllWindows()
#释放以及关闭进程
