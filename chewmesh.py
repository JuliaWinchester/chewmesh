'''
Created on Sep 22, 2016

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
(# of input files) * (# of simplification levels) * (# of smoothing levels + 1)

@author: Julie Winchester
'''
import inspect
from os import listdir, makedirs, remove, rmdir
from os.path import isfile, join, exists
from subprocess import call

def write_simplify_script(file_dir, out_dir, file_name, script, simp_target):
	if simp_target == 'None':
		new_file_loc = join(out_dir, file_name)
		script.write('load ' + join(file_dir, file_name) + '\n')
		script.write(file_name + 'save "Stanford PLY" ' + new_file_loc + '\n')
		return file_name

	new_file_name = file_name[:-4] + '-simp' + str(simp_target) + '.ply'
	new_file_loc = join(out_dir, new_file_name)
	script.write('load ' + join(file_dir, file_name) + '\n')
	script.write('create HxSimplifier Simplifier\n')
	script.write('Simplifier attach {' + file_name + '}\n')
	script.write('Simplifier simplifyParameters setValue faces ' + str(simp_target) + '\n')
	script.write('Simplifier simplifyAction setIndex 0\n')
	script.write('Simplifier fire\n')
	script.write(file_name + ' save "Stanford PLY" ' + new_file_loc + '\n\n')
	return new_file_name

def write_smooth_script(file_dir, out_dir, file_name, script, smooth_iter):
	smooth_file_name = file_name[:-4] + '-smooth' + str(smooth_iter) + '.ply'
	smooth_file_loc = join(out_dir, smooth_file_name)
	script.write('create HxSurfaceSmooth SmoothSurface\n')
	script.write('SmoothSurface data connect ' + file_name + '\n')
	script.write('SmoothSurface parameters setValue iterations ' + str(smooth_iter) + '\n')
	script.write('SmoothSurface action setIndex 0\n')
	script.write('SmoothSurface fire\n')
	script.write(file_name[:-4]+'.smooth save "Stanford PLY" ' + smooth_file_loc + '\n')
	script.write('remove ' + smooth_file_name + '\n\n')
	return

app_bin = '/Applications/Amira-5.3.2/Amira.app/Contents/MacOS/Amira'
mesh_dir = '/Users/Julie/Documents/Code/chewmesh/meshes'
output_dir = '/Users/Julie/Documents/Code/chewmesh/output'

simplification_levels = [100, 1000, 2500, 5000, 10000, 15000, 20000, 30000, 50000, 100000]
smoothing_levels = [50, 100]

if not exists(output_dir):
	makedirs(output_dir)
if not exists(join(output_dir, 'temp')):
	makedirs(join(output_dir, 'temp'))

for file in [f for f in listdir(mesh_dir) if isfile(join(mesh_dir, f))]:
	hx_script = open(join(output_dir, 'temp', 'script.hx'), 'wb')
	hx_script.write('# Amira Script\n')

	for simp_target in simplification_levels:
		simp_file = write_simplify_script(mesh_dir, output_dir, file, hx_script, simp_target)
		for smooth_iter in smoothing_levels:
			write_smooth_script(mesh_dir, output_dir, simp_file, hx_script, smooth_iter)
		hx_script.write('remove ' + simp_file + '\n')

	hx_script.close()
	call([app_bin, '-no_gui', join(output_dir, 'temp', 'script.hx')])

remove(join(output_dir, 'temp', 'script.hx'))
rmdir(join(output_dir, 'temp'))



