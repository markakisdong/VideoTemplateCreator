import numpy as np
import gizeh

# helper function
rotMatrix = lambda a: np.array( [[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]] )

def ef_intro_circle(t):
    surface = gizeh.Surface(640, 480, (1, 1, 1)) # width, height
    radius = 240 * (t**8) / 8 # the radius varies over time
    circle = gizeh.circle(radius, xy = (320, 240), fill=(0, 0, 0))
    circle.draw(surface)
    return surface.get_npimage() # returns a 8-bit RGB array

def ef_vortex(screenpos, i, nletters):
    d = lambda t : 1.0 / (0.3 + t**8) #damping
    a = i * np.pi / nletters # angle of the movement
    v = rotMatrix(a).dot([-1, 0])
    if i%2 : v[1] = -v[1]
    return lambda t: screenpos + 400 * d(t) * rotMatrix(0.5 * d(t) * a).dot(v)

def ef_cascade(screenpos, i, nletters):
    v = np.array([0, -1])
    d = lambda t : 1 if t < 0 else abs(np.sinc(t) / (1 + t**4))
    return lambda t: screenpos + v * 400 * d(t - 0.15 * i)

def ef_arrive(screenpos, i, nletters):
    v = np.array([-1, 0])
    d = lambda t : max(0, 3 - 3 * t)
    return lambda t: screenpos - 400 * v * d(t - 0.2 * i)

def ef_vortexout(screenpos, i, nletters):
    d = lambda t : max(0, t) #damping
    a = i * np.pi / nletters # angle of the movement
    v = rotMatrix(a).dot([-1, 0])
    if i % 2 : v[1] = -v[1]
    return lambda t: screenpos + 400 * d(t - 0.1 * i) * rotMatrix(-0.2 * d(t) * a).dot(v)


def ef_moveLetters(letters, funcpos):
    return [ letter.set_pos(funcpos(letter.screenpos, i, len(letters))) \
              for i,letter in enumerate(letters)]
