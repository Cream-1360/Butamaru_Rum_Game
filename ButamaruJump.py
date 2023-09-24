import pyxel
import copy
import numpy as np
import random
import json

area_list = ["Grassland","StoneBlocks","Desert","IceField"]

tile_dic = {"All":[0,0,2048,128],
            "Grassland": [0, 0, 512, 128],
            "StoneBlocks": [0, 128, 512, 128],
            "Desert": [0, 256, 512, 128],
            "IceField": [0, 384, 512, 128],
            "Title":[0,128,192,256]
            }

item_dic = {"Butamal_Mask_Walk1" :[0,0,16,16,1,0,14,16],
            "Butamal_Mask_Walk2" :[16,0,16,16,1,0,14,16],
            "Butamal_Mask_Walk3" :[32,0,16,16,1,0,14,16],
            "Butamal_Mask_Walk4" :[48,0,16,16,1,0,14,16],
            "Butamal_Mask_Jump"  :[64,0,16,16,1,0,14,16],
            "Butamal_Mask_Squat" :[80,0,16,16,1,8,14,8],
            "Butamal_Mask_Damage":[96,0,16,16,0,0,16,16],
            "Butamal_Hair_Walk1" :[0,16,16,16,1,0,14,16],
            "Butamal_Hair_Walk2" :[16,16,16,16,1,0,14,16],
            "Butamal_Hair_Walk3" :[32,16,16,16,1,0,14,16],
            "Butamal_Hair_Walk4" :[48,16,16,16,1,0,14,16],
            "Butamal_Hair_Jump"  :[64,16,16,16,1,0,14,16],
            "Butamal_Hair_Squat" :[80,16,16,16,1,8,14,8],
            "Butamal_Hair_Damage":[96,16,16,16,0,0,16,16],
            "Butamal_Lion_Walk1" :[0,32,16,16,1,0,14,16],
            "Butamal_Lion_Walk2" :[16,32,16,16,1,0,14,16],
            "Butamal_Lion_Walk3" :[32,32,16,16,1,0,14,16],
            "Butamal_Lion_Walk4" :[48,32,16,16,1,0,14,16],
            "Butamal_Lion_Jump"  :[64,32,16,16,1,0,14,16],
            "Butamal_Lion_Squat" :[80,32,16,16,1,8,14,8],
            "Butamal_Lion_Damage":[96,32,16,16,0,0,16,16],
            "Kangaroo1":[0,48,16,16,5,0,10,16],
            "Kangaroo2":[16,48,16,16,5,0,10,16],
            "Kangaroo3":[32,48,16,16,5,0,10,16],
            "Kangaroo4":[48,48,16,16,1,0,14,16],
            "SeaLion1":[0,64,16,16,0,0,11,16],
            "SeaLion2":[16,64,16,16,0,0,11,16],
            "SeaLion3":[32,64,16,16,0,0,11,16],
            "SeaLion4":[48,64,16,16,0,0,11,16],
            "Ostrich1":[0,80,16,16,3,0,11,16],
            "Ostrich2":[16,80,16,16,3,0,11,16],
            "Ostrich3":[32,80,16,16,3,0,11,16],
            "Ostrich4":[48,80,16,16,3,0,11,16],
            "Eagle1":[0,96,16,16,0,0,16,16],
            "Eagle2":[16,96,16,16,0,0,16,16],
            "Eagle3":[32,96,16,16,0,0,16,16],
            "Eagle4":[48,96,16,16,0,0,16,16],
            "WaterMelon":[0,112,16,16,0,0,12,12],
            "GoldWaterMelon":[16,112,16,16,0,0,12,12],
            "Mushroom":[32,112,16,16,0,1,16,12],
            "Ribbon":[48,112,16,16,0,0,16,16],
            "Sky":[64,112,8,8],
            "SmallCloud":[40,128,8,8],
            "MiddleCloud":[32,136,16,8],
            "LargeCloud":[0,128,32,16],
            "RightLeftAllow":[16,160,16,16],
            "DownAllow":[32,160,16,16],
            
             }

