import streamlit as st
import src.utils as utils
import math
import datetime as dt

class Sentence:
    def __init__(self, value: float, unit: str):        
        self.unit = unit
        self.value = value
        
        if unit == "years":
            match value:
                case v if v < 1/52:
                    self.unit = "days"
                    self.value = math.ceil(value * 365)
                case v if v < 1/12:
                    self.unit = "weeks"
                    self.value = math.ceil(value*52)
                case v if v < 1:
                    self.value = math.ceil(value*12)
                case v if v > 1:
                    self.value = round(value,2)
    
    def get_sentence_str(self) -> str:
        if self.value.is_integer():
            self.value = int(self.value)
        return " ".join([str(self.value), self.unit])
    
    def convert_to_years(self):
        if self.unit == "years":
            return self.value
        elif self.unit == "months":
            return self.value / 12
        elif self.unit =="weeks":
            return self.value/52
        elif self.unit =="days":
            return self.value/365
            
class Crime:
    def __init__(self, crime_data: dict):
        self.data = crime_data
        self.crime = self.data["crime"]
        self.standard = self.data["standard"]
        self.standard_max_sentence = Sentence(self.standard["prison"]["max"]["value"], self.standard["prison"]["max"]["unit"])
        self.standard_min_sentence = Sentence(self.standard["prison"]["min"]["value"], self.standard["prison"]["min"]["unit"])
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
        self.crime: Crime = None
        self.current_max_sentence = None
        self.current_min_sentence = None
        self.current_min_fine = None
        self.current_max_fine = None
        self.agg_max_sentence = None
        self.agg_min_sentence = None
        self.aggrevation = None
        self.prev_conviction = None
        self.prev_conviction_pardon = None
        self.prev_conviction_type = None
        self.felony_misd_pronounced_5y = None
        self.special_revoke_reasons = None
        self.final_judgement_in_5y = None
        self.basis_of_mitigations = None
        self.community_service = None
        self.community_service_hours = None
        self.community_service_timeframe = None
        self.time_for_performance_of_cs = None
        self.offer_to_reprimand = None
        self.reprimand_granted = None
        self.intended_sentence = None
        self.intended_fine = None
        self.sentence_suspended = None
        self.fine_suspended = None
        self.sentence_amount_to_suspend = None
        self.fine_amount_to_suspend = None
        self.intended_sentence_str=None
        self.additonal_penalties = None
        self.probation_length_months = None
        self.probation_measures = None
        

    def initialise_with_crime(self, crime_obj: Crime) -> None:
        self.crime = crime_obj
        self.current_max_sentence = self.set_current_max_sentence(self.crime.standard_max_sentence)
        self.current_min_sentence = self.set_current_min_sentence(self.crime.standard_min_sentence)
        self.current_min_fine = self.crime.standard_min_fine
        self.current_max_fine = self.crime.standard_max_fine
        
    def set_current_max_sentence(self, sentence: Sentence):
        self.current_max_sentence = sentence
        st.session_state["current_max_s"] = self.current_max_sentence.get_sentence_str()
        
    def set_current_min_sentence(self, sentence: Sentence):
        self.current_min_sentence = sentence
        st.session_state["current_min_s"] = self.current_min_sentence.get_sentence_str()
        
    
    def set_agg_max_sentence(self, aggrevation: str) -> None:
        if aggrevation == "None":
            #if self.current_max_sentence > self.crime.standard_max_sentence:
            self.set_current_max_sentence(self.crime.standard_max_sentence)
            sentence = self.crime.standard_max_sentence
        else:
            sentence = Sentence(self.crime.aggrevations[aggrevation]["prison"]["max"]["value"], self.crime.aggrevations[aggrevation]["prison"]["max"]["unit"])
            self.set_current_max_sentence(sentence)
        self.agg_max_sentence = sentence

    def set_agg_min_sentence(self, aggrevation: str) -> None:
        if aggrevation == "None":
            sentence = self.crime.standard_min_sentence
        else:
            sentence = Sentence(self.crime.aggrevations[aggrevation]["prison"]["min"]["value"], self.crime.aggrevations[aggrevation]["prison"]["min"]["unit"])
        self.agg_min_sentence = sentence
        self.set_current_min_sentence(sentence)


    def mitigate_fine_article_94(self) -> float:
        self.current_min_fine /= 2
        return self.current_min_fine * -1
    

    def mitigtate_sentence_article_94(self) -> None:
        new_min_sentence=None
        if self.current_min_sentence.unit == "years":
            match self.current_min_sentence.value:
                case cms if cms < 2:
                    new_min_sentence = Sentence(1, "days")
                case cms if 2<= cms < 5:
                    new_min_sentence = Sentence(6, "months")
                case cms if 5<= cms < 10:
                    new_min_sentence = Sentence(1, "years")
                case cms if cms >= 10:
                    new_min_sentence = Sentence(2, "years")
            
        elif self.current_min_sentence.unit == "days":
            match self.current_min_sentence.value:
                case cms if 730 > cms > 6:
                    new_min_sentence = Sentence(1, "days")
                # case cms if cms < 6:
                #     new_min_sentence = Sentence(1, "days")
        else:
            new_min_sentence = Sentence(1, "days")
        
        diff = utils.create_sentence_period(new_min_sentence.convert_to_years() - self.current_min_sentence.convert_to_years())
        self.set_current_min_sentence(new_min_sentence)
        return diff

    
    def possible_to_reprimand(self):
        if (
            self.current_min_sentence.convert_to_years() < 5 and self.prev_conviction and not self.final_judgement_in_5y) or (
            self.current_min_sentence.convert_to_years() < 5 and self.prev_conviction == False
            ):
                return True
        else:
            return False
    
    def generate_report(self):
        report = f"""
Sentence Guidelines Report

Report Date: {dt.datetime.today().strftime('%d/%m/%Y %H:%M:%S')}

Sentence guideline maximum: {self.current_max_sentence.get_sentence_str()}
Sentence guideline minimum: {self.current_min_sentence.get_sentence_str()}

"""
        if self.intended_sentence:
            
            report += f"""
Final sentence: {self.intended_sentence_str} {" - Wholly Suspended" if self.sentence_suspended else ""}
{"\nPart Suspended: " + str(self.sentence_amount_to_suspend.get_sentence_str()) if self.sentence_amount_to_suspend else ""}

Final fine: ៛{'{:,.2f}'.format(self.intended_fine)} {" - Wholly Suspended" if self.fine_suspended else ""}
{"\nPart Suspended: ៛" + str('{:,.2f}'.format(self.fine_amount_to_suspend)) if self.fine_amount_to_suspend else ""}
        """
    
        elif self.community_service:
            report += f"""
Community Service awarded

Community service hours: {self.community_service_hours}
Community service months to complete: {self.community_service_timeframe}
        """
        
        if self.aggrevation:
            report += f"""
Aggravation: \n {self.aggrevation + "\n " + "\n ".join(self.crime.aggrevations[self.aggrevation]["clauses"])}
            """
        
        if self.prev_conviction:
            report += f"""
Previous convictions: {str(self.prev_conviction)}  
Type: {self.prev_conviction_type}  
Pardoned: {str(self.prev_conviction_pardon)}  
Special reasons not to revoke a prior suspended sentence: {self.special_revoke_reasons}  
        """
        
        for i in self.additional_penalties:
            report += f"""\n
Additional penalty: {i[0]}  
Term: {i[1]} {i[2]}  \n
        """
        
        if self.probation_length_months:
            report += f"  \nProbation: {self.probation_length_months} months  \n"
            if self.probation_measures:
                for i in self.probation_measures:
                    report += f"{i}  \n"
        
        return report
    
    
        
    