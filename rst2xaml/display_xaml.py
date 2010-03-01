# requires IronPython and .NET 3

import sys
import clr
clr.AddReference('PresentationFramework')
clr.AddReference('PresentationCore')
clr.AddReference('windowsbase')
from System.Windows.Controls import *
from System.Windows.Markup import XamlReader
from System.Windows import Window, Application

if len(sys.argv) == 1:
    from Microsoft.Win32 import OpenFileDialog
    
    dialog = OpenFileDialog()
    dialog.ShowDialog()
    
    filename = dialog.FileName
    if filename is None:
        sys.exit()
    stream = dialog.OpenFile()
elif len(sys.argv) > 2:
    print 'display_xaml [xaml_file]'
    sys.exit(1)
else:
    from System.IO import File
    filename = sys.argv[1]
    stream = File.OpenRead(filename)

reader = FlowDocumentReader()
flowDocument = XamlReader.Load(stream)
stream.Close()
reader.Document = flowDocument
w = Window()
w.Title = "Displaying %r" % filename
w.Content = reader
Application().Run(w)

