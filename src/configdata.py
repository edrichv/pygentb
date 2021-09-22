class ConfigData:
    def __init__(self, data: dict):
        self.tp_type = data["TestPattern"]["type"]
        self.bpdelay = data["TestPattern"]["bpdelay"]
        self.acdelay = data["TestPattern"]["acdelay"]
        self.numrandom = data["TestPattern"]["numrandom"]
        self.pattern = data["TestPattern"]["pattern"]
        self.seed = data["TestPattern"]["seed"]
        self.vecfilepath = data["Files"]["vecfilepath"]
        self.toppath = data["Files"]["toppath"]
        self.outpath = data["Files"]["outpath"]
        self.clockname = data["TestbenchParams"]["clockname"]
        self.timescale = data["TestbenchParams"]["timescale"]
        self.clkperiod = data["TestbenchParams"]["clkperiod"]
        self.simlength = data["TestbenchParams"]["simlength"]
        