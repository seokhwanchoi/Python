
import os
import PySpin
import sys, json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print('dir : ',dir())
import socket, threading
import acq3
#from acq3 import acquisition3

class acquisition3:
    

    def acquire_images(self,cam, nodemap, nodemap_tldevice, msg):
        
        print('*** IMAGE ACQUISITION ***\n')
        try:
            result = True

        
            node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
            if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode): #파이썬에서 0은 False, True는 1
                print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...') # abort : 중단하다, retrieval : 검색
                return False

            # Retrieve entry node from enumeration node   //// entry : 입장, 입력
            node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
            if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(node_acquisition_mode_continuous):
                print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
                return False

            # Retrieve integer value from entry node
            acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

            # Set integer value from entry node as new value of enumeration node
            node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

            print('Acquisition mode set to continuous...')

            cam.BeginAcquisition()

            print('Acquiring images...')

            device_serial_number = ''
            node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
            if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
                device_serial_number = node_device_serial_number.GetValue()
                print('Device serial number retrieved as %s...' % device_serial_number)

            # Retrieve, convert, and save images
     
            try:

         
                image_result = cam.GetNextImage(1000) #1000ms 1초?

                
                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())

                else:

                    image_converted = image_result.Convert(PySpin.PixelFormat_Mono8, PySpin.HQ_LINEAR)

          
                    filename =  msg 

                    image_converted.Save(filename)

                    print('Image saved at %s' % filename)

                    image_result.Release()
                    print('')

            except PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                return False

            #  End acquisition
            #
            #  *** NOTES ***
            #  Ending acquisition appropriately helps ensure that devices clean up
            #  properly and do not need to be power-cycled to maintain integrity.
            cam.EndAcquisition()
        
        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

        return result


    def print_device_info(self, nodemap):


        print('*** DEVICE INFORMATION ***\n')

        try:
            result = True
            node_device_information = PySpin.CCategoryPtr(nodemap.GetNode('DeviceInformation'))

            if PySpin.IsAvailable(node_device_information) and PySpin.IsReadable(node_device_information):
                features = node_device_information.GetFeatures()
                for feature in features:
                    node_feature = PySpin.CValuePtr(feature)
                    print('%s: %s' % (node_feature.GetName(),
                                    node_feature.ToString() if PySpin.IsReadable(node_feature) else 'Node not readable'))

            else:
                print('Device control information not available.')

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

        return result


    def run_single_camera(self,cam, msg):

        try:
            result = True

            # Retrieve TL device nodemap and print device information
            nodemap_tldevice = cam.GetTLDeviceNodeMap() #TransportLayerDevice

            result &= self.print_device_info(nodemap_tldevice)

            # Initialize camera
            cam.Init()

            # Retrieve GenICam nodemap
            nodemap = cam.GetNodeMap()

            # Acquire images
            result &= self.acquire_images(cam, nodemap, nodemap_tldevice, msg)

            # Deinitialize camera
            cam.DeInit()

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result


    def main(self, msg):
        print('hello')
        try:
            test_file = open('test.txt', 'w+')   # w+ : 읽기 또는 쓰기 모드, 파일이 없으면 새로 만든다
        except IOError:
            print('Unable to write to current directory. Please check permissions.')
            input('Press Enter to exit...')
            return False

        test_file.close()
        os.remove(test_file.name)

        result = True

        # Retrieve singleton reference to system object       (시스템 객체에 대한 싱글톤 참조) Retrieve : 회수하다, 검색하다
        system = PySpin.System.GetInstance()

        #싱글톤이란? -> 하나의 클래스에 대해 애플리케이션이 시작될 때 최초 한번만 메모리를 할당하고 그 메모리에 인스턴스를 생성
        # 즉, 인스턴스를 단 하나만 생성해 메모리 낭비를 방지하고, 다른 클래스의 인스턴스들이 데이터를 공유하고 변경할 수 있다.

        # Get current library version
        version = system.GetLibraryVersion()
        print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))

        # Retrieve list of cameras from the system
        cam_list = system.GetCameras()

        num_cameras = cam_list.GetSize()

        print('Number of cameras detected: %d' % num_cameras)

        # Finish if there are no cameras
        if num_cameras == 0:

            # Clear camera list before releasing system
            cam_list.Clear()

            # Release system instance
            system.ReleaseInstance()

            print('Not enough cameras!')
            input('Done! Press Enter to exit...')
            return False

        # Run example on each camera
        for i, cam in enumerate(cam_list):

            print('Running example for camera %d...' % i)

            result &= self.run_single_camera(cam, msg)
            print('Camera %d example complete... \n' % i)

        # Release reference to camera
        # NOTE: Unlike the C++ examples, we cannot rely on pointer objects being automatically
        # cleaned up when going out of scope.
        # The usage of del is preferred to assigning the variable to None.
        del cam

        # Clear camera list before releasing system
        cam_list.Clear()

        # Release system instance
        system.ReleaseInstance()

        input('Done! Press Enter to exit...')
        return result

class acqser:
    def __init__(self):
            # 소켓 레벨과 데이터 형태를 설정한다.
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def close(self):
        self.client_socket.close()

    def bind(self):
        self.server_socket.bind(('', 9999)) #port
        self.server_socket.listen()

    def thread(self):
        # 서버는 여러 클라이언트를 상대하기 때문에 무한 루프를 사용한다.
        try:
            while True:
            # client로 접속이 발생하면 accept가 발생한다.
            # 그럼 client 소켓과 addr(주소)를 튜플로 받는다.
                self.client_socket, addr = self.server_socket.accept()
                # 쓰레드를 이용해서 client 접속 대기를 만들고 다시 accept로 넘어가서 다른 client를 대기한다.
                th = threading.Thread(target=self.thread_body, args = (self.client_socket,addr));
                th.start();
        except:
            print("server")
        finally:
            self.server_socket.close()

    def thread_body(self,client_socket,addr):
        lock=threading.Lock()
        lock.acquire()
        print('Connected by', addr)
        try:
            while True:
                self.recv_loop(client_socket)
        except:
            print("except : " , addr)        
        finally:
            self.close()
        lock.release()

    def recv_loop(self,client_socket):
        # RX DATA
        self.data = client_socket.recv(4096)
        
        jsonStr=self.data.decode('UTF-8')

        jsonObject=json.loads(jsonStr)
        #loads : str -> dict   역직렬화
     
        #echo back
        self.client_socket.sendall(self.data) #main 들어가기전 send해줌으로서 client의 무한루프 해결


        if(jsonObject.get("command")=='save'):
            cq3.main(jsonObject.get("contents")) #acquisition3 객체 불르는 부분






if __name__ == '__main__':
    cq3=acquisition3()
    aq=acqser()
    aq.bind()
    aq.thread()
    print('server is ended')
    sys.exit(0)

    #if aq.main():
    #    aq.thread()
    #    sys.exit(0)  #성공 수행 -> process finished with exit code 0
    #else:
    #    sys.exit(1)
