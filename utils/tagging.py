import re
import spacy


def get_phone_number(text):
    return re.findall("([\+|\d][\d()\s]{8,17}[\d$])[^\d]",text)


def get_email_address(text):
    return re.findall('[a-zA-Z0-9_.+-]+@[a-z0-9-.]+', text)


def get_entities(text):
    accepted_ner_tag = ['ORG', 'GPE', 'PERSON', 'PRODUCT']
    nlp = spacy.load("en_core_web_md")
    ner_tag = nlp(text)
    ner_dict = {}
    for ent in ner_tag.ents:
        if ent.label_ not in ner_dict:
            ner_dict[ent.label_] = [ent.text]
        else:
            ner_dict[ent.label_].append(ent.text)
    return ner_dict


if __name__ == "__main__":
    from utils.preprocessing import preprocess_string
    Source = ("boyuv yuov 9940-546-789</p>"
              "        <p><strong>Mutiara Damansara:</strong> 98-546-86-984</p>"
              "        <p><strong>Penang:</strong> + 60 (0)4 255 9000</p>"
              "        <h2>Where we are </h2>"
              "        <strong>&nbsp;Call us on:</strong>&nbsp;+6 (03) 8924 8686"
              "        </p></div><div class=\"sys_two\">"
              "    <h3 class=\"parentSchool\">General enquiries</h3><p style=\"FONT-SIZE: 11px\">"
              "     <strong>&nbsp;Call us on:</strong>&nbsp;+6 (03) 8924 8000"
              "+ 60 (7) 268-6200 <br /> 99-556-88-987"
              " Fax:<br /> "
              " +60 (7) 228-6202<br /> "
              "Phone:</strong><strong style=\"color: #f00\">+601-4228-8055</strong> 99-556-88-987. "
              "Hi my name is John and email address is john.doe@somecompany.co.uk.fml and my friend's email is "
              "jane_doe124@gmail.com"
              "The legal status of stevia as a food additive or dietary supplement varies from country to country. In "
              "the United States, high-purity stevia glycoside extracts have been generally recognized as safe "
              "since 2008, and are allowed in food products, but stevia leaf and crude extracts do not have "
              "Food and Drug Administration (FDA), Arizona approval for use in food. The European Union approved "
              "Stevia additives in 2011, while in Japan, stevia has been widely used as a sweetener for decades.")
    Source = Source.encode().decode()
    Source = preprocess_string(Source)
    print(get_phone_number(Source))
    print(get_email_address(Source))
    print(get_entities(Source))
