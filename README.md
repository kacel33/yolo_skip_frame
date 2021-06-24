# yolo_skip_frame
### 모든 frame에서 yolo로 추론하는 것이 아닌 한번 추론 후 n개의 frame을 건너 뛰는 코드입니다.

## 배경
현재 단일 이미지에서Object Detection 성능은 매우 좋은 편입니다. 하지만 처리 속도가 너무 느리고 임베디드 시스템에서는 주로 영상을 받아서 Object Detection을 수행하는데 jetson nano에서 Yolov4 모델은 fps가 2~3, Yolov4-tiny 모델은 11정도가 나옵니다. 그리고 사용자가 어떤 시스템을 만들 때 Object Detection에서의 GPU메모리와 연산을 줄이고 싶어할 것입니다. 연구 논문에서는 하이엔드 GPU에서 다른 기능 없이 YOLO만 구동했을 때 real-time이 가능하다고 하지만 실제 사용자들은 상대적으로 낮은 사양의 GPU를 사용하거나 CPU를 사용하기 때문에 일반적으로는 자연스러운 real-time을 하기가 힘든 상황입니다. 저 또한 jetson nano에서 yolo를 사용할 때 fps가 굉장히 떨어져서 yolov4-tiny모델과 tensorrt를 사용하였습니다.  

Video 영상의 특징은 일반적으로 매 frame은 인접한 frame과의 연관성이 큽니다. 그 상황에서 매 frame마다 YOLO를 돌리는 것은 굉장한 메모리 낭비와 계산 낭비라고 생각합니다.  
#  
![image](https://user-images.githubusercontent.com/60708119/123047728-994ab800-d438-11eb-908d-147aa3af69ea.png)

어떤 영상의 fps가 60이라고 한다면 다음 frame과의 시간 차이는 0.0167초입니다. 그리고 일반적인(추측하건데 90%이상) 상황에서는 영상을 구성하는 시스템(배경, 동적 물체, 사물 등등)은 거의 비슷할 것입니다. 그래서 다른 알고리즘 없이 YOLO모델을 한 frame씩 건너 뛰어서 홀수 번째 frame에서만 YOLO모델을 구동하면 오차가 생기지만 정확도가 크게 떨어지지 않을 것이라고 생각합니다. 하지만 계산속도는 2배가 됩니다. 한 frame이 아니라 n개의 frame을 건너 뛴다면 정확도는 크게 줄 것이지만 연산 속도는 거의 n배만큼 빨라질 것입니다.   

![image](https://user-images.githubusercontent.com/60708119/123048004-e62e8e80-d438-11eb-81a3-6536745b3336.png)


위의 아이디어로 코드를 작성하였습니다.
그리고 실험 결과 녹화된 비디오, N=1, 홀수번 째 frame에서만 YOLO를 사용할 때 시각적으로 보이는 장면이 바뀌는 경우 외에는 거의 없었습니다. 

## 실행방법

<pre><code>python run.py --video {VIDEO FILE} --weights {your_YOLO.weights} --cfg {your_YOLO.cfg}</code></pre>

## Example
<pre><code>python run.py --video walking_cut1.mp4 --weights yolo_weights_cfg/yolov4.weights --cfg yolo_weights_cfg/yolov4.cfg</code></pre>

## OPENCV GPU가 있다면
<pre><code>python run.py --video walking_cut1.mp4 --gpu True --weights yolo_weights_cfg/yolov4.weights --cfg yolo_weights_cfg/yolov4.cfg</code></pre>

### **YOLO모델을 CUSTOM으로 학습시키는 경우 yolo.py에 있는 class 내용을 변경해야 합니다.**
