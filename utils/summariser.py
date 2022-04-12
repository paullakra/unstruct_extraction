from transformers import BertTokenizerFast, EncoderDecoderModel
import torch
import re


def load_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokenizer = BertTokenizerFast.from_pretrained(
        'mrm8488/bert-small2bert-small-finetuned-cnn_daily_mail-summarization')
    model = EncoderDecoderModel.from_pretrained(
        'mrm8488/bert-small2bert-small-finetuned-cnn_daily_mail-summarization').to(
        device)
    return tokenizer, model, device


def generate_summary(text):
    # cut off at BERT max length 512
    tokenizer, model, device = load_model()
    inputs = tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)

    output = model.generate(input_ids, attention_mask=attention_mask)

    return tokenizer.decode(output[0], skip_special_tokens=True)


def summarise_long_text(text):
    summary = ""
    sentence_list = text.split(".")
    chunk = ""
    for sentence in sentence_list:
        if len((chunk+" "+sentence).split(" ")) <= 512:
            chunk += sentence+'. '
        else:
            chunk = re.sub(' +', ' ', chunk)
            summary += generate_summary(chunk)+' '
            chunk = ""
    summary += generate_summary(chunk)+' '
    return summary


if __name__ == "__main__":
    temp = (
        "After finishing Billy Hatcher and the Giant Egg (2003), Sonic Team began to plan its next project. Among "
        "the ideas the team was considering was a game with a realistic tone and an advanced physics engine. When "
        "Sega reassigned the team to start working on a new game in the bestselling Sonic series, they decided to "
        "retain the realistic approach. Sonic the Hedgehog was conceived for sixth-generation consoles, "
        "but Sonic Team realized its release would coincide with the series' 15th anniversary and decided to develop "
        "it for seventh-generation consoles such as the PlayStation 3 and Xbox 360. Series co-creator and team "
        "lead Yuji Naka wanted the first Sonic game for seventh-generation systems to reach a wide audience. Naka "
        "noted the success of superhero films such as Spider-Man 2 (2004) and Batman Begins (2005): \"When Marvel or "
        "DC Comics turn their characters into films, they are thinking of them as blockbusters, huge hits, "
        "and that's what we were trying to emulate with Sonic.\" Thus, development of Sonic the Hedgehog began in "
        "late 2004. Sonic Team used the same title as the original 1991 Sonic the Hedgehog to indicate that "
        "it would be a major advance from the previous games and a reboot that returned to the series' roots."
        " The Havok physics engine, previously used in their PlayStation 2 game Astro Boy (2004), allowed "
        "Sonic Team to create expansive levels previously impossible on earlier sixth-generation consoles and "
        "experiment with multiple play-styles. In addition, the engine also enabled Sonic Team to experiment with "
        "aspects such as global illumination, a night-and-day system, and giving Sonic new abilities like using ropes "
        "to leap into the air. Director Shun Nakamura demonstrated the engine during their stage shows at the Tokyo "
        "Game Show (TGS) in 2005. As the hardware of the Xbox 360 and PlayStation 3 was more powerful compared to "
        "the prior generation's consoles, the design team was able to create a more realistic setting than "
        "those of previous Sonic games. Sonic and Doctor Eggman were redesigned to better suit this updated "
        "environment: Sonic was made taller, with longer quills, and Eggman was made slimmer and given a more "
        "realistic appearance. Nakamura and producer Masahiro Kumono reasoned this was because the characters "
        "would be interacting with more humans, and felt it would make the game more appealing to older players. "
        "At one point, Sonic Team considered giving Sonic realistic fur and rubber textures. While Sonic Team had "
        "a major focus on the visuals, they considered their primary challenge creating a game that was as appealing "
        "as the original Sega Genesis Sonic games. They felt Sonic Heroes (2003) and Shadow the Hedgehog (2005) "
        "had veered into different directions and wanted to return the series to its speed-based roots in new ways. "
        "For example, they wanted to include multiple paths in levels, like the Genesis games had, a goal the "
        "realistic environments helped achieve. Sonic Team sought to \"aggressively\" address problems with the "
        "virtual camera system from earlier Sonic games, about which they had received many complaints. Concept "
        "art for the character who would eventually become Silver the Hedgehog. More that fifty designs were made for "
        "the character before settling on his final appearance."
        "Early concept art of Silver the Hedgehog Silver the Hedgehog's gameplay style was born out of Sonic Team's "
        "desire to take advantage of Havok's realistic physics capabilities. The first design concept for Silver's "
        "character was an orange mink; he attained his final hedgehog look after over 50 design iterations. In "
        "designing Shadow's gameplay, the developers abandoned the concept of firearms previously used in Shadow the "
        "Hedgehog (2005) in favor of combat elements to differentiate him from the other characters. Shadow's "
        "gameplay was further fleshed out with the addition of vehicles; each vehicle uses its own physical engine.["
        "22] The game also features several CGI cutscenes produced by Blur Studio. Animation supervisor Leo Santos "
        "said Blur faced challenges animating the opening scene due to the placement of Sonic's mouth. As "
        "development progressed, Sonic Team faced serious problems. In March 2006, Naka resigned as head of Sonic "
        "Team to form his own company, Prope. Naka has said he resigned because he did not want to "
        "continue making Sonic games and instead wished to focus on original properties. With his departure, "
        "\"the heart and soul of Sonic\" was gone, according to former Sega of America CEO Tom Kalinske. Sonic "
        "the Hedgehog was originally intended for release on all major seventh-generation consoles as well as "
        "Windows, but Sega was presented with development kits for Nintendo's less powerful Wii console. Sega "
        "believed porting the game to Wii would take too long, and so conceived a Sonic game that would use the "
        "motion detection function of its controller. Therefore, the team was split in two: Nakamura led one "
        "team to finish Sonic the Hedgehog for Xbox 360 and PlayStation 3 while producer Yojiro Ogawa led the other "
        "to begin work on Sonic and the Secret Rings for the Wii. The split left an unusually small team to "
        "work on Sonic the Hedgehog. Sega pressured the team to finish the game in time for the 2006 holiday shopping "
        "season, so with the deadline quickly approaching, Sonic Team rushed the final stages of development, "
        "ignoring bug reports from Sega's quality assurance department and control problems. In "
        "retrospect, Ogawa noted that the final period proved to be a large challenge for the team. Not only was the "
        "Xbox 360 release imminent, but the PlayStation 3 launch was scheduled not long afterwards. This put "
        "tremendous pressure on the team to develop for both systems. Producer Takashi Iizuka similarly recalled, "
        "\"we didn't have any time to polish and we were just churning out content as quick as we could.\" The "
        "cast of the Sonic X anime series reprised their voice roles for Sonic the Hedgehog, and actress Lacey "
        "Chabert supplied the voice of series newcomer and damsel in distress Princess Elise. The score for the "
        "game was primarily composed by Tomoya Ohtani along with Hideaki Kobayashi, Mariko Nanba, Taihei Sato, "
        "and Takahito Eguchi. It was the first Sonic game that Ohtani, who had previously contributed to "
        "Sonic Heroes (2003) and Shadow the Hedgehog, worked on as sound director. The main theme for the game, "
        "the fantasy-rap song \"His World\", was performed by Ali Tabatabaee and Matty Lewis of the band Zebrahead."
        " Crush 40 performed Shadow's theme, \"All Hail Shadow\", while vocalist Bentley Jones (previously "
        "known as Lee Brotherton) sang Silver's theme, \"Dreams of an Absolution\". R&B artist Akon performed a "
        "remix of the Dreams Come True song \"Sweet Sweet Sweet\", a song previously used as the ending theme to "
        "Sonic the Hedgehog 2 (1992). Because Sonic the Hedgehog was the first Sonic game for "
        "seventh-generation consoles, Ohtani \"aimed to emphasise that it was an epic next-generation title\". "
        "Two soundtrack albums were released on January 10, 2007, under Sega's Wave Master label: Sonic the Hedgehog "
        "Vocal Traxx: Several Wills and Sonic the Hedgehog Original Soundtrack. Vocal Traxx: Several Wills "
        "contains seven songs; four are from the game, while the remaining three are remixes, including a version of "
        "\"His World\" performed by Crush 40. Original Soundtrack includes all 93 tracks featured in Sonic the "
        "Hedgehog, spanning three discs."
        )
    print(summarise_long_text(temp))
