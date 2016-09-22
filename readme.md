# chewmesh
This Python script leverages 3D visualization applications Amira or Avizo to 
simplify and smooth groups of 3D mesh files. Given a directory of specimens and
desired parameters for simplification and smoothing, Amira/Avizo is called with 
an automatically-generated Tcl script to perform requested mesh editing. 
Simplification levels should be given as either an integer representing the 
target number of mesh polygons post-simplification, or 'None' for no 
simplification. Smoothing levels should be given as an integer representing 
iterations of smoothing to be performed. 

Simplification is performed before smoothing. For each simplification level, 
an unsmoothed mesh will also be saved along with the simplified and smoothed 
meshes. As a result, the total number of files saved will equal:

(Number of input files) x (Number of simplification levels) x (Number of smoothing levels + 1)
