import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# 현재 모듈의 절대 경로를 알아내어 상위 폴더 절대경로를 참조 path에 추가하는 방식

# 예를 들면 현재모듈의 절대경로 /home/tommy/augmentation/task/doQuick이면
# 상위 폴더 절대경로인 /home/tommy/augmentation/task를 참조 path에 추가해야한다

# doQuick 모듈이 참조 path에 추가되었는지는 dir()함수를 통해 파악할 수 있다

#  참고 : https://brownbears.tistory.com/296


from qsort import doQuick #qsort.py의 doQuick 클래스(모듈)을 import



if __name__ == "__main__": #entry point : 진입점
    print('dir : ',dir())
    arr = [1, 10, 2, 5, 3, 4, 9, 6, 8, 7]
    print('arr 정렬 전 : ', arr)
    qui=doQuick()
    print('타입 : ',type(qui))
    qui.quick_sort(arr)
    print('arr 정렬 후 : ', arr)
