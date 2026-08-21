from dataclasses import dataclass,field
from world import World
from memory import Memory
from config import *

@dataclass
class Agent:
    x:int=12; y:int=12; energy:int=INITIAL_ENERGY; water:int=INITIAL_WATER
    health:int=INITIAL_HEALTH; age:int=0; inventory:dict=field(default_factory=dict)

class Engine:
    def __init__(self,seed=814237):
        self.seed=seed; self.world=World(WORLD_SIZE,seed); self.memory=Memory()
        self.agent=Agent(); self.life=0; self.cycle=0; self.total=0; self.max_lives=50
        self.running=False; self.completed=False; self.log=[]
    def start(self,lives):
        self.__init__(self.seed); self.max_lives=lives; self.life=1; self.running=True
        self._record("birth",{"reason":"experiment_start","memory_preserved":True}); return self.public_state()
    def _record(self,kind,data):
        e={"life":self.life,"cycle":self.cycle,"total_cycle":self.total,"kind":kind,"data":data}
        self.log.append(e); self.memory.event(self.life,self.cycle,kind,data)
    def observation(self):
        if not self.running: return {"running":False}
        return {"life":self.life,"cycle":self.cycle,"total_cycle":self.total,
                "state":{"energy":self.agent.energy,"water":self.agent.water,"health":self.agent.health,"age":self.agent.age},
                "environment":self.world.visible(self.agent.x,self.agent.y),
                "available_actions":["observe","move","search","collect","consume","rest","combine"]}
    def step(self,action,p):
        if not self.running: raise ValueError("No running experiment")
        before=self.observation()["state"].copy()
        result=self._act(action,p or {})
        self.cycle+=1; self.total+=1; self.agent.age+=1
        self.agent.energy-=1
        if action=="move": self.agent.energy-=MOVE_ENERGY-1; self.agent.water-=MOVE_WATER
        cell=self.world.get(self.agent.x,self.agent.y)
        if cell.danger: self.agent.health-=max(1,cell.danger//10)
        death=self._cause()
        self._record("action",{"action":action,"params":p,"before":before,"result":result,"death":death})
        if death: self._die(death)
        return self.public_state()
    def _act(self,a,p):
        c=self.world.get(self.agent.x,self.agent.y)
        if a=="observe": return {"environment":self.world.visible(self.agent.x,self.agent.y)}
        if a=="move":
            dx=int(p.get("dx",0)); dy=int(p.get("dy",0))
            if abs(dx)>1 or abs(dy)>1 or (dx==0 and dy==0): raise ValueError("dx/dy must be -1..1")
            self.agent.x=(self.agent.x+dx)%WORLD_SIZE; self.agent.y=(self.agent.y+dy)%WORLD_SIZE
            return {"terrain":self.world.get(self.agent.x,self.agent.y).terrain}
        if a=="search":
            found=[]
            if c.water: found.append("water")
            if c.food: found.append("food")
            if c.material: found.append("material")
            if c.danger: found.append("danger")
            return {"found":found or ["nothing_obvious"]}
        if a=="collect":
            got={}
            for k in ["water","food","material"]:
                n=min(20 if k=="water" else 10,getattr(c,k))
                if n: setattr(c,k,getattr(c,k)-n); self.agent.inventory[k]=self.agent.inventory.get(k,0)+n; got[k]=n
            for k,n in got.items(): self.memory.discover(f"Resource collected: {k}",{"life":self.life,"cycle":self.cycle,"amount":n})
            return {"collected":got}
        if a=="consume":
            item=p.get("item"); amount=min(20 if item=="water" else 10,self.agent.inventory.get(item,0))
            if amount:
                self.agent.inventory[item]-=amount
                if item=="water": self.agent.water=min(100,self.agent.water+amount)
                if item=="food": self.agent.energy=min(100,self.agent.energy+amount*3)
            return {"consumed":amount,"item":item}
        if a=="rest":
            self.agent.energy=min(100,self.agent.energy+REST_ENERGY); self.agent.water=max(0,self.agent.water-REST_WATER); return {"rested":True}
        if a=="combine":
            items=sorted(p.get("items",[]))
            if items==["food","material"] and self.agent.inventory.get("food",0)>=1 and self.agent.inventory.get("material",0)>=1:
                self.agent.inventory["food"]-=1; self.agent.inventory["material"]-=1
                self.agent.inventory["tool"]=self.agent.inventory.get("tool",0)+1
                self.memory.discover("Created a tool from food + material",{"life":self.life,"cycle":self.cycle})
                return {"created":"tool"}
            return {"created":None}
        raise ValueError("Unknown action")
    def _cause(self):
        if self.agent.health<=0:return "health_zero"
        if self.agent.energy<=0:return "energy_zero"
        if self.agent.water<=0:return "water_zero"
        return None
    def _die(self,cause):
        ctx={"energy":self.agent.energy,"water":self.agent.water,"health":self.agent.health}
        self.memory.death(self.life,self.cycle,cause,ctx); self._record("death",{"cause":cause})
        if self.life>=self.max_lives: self.running=False; self.completed=True; return
        self.life+=1; self.cycle=0; self.agent=Agent()
        self._record("birth",{"reason":"rebirth","memory_preserved":True})
    def public_state(self):
        score=min(100,len(self.memory.discoveries)*5)
        return {"running":self.running,"completed":self.completed,"life":self.life,"max_lives":self.max_lives,
                "cycle":self.cycle,"total_cycles":self.total,
                "character":{"energy":self.agent.energy,"water":self.agent.water,"health":self.agent.health,
                             "age":self.agent.age,"evolution_score":score},
                "discoveries":len(self.memory.discoveries),"deaths":len(self.memory.deaths)}
    def memory_public(self): return self.memory.public()
    def history(self,limit=200): return self.log[-max(1,min(limit,5000)):]
    def experiment_summary(self):
        return [{"id":"current","completed":self.completed,"life":self.life,"max_lives":self.max_lives,
                 "total_cycles":self.total,"discoveries":len(self.memory.discoveries),"deaths":len(self.memory.deaths)}]
    def results(self):
        return {"completed":self.completed,"lives_reached":self.life,"total_cycles":self.total,
                "discoveries":self.memory.discoveries,"deaths":self.memory.deaths,"events":len(self.memory.events)}
