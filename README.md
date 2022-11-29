# Bonzomatic To Shadertoy
Python script to convert bonzomatic glsl fragment shaders to use them on shadertoy.com

## Usage
- Place your shader.glsl file in the folder
- Execute BonzomaticToShadertoy.bat
- In a command line, you can also specify the name of the shader file: "BonzomaticToShadertoy.bat filename.glsl"
- Open the shader.webgl file that has been created in a text editor
- Copy-paste the code into a new shader on shadertoy.com

## Limitations
- As Bonzomatic textures are not present in Shadertoy, the tool just give each a different channels and you have to assign textures in shadertoy yourself
- FFT textures are currently assigned to a different channel each
- Using previous frame texture will just be assigned to a texture channel, in Shadertoy you need to put your shader in "Buffer A" instead of Image so you can sample the previous frame
- float numbers are rounded to 4 digits, because otherwise the tool would output weird numbers like 0.199999998
- intermediary variables are often inserted before function calls
- if you use "half" as a variable name, it will cause issues

## Todo
- Better FFT handling
- Option to generate a json for importing with "Shadertoy unofficial plugin"
- replace texNoise with a call to a perlin noise function
- maybe replacing python by an exe tool so it can be autonomous
- fixing weird float numbers inside glslangValidator/spirv-cross source code instead of afterward
- fixing intermediary variables inserted before function calls

## How it works
- Use glslangValidator (github.com/KhronosGroup/glslang) to convert glsl to a spirv shader
- Use spriv-cross (github.com/KhronosGroup/SPIRV-Cross) to convert the spirv shader back to webgl-ready code
- Use python to replace part of the code to adapt the Bonzomatic shader to Shadertoy
    - replace input variables (pixel coordinates, resolution, time, main function name)
    - remove useless lines (texture definitions, version, highp)
    - round floats to 4 digits (glslangValidator/spirv-cross generate weird numbers)
    - assign textures to shadertoy channels
