#ifndef RAM_H
#define RAM_H

int ram_read(int id, bool signed_value = true);
void ram_write(int id, int new_data, bool signed_value = true);

#endif