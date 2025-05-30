import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import display
from esphome.const import (
    CONF_HEIGHT,
    CONF_ID,
    CONF_LAMBDA,
    CONF_UPDATE_INTERVAL,
    CONF_WIDTH,
)

DEPENDENCIES = ["esp32"]

MATRIX_ID = "matrix_id"
CHAIN_LENGTH = "chain_length"
BRIGHTNESS = "brightness"

R1_PIN = "R1_pin"
G1_PIN = "G1_pin"
B1_PIN = "B1_pin"
R2_PIN = "R2_pin"
G2_PIN = "G2_pin"
B2_PIN = "B2_pin"

A_PIN = "A_pin"
B_PIN = "B_pin"
C_PIN = "C_pin"
D_PIN = "D_pin"
E_PIN = "E_pin"

LAT_PIN = "LAT_pin"
OE_PIN = "OE_pin"
CLK_PIN = "CLK_pin"

DRIVER = "driver"
I2SSPEED = "i2sspeed"
LATCH_BLANKING = "latch_blanking"
CLOCK_PHASE = "clock_phase"

USE_CUSTOM_LIBRARY = "use_custom_library"

VIRTUAL_DISPLAY = "virtual_display"
SCAN_TYPE = "scan_type"
CHAIN_TYPE = "chain_type"
COLUMNS = "columns"
ROWS = "rows"

matrix_display_ns = cg.esphome_ns.namespace("matrix_display")
MatrixDisplay = matrix_display_ns.class_(
    "MatrixDisplay", cg.PollingComponent, display.DisplayBuffer
)
VirtualMatrixDisplay = matrix_display_ns.class_("VirtualMatrixDisplay", MatrixDisplay)

shift_driver = cg.global_ns.namespace("HUB75_I2S_CFG").enum("shift_driver")
DRIVERS = {
    "SHIFTREG": shift_driver.SHIFTREG,
    "FM6124": shift_driver.FM6124,
    "FM6126A": shift_driver.FM6126A,
    "ICN2038S": shift_driver.ICN2038S,
    "MBI5124": shift_driver.MBI5124,
    "SM5266": shift_driver.SM5266P,
    "DP3246_SM5368": shift_driver.DP3246_SM5368,
}

clk_speed = cg.global_ns.namespace("HUB75_I2S_CFG").enum("clk_speed")
CLOCK_SPEEDS = {
    "HZ_8M": clk_speed.HZ_8M,
    "HZ_10M": clk_speed.HZ_10M,
    "HZ_15M": clk_speed.HZ_15M,
    "HZ_16M": clk_speed.HZ_16M,
    "HZ_20M": clk_speed.HZ_20M,
}

# FIXME: Avoid polluting global namespace
scan_type = cg.global_ns.enum("PANEL_SCAN_TYPE")
SCAN_TYPES = {
    "STANDARD_TWO_SCAN": scan_type.STANDARD_TWO_SCAN,
    "FOUR_SCAN_16PX_HIGH": scan_type.FOUR_SCAN_16PX_HIGH,
    "FOUR_SCAN_32PX_HIGH": scan_type.FOUR_SCAN_32PX_HIGH,
    "FOUR_SCAN_40PX_HIGH": scan_type.FOUR_SCAN_40PX_HIGH,
    "FOUR_SCAN_40_80PX_HFARCAN": scan_type.FOUR_SCAN_40_80PX_HFARCAN,
    "FOUR_SCAN_64PX_HIGH": scan_type.FOUR_SCAN_64PX_HIGH,
}

# FIXME: Avoid polluting global namespace
panel_chain_type = cg.global_ns.enum("PANEL_CHAIN_TYPE")
CHAIN_TYPES = {
    "CHAIN_NONE": panel_chain_type.CHAIN_NONE,
    "CHAIN_TOP_LEFT_DOWN": panel_chain_type.CHAIN_TOP_LEFT_DOWN,
    "CHAIN_TOP_RIGHT_DOWN": panel_chain_type.CHAIN_TOP_RIGHT_DOWN,
    "CHAIN_BOTTOM_LEFT_UP": panel_chain_type.CHAIN_BOTTOM_LEFT_UP,
    "CHAIN_BOTTOM_RIGHT_UP": panel_chain_type.CHAIN_BOTTOM_RIGHT_UP,
    "CHAIN_TOP_LEFT_DOWN_ZZ": panel_chain_type.CHAIN_TOP_LEFT_DOWN_ZZ,
    "CHAIN_TOP_RIGHT_DOWN_ZZ": panel_chain_type.CHAIN_TOP_RIGHT_DOWN_ZZ,
    "CHAIN_BOTTOM_RIGHT_UP_ZZ": panel_chain_type.CHAIN_BOTTOM_RIGHT_UP_ZZ,
    "CHAIN_BOTTOM_LEFT_UP_ZZ": panel_chain_type.CHAIN_BOTTOM_LEFT_UP_ZZ,
}

