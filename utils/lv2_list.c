/* lv2_list - List system installed LV2 plugins.
 * Copyright (C) 2007 Dave Robillard <drobilla.net>
 *  
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#include <stdio.h>
#include <slv2/slv2.h>


void
list_plugins(SLV2List list)
{
	for (size_t i=0; i < slv2_list_get_length(list); ++i) {
		const SLV2Plugin* const p = slv2_list_get_plugin_by_index(list, i);
		printf("%s\n", slv2_plugin_get_uri(p));
	}
}


int
main()//int argc, char** argv)
{
	SLV2List plugins = slv2_list_new();
	slv2_list_load_all(plugins);

	list_plugins(plugins);
	
	return 0;
}
