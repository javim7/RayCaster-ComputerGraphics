import cyglfw3 as glfw
from OpenGL.GL import *

glfw.Init()

window = glfw.CreateWindow(800, 600, "Opengl")

while not glfw.WindowShouldClose(window):
    glfw.PollEvents()

glfw.Terminate()
