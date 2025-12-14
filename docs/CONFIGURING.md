# CONFIGURING.md: How to set up the app_config.json file

Note that ALL TOP-LEVEL ITEMS (e.g. 'app', 'logging', etc) are REQUIRED.

```json
{
    "app": {
        "name": "Blink's Block Blitz",      # REQUIRED: Game Name
        "screen_width": 800,                # REQUIRED: Screen Width
        "screen_height": 600,               # REQUIRED: Screen Height
        "fps": 60                           # REQUIRED: Framerate Cap
    },
    "logging":{
        "level": "INFO",                    # REQUIRED: Logging Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                                            #           Log entries labeled below this level will be ignored.
        "file": "blink-block-blitz.log"     # OPTIONAL: Log file name.  You can leave this off and log entries will
                                            #           be written only to the console, or you can provide a filename.
    }
}
```