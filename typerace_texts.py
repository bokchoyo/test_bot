import random


texts = [
    "Toys that talk back are one of the hottest holiday gifts this year. Hackers may soon be going after these toys too, to steal information from children. People who study internet security discovered that the system behind Hello Barbie is not secure. Hello Barbie is a talking doll that works by connecting to the internet. The researchers reviewed the toy to see if it was safe for kids and they said that it was not safe when it connected to the internet. Sending information online made it easy for hackers to get personal information about kids from the toy. One of the researchers said that any toy that connects to the internet could let other people listen to children or get their information.",
    "The third thing you want to include on your family tree website is a little bit of information about each family member. This kind of detailed information helps make your family tree website more than just a static page of dates and names. It makes it an interesting gathering place for people who could possibly be your kinfolk. Fourth on your list of must-have ingredients for a family tree website is information you're still seeking. Broadcasting it on a family tree website can help others know what they need to do to pitch in.",
    "Life is not fair. That is something that children seem to understand at a young age. However, how children develop a sense of what is fair and what is unfair, and how they act on that sense, has been a puzzle for scientists. A team of scientists recently traveled to seven countries to study how children understand fairness. They wanted to know how much of a child's sense of what is fair is natural and how much is learned. To do this, the scientists created an experiment to study how children responded to two types of unfair situations.",
    "Other folktales feature clever tricksters who fool other characters. Fables, fairy tales, and nursery rhymes are common types of folk stories. A fable is a short folktale that teaches a lesson about how people should behave. It usually has animal characters that speak and act like people. Fairy tales tell about magical beings such as fairies, elves, dragons, and trolls. Nursery rhymes tell entertaining stories in short, clever poems. People have told such stories to children for centuries.",
    "Even if you don't understand the words, you can appreciate and capture the spirit of the beat. This is why music has the platform it does today, as well as the adoration and allure. Instruments play a major role in the art of music. In principle, any object that produces sound can be considered a musical instrument. Dating back over sixty thousand years, the flute is considered to be the oldest musical instrument. Today there are many instruments used to produce melodies and sound. This is due to the conversion of cultures that have influenced the design of instruments throughout history. So, what began on the shores of West Africa as a tree stump and a hand, is now known as drums throughout the world.",
    "You can either search about them online or can call the operations unit and ask your queries. If you do not have any skate parks in your hometown, make sure to check accommodation facilities beforehand. In addition to skateboard helmets and pads, you may also consider carrying an extra skate board in case one breaks. If you have not carried any protective gear along with you, you can ask the locals about the best skate shops around. The locals will also be able to help you with other attraction for skaters in the town.",
    "One summer night a man stood on a low hill overlooking a wide expanse of forest and field. By the full moon hanging low in the west he knew what he might not have known otherwise: that it was near the hour of dawn. A light mist lay along the earth, partly veiling the lower features of the landscape. Above it, the taller trees showed in well-defined masses against a clear sky. Two or three farmhouses were visible through the haze, but in none of them, naturally, was a light. Nowhere, was any sign or suggestion of life except the barking of a distant dog. It repeated with mechanical iteration and served rather to accentuate than dispel the loneliness of the scene."
]


def get_random_text():
    return texts[random.randint(0, len(texts) - 1)]


def get_random_sentence():
    text = get_random_text().split(".")
    return text[random.randint(0, len(text) - 2)].strip()


def get_two_sentences():
    result = []
    sentences = get_random_text().split(".")
    sentence_index = random.randint(0, len(sentences) - 3)

    for i in range(2):
        result.append(sentences[sentence_index] + ".")
        sentence_index += 1

    return ''.join(result).strip()
