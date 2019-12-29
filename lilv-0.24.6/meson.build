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

lilv_cdata = configuration_data ()
if pcre_dep.found()
  lilv_cdata.set('HAVE_PCRE', 1)
endif
lilv_check_headers = [
  'stdlib.h',
  'fcntl.h',
  'stdio.h',
  ]
foreach h : lilv_check_headers
  if cc.has_header(h)
    lilv_cdata.set('HAVE_' + h.underscorify().to_upper(), 1)
  endif
endforeach
lilv_cdata.set_quoted('LILV_VERSION', '0.24.6')
if cc.has_function('lstat')
  lilv_cdata.set('HAVE_LSTAT', 1)
endif
if cc.has_function('flock')
  lilv_cdata.set('HAVE_FLOCK', 1)
endif
if cc.has_function('fileno')
  lilv_cdata.set('HAVE_FILENO', 1)
endif
if cc.has_function('clock_gettime')
  lilv_cdata.set('HAVE_CLOCK_GETTIME', 1)
endif
dl_dep = dependency('dl', required: false)
if dl_dep.found()
  lilv_cdata.set('HAVE_LIBDL', 1)
endif
lilv_cdata.set_quoted('LILV_PATH_SEP', ':')
lilv_cdata.set_quoted('LILV_DIR_SEP', '/')
lilv_cdata.set_quoted('LILV_DEFAULT_LV2_PATH', '~/.lv2:/usr/@0@/lv2:/usr/local/@0@/lv2'.format(get_option('libdir')))
lilv_config_h = configure_file (
  output: 'lilv_config.h',
  configuration: lilv_cdata,
  )
lilv_config_h_dep = declare_dependency (
  sources: lilv_config_h,
  )

lilv = static_library (
  'lilv',
  sources: lilv_src,
  dependencies: [
    lilv_config_h_dep,
    lv2_dep,
    serd_dep,
    sord_dep,
    sratom_dep,
    ],
  include_directories: 'src',
  install: false,
)

lilv_dep = declare_dependency (
  include_directories: '.',
  link_with: lilv)
