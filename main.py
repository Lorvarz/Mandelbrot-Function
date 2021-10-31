import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider




base = complex(0, 0) #Number to square

real = -(0.5) #starting real component of C
imaginary = 0.2 #starting imaginary component of C

C = complex(real, imaginary) #Number to add



def iterate(base : complex, add : complex) -> [complex]:
    """
    Takes in a complex number and returns its Mandelbrot function
    :param base: Initial complex Number (Z_(0) in the Mandelbrot function)
    :param add: complex number to add (C in the Mandelbrot function)
    :return: Array of X and Y values of add's Mandelbrot function
    """

    def func(num, C ) -> complex:
        """
        Takes in 2 complex numbers and returns the next number in the Mandelbrot function
            Mandelbrot function: Z_(n)^2 + C = Z_(n+1)
        :param num: number to square (Z_(n) in the Mandelbrot function)
        :param C: number to add (C in the Mandelbrot function)
        :return: Next Z in the Mandelbrot function (Z_(n+1))
        """
        return num**2 + C

    #puts the base's values in the coordinates arrays
    XVals = [base.real]
    YVals = [base.imag]


    new = func(base, add)#Runs the first iteration of the Mandelbrot function

    #iterates the Mandelbrot function 20 times
    for i in range(20):
        new = func(new, add)
        XVals.append((new.real))
        YVals.append((new.imag))

    return (XVals, YVals)




#sets up graph so origin is in the middle
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

area = 1.3
plt.xlim(-area, area)
plt.xticks(np.arange(0, 0, 1.0))

plt.ylim(-area, area)
plt.yticks(np.arange(0, 0, 1.0))



#Mouse coordinates
mouseX = 0
mouseY = 0


plt.scatter([0],[0], s = 10,c="red") #graphs the origin
connect, = plt.plot(*iterate(base, C)) #plots the original function

plt.subplots_adjust(left=0.25, bottom=0.25) #adjusts graph position


axcolor = 'lightgoldenrodyellow' #color of the axis

# Makew a horizontally oriented slider to control the real component
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
real_slider = Slider(
    ax=axfreq,
    label='Real',
    valmin=-1,
    valmax=1,
    valinit=0,
)


# Makew a vertically oriented slider to control the imaginary component
axamp = plt.axes([0.1, 0.25, 0.0225, 0.63], facecolor=axcolor)
imag_slider = Slider(
    ax=axamp,
    label="Imaginary",
    valmin=-1,
    valmax=1,
    valinit=0,
    orientation="vertical"
)

# The function to be called anytime a slider's value changes
def update(event = None) -> None:
    """
    Updates the graph
    :param event: instance of the slider event, mouse gives no event
    :return: None
    """

    if draw:
        C = complex(mouseX, mouseY) #sets C to the mouse position
        x, y = iterate(base, C) #gets X and Y values
    else:
        C = complex(real_slider.val, imag_slider.val)  # sets C to the mouse position
        x, y = iterate(base, C)  # gets X and Y values

    #updates graph with the new values
    connect.set_xdata(x)
    connect.set_ydata(y)

    fig.canvas.draw_idle()#redraws graph




def setMouse(event) -> None:
    """
    Records the mouse coordinates and calls to update
    :param event: Instance of mouse movement event
    :return: None
    """
    global mouseX
    global mouseY
    if draw:
        mouseX = event.xdata
        mouseY = event.ydata
        update()


draw = True #whether to update the graph or not

def onClick(event) -> None:
    """
    Stops the update of the function or resumes it on right-click
    :param event: instance of the click
    :return: None
    """
    global draw
    if event.button == plt.MouseButton.RIGHT:
        draw = not draw
        real_slider.set_val(mouseX)
        imag_slider.set_val(mouseY)
        if draw:
            setMouse(event)

#connects the mouse to its functions
plt.connect('button_press_event', onClick)
plt.connect('motion_notify_event', setMouse)

# connect the update function to each slider
real_slider.on_changed(update)
imag_slider.on_changed(update)




plt.show() #shows the canvas and loops it



