import threading

class CTheadeing:
    def __init__(self) -> None:
        self.all_theards = []
        self.run = None

    def add(self ,target ,args:tuple=None):
        if self.all_theards: run = False
        else: run = True
        thread = threading.Thread(target=target, args=args)
        self.all_theards.append(thread)
        thread.start()
        if run: self.run = threading.Thread(target=self.runing)
        return

    def runing(self):
        while self.all_theards:
            for i,v in enumerate(self.all_theards):
                if v.is_alive(): del self.all_theards[i]
            if len(self.all_theards) == 0: break
        return
