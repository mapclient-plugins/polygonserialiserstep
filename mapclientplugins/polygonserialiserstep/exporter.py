"""
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
"""

from os import path

from vtkmodules.vtkCommonCore import vtkPoints, VTK_VERSION
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolygon, vtkPolyData
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor, vtkRenderer, vtkRenderWindow
from vtkmodules.vtkIOExport import vtkOBJExporter, vtkVRMLExporter
from vtkmodules.vtkIOPLY import vtkPLYWriter
from vtkmodules.vtkIOGeometry import vtkSTLWriter
from vtkmodules.vtkIOLegacy import vtkPolyDataWriter


def polygons2Polydata(vertices, faces):
    """
    Uses create a vtkPolyData instance from a set of vertices and
    faces.

    Inputs:
    vertices: (nx3) array of vertex coordinates
    faces: list of lists of vertex indices for each face
    clean: run vtkCleanPolyData
    normals: run vtkPolyDataNormals

    Returns:
    P: vtkPolyData instance
    """
    # define points
    points = vtkPoints()
    for x, y, z in vertices:
        points.InsertNextPoint(x, y, z)

    # create polygons
    polygons = vtkCellArray()
    for f in faces:
        polygon = vtkPolygon()
        polygon.GetPointIds().SetNumberOfIds(len(f))
        for fi, gfi in enumerate(f):
            polygon.GetPointIds().SetId(fi, gfi)
        polygons.InsertNextCell(polygon)

    # create polydata
    P = vtkPolyData()
    P.SetPoints(points)
    P.SetPolys(polygons)

    return P


class Writer(object):
    """Class for writing polygons to file formats supported by VTK.
    """

    def __init__(self, **kwargs):
        """Keyword arguments:
        filename: output filename
        polydata: vtkPolydata instance
        v: array of vertices coordinates
        f: list of faces composed of lists of vertex indices
        rw: vtkRenderWindow instance
        colour: 3-tuple of colour (only works for ply)
        ascii: boolean, write in ascii (True) or binary (False)
        """
        self.filename = kwargs.get('filename')
        if self.filename is not None:
            self._parse_format()
        self._polydata = kwargs.get('polydata')
        self._vertices = kwargs.get('v')
        self._faces = kwargs.get('f')
        self._render_window = kwargs.get('rw')
        self._colour = kwargs.get('colour')
        # self._field_data = kwargs.get('field')
        self._write_ascii = kwargs.get('ascii')
        self._isoldvtk = int(VTK_VERSION.split('.')[0]) < 6

    def setFilename(self, f):
        self.filename = f
        self._parse_format()

    def _parse_format(self):
        self.file_prefix, self.file_ext = path.splitext(self.filename)
        self.file_ext = self.file_ext.lower()

    def _make_polydata(self):
        self._polydata = polygons2Polydata(self._vertices, self._faces)

    def _make_render_window(self):
        if self._polydata is None:
            self._make_polydata()
        ply_mapper = vtkPolyDataMapper()
        if self._isoldvtk:
            ply_mapper.SetInput(self._polydata)
        else:
            ply_mapper.SetInputDataObject(self._polydata)
        ply_actor = vtkActor()
        ply_actor.SetMapper(ply_mapper)

        ren1 = vtkRenderer()
        self._render_window = vtkRenderWindow()
        self._render_window.AddRenderer(ren1)
        ren1.AddActor(ply_actor)

    def write(self, filename=None, ascenc=True):
        if filename is not None:
            self.filename = filename

        filePrefix, fileExt = path.splitext(self.filename)
        fileExt = fileExt.lower()
        if fileExt == '.obj':
            self.write_obj()
        elif fileExt == '.wrl':
            self.write_vrml()
        elif fileExt == '.stl':
            self.write_stl(ascenc=ascenc)
        elif fileExt == '.ply':
            self.write_ply(ascenc=ascenc)
        elif fileExt == '.vtp':
            self.write_vtp(ascenc=ascenc)
        else:
            raise ValueError('unknown file extension')

    def write_obj(self, filename=None):
        if filename is not None:
            self.filename = filename
        if self._render_window is None:
            self._make_render_window()

        w = vtkOBJExporter()
        w.SetRenderWindow(self._render_window)
        w.SetFilePrefix(path.splitext(self.filename)[0])
        w.Write()

    def write_ply(self, filename=None, ascenc=True):
        if filename is not None:
            self.filename = filename
        if self._polydata is None:
            self._make_polydata()

        w = vtkPLYWriter()
        if self._isoldvtk:
            w.SetInput(self._polydata)
        else:
            w.SetInputDataObject(self._polydata)
        w.SetFileName(self.filename)
        if ascenc:
            w.SetFileTypeToASCII()
        else:
            w.SetFileTypeToBinary()
        w.SetDataByteOrderToLittleEndian()
        # w.SetColorModeToUniformCellColor()
        # w.SetColor(255, 0, 0)
        w.Write()

    def write_stl(self, filename=None, ascenc=True):
        if filename is not None:
            self.filename = filename
        if self._polydata is None:
            self._make_polydata()

        w = vtkSTLWriter()
        if self._isoldvtk:
            w.SetInput(self._polydata)
        else:
            w.SetInputDataObject(self._polydata)
        w.SetFileName(self.filename)
        if ascenc:
            w.SetFileTypeToASCII()
        else:
            w.SetFileTypeToBinary()
        w.Write()

    def write_vrml(self, filename=None):
        if filename is not None:
            self.filename = filename
        if self._render_window is None:
            self._make_render_window()

        w = vtkVRMLExporter()
        w.SetRenderWindow(self._render_window)
        w.SetFileName(self.filename)
        w.Write()

    def write_vtp(self, filename=None, ascenc=True):
        if filename is not None:
            self.filename = filename
        if self._polydata is None:
            self._make_polydata()

        w = vtkPolyDataWriter()
        if self._isoldvtk:
            w.SetInput(self._polydata)
        else:
            w.SetInputDataObject(self._polydata)
        w.SetFileName(self.filename)
        if ascenc:
            w.SetFileTypeToASCII()
        else:
            w.SetFileTypeToBinary()
        w.Write()


supported_suffixes = ('stl', 'wrl', 'obj', 'ply', 'vtp')


def export_polygon(v, f, suffix, filename):
    if len(v.shape) != 2:
        raise ValueError('v array must be of shape [n, 3]')
    if v.shape[1] != 3:
        raise ValueError('v array must be of shape [n, 3]')
    if len(f.shape) != 2:
        raise ValueError('f array must be 2 dimensional')
    if suffix not in supported_suffixes:
        raise ValueError('Unsupported suffix {}'.format(suffix))

    w = Writer(v=v, f=f)
    f_prefix, f_ext = path.splitext(filename)
    if f_ext == '':
        filename = f_prefix + '.' + suffix
    else:
        suffix = f_ext[1:].lower()

    print('writing {} vertices and {} faces to {}'.format(len(v), len(f), filename))
    print('suffix: {}'.format(suffix))

    if suffix == 'obj':
        w.write_obj(filename)
    elif suffix == 'wrl':
        w.write_vrml(filename)
    elif suffix == 'stl':
        w.write_stl(filename)
    elif suffix == 'ply':
        w.write_ply(filename)
    elif suffix == 'vtp':
        w.write_vtp(filename)
