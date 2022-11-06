/** \file
 *
 *  Header file for Commands.c.
 */

#pragma once

#include "Joystick.h"

typedef struct {
	Buttons_t button;
	uint16_t duration;
} Command; 

bool GetNextReportFromCommands(const Command* const commands, int step_size, USB_JoystickReport_Input_t* const ReportData);

// The commands that run independently from a PC
// Store arrays in Flash memory to save a SRAM data capacity

// controller sync (use for ease of debugging)
extern const Command sync[];
extern const int sync_size;

// controller unsync
extern const Command unsync[];
extern const int unsync_size;

// Mash A Button
extern const Command mash_a_commands[];
extern const int mash_a_size;

// Mash X Button (for debug)
extern const Command mash_x_commands[];
extern const int mash_x_size;

// Mash HOME Button (for debug)
extern const Command mash_home_commands[];
extern const int mash_home_size;

// Auto League
extern const Command auto_league_commands[];
extern const int auto_league_size;

// Infinity Watt
extern const Command inf_watt_commands[];
extern const int inf_watt_size;

// Pick Up Berry
extern const Command pickupberry_commands[];
extern const int pickupberry_size;

//Change the Year
extern const Command changetheyear_commands[];
extern const int changetheyear_size;