VD_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_WIDTH): cv.positive_int,
        cv.Required(CONF_HEIGHT): cv.positive_int,
        cv.Optional(ROWS, default=1): cv.positive_int,
        cv.Optional(COLUMNS, default=1): cv.positive_int,
        cv.Optional(SCAN_TYPE, default="STANDARD_TWO_SCAN"): cv.enum(
            SCAN_TYPES, upper=True, space="_"
        ),
        cv.Optional(CHAIN_TYPE, default="CHAIN_NONE"): cv.enum(
            CHAIN_TYPES, upper=True, space="_"
        ),
    }
)
CONFIG_SCHEMA = display.FULL_DISPLAY_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(VirtualMatrixDisplay),
        cv.Required(CONF_WIDTH): cv.positive_int,
        cv.Required(CONF_HEIGHT): cv.positive_int,
        cv.Optional(USE_CUSTOM_LIBRARY, default=False): cv.boolean,
        cv.Optional(CHAIN_LENGTH, default=1): cv.positive_int,
        cv.Optional(BRIGHTNESS, default=128): cv.int_range(min=0, max=255),
        cv.Optional(
            CONF_UPDATE_INTERVAL, default="16ms"
        ): cv.positive_time_period_milliseconds,
        cv.Optional(R1_PIN, default=25): pins.gpio_output_pin_schema,
        cv.Optional(G1_PIN, default=26): pins.gpio_output_pin_schema,
        cv.Optional(B1_PIN, default=27): pins.gpio_output_pin_schema,
        cv.Optional(R2_PIN, default=14): pins.gpio_output_pin_schema,
        cv.Optional(G2_PIN, default=12): pins.gpio_output_pin_schema,
        cv.Optional(B2_PIN, default=13): pins.gpio_output_pin_schema,
        cv.Optional(A_PIN, default=23): pins.gpio_output_pin_schema,
        cv.Optional(B_PIN, default=19): pins.gpio_output_pin_schema,
        cv.Optional(C_PIN, default=5): pins.gpio_output_pin_schema,
        cv.Optional(D_PIN, default=17): pins.gpio_output_pin_schema,
        cv.Optional(E_PIN): pins.gpio_output_pin_schema,
        cv.Optional(LAT_PIN, default=4): pins.gpio_output_pin_schema,
        cv.Optional(OE_PIN, default=15): pins.gpio_output_pin_schema,
        cv.Optional(CLK_PIN, default=16): pins.gpio_output_pin_schema,
        cv.Optional(DRIVER): cv.enum(DRIVERS, upper=True, space="_"),
        cv.Optional(I2SSPEED): cv.enum(CLOCK_SPEEDS, upper=True, space="_"),
        cv.Optional(LATCH_BLANKING): cv.positive_int,
        cv.Optional(CLOCK_PHASE): cv.boolean,
        cv.Optional(VIRTUAL_DISPLAY): VD_SCHEMA,
    }
)


async def to_code(config: dict):
    if not config[USE_CUSTOM_LIBRARY]:
        cg.add_library("SPI", None)
        cg.add_library("Wire", None)
        cg.add_library("Adafruit BusIO", None)
        cg.add_library("adafruit/Adafruit GFX Library", None)
        cg.add_library(
            "https://github.com/diferhe/ESP32-HUB75-MatrixPanel-DMA#optional_logging",
            None,
        )
    if vd_config := config.get(VIRTUAL_DISPLAY):
        template_args = (vd_config.get(a) for a in (CHAIN_TYPE, SCAN_TYPE))
        args = (vd_config.get(a) for a in (ROWS, COLUMNS, CONF_WIDTH, CONF_HEIGHT))
    else:
        template_args = ()
        args = (1, 1, config[CONF_WIDTH], config[CONF_HEIGHT])
    var = cg.new_Pvariable(config[CONF_ID], cg.TemplateArguments(*template_args), *args)
    cg.add(var.set_panel_width(config[CONF_WIDTH]))
    cg.add(var.set_panel_height(config[CONF_HEIGHT]))
    cg.add(var.set_chain_length(config[CHAIN_LENGTH]))
    cg.add(var.set_initial_brightness(config[BRIGHTNESS]))

    R1_pin = await cg.gpio_pin_expression(config[R1_PIN])
    G1_pin = await cg.gpio_pin_expression(config[G1_PIN])
    B1_pin = await cg.gpio_pin_expression(config[B1_PIN])
    R2_pin = await cg.gpio_pin_expression(config[R2_PIN])
    G2_pin = await cg.gpio_pin_expression(config[G2_PIN])
    B2_pin = await cg.gpio_pin_expression(config[B2_PIN])

    A_pin = await cg.gpio_pin_expression(config[A_PIN])
    B_pin = await cg.gpio_pin_expression(config[B_PIN])
    C_pin = await cg.gpio_pin_expression(config[C_PIN])
    D_pin = await cg.gpio_pin_expression(config[D_PIN])

    LAT_pin = await cg.gpio_pin_expression(config[LAT_PIN])
    OE_pin = await cg.gpio_pin_expression(config[OE_PIN])
    CLK_pin = await cg.gpio_pin_expression(config[CLK_PIN])

    if E_PIN in config:
        E_pin = await cg.gpio_pin_expression(config[E_PIN])
    else:
        E_pin = 0

    cg.add(
        var.set_pins(
            R1_pin,
            G1_pin,
            B1_pin,
            R2_pin,
            G2_pin,
            B2_pin,
            A_pin,
            B_pin,
            C_pin,
            D_pin,
            E_pin,
            LAT_pin,
            OE_pin,
            CLK_pin,
        )
    )

    if DRIVER in config:
        cg.add(var.set_driver(config[DRIVER]))

    if I2SSPEED in config:
        cg.add(var.set_i2sspeed(config[I2SSPEED]))

    if LATCH_BLANKING in config:
        cg.add(var.set_latch_blanking(config[LATCH_BLANKING]))

    if CLOCK_PHASE in config:
        cg.add(var.set_clock_phase(config[CLOCK_PHASE]))

    await display.register_display(var, config)

    if CONF_LAMBDA in config:
        lambda_ = await cg.process_lambda(
            config[CONF_LAMBDA], [(display.DisplayRef, "it")], return_type=cg.void
        )
        cg.add(var.set_writer(lambda_))
