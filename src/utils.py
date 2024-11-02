


class SentenceGuide:
    def __init__(self, crime_data: dict):
        self.data = crime_data
        self.crime = self.data["crime"]
        self.standard = self.data["standard"]
        self.standard_max_sentence = self.standard["prison"]["max"]
        self.standard_min_sentence = self.standard["prison"]["min"]
        self.standard_max_fine = self.standard["fine"]["max"]
        self.standard_min_fine = self.standard["fine"]["min"]
        self.aggrevations = self.data["aggrevations"]
        self.aggrevation_articles = [self.data["aggrevations"][x]["article"] for x in self.data["aggrevations"]]
        self.aggrevation_clauses = [";  \n".join(self.data["aggrevations"][x]["clauses"]) for x in self.data["aggrevations"]]
        self.agg_max_sentence = None
        self.agg_min_sentence = None
        self.prev_conviction = None
        self.prev_conviction_pardon = None


    def set_agg_max_sentence(self, aggrevation: str):
        self.agg_max_sentence = self.aggrevations[aggrevation]["prison"]["max"]

    def set_agg_min_sentence(self, aggrevation: str):
        self.agg_min_sentence = self.aggrevations[aggrevation]["prison"]["min"]

    def initialise_aggrevation_clauses(self):
        pass


