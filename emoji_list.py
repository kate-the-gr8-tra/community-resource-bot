import emoji

class EmojiList:
    def __init__(self):
        emoji_list = []
        for descript, emji in emoji.EMOJI_DATA.items():
            unicode_form = ''.join(f'\\U{ord(char):08X}' for char in emji)
            emoji_list.append((descript, emji, unicode_form))
        
        self.__emoji_list = emoji_list

    def get(self, emoji: str):
        for item in self.emoji_list:
            if item[1] == emoji:
                return item[2]