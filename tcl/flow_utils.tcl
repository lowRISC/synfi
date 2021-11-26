# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

proc set_flow_var {var_name var_default var_friendly_name} {
  global lr_convert_flow_var_quiet

  set var_name "lr_convert_${var_name}"
  global $var_name
  set env_var_name [string toupper $var_name]

  if { [info exists ::env($env_var_name)] } {
    set $var_name $::env($env_var_name)
    puts "$var_friendly_name: $::env($env_var_name)"
  } else {
    set $var_name $var_default
    puts "$var_friendly_name: $var_default (default)"
  }
}