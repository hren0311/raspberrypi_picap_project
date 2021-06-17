from button import *
import json 

class Key:
    def __init__(self) -> None:
        self.step = 1
        self.button = [False]*8
        self.code = ""
        
        try :
            json_open = open('keymap.json', 'r')
            self.key_map = json.load(json_open)
        except Exception as e:
            print(e)
        

    def keyInput(self,touch_l,release_l):
        #変化がなければ処理しない
        if(len(touch_l)==0 and len(release_l)==0):
            return

        #ボタンが押された場合とリリースされた場合の処理
        if( self.step == 1 ):
            self.consonantTouch(touch_l)
        elif( self.step == 2 ):
            self.consonantFlick(release_l)

        #ボタンの状況
        for i in touch_l:
            self.button[i] = True
        for i in release_l:
            self.button[i] = False

        #触れられて無ければコードを保存する
        if(sum(self.button)==0):
            self.save()
            self.step = 1
            self.code = ""
            return


    def consonantTouch(self,touch_l,release_l):
        a_cnt,b_cnt,c_cnt = touch_l.count(A),touch_l.count(B),touch_l.count(C)
        if((a_cnt + b_cnt + c_cnt ) != 1):
            self.step = 1
            return

        if(a_cnt == 1):
            self.code = "11"
        elif(b_cnt == 1):
            self.code = "22"
        elif(c_cnt == 1):
            self.code = "33"

        self.step = 2

    def consonantFlick(self,release_l):
        
        #Button A (←D↑E→C↓B)
        if(self.code[0]=="1"):
            button_l,code_l = [A,D,E,C,B],["1","4","5","6","7"]
            
        #Button B (←D↑A→C↓G)
        if(self.code[0]=="2"):
            button_l,code_l = [B,D,A,C,G],["2","4","5","6","7"]
            
        #Button C (←AB↑E→F↓G)
        if(self.code[0]=="3"):
            button_l,code_l = [C,A,B,E,F,G],["3","4","4","5","6","7"]

        self.changeCode(release_l,button_l,code_l)


    def changeCode(self,release_l,button_l,code_l):

        for num,c in zip(button_l,code_l):
            if(num in release_l):
                self.code[1] = c

    def save(self):
        print('keycode:',self.code,"word:",self.key_map[self.code])
