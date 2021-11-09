from esphome.components import switch
import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.const import CONF_ID
from .. import mi_ns, CONF_MI_ID, Mi

DEPENDENCIES = ["mi"]
CODEOWNERS = ["@hencou"]

REMOTE_TYPES = {
    "rgb_cct" : "rgb_cct",
    "cct" : "cct",
    "rgb" : "rgb",
    "rgbw" : "rgbw",
    "fut089" : "fut089",
    "fut091" : "fut091",
    "fut020" : "fut020",
}

COMMANDS = {
    "unpair" : "unpair",
    "pair" : "pair",
    "set_white" : "set_white",
    "night_mode" : "night_mode",
    "level_up" : "level_up",
    "level_down" : "level_down",
    "temperature_up" : "temperature_up",
    "temperature_down" : "temperature_down",
    "next_mode" : "next_mode",
    "previous_mode" : "previous_mode",
    "mode_speed_down" : "mode_speed_down",
    "mode_speed_up" : "mode_speed_up",
    "toggle" : "toggle",
}

CODEOWNERS = ["@hencou"]
CONF_DEVICEID = "device_id"
CONF_GROUPID = "group_id"
CONF_REMOTETYPE = "remote_type"
CONF_COMMAND = "command"

MiSwitch = mi_ns.class_("MiSwitch", switch.Switch, cg.Component)

CONFIG_SCHEMA = switch.SWITCH_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MiSwitch),
        cv.GenerateID(CONF_MI_ID): cv.use_id(Mi),
        cv.Required(CONF_DEVICEID, "device_id"): cv.uint16_t,
        cv.Required(CONF_GROUPID, "group_id"): cv.uint8_t,
        cv.Required(CONF_REMOTETYPE, "remote_type"): cv.enum(REMOTE_TYPES),
        cv.Required(CONF_COMMAND, "command"): cv.enum(COMMANDS),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await switch.register_switch(var, config)

    paren = await cg.get_variable(config[CONF_MI_ID])
    cg.add(var.set_mi_parent(paren))
    
    cg.add(var.set_switch(config[CONF_DEVICEID], config[CONF_GROUPID], config[CONF_REMOTETYPE], config[CONF_COMMAND]))