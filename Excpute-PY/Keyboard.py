import Port
import pygame

key_bitmasks = {
    pygame.K_SPACE: [0, 0b10000000],
    pygame.K_BACKQUOTE: [0, 0b01000000],
    pygame.K_1: [0, 0b00100000],
    pygame.K_2: [0, 0b00010000],
    pygame.K_3: [0, 0b00001000],
    pygame.K_4: [0, 0b00000100],
    pygame.K_5: [0, 0b00000010],
    pygame.K_6: [0, 0b00000001],
    pygame.K_7: [1, 0b10000000],
    pygame.K_8: [1, 0b01000000],
    pygame.K_9: [1, 0b00100000],
    pygame.K_0: [1, 0b00010000],
    pygame.K_MINUS: [1, 0b00001000],
    pygame.K_EQUALS: [1, 0b00000100],
    pygame.K_q: [1, 0b00000010],
    pygame.K_w: [1, 0b00000001],
    pygame.K_e: [2, 0b10000000],
    pygame.K_r: [2, 0b01000000],
    pygame.K_t: [2, 0b00100000],
    pygame.K_y: [2, 0b00010000],
    pygame.K_u: [2, 0b00001000],
    pygame.K_i: [2, 0b00000100],
    pygame.K_o: [2, 0b00000010],
    pygame.K_p: [2, 0b00000001],
    pygame.K_LEFTBRACKET: [2, 0b00000001],
    pygame.K_RIGHTBRACKET: [3, 0b10000000],
    pygame.K_BACKSLASH: [3, 0b00100000],
    pygame.K_a: [3, 0b00010000],
    pygame.K_s: [3, 0b00001000],
    pygame.K_d: [3, 0b00000100],
    pygame.K_f: [3, 0b00000010],
    pygame.K_g: [3, 0b00000001],
    pygame.K_h: [4, 0b10000000],
    pygame.K_j: [4, 0b01000000],
    pygame.K_k: [4, 0b00100000],
    pygame.K_l: [4, 0b00010000],
    pygame.K_SEMICOLON: [4, 0b00001000],
    pygame.K_QUOTE: [4, 0b00000100],
    pygame.K_z: [4, 0b00000010],
    pygame.K_x: [4, 0b00000001],
    pygame.K_c: [5, 0b10000000],
    pygame.K_v: [5, 0b01000000],
    pygame.K_b: [5, 0b00100000],
    pygame.K_n: [5, 0b00010000],
    pygame.K_m: [5, 0b00001000],
    pygame.K_COMMA: [5, 0b00000100],
    pygame.K_PERIOD: [5, 0b00000010],
    pygame.K_SLASH: [5, 0b00000001],
    pygame.K_BACKSPACE: [6, 0b10000000],
    pygame.K_TAB: [6, 0b01000000],
    pygame.K_RETURN: [6, 0b00100000],
    pygame.K_LSHIFT: [6, 0b00010000],  # Combined Shift
    pygame.K_RSHIFT: [6, 0b00010000],  # Combined Shift
    pygame.K_UP: [6, 0b00001000],
    pygame.K_LEFT: [6, 0b00000100],
    pygame.K_DOWN: [6, 0b00000010],
    pygame.K_RIGHT: [6, 0b00000001],
    pygame.K_CAPSLOCK: [7, 0b10000000],
    pygame.K_LCTRL: [7, 0b01000000],  # Combined Control
    pygame.K_RCTRL: [7, 0b01000000],  # Combined Control
    pygame.K_LALT: [7, 0b00100000],  # Combined Alt
    pygame.K_RALT: [7, 0b00100000],  # Combined Alt
    # pygame.K_0: [7, 0b00010000],  # FN key DOESNT EXIST SHIADHODSAHODSIUDSAOBDSBAOBUOBIUOBUSAOBUDSABUODSABIUDSAOBIUDSADSADSOBAIUSODBAUODBIUOAOBUIDOBUSAIBDSAOBIUBUDSABUOIDSAIUDSAOBIUDSABIDSOBIUDSAOBIUIUDSADSABDSUBDUOSDBIUSBIUOBIUAOBAIUUSABAUDSIOSBIUBUBUODSBAIUBIUUDBIAOBIUDSAUDuodsbiuodsbai
    pygame.K_ESCAPE: [7, 0b00010000],
    pygame.K_PRINTSCREEN: [7, 0b00001000],
    pygame.K_INSERT: [7, 0b00000100],
    pygame.K_DELETE: [7, 0b00000010],
    # one more spot for fun OIHHDSAUOIHOSBIUSBAHHOIOBIUSODHIDSOIUDSADAHOBIUDSA 11/12/24
}


def handle_keyboard_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key in key_bitmasks:
            index, bitmask = key_bitmasks[event.key]
            Port.Ports[index] ^= bitmask  # Use the index and bitmask
    elif event.type == pygame.KEYUP:
        if event.key in key_bitmasks:
            index, bitmask = key_bitmasks[event.key]
            Port.Ports[index] &= ~bitmask  # Use the index and bitmask
