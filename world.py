from dataclasses import dataclass
import random

@dataclass
class Cell:
    terrain:str="plain"
    water:int=0
    food:int=0
    material:int=0
    danger:int=0
    temperature:int=20

class World:
    def __init__(self,size=25,seed=814237):
        self.size=size; self.seed=seed; self.rng=random.Random(seed); self.cells={}; self.generate()
    def generate(self):
        for y in range(self.size):
            for x in range(self.size):
                r=self.rng.random(); c=Cell()
                if r<.08: c.terrain="water_source"; c.water=self.rng.randint(35,100)
                elif r<.18: c.terrain="forest"; c.food=self.rng.randint(15,55); c.material=self.rng.randint(10,45)
                elif r<.27: c.terrain="rocky"; c.material=self.rng.randint(15,65)
                elif r<.31: c.terrain="hazard"; c.danger=self.rng.randint(15,45)
                else: c.food=self.rng.randint(0,12); c.material=self.rng.randint(0,10)
                c.temperature=self.rng.randint(14,31); self.cells[(x,y)]=c
    def get(self,x,y): return self.cells[(x%self.size,y%self.size)]
    def visible(self,x,y,r=1):
        out=[]
        for dy in range(-r,r+1):
            for dx in range(-r,r+1):
                if dx==0 and dy==0: continue
                c=self.get(x+dx,y+dy)
                out.append({"relative":[dx,dy],"terrain":c.terrain,"temperature":c.temperature,
                            "water_visible":c.water>0,"food_visible":c.food>0,
                            "material_visible":c.material>0,"danger_visible":c.danger>0})
        return out