sound_dic ={"Jump":0,
            "GetWaterMerlon":2,
            "GetMushroom":3,
            "GameOver":4,
            "Damage":5,
            "GetRibbon":6,
            "NoDamage":7
            }

def getDirectedItem(key,dx,dy=1):
    v = copy.copy(item_dic[key])
    if dx<0:
        v[2]*=-1
    if dy<0:
        v[3]*=-1
    return v[:4]
    

score = 0

def getScore():
    return score

def resetScore():
    global score
    score = 0
    
def addScore(val):
    global score
    score += val
        

WIDTH  = 192
HEIGHT = 128

G_WITDH = 2048
G_HEIGHT = HEIGHT-40

ONE_AREA_WIDTH = 512


TRANS_COLOR = 6

player = None

enemy_list = []
item_list = []

areaFrameInit = 0

SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面

game_scene = SCENE_TITLE

def setGameScene(val):
    global game_scene
    game_scene = val
    

def getArea(x):
    return area_list[(int(x)%G_WITDH)//ONE_AREA_WIDTH]

def getStageFrameCount():
    return pyxel.frame_count - areaFrameInit

def setStageFrameCountInit():
    global areaFrameInit
    areaFrameInit =  pyxel.frame_count
    

def getGlobalToLocalX(x):
    return (x-getStageFrameCount())

def getLocalToGlobalX(x):
    return getStageFrameCount()+x


def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if elem.is_alive:
            i += 1
        else:
            list.pop(i)

def updateField(start,end,enemy_num_in_range,item_num_in_range):
    global enemy_list
    global item_list
    
    cleanup_list(enemy_list)
    cleanup_list(item_list)
    
    interval = (end-start)//enemy_num_in_range
    eagle_list = []
    for n in range(enemy_num_in_range):
        val = start+interval*n+random.randint(32, interval)
        etype = random.randint(1, 1000)
        if etype < 300:
            enemy_list.append(SeaLion(val,G_HEIGHT))
        elif etype < 600:
            enemy_list.append(Kangaroo(val,G_HEIGHT))
        elif etype < 800:
            enemy_list.append(Ostrich(val,G_HEIGHT))
        else:
            enemy_list.append(Eagle(val,G_HEIGHT-25))
            eagle_list.append(val)
        
    interval = (end-start)//item_num_in_range
    for n in range(item_num_in_range):
        val = start+interval*n+random.randint(32, interval)
        flag=False
        for eval in eagle_list:
            if abs(eval-val)<16:
                flag=True
                continue
        if flag:
            continue
        itype = random.randint(1,1000)
        if itype < 400:
            item_list.append(WaterMelon(val,G_HEIGHT-24))
        elif itype < 700:
            item_list.append(GoldWaterMelon(val,G_HEIGHT-24))
        elif itype <900:
            item_list.append(Mushroom(val,G_HEIGHT-24))
        else:
            item_list.append(Ribbon(val,G_HEIGHT-24))
        
    
    
class ObjectBase:
    def __init__(self,key,gx,y):
        self.object_gx = gx
        self.object_y = y
        self.object_dx = 0
        self.object_dy = 0
        self.direction=1
        self.hasCollison=True
        self.is_enable=False
        self.is_alive=True
        self.key = key
        
    def checkEnable(self):
        curPos = (getStageFrameCount())
        if curPos-WIDTH-16>self.object_gx or curPos+WIDTH+16<self.object_gx:
            self.is_enable = False
            if curPos-WIDTH-16>self.object_gx:
                self.is_alive=False   
            return False
        self.is_enable = True
        return True    
    
    def update(self):
        if not self.checkEnable():
            return     
           
    def chechColison(self,px,py,prect,rect):
        sx0 = px+prect[0]
        sy0 = py+prect[1]
        ex0 = sx0+prect[2]
        ey0 = sy0+prect[3]
        
        sx1 = self.object_gx+rect[0]
        sy1 = self.object_y+rect[1]
        ex1 = sx1+rect[2]
        ey1 = sy1+rect[3]
        
        
        minx = np.min(np.array([sx0,ex0,sx1,ex1]))
        maxx = np.max(np.array([sx0,ex0,sx1,ex1]))
        
        miny = np.min(np.array([sy0,ey0,sy1,ey1]))
        maxy = np.max(np.array([sy0,ey0,sy1,ey1]))
        
        if maxx-minx <=abs(sx0-ex0)+abs(sx1-ex1) and maxy-miny <=abs(sy0-ey0)+abs(sy1-ey1):
            return True
        return False


class ItemBase(ObjectBase):
    def __init__(self,key,gx,y):
        super().__init__(key,gx,y)
    
    def draw(self):
        if not self.is_alive:
            return
        x = getGlobalToLocalX(self.object_gx)
        if  (pyxel.frame_count//12)%2==0:
            pyxel.blt(x, self.object_y, 0, *getDirectedItem(f"{self.key}",1,1) , TRANS_COLOR)
        elif (pyxel.frame_count//12)%2==1:
            pyxel.blt(x, self.object_y, 0, *getDirectedItem(f"{self.key}",-1,1) , TRANS_COLOR)
        
    def detectColison(self,px,py,prect):
        if not self.is_alive:
            return
        
        rect =  item_dic[f"{self.key}"][4:]
        if not self.chechColison(px,py,prect,rect):
            return False
    
        self.hasCollison=False
        self.is_alive = False
        return True
    
    
    
class EnemyBase(ObjectBase):
    def __init__(self,key,gx,y):
        super().__init__(key,gx,y)
        
    def draw(self):
        if not self.is_enable:
            return
        x = getGlobalToLocalX(self.object_gx)
        if  (pyxel.frame_count//6)%4==0:
            pyxel.blt(x, self.object_y, 0, *getDirectedItem(f"{self.key}1",self.direction) , TRANS_COLOR)
        elif (pyxel.frame_count//6)%4==1:
            pyxel.blt(x, self.object_y, 0, *getDirectedItem(f"{self.key}2",self.direction) , TRANS_COLOR)
        elif (pyxel.frame_count//6)%4==2:
            pyxel.blt(x, self.object_y, 0, *getDirectedItem(f"{self.key}3",self.direction) , TRANS_COLOR)
        elif (pyxel.frame_count//6)%4==3:
            pyxel.blt(x, self.object_y, 0, *getDirectedItem(f"{self.key}4",self.direction) , TRANS_COLOR)
    
    def detectColison(self,px,py,prect):
        
        if not self.is_enable:
            return
        if not self.hasCollison:
            return
        
        if  (pyxel.frame_count//6)%4==0:
           rect =  item_dic[f"{self.key}1"][4:]
        elif (pyxel.frame_count//6)%4==1:
           rect =  item_dic[f"{self.key}2"][4:]
        elif (pyxel.frame_count//6)%4==2:
           rect =  item_dic[f"{self.key}3"][4:]
        elif (pyxel.frame_count//6)%4==3:
           rect =  item_dic[f"{self.key}4"][4:]
           
        if self.chechColison(px,py,prect,rect):
            self.hasCollison=False
            return True
        
        return False
    
        
class WaterMelon(ItemBase):
    def __init__(self,gx,y):
        super().__init__("WaterMelon",gx,y)
        
class GoldWaterMelon(ItemBase):
    def __init__(self,gx,y):
        super().__init__("GoldWaterMelon",gx,y)

class Mushroom(ItemBase):
    def __init__(self,gx,y):
        super().__init__("Mushroom",gx,y)
        

class Ribbon(ItemBase):
    def __init__(self,gx,y):
        super().__init__("Ribbon",gx,y)              
    


class Kangaroo(EnemyBase):
    def __init__(self,gx,y):
        super().__init__("Kangaroo",gx,y)
        self.object_dx = -0.5
        self.counter=0
        
    def update(self):
        
        if not self.checkEnable():
            return

        self.object_gx += self.object_dx
        self.counter+=1
            
        if self.counter==32:
            self.object_dx *=-1
            self.counter=0

class SeaLion(EnemyBase):
    def __init__(self,gx,y):
        super().__init__("SeaLion",gx,y)
        



class Ostrich(EnemyBase):
    def __init__(self,gx,y):
        super().__init__("Ostrich",gx,y)
        self.object_dx = -0.5
        
    def update(self):
        
        if not self.checkEnable():
            return
        self.object_gx += self.object_dx
       
            
class Eagle(EnemyBase):
    def __init__(self,gx,y):
        super().__init__("Eagle",gx,y)
        self.object_dy=0.5
        
    def update(self):
        
        if not self.checkEnable():
            return
        #y位置計算
        if self.object_dy<0:
            self.object_y = max(self.object_y + self.object_dy, 40)
        else:
            self.object_y = min(self.object_y + self.object_dy, G_HEIGHT-9)

        if self.object_y==40 or self.object_y==G_HEIGHT-9:
            self.object_dy*=-1

        
        
class Player:
    def __init__(self,x,y):
        
        self.player_x = x
        self.player_y = y
        self.player_dx = 0
        self.player_dy = 0

        self.direction=1
        self.life = 2
        self.Gravity = -3.5
        self.Power = -0.25
        self.isJump=False
        self.isSquat=False
        self.hasCollison=True
        self.damageTimer=0
        self.recoveryTimer=0
        self.invincibleTimer=0
    
    
    def invincible(self):
        self.invincibleTimer=180
        self.hasCollison=False
        
    
    def damage(self):
        
        if self.hasCollison==False:
            return
        if self.life<=0:
            return
        
        self.life -=1
        
        if self.life==0:
            pyxel.play(3,sound_dic["GameOver"])
            setGameScene(SCENE_GAMEOVER)
            
        
        self.hasCollison=False
        self.damageTimer=60
        
    def recovery(self):
        if self.life>=2:
            return
        self.life +=1    
        self.damageTimer=0
        self.hasCollison=False
        self.recoveryTimer=15
    
    
    def detectColison(self):

        gx = getLocalToGlobalX(self.player_x)
        gy = self.player_y
        if self.isSquat:
            rect = item_dic["Butamal_Mask_Squat"][4:]
        else:
            rect = item_dic["Butamal_Mask_Walk1"][4:]
        global item_list
        for item in item_list:
            if item.detectColison(gx,gy,rect):
                if item.key=="WaterMelon":
                    pyxel.play(3,sound_dic["GetWaterMerlon"])
                    addScore(100)
                elif item.key=="GoldWaterMelon":
                    pyxel.play(3,sound_dic["GetWaterMerlon"])
                    addScore(500)
                elif item.key=="Mushroom":
                    pyxel.play(3,sound_dic["GetMushroom"])
                    addScore(100)
                    self.recovery()
                elif item.key=="Ribbon":
                    pyxel.play(3,sound_dic["GetRibbon"])
                    addScore(100)
                    self.invincible()
                    
       
        for enemy in enemy_list:
            if enemy.detectColison(gx,gy,rect):
                if self.hasCollison:
                    pyxel.play(3,sound_dic["Damage"])
                else:
                    pyxel.play(3,sound_dic["NoDamage"])
                    
                self.damage()    
            
    def update(self):
        
        area = getArea(getStageFrameCount()+self.player_x)

        #X方向加速度 雪上では滑り続ける　砂漠では遅い        
        dx = 1.5 if area != area_list[2] else 0.8
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            # self.direction =-1
            self.player_dx = -dx-1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            # self.direction =1
            self.player_dx = dx
            
        #下ボタンでしゃがむ
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.isSquat = True
        else:
            self.isSquat = False
            
        #x位置計算
        if self.player_dx<0:
            self.player_x = max(self.player_x+self.player_dx, 0)
        else:
            self.player_x = min(self.player_x + self.player_dx, WIDTH - 16)

        #x方向加速度減衰（氷以外のときは0）
        if area == area_list[3]:
            self.player_dx *= 0.95
            if abs(self.player_dx)<0.1:
                self.player_dx =0
        else:
            self.player_dx =0                  

        
        #ジャンプ発生時
        if not self.isSquat and not self.isJump and (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)):
            self.player_dy = self.Gravity if area!= area_list[1] else self.Gravity*1.3
            self.isJump = True
            pyxel.play(3, 0)
            
            # self.start = getStageFrameCount()
        
        #ジャンプ中にy位置計算と加速度減衰
        if self.isJump:
            self.player_y = self.player_y + self.player_dy
            self.player_dy -= self.Power
            # print("Jump is ",getStageFrameCount()-self.start, self.player_y,self.player_dy)
            

        #着地判定
        if self.isJump and self.player_y >= G_HEIGHT:
            self.isJump=False
            self.player_dy=0
            self.player_y = G_HEIGHT
            
            
        #ダメージリアクション用タイマー減衰
        if self.damageTimer>0:
           self.damageTimer-=1
           if self.damageTimer==0:
               self.hasCollison=True
               
        #回復用タイマー減衰
        if self.recoveryTimer>0:
           self.recoveryTimer-=1
           if self.recoveryTimer==0:
               self.hasCollison=True
        
        #無敵用タイマー減衰
        if self.invincibleTimer>0:
           self.invincibleTimer-=1
           if self.invincibleTimer==0:
                self.hasCollison=True
               
           
        self.detectColison()
        
            

        
    def draw(self):
        
        
        frame_count = getStageFrameCount()
        
        #Butamaru Status
        if self.damageTimer>45 and self.life==1:
            state ="Mask"
        elif self.damageTimer>45:
            state ="Hair"
        elif self.invincibleTimer>90 or (self.invincibleTimer>0 and (self.invincibleTimer//3)%2==0):
            state = "Lion"
        elif (self.recoveryTimer>0 and (self.recoveryTimer//3)%2==1):
            state = "Mask"
        elif (self.recoveryTimer>0 and (self.recoveryTimer//3)%2==0):
            state = "Hair"
        elif self.life==2:
            state = "Mask"
        elif self.life==1:
            state = "Hair"
        else:
            return
        
        #Actions
        if self.damageTimer>45:       
            action = "Damage"
        elif self.damageTimer>0 and frame_count%4<1:
            return
        elif self.isSquat:
            action = "Squat"
        elif self.isJump:
            action = "Jump"
        else:
            action = f"Walk{(frame_count//4)%4+1}"
            
        pyxel.blt(self.player_x, self.player_y, 0, *getDirectedItem(f"Butamal_{state}_{action}",self.direction) , TRANS_COLOR)
                                  
      


class App:
    def __init__(self):
        
        
        #遠い雲
        self.far_cloud = [(10, 25), (40, 35),(74, 15), (100, 45), (150, 24)]
        #近い雲
        self.near_cloud = [(23, 15), (75, 65), (134, 35), (170, 48)] 
            
        pyxel.init(WIDTH, HEIGHT, title="Butamaru Jump")
        pyxel.load("./assets/myapp.pyxres")
        pyxel.run(self.update, self.draw)


    def initPlay(self):
        global player
        player = Player(WIDTH//3, G_HEIGHT)
        global enemy_list,item_list
        enemy_list =[]
        item_list =[]
        updateField(128,1280,10,16)
        
    
    def upadate_title(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            resetScore()
            setStageFrameCountInit()
            self.initPlay()
            setGameScene(SCENE_PLAY)

            
    def update_play(self):
        
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        if pyxel.btn(pyxel.KEY_0):
            player.damage()
        elif pyxel.btn(pyxel.KEY_1):
            player.recovery()
        elif pyxel.btn(pyxel.KEY_2):
            player.becomeInvincible()
        
        
        
        for item in item_list:
            item.update()
        for enemy in enemy_list:
            enemy.update()
        player.update()
        
        curPos = getStageFrameCount()
        if curPos%512==256:
            updateField(curPos+ONE_AREA_WIDTH*2,curPos+ONE_AREA_WIDTH*3,8,10)

   
    def update_gameover(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            resetScore()
            setGameScene(SCENE_TITLE)

    def update(self):
        
        if pyxel.btnp(pyxel.KEY_Q):
            exit()
        
        if game_scene == SCENE_TITLE:
            self.upadate_title()
        elif game_scene == SCENE_PLAY:
            self.update_play()
        elif game_scene == SCENE_GAMEOVER:
            self.update_gameover()
            
        
        
    def draw_title(self):
        pyxel.cls(12)
        
        # pyxel.bltm(i * G_WITDH - offset, 0,0, *tile_dic["All"],TRANS_COLOR)
        
        pyxel.blt(120, 60, 0, *getDirectedItem(f"WaterMelon",1,1) , TRANS_COLOR)
        pyxel.blt(120, 76, 0, *getDirectedItem(f"GoldWaterMelon",1,1) , TRANS_COLOR)
        pyxel.blt(120, 92, 0, *getDirectedItem(f"Mushroom",1,1) , TRANS_COLOR)
        pyxel.blt(120, 108, 0, *getDirectedItem(f"Ribbon",1,1) , TRANS_COLOR)
        
        pyxel.text(140, 60+5, "SCORE +100", 1)
        pyxel.text(139, 60+5, "SCORE +100", 7)
        pyxel.text(140, 76+5, "SCORE +500", 1)
        pyxel.text(139, 76+5, "SCORE +500", 7)
        pyxel.text(140, 92+5, "LIFE UP", 1)
        pyxel.text(139, 92+5, "LIFE UP", 7)
        pyxel.text(140, 108+5, "SUPER MODE", 1)
        pyxel.text(139, 108+5, "SUPER MODE", 7)
        
        
        
        pyxel.blt(10, 60, 0, *getDirectedItem(f"RightLeftAllow",1,1) , TRANS_COLOR)
        pyxel.blt(10, 76, 0, *getDirectedItem(f"DownAllow",1,1) , TRANS_COLOR)
        pyxel.text(8, 97, "SPACE", 7)
        
        
        pyxel.text(30, 60+5, "MOVE", 1)
        pyxel.text(29, 60+5, "MOVE", 7)
        pyxel.text(30, 76+5, "SQUAT", 1)
        pyxel.text(29, 76+5, "SQUAT", 7)
        pyxel.text(30, 92+5, "JUMP", 1)
        pyxel.text(29, 92+5, "JUMP", 7)
        
        
        pyxel.blt(50, 15, 0, *getDirectedItem(f"Butamal_Mask_Walk1",1,1) , TRANS_COLOR)
        pyxel.blt(125, 15, 0, *getDirectedItem(f"Butamal_Mask_Walk2",1,1) , TRANS_COLOR)
        pyxel.text(70, 20, "BUTAMARU JUMP", 1)
        pyxel.text(69, 20, "BUTAMARU JUMP", 7)
        pyxel.text(65, 40, "- PRESS ENTER -", 1)
        pyxel.text(64, 40, "- PRESS ENTER -", 7)
        
    def draw_play(self):
        pyxel.cls(12)

        CurrPos = getStageFrameCount()


        offset = CurrPos % G_WITDH
        for i in range(2):
            pyxel.bltm(i * G_WITDH - offset, 0,0, *tile_dic["All"],TRANS_COLOR)
            
            
    #Draw Near Cloud
        offset = (CurrPos // 8) % WIDTH
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * WIDTH - offset, y, 0, *item_dic["MiddleCloud"],TRANS_COLOR)
    #Draw Far Cloud
        offset = (CurrPos // 4) % WIDTH
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * WIDTH - offset, y, 0, *item_dic["LargeCloud"],TRANS_COLOR)
        
        for item in item_list:
            item.draw()
        
        for enemy in enemy_list:
            enemy.draw()
            
        player.draw()
        
        if CurrPos%64==63:
            addScore(10)
        s = f"SCORE {getScore():>4}"
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)
        
    def draw_gameover(self):
        pyxel.cls(12)
        pyxel.text(75, 40, "GAME OVER", 1)
        pyxel.text(74, 40, "GAME OVER", 8)
          
        s = f"SCORE {getScore():>4}"
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)
        
        pyxel.text(65, 90, "- PRESS ENTER -", 1)
        pyxel.text(64, 90, "- PRESS ENTER -", 7)
        
    def draw(self):
        if game_scene == SCENE_TITLE:
            self.draw_title()
        elif game_scene == SCENE_PLAY:
            self.draw_play()
        elif game_scene == SCENE_GAMEOVER:
            self.draw_gameover()
App()
