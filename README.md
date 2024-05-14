# Blender-Exporter

![](https://i1.wp.com/paladinstudios.com/wp-content/uploads/2020/03/logo-1.png)

 * [Description](#description)
 * [Best Practices](#bestpractices)
 * [Requirements](#requirements)
 * [Developing & Testing](#develop)
 * [Creating a release](#release)

<a name="description"/>

# Description

<img width="360" alt="image" align="center" src="https://github.com/PaladinStudiosBVs/Blender-Exporter/assets/3831890/6276cf1f-e728-41bd-b9d3-8d0055d8e442">

The Blender Exporter assists with the workflow of exporting `.fbx` files. Collections can be defined to be exported, as well as the target path of where objects should be exported to. All configuration is saved within the `.blend` file.

<a name="bestpractices"/>

# Best Practices

The main export path is where `.fbx` files will be exported to.

Added collections will be exported on an per object bases within the collection. The exported `.fbx` files will have their object's name as filename. When enabling the `Collection Icon` the whole collection will be exported as a single fbx with it's origin at `000`

When exporting to multiple folders is required an export path can be defined for each collection:
<img width="332" alt="image" src="https://github.com/PaladinStudiosBVs/Blender-Exporter/assets/3831890/51a43657-8b07-4cf8-935a-f5510c9d6cc9">

The `Lock Icon` bool will export every object within a collection at it's position in world space essentially locking it in place when exporting. Default functionality moves the exported objects to `000` in world space.

When exporting a rig with animations, the export setting should be set to `Unity Animation`

When exporting animations only, the export setting should be set to `Unity Animation Only`

<a name="requirements"/>

# Requirements

Minimium Blender version 3.0.1 is required. As well as Unity version 2020.3 (using the `Bake Axis Conversion` import setting).
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
Update the version in ```addons/BlenderExporter/__init__.py```

When changes are merged to the ```main``` branch and a new version is detected, the release automation will create a new package
