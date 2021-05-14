    # <퀵 정렬>
    # 
    #   시간 복잡도 -> 평균 : nlogn , 최악일 때 : n^2  

class doQuick:
    def __init__(self):
        pass


    def quick_sort(self,arr): 
      
        def sort(low, high): # sort() 함수는 재귀 함수이며 정렬 범위를 시작 인덱스와 끝 인덱스로 인자로 받습니다. 

            if high <= low:  # high가 low보다 작거나 같을때까지 반복
                return

            mid = partition(low, high) # partition() 함수는 정렬 범위를 인자로 받으며 다음 로직을 따라서 좌우측의 값들을 정렬하고 분할 기준점의 인덱스를 리턴합니다. 
           
            sort(low, mid - 1)
            sort(mid, high) # 이 분할 기준점(mid)는 sort()를 재귀적으로 호출할 때 우측 리스트의 시작 인덱스로 사용됩니다.

        def partition(low, high):
            pivot = arr[(low + high) // 2]
            #1. 리스트 안에 있는 한 요소를 선택한다. 이렇게 고른 원소를 피벗(pivot) 이라고 한다.
            # pivot은 가운데로 잡을 때 가장 속도가 빠른 것으로 나타난다. 참고 : https://ghd5262.tistory.com/25

            while low <= high: #while 루프를 두 인덱스가 서로 교차해서 지나칠 때까지 반복

                while arr[low] < pivot:     # 시작 인덱스(low)가 가리키는 값과 pivot 값을 비교해서 더 작은 경우
                    low += 1                # 시작 인덱스(low)는 계속 증가 시키고, 

                while arr[high] > pivot:    # 끝 인덱스(high)가 가리키는 값과 pivot 값을 비교해서 더 작은 경우
                    high -= 1               # 끝 인덱스(high)는 계속 감소 시킨다.


                if low <= high: # 두 인덱스가 아직 서로 교차해서 지나치치 않았다면 swap
                    arr[low], arr[high] = arr[high], arr[low]
                    low, high = low + 1, high - 1 #두 인덱스를 각자 진행 방향으로 한 칸씩 이동

            return low #다음 재귀 호출의 분할 기준점이될 시작 인덱스를 리턴

        return sort(0, len(arr) - 1)






