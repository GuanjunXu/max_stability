#coding=utf-8
#from uiautomator import device as d
from uiautomator import Device
import unittest
import os
import time
import commands
import random

deviceId = '5bda3b07'
d = Device(deviceId)

screen_x = 2560
screen_y = 1440

TEST_CYCLE = 500

launcher_p     = 'com.lvr.launcher'
local_video_p  = 'com.lvr.player'
game_center_p  = 'com.lvr.gamecenter'
gallery_p      = 'com.lvr.gallery'
settings_p     = 'com.lvr.settings'
super_lvr_p    = 'com.lvr.superlvrpro'
# pass_through_p = 'com.lvr.passthrough'

launcher_a     = launcher_p     + '/com.lvr.launcher.VRLauncherActivity --es pkgName com.lvr.wizzard'
local_video_a  = local_video_p  + '/com.lvr.player.activity.LocalVideoLoadActivity'
game_center_a  = game_center_p  + '/com.lvr.gamecenter.activity.GameCenterMainActivity'
gallery_a      = gallery_p      + '/com.lvr.gallery.LvrGalleryActivity'
settings_a     = settings_p     + '/com.lvr.settings.SettingsActivity --es pkgName com.lvr.wizzard'
super_lvr_a    = super_lvr_p    + '/com.lvr.superlvrpro.vr.VRChannelActivity'
# pass_through_a = pass_through_p + '/com.lvr.passthrough.Camera2RenderscriptActivity'

apps           = {
                    'launcher'    :[launcher_p, launcher_a],
                    'local_video' :[local_video_p, local_video_a],
                    'game_center' :[game_center_p, game_center_a],
                    'gallery'     :[gallery_p, gallery_a],
                    'settings'    :[settings_p, settings_a],
                    'super_lvr'   :[super_lvr_p, super_lvr_a]                    
                } # 'pass_through':[pass_through_p, pass_through_a]

