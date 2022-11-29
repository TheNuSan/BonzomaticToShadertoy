@echo off
IF "%~dpn1"=="" ( SET "infile=shader" ) ELSE ( SET "infile=%~dpn1" )
IF EXIST %infile%.glsl (
	glslangValidator.exe -H -V -R -S frag --amb --aml --target-env opengl -o %infile%.spv %infile%.glsl
	spirv-cross.exe --remove-unused-variables --force-zero-initialized-variables --version 310 --es %infile%.spv > %infile%.webgl
	python BonzomaticToShadertoy.py %infile%
	del %infile%.spv
) ELSE (
	ECHO file %infile%.glsl does not exist
)
