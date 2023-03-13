# Prereqs
## Running as root
The library requires to access hardware registers to control the LED matrix, and create accurate timings. These hardware accesses require to run as root user.

For security reasons, it is usually not a good idea to run an application as root entirely, so this library makes sure to drop privileges immediately after the hardware is initialized.

You can switch off the privilege dropping with the [`--led-no-drop-privs`](https://github.com/hzeller/rpi-rgb-led-matrix#user-content-no-drop-priv) flag, or, if you do this programmatically, choose the configuration in the [`RuntimeOptions struct`](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/include/led-matrix.h#L401).

Note, you _could_ run as non-root, which will use `/dev/gpiomem` to at least write to GPIO, however the precise timing hardware registers are not accessible. This will result in flicker and color degradation. Starting as non-root is not recommended.

> Source: https://github.com/hzeller/rpi-rgb-led-matrix#running-as-root

# How the API Works
https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/examples-api-use

# Performance Tips and Limits
Regardless of which driving hardware you use, ultimately you can only push pixels so fast to a string of panels before you get flickering due to too low a refresh rate (less than 80-100Hz), or before you refresh the panel lines too fast and they appear too dim because each line is not displayed long enough before it is turned off.

Basic performance tips:

-   Use --led-show-refresh to see the refresh rate while you try parameters
-   use an active-3 board with led-parallel=3
-   led-pwm-dither-bits=1 gives you a speed boost but less brightness
-   led-pwm-lsb-nanoseconds=50 also gives you a speed boost but less brightness
-   led-pwm-bits=7 or even lower decrease color depth but increases refresh speed
-   AB panels and other panels with that use values of led-multiplexing bigger than 0, will also go faster, although as you tune more options given above, their advantage will decrease.
-   32x16 ABC panels are faster than ABCD which are faster than ABCDE, which are faster than 128x64 ABC panels (which do use 5 address lines, but over only 3 wires)
-   Use at least an rPi3 (rPi4 is still slightly faster but may need --led-slowdown-gpio=2)
> Source: https://github.com/hzeller/rpi-rgb-led-matrix#performance-improvements-and-limits
# More settings to review
```
--led-pwm-bits=<1..11>    : PWM bits (Default: 11).
```

The LEDs can only be switched on or off, so the shaded brightness perception is achieved via PWM (Pulse Width Modulation). In order to get a good 8 Bit per color resolution (24Bit RGB), the 11 bits default per color are good (why ? Because our eyes are actually perceiving brightness logarithmically, so we need a lot more physical resolution to get 24Bit sRGB).

With this flag, you can change how many bits it should use for this; lowering it means the lower bits (=more subtle color nuances) are omitted. Typically you might be mostly interested in the extremes: 1 Bit for situations that only require 8 colors (e.g. for high contrast text displays) or 11 Bit for everything else (e.g. showing images or videos). Why would you bother at all ? Lower number of bits use slightly less CPU and result in a higher refresh rate.

```
--led-show-refresh        : Show refresh rate.
```

This shows the current refresh rate of the LED panel, the time to refresh a full picture. Typically, you want this number to be pretty high, because the human eye is pretty sensitive to flicker. Depending on the settings, the refresh rate with this library are typically in the hundreds of Hertz but can drop low with very long chains. Humans have different levels of perceiving flicker - some are fine with 100Hz refresh, others need 250Hz. So if you are curious, this gives you the number (shown on the terminal).

The refresh rate depends on a lot of factors, from `--led-rows` and `--led-chain` to `--led-pwm-bits`, `--led-pwm-lsb-nanoseconds` and `--led-pwm-dither-bits`. If you are tweaking these parameters, showing the refresh rate can be a useful tool.

```
--led-limit-refresh=<Hz>  : Limit refresh rate to this frequency in Hz. Useful to keep a
                            constant refresh rate on loaded system. 0=no limit. Default: 0
```

This allows to limit the refresh rate to a particular frequency to approach a fixed refresh rate.

This can be used to mitigate some situations in which you have a faint flicker, which can happen due to hardware events (network access) or other situations such as other IO or heavy memory access by other processes. Also when you see wildly changing refresh frequencies with `--led-show-refresh`.

You trade a slightly slower refresh rate and display brightness for less visible flicker situations.

For this to calibrate, run your program for a while with --led-show-refresh and watch the line that shows the current refresh rate and minimum refresh rate observed. So wait a while until that value doesn't change anymore (e.g. a minute, so that you catch tasks that happen once a minute, such as ntp updated). Use this as a guidance what value to choose with `--led-limit-refresh`.

The refresh rate will now be adapted to always reach this value between frames, so faster refreshes will be slowed down, but the occasional delayed frame will fit into the time-window as well, thus reducing visible brightness fluctuations.

You can play with value a little and reduce until you find a good balance between refresh rate and flicker suppression.

Use this also if you want to have a stable baseline refresh rate when using the vsync-multiple flag `-V` in the [led-image-viewer](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/utils#image-viewer) or [video-viewer](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/utils#video-viewer) utility programs.

```
--led-scan-mode=<0..1>    : 0 = progressive; 1 = interlaced (Default: 0).
```

This switches from progressive scan and interlaced scan. The latter might look be a little nicer when you have a very low refresh rate, but typically it is more annoying because of the comb-effect (remember 80ies TV ?).

```
--led-pwm-lsb-nanoseconds : PWM Nanoseconds for LSB (Default: 130)
```

This allows to change the base time-unit for the on-time in the lowest significant bit in nanoseconds. Lower values will allow higher frame-rate, but will also negatively impact qualty in some panels (less accurate color or more ghosting).

Good values for full-color display (PWM=11) are somewhere between 100 and 300.

If you you use reduced bit color (e.g. PWM=1) and have sharp contrast applications, then higher values might be good to minimize ghosting.

How to decide ? Just leave the default if things are fine. But some panels have trouble with sharp contrasts and short pulses that results in ghosting. It is particularly apparent in situations such as bright text on black background. In these cases increase the value until you don't see this ghosting anymore.

The following example shows how this might look like:

Ghosting with low --led-pwm-lsb-nanoseconds

No ghosting after tweaking

[![](https://github.com/hzeller/rpi-rgb-led-matrix/raw/master/img/text-ghosting.jpg)](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/img/text-ghosting.jpg)

[![](https://github.com/hzeller/rpi-rgb-led-matrix/raw/master/img/text-no-ghosting.jpg)](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/img/text-no-ghosting.jpg)

If you tweak this value, watch the framerate (`--led-show-refresh`) while playing with this number.

```
--led-pwm-dither-bits   : Time dithering of lower bits (Default: 0)
```

The lower bits can be time dithered, i.e. their brightness contribution is achieved by only showing them some frames (this is possible, because the PWM is implemented as binary code modulation). This will allow higher refresh rate (or same refresh rate with increased `--led-pwm-lsb-nanoseconds`). The disadvantage could be slightly lower brightness, in particular for longer chains, and higher CPU use. CPU use is not of concern for Rasbperry Pi 2 or 3 (as we run on a dedicated core anyway) but proably for Raspberry Pi 1 or Pi Zero. Default: no dithering; if you have a Pi 3 and struggle with low frame-rate due to high multiplexing panels (1:16 or 1:32) or long chains, it might be worthwhile to try.

```
--led-no-hardware-pulse   : Don't use hardware pin-pulse generation.
```

This library uses a hardware subsystem that also is used by the sound. You can't use them together. If your panel does not work, this might be a good start to debug if it has something to do with the sound subsystem (see Troubleshooting section). This is really only recommended for debugging; typically you actually want the hardware pulses as it results in a much more stable picture.

```
--led-no-drop-privs       : Don't drop privileges from 'root' after initializing the hardware.
```

You need to start programs as root as it needs to access some low-level hardware at initialization time. After that, it is typically not desirable to stay in this role, so the library then drops the privileges.

This flag allows to switch off this behavior, so that you stay root. Not recommended unless you have a specific reason for it (e.g. you need root to access other hardware or you do the privilege dropping yourself).

```
--led-daemon              : Make the process run in the background as daemon.
```

If this is set, the program puts itself into the background (running as 'daemon'). You might want this if started from an init script at boot-time.