import sys
import subprocess
import os

#give me the pillow
try:
    from PIL import Image, ImageTk
except ImportError:
    print("Pillow not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageTk
    
import tkinter as tk
import random

class Cat:
    def __init__(self):
        self.window = tk.Tk()
        self.walking = True
        self.floating = False
        self.look_left = False
        
        #setup
        self.window.config(highlightbackground="black")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        
        #delete that black
        self.window.wm_attributes("-transparentcolor", "black")
        
        #make cat big
        self.cat_size = 150 #cat size you understand it?
        
        #make canvas one
        self.canvas = tk.Canvas(self.window, width = self.cat_size, height = self.cat_size, bg = "black", bd = 0, highlightthickness = 0)
        self.canvas.pack()
        
        #adopt cat
        #Finding cat
        program_folder = os.path.dirname(os.path.abspath(__file__))
        
        self.load_animation("Hi.gif")
        self.pet = self.canvas.create_image(self.cat_size // 2,self.cat_size // 2,image=self.frames[0])

        self.animate()
        
        #positioning
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.x = 200
        self.y = self.screen_height - 200 #more number = higher lower = lower
        
        #walk
        self.speed_x = 1
        self.speed_y = 0
        
        #move
        self.update_movement()
        #gambling
        self.random_behavior()
        #don't place anything under ts
        self.window.mainloop()
        
    def animate(self):
        if not self.frames:
            return
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.canvas.itemconfig(self.pet,image=self.frames[self.current_frame])
        self.window.after(200, self.animate)
        
    def load_animation(self, filename):
        program_folder = os.path.dirname(os.path.abspath(__file__))
        cat_path = os.path.join(program_folder,"Cat_Gif",filename)
        if not os.path.exists(cat_path):
            print("Animation not found:", cat_path)
            return False
        try:
            gif = Image.open(cat_path)
            new_frames = []
            for frame_number in range(gif.n_frames):
                gif.seek(frame_number)
                frame = gif.convert("RGBA")
                frame = frame.resize((self.cat_size, self.cat_size),Image.Resampling.NEAREST)
                if self.look_left:
                    frame = frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                new_frames.append(ImageTk.PhotoImage(frame))
            self.frames = new_frames
            self.current_frame = 0
            
        except Exception as error:
            print(f"Could not load {filename}: {error}")
            return False
            
    def update_movement(self):
        if self.walking:
            self.x += self.speed_x
            self.y += self.speed_y
            #turn around
            if self.x <0 or self.x > self.screen_width - self.cat_size:
                self.speed_x = -self.speed_x
                self.look_left = self.speed_x < 0
                if abs(self.speed_x) > 4:
                    self.load_animation("Run.gif")
                else:
                    self.load_animation("Walk.gif")
            self.window.geometry(f"{self.cat_size}x"f"{self.cat_size}+"f"{int(self.x)}+"f"{int(self.y)}")
        self.window.after(20, self.update_movement)
        
    #Touching the sky
    def Jump(self):
        if self.floating:
            return
        self.floating = True
        self.walking = True
        self.load_animation("Jump.gif")
        float_time = len(self.frames) * 200
        self.window.after(float_time,self.noJump)
        
    #Touching the ground
    def noJump(self):
        self.floating = False
        self.walking = True
        if abs(self.speed_x) > 4:
            self.load_animation("Run.gif")
        else:
            self.load_animation("Walk.gif")
            
    #what behind gambling
    def random_behavior(self):
        if self.walking:
            #start lazy
            self.speed_x = 0
            self.walking = False
            if random.random() < 0.25:
                self.walking = True
            
            #lazy
            rest_time = random.randint(2000, 10000)
            if rest_time < 4000:
                rest_time = rest_time * 7
                self.load_animation("ZZZ.gif")
            else:
                x = random.choice([1,2,3,4,5])
                if x == 1:
                    self.load_animation("Sit.gif")
                elif x == 2:
                    self.load_animation("Hi.gif")
                elif x == 3:
                    self.load_animation("SitUp.gif")
                elif x == 4:
                    self.load_animation("SitMed.gif")
                else:
                    self.load_animation("Clean.gif")
            
            self.window.after(rest_time, self.random_behavior)
            
        else:
            #walk :3
            self.walking = True
            
            self.speed_x = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            self.look_left = self.speed_x < 0
            if random.random() < 0.2:
                self.Jump()
                if abs(self.speed_x) < 4:
                    if self.speed_x < 0:
                        self.speed_x = random.choice([-5, -4])
                    else:
                        self.speed_x = random.choice([4, 5])
            else:
                if abs(self.speed_x) > 4:
                    self.load_animation("Run.gif")
                else:
                    self.load_animation("Walk.gif")
            #stop lazy
            walk_time = random.randint(1000, 20000)
            self.window.after(walk_time, self.random_behavior)
        
if __name__ == "__main__":
    Cat()