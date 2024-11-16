# this imports everything from the tkinter module
from tkinter import *
# importing the ttk module from tkinter that's for styling widgets
from tkinter import ttk
# importing message boxes like showinfo, showerror, askyesno from tkinter.messagebox
from tkinter.messagebox import showinfo, showerror, askyesno
# importing filedialog from tkinter
from tkinter import filedialog as fd
# this imports the qrcode module
import qrcode

# the function to close the window
def close_window():
    # this will ask the user whether to close or not
    if askyesno(title='Close QR Code Generator', message='Are you sure you want to close the application?'):
        # this destroys the window
        window.destroy()

# the function for generating the QR Code

def generate_qrcode():
    qrcode_data = str(data_entry.get())
    qrcode_name = str(filename_entry.get())


    if qrcode_name == '':
        showerror(title='Error', message='An error occurred' \
                                         '\nThe following is ' \
                                         'the cause:\n->Empty filename entry field\n' \
                                         'Make sure the filename entry field is filled when generating the QRCode')
    else:
        # confirm from the user whether to generate QR code or not
        if askyesno(title='Confirmation', message=f'Do you want to create a QRCode with the provided information?'):
            # the try block for generating the QR Code
            try:
                # Creating an instance of QRCode class
                qr = qrcode.QRCode(version=1, box_size=6, border=4)
                # Adding data to the instance 'qr'
                qr.add_data(qrcode_data)
                qr.make(fit=True)
                # the name for the QRCode
                name = qrcode_name + '.png'
                # making the QR code

                qrcode_image = qr.make_image(fill_color='black', back_color='white')

                # saving the QR code

                qrcode_image.save(name)

                # making the Image variable global
                global Image
                Image = PhotoImage(file=f'{name}')
                image_label1.config(image=Image)


                # the button for resetting or clearing the QR code image on the canvas
                reset_button.config(state=NORMAL, command=reset)

            # this will catch all the errors that might occur
            except:
                showerror(title='Error', message='Please provide a valid filename')

# the function for resetting or clearing the image label
def reset():
    # confirming if the user wants to reset or not
    if askyesno(title='Reset', message='Are you sure you want to reset?'):
        # if yes reset the label
        image_label1.config(image='')
        # and disable the button again
        reset_button.config(state=DISABLED)

# Create the main window
window = Tk()
# creates title for the window
window.title('QR Code Generator')
# adding the window's icon
window.iconbitmap(window, 'icon.ico')
# dimensions and position of the window
window.geometry('500x480+440+180')
# makes the window non-resizable
window.resizable(height=FALSE, width=FALSE)

window.protocol('WM_DELETE_WINDOW', close_window)

"""Styles for the widgets, labels, entries, and buttons"""
# style for the labels
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 11))

# style for the entries
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))

# style for the buttons
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font=('DotumChe', 10))

# creating the Notebook widget
tab_control = ttk.Notebook(window)

# creating the tab with the ttk.Frame()
first_tab = ttk.Frame(tab_control)

# adding the tab to the Notebook
tab_control.add(first_tab, text='QR Code Generator')
# this makes the Notebook fill the entire main window so that its visible
tab_control.pack(expand=1, fill="both")

# creates the canvas for containing all the widgets in the first tab
first_canvas = Canvas(first_tab, width=500, height=480)
# packing the canvas to the first tab
first_canvas.pack()

"""Widgets for the first tab"""

# creating an empty label
image_label1 = Label(window)
# adding the label to the canvas
first_canvas.create_window(250, 150, window=image_label1)

# creating a ttk label
qrdata_label = ttk.Label(window, text='QRcode Data', style='TLabel')
# creating a ttk entry
data_entry = ttk.Entry(window, width=55, style='TEntry')

# adding the label to the canvas
first_canvas.create_window(70, 330, window=qrdata_label)
# adding the entry to the canvas
first_canvas.create_window(300, 330, window=data_entry)

# creating a ttk label
filename_label = ttk.Label(window, text='Filename', style='TLabel')
# creating a ttk entry
filename_entry = ttk.Entry(width=55, style='TEntry')

# adding the label to the canvas
first_canvas.create_window(84, 360, window=filename_label)
# adding the entry to the canvas
first_canvas.create_window(300, 360, window=filename_entry)

# creating the reset button in a disabled mode
reset_button = ttk.Button(window, text='Reset', style='TButton', state=DISABLED)
# creating the generate button
generate_button = ttk.Button(window, text='Generate QRCode', style='TButton', command=generate_qrcode)

# adding the reset button to the canvas
first_canvas.create_window(300, 390, window=reset_button)
# adding the generate button to the canvas
first_canvas.create_window(410, 390, window=generate_button)

# run the main window infinitely
window.mainloop()