class UnityTest(unittest.TestCase):
    CYCLE_NOW = 0
    start_time = 0
    CASE_NOW = ''

    def setUp(self):
        super(UnityTest, self).setUp()
        # commands.getoutput('adb -s 5bda3b07shell ls /data/local/tmp')
        commands.getoutput('adb -s 5bda3b07 shell touch /data/local/tmp/LVR_MONKEY_TEST')
        commands.getoutput('adb -s 5bda3b07 shell touch /sdcard/LVR_MONKEY_TEST')
        self.start_time = int(time.time())
        print 'start: \t%s'%(time.strftime('%Y%m%d_%H%M%S',time.localtime(self.start_time)))

    def tearDown(self):
        super(UnityTest, self).tearDown()
        end_time = int(time.time())
        commands.getoutput('adb -s 5bda3b07 shell /system/bin/screencap -p /sdcard/%s.png'%(end_time))
        duration = end_time - self.start_time
        print 'End at %s'%end_time
        print 'Duration %ss'%(duration)
        print '\t ... end at %s time(s)'%(self.CYCLE_NOW)
        str_path = 'max_eui_st_test_from_%s_to_%s'%(self.start_time,end_time)
        try:
            os.makedirs(str_path)
        except:
            pass
        commands.getoutput('adb -s 5bda3b07 shell logcat -v time -d > %s/0_logcat_%s.txt'%(str_path,str(int(end_time))))
        commands.getoutput('adb -s 5bda3b07 bugreport > %s/0_bugreport.log'%str_path)
        commands.getoutput('adb -s 5bda3b07 pull /sdcard/%s.png %s/%s'%(end_time,os.getcwd(),str_path))

    # def goVRLauncher(self):
    #     commands.getoutput('adb -s 5bda3b07 shell am start -n com.lvr.launcher/.VRLauncherActivity --es pkgName com.lvr.wizzard')
    #     time.sleep(5)
    #     assert d(packageName = 'com.lvr.launcher').wait.exists(timeout = 3000)

    def exitRecent(self):
        d.press('recent')
        info_th = d(resourceId = 'com.android.systemui:id/leui_recent_thumbnail', instance = 1).info
        boun_th = info_th['bounds']
        cent_th_y = (boun_th['bottom'] + boun_th['top'])/2
        cent_th_x = (boun_th['right'] + boun_th['left'])/2
        d.swipe(cent_th_x, cent_th_y, cent_th_x, boun_th['top']/2, 5) # Slide up to remove recent task
        d.press('back')

    def exitToDesktop(self):
        d.press('recent')
        info_th = d(resourceId = 'com.android.systemui:id/leui_recent_thumbnail', instance = 1).info
        boun_th = info_th['bounds']
        cent_th_y = (boun_th['bottom'] + boun_th['top'])/2
        cent_th_x = (boun_th['right'] + boun_th['left'])/2
        while d(resourceId = 'com.android.systemui:id/leui_recent_thumbnail').count > 1:
            d.swipe(cent_th_x, cent_th_y, cent_th_x, boun_th['top']/2, 5)
            time.sleep(1)
        d.press('back')

    def goVRApp(self, app):
        self.CASE_NOW = app
        print "Testing app: %s"%self.CASE_NOW,
        commands.getoutput('adb -s 5bda3b07 shell am start -n %s'%apps[app][1])
        time.sleep(10)
        assert d(packageName = apps[app][0]).wait.exists()

    def exitVRApp(self, app):
        assert d(packageName = apps[app][0]).wait.exists()
        i = 0
        print "\t ... exit %s ... "%app,
        while d(packageName = apps[app][0]).wait.exists():
            d.press('back')
            i = i + 1
            if i > 10:
                break
        print "done."

    def installGame(self,num = 1):
        self.goVRApp('game_center')
        app_list_x = [450,680,920]
        app_list_y = [590,700,840]
        loc_list = []
        for i in range(num):
            x = random.choice(app_list_x)
            y = random.choice(app_list_y)
            while (x,y) in loc_list:
                x = random.choice(app_list_x)
                y = random.choice(app_list_y)
            loc_list.append((x,y))
            d.click(x,y)
            time.sleep(3)
            d.click(760,660) # 安装按钮
            print 'Waiting for installing'
            time.sleep(300)
            if num > 1:
                d.press('back')

    def testPlayingVideo(self, cycle=1):
        '''
            Playing video
        '''
        y = 660
        x = [370,710] #[370,540,710,880]
        for i in range(cycle):
            self.goVRApp('local_video')
            self.CYCLE_NOW = i + 1
            x_c = random.choice(x)
            time.sleep(3)
            d.click(x_c,y)
            assert d(packageName = apps['local_video'][0]).wait.exists()
            time.sleep(3)
            d.click(600,600)
            assert d(packageName = apps['local_video'][0]).wait.exists()
            time.sleep(60)
            for j in range(6):
                d.press('back')

    def installAndPlayGame(self,num = 1):
        for i in range(num):
            self.installGame()
            d.click(760,660) # 打开按钮
            time.sleep(10)
            for j in range(500): # 游戏内随机点击
                x = random.choice(range(screen_x))
                y = random.choice(range(screen_y))
                d.click(x,y)
                time.sleep(1)
            # if num > 1:
            #     d.press('back')

    def testStability(self):
        '''
            Stability
        '''
        for i in range(TEST_CYCLE):
            self.CYCLE_NOW = i + 1
            print "\nCycle now is %s\n=-*-=-*=-*-=-*=-*-=-*=-*-=-*=-*-=-*"%self.CYCLE_NOW
            # To VR Launcher
            self.goVRApp('launcher')
            print ""
            # 进入设置
            self.goVRApp('settings')
            time.sleep(5)
            self.exitVRApp('settings')
            # 看2D视频
            self.goVRApp('local_video')
            d.click(580,730)
            time.sleep(30)
            d.click(640,570)
            d.press('back')
            # 看全景视频
            d.click(730,730)
            time.sleep(30)
            d.click(640,570)
            self.exitVRApp('local_video')
            # 安装游戏
            # 进入游戏
            self.goVRApp('game_center')
            d.click(640,840) # Only this one could exit by double click on back key
            time.sleep(5)
            d.click(750,660)
            if i == 0:
                time.sleep(300)
                print "\t ... Installing game ..."
                d.click(750,660)
                time.sleep(30)
                for i in range(10):
                    d.press('back')
            self.exitVRApp('game_center')
            # 乐视界看全景视频
            self.goVRApp('super_lvr')
            d.click(640,640)
            time.sleep(30)
            d.click(640,640) # Fullscreen
            time.sleep(30)
            d.press('back') # Exit fullscreen
            d.press('back') # Exit to home in super pro
            # 乐视界看3D视频
            time.sleep(5)
            d.swipe(640,640,1940,640)
            time.sleep(5)
            d.click(640,640) # Enter player
            time.sleep(30)
            d.click(640,640) # Fullscreen
            time.sleep(30)
            self.exitVRApp('super_lvr')
            # 看外面
            # self.goVRApp('pass_through')
            # time.sleep(60)
            # self.exitVRApp('pass_through')
            # 校准
            # d.click(580,550) # Calibration option
            # self.exitVRApp('settings')