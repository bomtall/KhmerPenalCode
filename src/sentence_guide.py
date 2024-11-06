


class Crime:
    def __init__(self, crime_data: dict):
        self.data = crime_data
        self.crime = self.data["crime"]
        self.standard = self.data["standard"]
        self.standard_max_sentence = self.standard["prison"]["max"]
        self.standard_min_sentence = self.standard["prison"]["min"]
        self.standard_max_fine = self.standard["fine"]["max"]
        self.standard_min_fine = self.standard["fine"]["min"]
        self.aggrevations = self.data["aggrevations"]
        self.aggrevation_articles = self.initialise_aggrevation_articles()
        self.aggrevation_clauses = self.initialise_aggrevation_clauses()
        
    def initialise_aggrevation_clauses(self):
        return [";  \n".join(self.data["aggrevations"][x]["clauses"]) for x in self.data["aggrevations"]]
    
    def initialise_aggrevation_articles(self):
        return [self.data["aggrevations"][x]["article"] for x in self.data["aggrevations"]]

class SentenceGuide:
    def __init__(self, crime_obj: Crime):
        self.crime = crime_obj
        self.current_max_sentence = self.crime.standard_max_sentence
        self.current_min_sentence = self.crime.standard_min_sentence
        self.agg_max_sentence = None
        self.agg_min_sentence = None
        self.prev_conviction = None
        self.prev_conviction_pardon = None
        self.prev_conviction_type = None
        self.felony_misd_pronounced_5y = None
        self.special_revoke_reasons = None
        self.final_judgement_in_5y = None


    def set_agg_max_sentence(self, aggrevation: str):
        sentence = self.crime.aggrevations[aggrevation]["prison"]["max"]
        self.agg_max_sentence = sentence
        self.current_max_sentence = sentence

    def set_agg_min_sentence(self, aggrevation: str):
        sentence = self.crime.aggrevations[aggrevation]["prison"]["min"]
        self.agg_min_sentence = sentence
        self.current_min_sentence = sentence
        
        
    # idea to replace function with generalised update func that compares to current and updates




