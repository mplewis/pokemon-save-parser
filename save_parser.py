import string
import json

MOVES_DATA = 'data/gen1/pkmn_moves.json'
INDEXES_DATA = 'data/gen1/pkmn_indexes.json'

PKMN_LENGTH = 44
PKMN_OFFSET = 0x08
TRAINER_LENGTH = 11
TRAINER_OFFSET = 0x110
NICKNAME_LENGTH = 11
NICKNAME_OFFSET = 0x152


def char_map_store(char_map, offset, symbols):
    """
    Store one or more characters in a charmap (dict) starting at the given
    offset.
    """
    for symbol in symbols:
        char_map[offset] = symbol
        offset += 1


def read_bytes(source, offset, length):
    """Read <length> bytes from <source> starting at <offset>."""
    return source[offset:offset+length]


def to_ascii(bytes, char_map):
    """
    Translate a sequence of bytes into a pseudo-ASCII string using the given
    charmap.
    """
    return ''.join([char_map[b] for b in bytes])


def term(ascii_array):
    """Chop off the end of a terminated array."""
    return ascii_array.split('#')[0]


def bytes_to_int(bytes):
    """Convert multiple bytes to an integer."""
    num = len(bytes)
    val = 0
    for pos, byte in enumerate(bytes):
        val += byte << ((num - pos - 1) * 8)
    return val


def money(save_data):
    """Return the amount of money the trainer has."""
    curr_pos = 5
    money = 0
    for b in read_bytes(save_data, 0x25F3, 3):
        money += int(ord(b) >> 4) * 10 ** curr_pos
        curr_pos -= 1
        money += int(ord(b) & 0x0F) * 10 ** curr_pos
        curr_pos -= 1
    return money


pkmn_char_map = {}

char_map_store(pkmn_char_map, 0x50, '#')
char_map_store(pkmn_char_map, 0x7F, ' ')
char_map_store(pkmn_char_map, 0x80, string.uppercase + '():;[]')
char_map_store(pkmn_char_map, 0xA0, string.lowercase)
char_map_store(pkmn_char_map, 0xE1, '{}-')
char_map_store(pkmn_char_map, 0xE6, '?!.')
char_map_store(pkmn_char_map, 0xF1, '*')
char_map_store(pkmn_char_map, 0xF3, '/,')
char_map_store(pkmn_char_map, 0xF6, string.digits)

with open(MOVES_DATA, 'r') as f:
    pkmn_move_map = json.load(f)

with open(INDEXES_DATA, 'r') as f:
    pkmn_index_map = json.load(f)


class PokemonGen1:
    def __init__(self, pkmn_data):
        self.index = pkmn_data[0]
        self.species = pkmn_index_map[self.index]
        self.hp_curr = bytes_to_int(pkmn_data[1:3])
        self.hp_max = bytes_to_int(pkmn_data[0x22:0x24])
        self.moves = pkmn_data[0x08:0x0C]
        self.move_names = [pkmn_move_map[move] for move in self.moves]
        self.move_pp = pkmn_data[0x1D:0x21]
        self.type_1 = pkmn_data[0x05]
        self.type_2 = pkmn_data[0x06]
        self.trainer_id = bytes_to_int(pkmn_data[0x0C:0x0E])
        self.level = pkmn_data[0x21]
        self.exp = bytes_to_int(pkmn_data[0x0E:0x11])
        self.ev_hp = bytes_to_int(pkmn_data[0x11:0x13])
        self.ev_attack = bytes_to_int(pkmn_data[0x13:0x15])
        self.ev_defense = bytes_to_int(pkmn_data[0x15:0x17])
        self.ev_speed = bytes_to_int(pkmn_data[0x17:0x19])
        self.ev_special = bytes_to_int(pkmn_data[0x19:0x1B])
        self.attack = bytes_to_int(pkmn_data[0x24:0x26])
        self.defense = bytes_to_int(pkmn_data[0x26:0x28])
        self.speed = bytes_to_int(pkmn_data[0x28:0x2A])
        self.special = bytes_to_int(pkmn_data[0x2A:0x2C])
        self.trainer_name = None
        self.nickname = None


class SaveDataGen1:
    def __init__(self, save_data):
        self.money = money(save_data)

        raw_trainer_name = [ord(b) for b in read_bytes(save_data, 0x2598, 8)]
        self.trainer_name = term(to_ascii(raw_trainer_name, pkmn_char_map))

        raw_trainer_id = [ord(b) for b in read_bytes(save_data, 0x2605, 2)]
        self.trainer_id = bytes_to_int(raw_trainer_id)

        raw_rival_name = [ord(b) for b in read_bytes(save_data, 0x25F6, 8)]
        self.rival_name = term(to_ascii(raw_rival_name, pkmn_char_map))

        self.num_party = ord(save_data[0x2F2C])

        pkmn_data = [ord(b) for b in read_bytes(save_data, 0x2F2C, 404)]
        self.party = []
        for num in xrange(self.num_party):
            pkmn_start = num * PKMN_LENGTH + PKMN_OFFSET
            pkmn_end_inc = pkmn_start + PKMN_LENGTH
            trainer_start = num * TRAINER_LENGTH + TRAINER_OFFSET
            trainer_end_inc = trainer_start + TRAINER_LENGTH
            nickname_start = num * NICKNAME_LENGTH + NICKNAME_OFFSET
            nickname_end_inc = nickname_start + NICKNAME_LENGTH

            one_pkmn_data_raw = pkmn_data[pkmn_start:pkmn_end_inc]
            trainer_data_raw = pkmn_data[trainer_start:trainer_end_inc]
            nickname_data_raw = pkmn_data[nickname_start:nickname_end_inc]

            one_pkmn_data = PokemonGen1(one_pkmn_data_raw)
            one_pkmn_data.trainer_name = term(to_ascii(trainer_data_raw,
                                                       pkmn_char_map))
            one_pkmn_data.nickname = term(to_ascii(nickname_data_raw,
                                                   pkmn_char_map))
            self.party.append(one_pkmn_data)
