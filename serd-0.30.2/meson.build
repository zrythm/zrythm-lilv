# Copyright (C) 2019 Alexandros Theodotou <alex at zrythm dot org>
#
# This file is part of Zrythm
#
# Zrythm is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zrythm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Zrythm.  If not, see <https://www.gnu.org/licenses/>.

subdir('src')

serd_cdata = configuration_data ()
serd_check_headers = [
  'stdlib.h',
  'fcntl.h',
  'stdio.h',
  ]
foreach h : serd_check_headers
  if cc.has_header(h)
    serd_cdata.set('HAVE_' + h.underscorify().to_upper(), 1)
  endif
endforeach
serd_cdata.set_quoted('SERD_VERSION', '0.30.2')
serd_config_h = configure_file (
  output: 'serd_config.h',
  configuration: serd_cdata,
  )
serd_config_h_dep = declare_dependency (
  sources: serd_config_h,
  )

serd = static_library (
  'serd',
  sources: serd_src,
  dependencies: [
    serd_config_h_dep,
    ],
  include_directories: 'serd',
  install: false,
)

serd_dep = declare_dependency (
  include_directories: '.',
  link_with: serd)
