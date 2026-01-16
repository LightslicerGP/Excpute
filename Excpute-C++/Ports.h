#ifndef PORTS_H
#define PORTS_H

void Port_hardware(SDL_Event event, int scale);
int port_read(int id, bool signed_value = true);
void port_write(int id, int new_data, bool signed_value = true);

extern std::array<int, 256> Port;

#endif