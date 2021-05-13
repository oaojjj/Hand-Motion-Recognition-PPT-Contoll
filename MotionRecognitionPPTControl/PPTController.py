import win32com.client
import win32api
import win32con
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

VK_CODE = {
    'spacebar': 0x20,
    'down_arrow': 0x28,
}


class PPTController:  # PPT의 제어에 관한 기능을 지닌 클래스
    path = None

    # # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    currentVolumeDb = volume.GetMasterVolumeLevel()  # 현재볼륨

    def __init__(self):
        self.app = win32com.client.Dispatch("PowerPoint.Application")  # win32com의 Dispatch 메소드를 통해 파워포인트 객체를 생성

    def fullScreen(self):
        self.app.Presentations.Open(FileName=self.path, ReadOnly=1)  # 생성된 객체를 얻어서 파워포인트를 염
        if self.hasActivePresentation():
            self.app.ActivePresentation.SlideShowSettings.Run()
            return self.getActivePresentationSlideIndex()

    def click(self):
        win32api.keybd_event(VK_CODE['spacebar'], 0, 0, 0)
        win32api.keybd_event(VK_CODE['spacebar'], 0, win32con.KEYEVENTF_KEYUP, 0)
        return self.getActivePresentationSlideIndex()

    def gotoSlide(self, index):
        if self.hasActivePresentation():
            try:
                self.app.ActiveWindow.View.GotoSlide(index)
                return self.app.ActiveWindow.View.Slide.SlideIndex
            except:
                self.app.SlideShowWindows(1).View.GotoSlide(index)
                return self.app.SlideShowWindows(1).View.CurrentShowPosition

    def nextPage(self):
        if self.hasActivePresentation():
            count = self.getActivePresentationSlideCount()
            index = self.getActivePresentationSlideIndex()
            return index if index >= count else self.gotoSlide(index + 1)

    def prePage(self):
        if self.hasActivePresentation():
            index = self.getActivePresentationSlideIndex()
            return index if index <= 1 else self.gotoSlide(index - 1)

    def getActivePresentationSlideIndex(self):  # PPT의 현재 페이지 index 가져오기
        if self.hasActivePresentation():
            try:
                index = self.app.ActiveWindow.View.Slide.SlideIndex
            except:
                index = self.app.SlideShowWindows(1).View.CurrentShowPosition
        return index

    def getActivePresentationSlideCount(self):  # PPT의 총 페이지 수
        return self.app.ActivePresentation.Slides.Count

    def getPresentationCount(self):
        return self.app.Presentations.Count

    def hasActivePresentation(self):  # 프레젠테이션 기능이 활성화되었는지 확인하는 메소드
        return True if self.getPresentationCount() > 0 else False

    def getCursor(self):  # 마우스 현재 위치 파악
        return pyautogui.position()

    def mouseCursor(self):  # 마우스 클릭
        pos = self.getCursor()
        x, y = pos
        pyautogui.click(x, y)

    def goToNext(self):
        pyautogui.press("right")

    def goToBack(self):
        pyautogui.press("left")

    # 25%의 볼륨 업
    def volumeUp(self):
        currentVolumeDb = self.volume.GetMasterVolumeLevel()
        self.volume.GetVolumeRange()
        self.volume.SetMasterVolumeLevel(currentVolumeDb + 1.0, None)

    # 25%의 볼륨 다운
    def volumeDown(self):
        currentVolumeDb = self.volume.GetMasterVolumeLevel()
        self.volume.GetVolumeRange()
        self.volume.SetMasterVolumeLevel(currentVolumeDb - 1.0, None)
