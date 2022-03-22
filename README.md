# Blender-Exporter

![](https://i1.wp.com/paladinstudios.com/wp-content/uploads/2020/03/logo-1.png)

 * [Description](#description)
 * [Developing & Testing](#develop)
 * [Creating a release](#release)

<a name="description"/>

# Description

![image](https://user-images.githubusercontent.com/10919737/159481452-bf4e2765-9696-4b31-a93c-1f01a2f06c9a.png)

The Paladin Exporter assists with the workflow of exporting `.fbx` files. Collections can be defined to be exported, as well as the target path of where objects should be exported to. All configuration is saved within the `.blend` file.

<a name="develop"/>

# Developing & Testing
To test during development, the contents of folder `PaladinExporter` need to be copied over to the Blender `%AppData%\Blender Foundation\Blender\Vx.xx\scripts\addons\PaladinExporter` installation folder. Where `Vx.xx` should be the installed Blender version. The included `SendToBlender.bat` file does this for Blender v2.93 for ease of use.


After copying the files, make sure to reload the python scripts within Blender. Click the top left Blender icon -> System -> Reload Scripts.

![image](https://user-images.githubusercontent.com/10919737/159488403-c4d14dc8-03d4-4b18-974c-e52eb3a4f739.png)


Now the addon scripts should be in Blender and the add-on can be enabled in the preferences menu. Search for `Paladin` with the `Community` tab enabled to find it.

![image](https://user-images.githubusercontent.com/10919737/159488622-1b6a5f81-5a4b-4d85-b040-aab91ece587e.png)

Click the checkbox to enable the add on.

The addon is now available in the main viewport on the 'N' panel. If it isn't visible, press `N` to reveal the panel and click on `Paladin Studios`. 

<a name="release"/>

# Creating a new release
Checkout the repository and switch to the branch you need a release from.

Zip the `PaladinExporter` folder to a `PaladinExporterVx.x.x.zip`, where x.x.x should be the relevant version number.

The zip file can now be distributed and installed using the add on preferences menu, by clicking `Install` and selecting the .zip file.
