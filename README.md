Polygon Serialiser Step
=======================
MAP Client plugin for writing polygon vertex coordinates and faces to file in a variety of file formats using VTK.

The supported file formats are: STL, OBJ, PLY, VRML, VTP.

Requires
--------
- GIAS2 : https://bitbucket.org/jangle/gias2
- VTK (>=5.10, 6) with Python bindins http://www.vtk.org/download/

Inputs
------
- **pointclouds** [list] : A list of vertex coordinates.
- **faces** [list] : A list of the vertex indices of each face.
- **string** [str][Optional] : Path of the file to be written.

Outputs
-------
None

Configuration
-------------
- **identifier** : Unique name for the step.
- **File Format** : Format of the file to be read. "Auto" will guess the format from the file suffix.
- **Filename** : Path of the file to be written. If filename is provided via the input port, this value will be ignored.

Usage
-----
This step is typically used at the end of workflows to write generated meshes to file.

Also see Polygon Source Step.
