class Memory:
    def __init__(self):
        self.events=[]; self.discoveries=[]; self.hypotheses=[]; self.deaths=[]
    def event(self,life,cycle,kind,data):
        self.events.append({"life":life,"cycle":cycle,"kind":kind,"data":data})
    def discover(self,text,evidence):
        for d in self.discoveries:
            if d["text"]==text:
                d["count"]+=1; d["evidence"].append(evidence); return
        self.discoveries.append({"text":text,"count":1,"evidence":[evidence]})
    def death(self,life,cycle,cause,context):
        d={"life":life,"cycle":cycle,"cause":cause,"context":context}
        self.deaths.append(d); self.event(life,cycle,"death",d)
    def public(self):
        return {"discoveries":self.discoveries[-100:],"hypotheses":self.hypotheses[-100:],
                "deaths":self.deaths[-100:],"event_count":len(self.events)}
