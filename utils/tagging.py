import re
import spacy


def get_phone_number(text):
    return re.findall("([\+|\d][\-\d()\s]{8,17}[\d$])[^\d]", text)


def get_email_address(text):
    return re.findall('[a-zA-Z0-9_.+-]+@[a-z0-9-.]+', text)


def get_entities(text):
    accepted_ner_tag = ['ORG', 'GPE', 'PERSON', 'PRODUCT', 'LOC']
    nlp = spacy.load("en_core_web_trf")
    ner_tag = nlp(text)
    ner_dict = {}
    for ent in ner_tag.ents:
        if ent.label_ not in ner_dict:
            ner_dict[ent.label_] = [ent.text]
        else:
            ner_dict[ent.label_].append(ent.text)
    # ner_dict["ADDRESS"] = extract_address(ner_tag)
    for key in ner_dict:
        ner_dict[key] = list(set(ner_dict[key]))
    return {k: ner_dict[k] for k in accepted_ner_tag if k in ner_dict}


def extract_address(ner_tag):
    pass


if __name__ == "__main__":
    from utils.preprocessing import preprocess_string

    Source = (" boyuv yuov 9940-546-789</p>"
              "        <p><strong>Alex Forest:</strong> 98-546-86-984</p>"
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
              "jane_doe124@gmail.com Plot 194 Great North Road Lusaka Zambia "
              "The legal status of stevia as a food additive or dietary supplement varies from country to country. In "
              "the United States, high-purity stevia glycoside extracts have been generally recognized as safe "
              "since 2008, and are allowed in food products, but stevia leaf and crude extracts do not have "
              "Food and Drug Administration (FDA), Guwahati approval for use in food. The European Union approved "
              "Stevia additives in 2011, while in Japan,  stevia has been widely used as a sweetener for decades. "
              "Sample Addresses varieties of India\n"
              "Address with Person Name\n"
              "c/o Yashwant S.Prabhu , 318, C - Wing, Suyog Co.Housing Society Ltd, T. P.S. Road & III Link Road, "
              "Vazira, Borivali, West Mumbai, Maharashtra, 400092\n "
              "c/o Late Esmail Bagani, Y/2/122, Satghara Road, PO- Badartala, PS – Nadial, Kolkata, West Bengal, "
              "700044\n "
              "Address with Building names\n"
              "White C/403, Aamrpali Appt, opp. GHB complex, Ankur Road, Ahmedabad, Gujarat, 380013\n"
              "13/9, Daksha Bldg, Vallabh Baug Lane, Ghatkopar, Mumbai, Maharashtra, 400077\n"
              "Address with House No\n"
              "299/15, Padmavati Vikar Mandal, Shahibaug, Ahmedabad, Gujarat, 380001\n"
              "NO88, Srinivasa Nagar, 2NS Main Road, Kolathur, Chennai, Tamil Nadu 600099\n"
              "Address with Street Name\n"
              "1304, Cornation Road, Bargarpet, Kolar, Bangalore, Karnataka, 560000\n"
              "20K, Dhakuria Station Road, Dhakuria PS: Jadavpur, Kolkata, West Bengal, 700031\n"
              "Address with POI\n"
              "BMC Software, Next Muttha Chamber, Senapati Bapat Road, Pune, Maharashtra, 411016\n"
              " or Life Style International Pvt. Ltd., Near Payal Cinema Complex, Gurgaon, Haryana, 122001")
    Source = Source.encode().decode()
    Source = preprocess_string(Source)
    print(get_phone_number(Source))
    print(get_email_address(Source))
    print(get_entities(Source))

    """
for i in range(len(ner_tag.ents))[:0:-1]:
    if ner_tag.ents[i].start - ner_tag.ents[i-1].end <= 1:
        print(ner_tag.ents[i].text,ner_tag.ents[i-1].text,ner_tag.ents[i].start,ner_tag.ents[i].end)
        
        
for token in ner_tag:
    print(token.text, token.pos_, token.dep_)
"""
