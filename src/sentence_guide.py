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
        self.additional_penalties = self.data["additional penalties"]
        
    def initialise_aggrevation_clauses(self):
        return [";  \n".join(self.data["aggrevations"][x]["clauses"]) for x in self.data["aggrevations"]]
    
    def initialise_aggrevation_articles(self):
        return [self.data["aggrevations"][x]["article"] for x in self.data["aggrevations"]]

class SentenceGuide:
    def __init__(self):
        self.crime = None
        self.current_max_sentence = None
        self.current_min_sentence = None
        self.current_min_fine = None
        self.current_max_fine = None
        self.agg_max_sentence = None
        self.agg_min_sentence = None
        self.prev_conviction = None
        self.prev_conviction_pardon = None
        self.prev_conviction_type = None
        self.felony_misd_pronounced_5y = None
        self.special_revoke_reasons = None
        self.final_judgement_in_5y = None
        self.community_service = None
        self.community_service_hours = None
        self.time_for_performance_of_cs = None
        self.consider_reprimand = None
        self.reprimand_granted = None
        
    def initialise_with_crime(self, crime_obj: Crime) -> None:
        self.crime = crime_obj
        self.current_max_sentence = self.crime.standard_max_sentence
        self.current_min_sentence = self.crime.standard_min_sentence
        self.current_min_fine = self.crime.standard_min_fine
        self.current_max_fine = self.crime.standard_max_fine


    def set_agg_max_sentence(self, aggrevation: str) -> None:
        if aggrevation == "None":
            self.agg_max_sentence = 0
        else:
            sentence = self.crime.aggrevations[aggrevation]["prison"]["max"]
            self.agg_max_sentence = sentence
            self.current_max_sentence = sentence

    def set_agg_min_sentence(self, aggrevation: str) -> None:
        if aggrevation == "None":
            self.agg_min_sentence = 0
        else:
            sentence = self.crime.aggrevations[aggrevation]["prison"]["min"]
            self.agg_min_sentence = sentence
            self.current_min_sentence = sentence


    def mitigate_fine_article_94(self) -> float:
        self.current_min_fine /= 2
        return self.current_min_fine * -1
    

    def mitigtate_sentence_article_94(self) -> float:
        new_min_sentence=None
        match self.current_min_sentence:
            case 0:
                new_min_sentence = 0
            case cms if 0.0164 <= cms < 2:
                new_min_sentence = 0.00821917808219178
            case cms if 2<= cms < 5:
                new_min_sentence = 0.5
            case cms if 5<= cms < 10:
                new_min_sentence = 1
            case cms if cms >= 10:
                new_min_sentence = 2
        difference = new_min_sentence - self.current_min_sentence 
        self.current_min_sentence = new_min_sentence
        return difference
    
    
    
        
    