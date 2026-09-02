import os
from PIL import Image, ImageTk
import tkinter as tk
import random
#what this?
#this file for modifying so you can feel free to modify
class Cat:
    def __init__(self):
        #setup
        self.window = tk.Tk()
        self.walking = True
        self.floating = False
        self.look_left = False
        
        #add color so more cat color (rgb color) min 0 max 255
        self.cat_color = random.choice([(65, 56, 57),(211, 145, 101),(196, 142, 54),(202, 206, 200),(78,60,46),(96, 97, 103),(239, 225, 213),(35, 22, 43),(255, 122, 0)])
        
        #more setup not reccommend fixing these
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.config(highlightbackground="black")
        self.window.wm_attributes("-transparentcolor", "black")
        
        self.cat_size = 150 #more cat size = bigger
        
        #more setup not reccommend fixing these
        self.canvas = tk.Canvas(self.window, width = self.cat_size, height = self.cat_size, bg = "black", bd = 0, highlightthickness = 0)
        self.canvas.pack()
        self.load_animation("Hi.gif")
        self.pet = self.canvas.create_image(self.cat_size // 2,self.cat_size // 2,image=self.frames[0])
        self.animate()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        
        #set position
        self.x = 200
        self.y = self.screen_height - 200
        
        #will change later so it useless to change
        self.speed_x = 1
        self.speed_y = 0
        
        #start loop
        self.update_movement()
        self.random_behavior()
        self.window.mainloop()
        
        #make it move so scary 100% pure magik
    def animate(self):
        if not self.frames:
            return
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.canvas.itemconfig(self.pet,image=self.frames[self.current_frame])
        self.window.after(200, self.animate)
        
        #magically data structure how?
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
                r, g, b = self.cat_color
                pixels = frame.load()
                for y in range(frame.height):
                    for x in range(frame.width):
                        old_r, old_g, old_b, alpha = pixels[x, y]
                        if alpha > 0:
                            if old_r < 70 and old_g < 70 and old_b < 70:
                                continue
                            pixels[x, y] = ((old_r + r) // 2,(old_g + g) // 2,(old_b + b) // 2,alpha)
                if self.look_left:
                    frame = frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                new_frames.append(ImageTk.PhotoImage(frame))
            self.frames = new_frames
            self.current_frame = 0
        except Exception as error:
            print(f"Could not load {filename}: {error}")
            return False
        
        #make cat walk normally
    def update_movement(self):
        if self.walking:
            self.x += self.speed_x
            self.y += self.speed_y
            if self.x <= 0:
                self.x = 0
                self.speed_x = abs(self.speed_x)
                self.look_left = False
                if abs(self.speed_x) > 4:
                    self.load_animation("Run.gif")
                else:
                    self.load_animation("Walk.gif")
            elif self.x >= self.screen_width - self.cat_size:
                self.x = self.screen_width - self.cat_size
                self.speed_x = -abs(self.speed_x)
                self.look_left = True
                if abs(self.speed_x) > 4:
                    self.load_animation("Run.gif")
                else:
                    self.load_animation("Walk.gif")
            self.window.geometry(f"{self.cat_size}x"f"{self.cat_size}+"f"{int(self.x)}+"f"{int(self.y)}")
        self.window.after(20, self.update_movement)
        
        #not real it just animation
    def Jump(self):
        if self.floating:
            return
        self.floating = True
        self.walking = True
        self.load_animation("Jump.gif")
        float_time = len(self.frames) * 200
        self.window.after(float_time,self.noJump)
        
        #just make sure cat doesn't jumping
    def noJump(self):
        self.floating = False
        self.walking = True
        if abs(self.speed_x) > 4:
            self.load_animation("Run.gif")
        else:
            self.load_animation("Walk.gif")
            
        #where all the magik come from
        #random behavier
    def random_behavior(self):
        if self.walking:
            self.speed_x = 0
            self.walking = False
            if random.random() < 0.25:
                self.walking = True
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
            walk_time = random.randint(1000, 20000)
            self.window.after(walk_time, self.random_behavior)
            
            
if __name__ == "__main__":
    Cat()