from transformers import BertTokenizerFast, EncoderDecoderModel
import torch
import re

from utils import preprocess_string

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = BertTokenizerFast.from_pretrained(
    'mrm8488/bert-small2bert-small-finetuned-cnn_daily_mail-summarization')
model = EncoderDecoderModel.from_pretrained(
    'mrm8488/bert-small2bert-small-finetuned-cnn_daily_mail-summarization').to(
    device)


def generate_summary(text):
    # cut off at BERT max length 512
    inputs = tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)

    output = model.generate(input_ids, attention_mask=attention_mask)

    return tokenizer.decode(output[0], skip_special_tokens=True)


def summarise_long_text(text, mode=None):
    modes = ['cumulative', 'separative']
    if mode not in modes:
        mode = 'separative'
    return globals()["{}_summary".format(mode)](text)


def cumulative_summary(text):
    summary = ""
    sentence_list = text.split(".")
    chunk = ""
    for sentence in sentence_list:
        summary = generate_summary(chunk + sentence+". ")
        if len(summary.split(" ")) >= len((chunk+sentence).split(" ")):
            chunk += sentence + '. '
        else:
            chunk = summary + ' '
    return summary


def separative_summary(text):
    summary = ""
    sentence_list = text.split(".")
    chunk = ""
    for sentence in sentence_list:
        if len((chunk + " " + sentence).split(" ")) <= 512:
            chunk += sentence + '. '
        else:
            chunk = re.sub(' +', ' ', chunk)
            summary += generate_summary(chunk) + ' '
            chunk = sentence + '. '
    summary += generate_summary(chunk) + ' '
    return summary


if __name__ == "__main__":
    temp = ("Africa’s under-representation in human genomics data is worse than previously reported because genetic \n"
            "and genomic studies are predominantly based on populations of European ancestry. A paper published in "
            "Nature \n "
            "Medicine warned that underrepresented populations may be excluded from better understanding of disease "
            "etiology, \n "
            "    early detection and diagnosis, rational drug design and improved clinical care. \n"
            "\n"
            "Segun Fatumo, from the London School of Hygiene and Tropical Medicine, who led the collaboration of "
            "researchers from \n "
            "South Africa, Uganda, the United Kingdom, and the United States told Nature Africa that because of the "
            "way genomics \n "
            "studies are structured, the proportion of the African population’s representation will continue to fall "
            "unless urgent \n "
            "action is taken. \n"
            "\n"
            "The researchers found that about 86% of genomics studies have been conducted in individuals of European "
            "descent by \n "
            "June 2021, increasing from 81% in 2016 — suggesting that in spite of calls for more diversity in "
            "genomics studies, \n "
            "the gap continues to widen. \n"
            "\n"
            "“This shows that progress toward diversification has been painfully slow. The genomic research community "
            "tends to \n "
            "extensively use resources with relatively straightforward access models, such the UK Biobank, "
            "which includes \n "
            "participants of mostly European descent, while other ancestry groups tend to have very few such "
            "resources and limited \n "
            "access models. Data from the International HundredK+ Cohorts Consortium (IHCC), a recently established "
            "consortium of \n "
            "international cohort studies, also show considerable ancestral disparities,” they reported. \n"
            "\n"
            "“The proportion of the genomic studies that were done in Africa was 3% in 2016, now it's 1.1%. I think "
            "that this is \n "
            "shameful,” Fatumo said. \n"
            "\n"
            "African Americans are not representing Africans Fatumo noted that genomic studies conducted in African "
            "American \n "
            "populations are being wrongly categorized as expanding Africa’s genomic data. “African Americans don't "
            "represent \n "
            "Africa because they only represent a small portion of Africa.” \n"
            "\n"
            "He said the number of initiatives intended to close the gap by only targeting African Americans would "
            "not diversify \n "
            "genomics studies and would continue to leave out the continent of Africa. \n"
            "\n"
            "Fatumo’s co-author, Tinashe Chikowore, of the Sydney Brenner Institute for Molecular Bioscience, "
            "Faculty University \n "
            "of the Witwatersrand, in South Africa, said that the current genomics study structure, also prevent the "
            "world from \n "
            "benefiting from the continent’s genetic diversity. \n"
            "\n"
            "He pointed to population-enriched clinically important variants that were only discovered in "
            "underrepresented \n "
            "populations. An example is the identification in populations with African ancestry, of loss-of-function "
            "variants in \n "
            "the PCSK9 gene that reduce low-density lipoprotein cholesterol, which led to the discovery of PCSK9 "
            "inhibitor drugs. \n "
            "\n"
            "“They are highly concentrated in African individuals and have led to drugs which benefit everyone "
            "globally,” he said.\n "
            "\n"
            "“To be successful in achieving equitable inclusion of underrepresented groups in genomic studies, "
            "the stakeholders \n "
            "must stimulate local participation, build trust and ensure mutual respect,” the researchers concluded. ")
    temp = preprocess_string(temp)
    print(summarise_long_text(temp, mode="cumulative"))
    print()
    print(summarise_long_text(temp))
    # print()
    # print(summarise_long_text(summarise_long_text(temp)))
