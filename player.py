class Player:
    def __init__(self, name, **kwargs):
        self.name = name
        self.backhand_skill = kwargs.get("backhand_skill", 0.95)
        self.forehand_skill = kwargs.get("forehand_skill", 0.95)
        self.serve_skill = kwargs.get("serve_skill", 0.95)
        self.return_skill = kwargs.get("return_skill", 0.95)
        self.speed = kwargs.get("speed", 0.5)
        self.variety = kwargs.get("variety", 0.5)
        self.position = 5
        self.serve_placement = [0.18, 0.15, 0.1, 0.05, 0.02, 0.02, 0.05, 0.1, 0.15, 0.18]
        self.forehand_placement = [0.025, 0.025, 0.025, 0.05, 0.1, 0.2, 0.3, 0.15, 0.1, 0.025] 
        self.backhand_placement = self.forehand_placement[::-1] # mirror for now