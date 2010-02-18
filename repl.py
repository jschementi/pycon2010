from Microsoft.Scripting.Silverlight import Repl

if 'document' not in globals():
  import System
  document = System.Windows.Browser.HtmlPage.Document
if 'window' not in globals():
  import System
  window = System.Windows.Browser.HtmlPage.Window

class PythonRepl(object):
  __ironpython__ = 'silverlightDlrRepl1'
  __minimize__ = 'silverlightDlrWindowLink'
  __container__ = 'silverlightDlrWindowContainer'

  def __init__(self):
    self.repl = Repl.Show('python')

  def hide_all_panels(self):
    window.Eval("sdlrw.hideAllPanels(document.getElementById(\"%s\"))" % self.__minimize__)
  
  def show_panel(self, id):
    window.Eval("sdlrw.showPanel(\"%s\")" % id)
  
  def show_ironpython(self):
    self.show_panel(self.__ironpython__)

  def remove(self):
    document.Body.RemoveChild(document.silverlightDlrWindowContainer)

def show():
  prepl = PythonRepl()
  repl = prepl.repl
  import sys
  sys.stdout = repl.OutputBuffer
  sys.stderr = repl.OutputBuffer
  return prepl

if document.QueryString.ContainsKey('console'): 
  prepl = show()
  if document.QueryString['console'] == 'hide':
    prepl.hide_all_panels()
  else:
    prepl.show_ironpython()

