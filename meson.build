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

project (
  'zrythm-lilv', ['c'],
  version: '0.24.6',
  license: 'ISC',
  meson_version: '>= 0.50.0',
  default_options: [
    'warning_level=1',
    'buildtype=debug',
    'c_std=gnu11',
    ],
  )

cc = meson.get_compiler ('c')
prefix = get_option ('prefix')
includedir = join_paths (
  prefix, get_option('includedir'))
libdir = join_paths (prefix, get_option ('libdir'))

cdata = configuration_data ()
cdata.set_quoted (
  'PACKAGE_VERSION',
  '@VCS_TAG@')
cdata.set_quoted (
  'COMPILER',
  meson.get_compiler('c').get_id())
cdata.set_quoted (
  'PREFIX', prefix)
cdata.set_quoted (
  'COMPILER_VERSION',
  meson.get_compiler('c').version())
cdata.set_quoted (
  'CONFIGURE_LIBDIR',
  libdir)

lv2_dep = dependency('lv2', version: '>=1.16.0')
pcre_dep = dependency('libpcre', required: false)

subdir('serd-0.30.2')
subdir('sord-0.16.4')
subdir('sratom-0.6.4')
subdir('lilv-0.24.6')
