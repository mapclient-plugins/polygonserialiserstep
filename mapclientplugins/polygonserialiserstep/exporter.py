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
import vtk

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
    points = vtk.vtkPoints()
    for x, y, z in vertices:
        points.InsertNextPoint(x, y, z)

    # create polygons
    polygons = vtk.vtkCellArray()
    for f in faces:
        polygon = vtk.vtkPolygon()
        polygon.GetPointIds().SetNumberOfIds(len(f))
        for fi, gfi in enumerate(f):
            polygon.GetPointIds().SetId(fi, gfi)
        polygons.InsertNextCell(polygon)

    # create polydata
    P = vtk.vtkPolyData()
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
        self._isoldvtk = int(vtk.VTK_VERSION.split('.')[0])<6

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
        ply_mapper = vtk.vtkPolyDataMapper()
        if self._isoldvtk:
            ply_mapper.SetInput(self._polydata)
        else:
            ply_mapper.SetInputDataObject(self._polydata)
        ply_actor = vtk.vtkActor()
        ply_actor.SetMapper(ply_mapper)

        ren1 = vtk.vtkRenderer()
        self._render_window = vtk.vtkRenderWindow()
        self._render_window.AddRenderer(ren1)
        ren1.AddActor(ply_actor)

    def write(self, filename=None, ascenc=True):
        if filename is not None:
            self.filename = filename

        filePrefix, fileExt = path.splitext(self.filename)
        fileExt = fileExt.lower()
        if fileExt == '.obj':
            self.writeOBJ()
        elif fileExt=='.wrl':
            self.writeVRML()
        elif fileExt=='.stl':
            self.writeSTL(ascenc=ascenc)
        elif fileExt=='.ply':
            self.writePLY(ascenc=ascenc)
        elif fileExt=='.vtp':
            self.writeVTP(ascenc=ascenc)
        else:
            raise ValueError('unknown file extension')

    def writeOBJ(self, filename=None):
        if filename is not None:
            self.filename = filename
        if self._render_window is None:
            self._make_render_window()

        w = vtk.vtkOBJExporter()
        w.SetRenderWindow(self._render_window)
        w.SetFilePrefix(path.splitext(self.filename)[0])
        w.Write()

    def writePLY(self, filename=None, ascenc=True):
        if filename is not None:
            self.filename = filename
        if self._polydata is None:
            self._make_polydata()

        w = vtk.vtkPLYWriter()
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

    def writeSTL(self, filename=None, ascenc=True):
        if filename is not None:
            self.filename = filename
        if self._polydata is None:
            self._make_polydata()

        w = vtk.vtkSTLWriter()
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

    def writeVRML(self, filename=None):
        if filename is not None:
            self.filename = filename
        if self._render_window is None:
            self._make_render_window()

        w = vtk.vtkVRMLExporter()
        w.SetRenderWindow(self._render_window)
        w.SetFileName(self.filename)
        w.Write()

    def writeVTP(self, filename=None, ascenc=True):
        if filename is not None:
            self.filename = filename
        if self._polydata is None:
            self._make_polydata()

        w = vtk.vtkPolyDataWriter()
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

def exportPolygon(v, f, suffix, filename, options=None):
    if len(v.shape)!=2:
        raise ValueError('v array must be of shape [n, 3]')
    if v.shape[1]!=3:
        raise ValueError('v array must be of shape [n, 3]')
    if len(f.shape)!=2:
        raise ValueError('f array must be 2 dimensional')
    if suffix not in supported_suffixes:
        raise ValueError('Unsupported suffix {}'.format(suffix))

    w = Writer(v=v, f=f)
    f_prefix, f_ext = path.splitext(filename)
    if f_ext=='':
        filename = f_prefix+'.'+suffix
    else:
        suffix = f_ext

    print('writing {} vertices and {} faces to {}'.format(len(v), len(f), filename))

    if suffix == 'obj':
        w.writeOBJ(filename)
    elif suffix=='wrl':
        w.writeVRML(filename)
    elif suffix=='stl':
        w.writeSTL(filename)
    elif suffix=='ply':
        w.writePLY(filename)
    elif suffix=='vtp':
        w.writeVTP(filename)
