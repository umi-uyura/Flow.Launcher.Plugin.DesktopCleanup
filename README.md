Desktop Cleanup (Flow.Launcher.Plugin.DesktopCleanup)
====================================================

Plugin for cleaning files and folders on your desktop for [Flow Launcher](https://flow-launcher.github.io/).

![](doc/example.gif)

Install
-------

```
pm install desktop cleanup
```

Usage
-----

| Keyword | Description |
|---------|-------------|
| `dc clean` | Remove all files and folders on the desktop |
| `dc trash` | Move all files and folders on the desktop to the trash |
| `dc sweep` | Move all files and folders on the desktop to a folder created on the desktop |
| `dc store` | Move all files and folders on the desktop to the specified folder |


Cautions

**This plugin also cleans the desktops of `Public` user（i.e. `All Users` ）.**


Configutation
-------------

.env

```
sweap_folder_name=!dcclean!  # folder name for `dc sweap`
store_folder_path=%USERPROFILE%\Documents\!dcclean!  # path for `dc store`
```

- - -

This plugin was created based on [Flow-Launcher/Flow.Launcher.Plugin.PythonTemplate](https://github.com/Flow-Launcher/Flow.Launcher.Plugin.PythonTemplate).
