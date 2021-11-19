# # NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# # All trademark and other rights reserved by their respective owners
# # Copyright 2008-2021 Neongecko.com Inc.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from simple_NER.annotators.datetime_ner import DateTimeNER, TimedeltaNER
from simple_NER.annotators.email_ner import EmailNER
from simple_NER.annotators.locations_ner import LocationNER
from simple_NER.annotators.names_ner import NamesNER
from simple_NER.annotators.nltk_ner import NltkNER
from simple_NER.annotators.numbers_ner import NumberNER
from simple_NER.annotators.units_ner import UnitsNER
from simple_NER.annotators.remote.dbpedia import SpotlightNER
from neon_transformers import UtteranceTransformer


class SimpleNERTagger(UtteranceTransformer):
    def __init__(self, name="simpleNER", priority=50):
        super().__init__(name, priority)

    def transform(self, utterances, context=None):
        entities = []
        context = context or {}
        lang = context.get("lang") or self.config.get("lang", "en-us")
        for utterance in utterances:
            # TODO make configurable
            # extract emails
            for ent in EmailNER().extract_entities(utterance):
                entities.append(ent.as_json())
            # extract Nouns
            for ent in NamesNER().extract_entities(utterance):
                # HACK TODO fix upstream
                if ent.value.lower() in ["the"]:
                    continue
                entities.append(ent.as_json())
            # extract numbers
            for ent in NumberNER().extract_entities(utterance):
                entities.append(ent.as_json())
            # extract Dates
            for ent in DateTimeNER().extract_entities(utterance):
                entities.append(ent.as_json())
            # extract Durations
            for ent in TimedeltaNER().extract_entities(utterance):
                entities.append(ent.as_json())
            # extract quantities
            for ent in UnitsNER().extract_entities(utterance):
                entities.append(ent.as_json())
            # extract Locations
            for ent in LocationNER().extract_entities(utterance):
                entities.append(ent.as_json())
            # nltk entities
            for ent in NltkNER().extract_entities(utterance):
                entities.append(ent.as_json())
            # dbpedia entities
            for ent in SpotlightNER().extract_entities(utterance):
                if float(ent.confidence) < 0.75:
                    continue
                entities.append(ent.as_json())
        # return unchanged utterances + data
        return utterances, {"entities": entities}

