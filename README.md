# Blender-Exporter

![](https://i1.wp.com/paladinstudios.com/wp-content/uploads/2020/03/logo-1.png)

 * [Description](#description)
 * [Best Practices](#bestpractices)
 * [Requirements](#requirements)
 * [Developing & Testing](#develop)
 * [Creating a release](#release)

<a name="description"/>

# Description

![image](https://user-images.githubusercontent.com/10919737/159481452-bf4e2765-9696-4b31-a93c-1f01a2f06c9a.png)

The Paladin Exporter assists with the workflow of exporting `.fbx` files. Collections can be defined to be exported, as well as the target path of where objects should be exported to. All configuration is saved within the `.blend` file.

<a name="bestpractices"/>

# Best Practices

The main export path is where `.fbx` files will be exported to.

Added collections will be exported on an per object bases within the collection. The exported `.fbx` files will have their object's name as filename. A good way of organizing your export is to add a `export` collection which contains all objects to be exported for that `.blend` file.

When exporting to multiple folders is required, a collection per export path can be added (having a custom path defined).

The `Reset Origin` bool will export every object within a collection at the world origin (0,0,0).

When exporting a rig without animation, the `Include Meshes` should be set to true and the `Bake Animation` set to false.

When exporting animations only, the `Include Meshes` should be set to false and the `Bake Animation` set to true. A filename suffix will be added as well.

<a name="requirements"/>

# Requirements

Minimium Blender version 2.93.1 is required. As well as Unity version 2020.3 (using the `Bake Axis Conversion` import setting).
Make sure the `Bake Axis Conversion` bool is set to true within Unity on `.fbx` files exported with the exporter.

![image](https://user-images.githubusercontent.com/10919737/174821463-2b928b8a-79eb-4d03-9077-d7af6fc46695.png)

<a name="develop"/>

# Developing & Testing
To test during development, add the path to the addons folder in this repo to the Scripts path in Blender Preferences. Preferences -> File Paths -> Data -> Scripts

After adding the path, make sure to reload the python scripts within Blender. Click the top left Blender icon -> System -> Reload Scripts.

![image](https://user-images.githubusercontent.com/10919737/159488403-c4d14dc8-03d4-4b18-974c-e52eb3a4f739.png)


Now the addon scripts should be in Blender and the add-on can be enabled in the preferences menu. Search for `Paladin` with the `Community` tab enabled to find it.

![image](https://user-images.githubusercontent.com/10919737/159488622-1b6a5f81-5a4b-4d85-b040-aab91ece587e.png)

Click the checkbox to enable the add on.

<b> Note: </b> When the addon has been enabled once, this step can be skipped. Reloading scripts is only required.

The addon is now available in the main viewport on the 'N' panel. If it isn't visible, press `N` to reveal the panel and click on `Paladin Studios`. 

<a name="release"/>

# Creating a new release
Checkout the repository and switch to the branch you need a release from.

Zip the `PaladinExporter` folder to a `PaladinExporterVx.x.x.zip`, where x.x.x should be the relevant version number.

The zip file can now be distributed and installed using the add on preferences menu, by clicking `Install` and selecting the .zip file.
