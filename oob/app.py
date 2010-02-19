from System.Windows import Application
Application.Current.LoadRootVisualFromString(open("app.xaml").read())
root = Application.Current.RootVisual

root.loading.Text = "Hello from Python!"

def say_ouch(s, e):
    s.Text = "Ouch!"

root.loading.MouseLeftButtonDown += say_ouch
